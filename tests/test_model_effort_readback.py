"""Tests for skills/dev-core/scripts/model_effort_readback.py (Issue #89, Issue #79 slice B, Issue #96; REQ-009).

Synthetic fixtures only: every tree, file, Git repository and ID is made in a temporary directory at run time. No test
reads a real transcript or the home directory. Of the environment and process data, the tests read only the user ID
and the effective user ID (os.getuid, os.geteuid), the list of open file descriptors in /dev/fd, the TMPDIR, TEMP or
TMP variable that tempfile reads to find the temporary directory, and PATH, which shutil.which reads to find git, sh,
cat, sleep and yes. The script runs as `sys.executable -I -B` with a timeout, by its path or from stdin. Run by its
path, it is a copy outside the repository (COPY, with a copy of the configuration file next to its scripts folder),
so that the repository check of Issue #96 PR-3 does not stop it; the module of the in-process cases is loaded from
that copy too, and SOURCE (the stdin form) and Static read the file of the repository, which a test compares with the
copy byte for byte. The environment of the script is empty, or holds only PATH set to the folder of git when it
calls git (Issue #96); the repository check cases add HOME set to a temporary directory, GIT_CONFIG_NOSYSTEM and the
GIT_ variables that a case names. The Git repositories of the fixtures are made with HOME set to a temporary
directory and without the system Git configuration. The cases that a subprocess cannot make (an argument with NUL,
a patched os.getuid, os.getcwd, os.lstat, os.stat, os.read or os.open, a missing open flag, a closed stdout, an
exception, a fake git with a short time budget) call its main() in this process. These fixtures prove only the
outcomes that they list (R-VER-1).
"""

import ast
import contextlib
import copy
import errno
import importlib.util
import io
import json
import os
import re
import secrets
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import time
import unittest
import uuid
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "skills", "dev-core", "scripts", "model_effort_readback.py")
CONFIG = os.path.join(ROOT, "skills", "dev-core", "model-config.json")
CONFIG_IN_REPO = "skills/dev-core/model-config.json"
OPUS = "claude-opus-5-5"
TIERS = {"haiku": 1, "sonnet": 2, "opus": 3, "fable": 4}
TOKENS = {
    "BAD_ARGS", "CONFIG", "NOT_FOUND", "AMBIGUOUS", "SYMLINK", "NOT_REGULAR", "OWNER", "LINK_COUNT", "PERMISSION",
    "TOO_LARGE", "MALFORMED", "BINDING_MISMATCH", "MISSING_FIELD", "INCONSISTENT", "NO_RECORD",
    "MODEL_NOT_RECOGNIZED", "EFFORT_NOT_ALLOWED", "INTERNAL", "IN_REPO", "REPO_CHECK"}
FAMILY = "(haiku|sonnet|opus|fable)"
LEVEL = "(low|medium|high|xhigh|max)"
TIER = "[1-9][0-9]*"
FLOOR = "(work|review-scan|review-routine|review-light|none)"
GRAMMAR = [  # (line pattern, exit code)
    (re.compile(f"PASS model={FAMILY} tier={TIER} effort={LEVEL} expected={FAMILY}/{LEVEL} expected_tier={TIER} "
                f"floor={FLOOR}"), 0),
    (re.compile(f"WARN model={FAMILY} tier={TIER} effort={LEVEL} expected={FAMILY}/{LEVEL} expected_tier={TIER} "
                f"floor={FLOOR}"), 4),
    (re.compile(f"BELOW model=({FAMILY}|unrecognized) tier=({TIER}|null|none) effort={LEVEL} "
                f"expected={FAMILY}/{LEVEL} expected_tier={TIER} floor={FLOOR}"), 3),
    (re.compile("STOP (" + "|".join(sorted(TOKENS)) + ")"), 2),
    (re.compile(f"CHECK model=({FAMILY}|unrecognized) match=(listed|version|name|none) tier=({TIER}|null|none) "
                f"effort={LEVEL} records=[1-9][0-9]*"), 5),
]
DEFAULT_EXPECT = ("opus", "low")
DROP = object()  # a record field to leave out
IS_ROOT = hasattr(os, "geteuid") and os.geteuid() == 0
GIT = shutil.which("git")
with open(CONFIG, "rb") as _fh:
    SHIPPED_BYTES = _fh.read()
SHIPPED = json.loads(SHIPPED_BYTES)
with open(SCRIPT, "rb") as _fh:
    SOURCE = _fh.read()
# Issue #96 PR-3: the copy that the path form and the in-process cases run, outside the repository; removed in
# tearDownModule
COPY_ROOT = os.path.realpath(tempfile.mkdtemp(prefix="readback-copy-"))
os.mkdir(os.path.join(COPY_ROOT, "scripts"))
COPY = os.path.join(COPY_ROOT, "scripts", "model_effort_readback.py")
shutil.copyfile(SCRIPT, COPY)
shutil.copyfile(CONFIG, os.path.join(COPY_ROOT, "model-config.json"))
CASE_INSENSITIVE = os.path.exists(os.path.join(COPY_ROOT, "SCRIPTS"))  # the file system of the temporary directory


def tearDownModule():
    shutil.rmtree(COPY_ROOT)


def load_script(path=COPY):
    """The script as a module, without writing bytecode next to it."""
    spec = importlib.util.spec_from_file_location("model_effort_readback", path)
    module = importlib.util.module_from_spec(spec)
    old, sys.dont_write_bytecode = sys.dont_write_bytecode, True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = old
    return module


MOD = load_script()


def open_fds():
    return len(os.listdir("/dev/fd"))


def result(word, model, tier, effort, expect=DEFAULT_EXPECT, floor="none"):
    """A PASS, WARN or BELOW line."""
    return (f"{word} model={model} tier={tier} effort={effort} expected={expect[0]}/{expect[1]} "
            f"expected_tier={TIERS[expect[0]]} floor={floor}")


def config_bytes(change=None) -> bytes:
    """The shipped configuration, changed in place by `change(config)` when given, as JSON bytes."""
    config = copy.deepcopy(SHIPPED)
    if change is not None:
        change(config)
    return json.dumps(config).encode("utf-8")


def retire_sonnet(config):
    """Sonnet retired (tier null) with its ID listed, and its roles moved to opus (card I96-C12 (a))."""
    config["families"]["sonnet"]["tier"] = None
    config["families"]["sonnet"]["ids"] = ["claude-sonnet-5-5"]
    for role in config["roles"].values():
        if role["family"] == "sonnet":
            role["family"] = "opus"


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.projects = os.path.join(self.tmp, "projects")
        os.mkdir(self.projects)
        self.slug = "-tmp-" + secrets.token_hex(4)
        self.session = str(uuid.uuid4())
        self.agent = secrets.token_hex(9)[:17]
        self.marker = "fixture-" + secrets.token_hex(6)  # text that must never reach the output

    # fixtures

    def other_agent(self):
        while True:
            other = secrets.token_hex(9)[:17]
            if other != self.agent:
                return other

    def rec(self, model=OPUS, effort="high", **fields):
        record = {"type": "assistant", "isSidechain": True, "agentId": self.agent, "sessionId": self.session,
                  "effort": effort, "perTurnEffort": effort, "requestedModel": "opus", "version": "0.0.0",
                  "message": {"model": model, "role": "assistant",
                              "content": [{"type": "text", "text": self.marker}]}}
        record.update(fields)
        return {key: value for key, value in record.items() if value is not DROP}

    def subagents_dir(self, slug=None, session=None):
        path = os.path.join(self.projects, slug or self.slug, session or self.session, "subagents")
        os.makedirs(path, exist_ok=True)
        return path

    def target(self, slug=None, session=None, agent=None):
        return os.path.join(self.subagents_dir(slug, session), f"agent-{agent or self.agent}.jsonl")

    def write(self, records=(), raw=None, slug=None, session=None, agent=None):
        path = self.target(slug, session, agent)
        data = raw if raw is not None else b"".join(json.dumps(r).encode() + b"\n" for r in records)
        with open(path, "wb") as fh:
            fh.write(data)
        return path

    def args(self, expect=DEFAULT_EXPECT, projects=None, agent=None, base=None, floor="none"):
        """subagent arguments; expect=() leaves out both expected values, floor=None leaves out --floor."""
        argv = ["subagent", "--projects-dir", self.projects if projects is None else projects,
                "--agent-id", self.agent if agent is None else agent]
        if expect:
            argv += ["--expect-model", expect[0], "--expect-effort", expect[1]]
        if base is not None:
            argv += ["--config-base", base]
        if floor is not None:
            argv += ["--floor", floor]
        return argv

    def check_args(self, candidate, projects=None, agent=None):
        return ["check", "--projects-dir", projects or self.projects, "--agent-id", agent or self.agent,
                "--candidate-config", candidate]

    def make_pack(self, config=SHIPPED_BYTES, script="model_effort_readback.py", parent="scripts"):
        """A copy of the script at <tmp>/pack-*/<parent>/<script> with the configuration bytes next to <parent>."""
        pack = tempfile.mkdtemp(prefix="pack-", dir=self.tmp)
        os.mkdir(os.path.join(pack, parent))
        shutil.copy(SCRIPT, os.path.join(pack, parent, script))
        if config is not None:
            with open(os.path.join(pack, "model-config.json"), "wb") as fh:
                fh.write(config)
        return os.path.join(pack, parent, script)

    def candidate(self, config=SHIPPED_BYTES, name="candidate.json"):
        path = os.path.join(self.tmp, name)
        with open(path, "wb") as fh:
            fh.write(config)
        return path

    # running

    def check(self, code, out, err, hidden=()):
        """The output is one line of the grammar with its exit code, stderr is empty, and nothing leaks."""
        self.assertEqual(err, "")
        self.assertTrue(out.endswith("\n") and out.count("\n") == 1, repr(out))
        line = out[:-1]
        kinds = [want for pattern, want in GRAMMAR if pattern.fullmatch(line)]
        self.assertEqual(len(kinds), 1, repr(line))
        self.assertEqual(code, kinds[0], line)
        for value in (self.tmp, self.projects, self.slug, self.session, self.agent, self.marker, *hidden):
            self.assertNotIn(value, out)
        return line

    def run_script(self, argv, hidden=(), script=COPY, cwd=None, env=None, stdin=False):
        """Run by its path (by default the copy outside the repository), or from stdin as the rules call the copy at a
        base."""
        command = [sys.executable, "-I", "-B", "-" if stdin else script, *argv]
        p = subprocess.run(command, cwd=cwd or self.tmp, env={} if env is None else env, capture_output=True,
                           input=SOURCE if stdin else None, timeout=60)
        return self.check(p.returncode, p.stdout.decode("ascii"), p.stderr.decode("ascii"), hidden)

    def run_inproc(self, argv, hidden=()):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = MOD.main(argv)
        return self.check(code, out.getvalue(), err.getvalue(), hidden)

    def assertStop(self, token, argv=None, inproc=False, hidden=(), **where):
        argv = self.args() if argv is None else argv
        line = self.run_inproc(argv, hidden) if inproc else self.run_script(argv, hidden, **where)
        self.assertEqual(line, "STOP " + token)

    def assertLine(self, want, argv=None, inproc=False, **where):
        argv = self.args() if argv is None else argv
        self.assertEqual(self.run_inproc(argv) if inproc else self.run_script(argv, **where), want)


class Normal(Base):
    def test_pass_takes_the_lowest_effort_over_all_records(self):
        self.write([self.rec(effort="xhigh"), self.rec(effort="high"), self.rec(effort="max")])
        self.assertLine(result("PASS", "opus", 3, "high"))

    def test_synthetic_record_is_skipped_without_other_checks(self):
        synthetic = {"type": "assistant", "message": {"model": "<synthetic>"}, "agentId": "x", "effort": 1}
        self.write([self.rec(effort="xhigh"), synthetic])
        self.assertLine(result("PASS", "opus", 3, "xhigh"))

    def test_pass_when_equal_or_above(self):
        self.write([self.rec(effort="xhigh")])
        self.assertLine(result("PASS", "opus", 3, "xhigh", ("opus", "xhigh")), self.args(("opus", "xhigh")))
        self.assertLine(result("PASS", "opus", 3, "xhigh", ("sonnet", "medium")), self.args(("sonnet", "medium")))
        self.assertLine(result("PASS", "opus", 3, "xhigh", ("haiku", "low")), self.args(("haiku", "low")))

    def test_below_effort(self):
        self.write([self.rec(effort="xhigh"), self.rec(effort="medium")])
        self.assertLine(result("BELOW", "opus", 3, "medium", ("opus", "high")), self.args(("opus", "high")))

    def test_below_model_of_a_lower_family(self):
        self.write([self.rec(model="claude-sonnet-5-5", effort="max")])
        self.assertLine(result("BELOW", "sonnet", 2, "max", ("opus", "high")), self.args(("opus", "high")))

    def test_expected_fable_is_above_a_listed_opus(self):  # fable has tier 4 in the file, so it is not BAD_ARGS
        self.write([self.rec(effort="max")])
        self.assertLine(result("BELOW", "opus", 3, "max", ("fable", "high")), self.args(("fable", "high")))

    def test_unrelated_symlinks_and_sessions_without_subagents_keep_pass(self):
        self.write([self.rec()])
        outside = os.path.join(self.tmp, "outside")
        os.mkdir(outside)
        os.symlink(outside, os.path.join(self.projects, "link-slug"))
        os.symlink("/nonexistent-" + secrets.token_hex(4), os.path.join(self.projects, "dangling"))
        os.symlink(outside, os.path.join(self.projects, self.slug, str(uuid.uuid4())))
        os.makedirs(os.path.join(self.projects, self.slug, str(uuid.uuid4())))  # no subagents directory
        os.makedirs(os.path.join(self.projects, "other-slug", str(uuid.uuid4()), "subagents"))
        with open(os.path.join(self.projects, "file.txt"), "w") as fh:
            fh.write("x")
        os.makedirs(os.path.join(self.projects, "bad name"))
        self.assertLine(result("PASS", "opus", 3, "high"))

    def test_file_descriptors_are_closed(self):
        self.write([self.rec()])
        self.write([self.rec()], slug="second-slug")
        before = open_fds()
        self.run_inproc(self.args())  # AMBIGUOUS
        self.write([self.rec()], session=str(uuid.uuid4()), slug="third-slug", agent=self.other_agent())
        os.unlink(self.target(slug="second-slug"))
        self.run_inproc(self.args())  # PASS
        self.write(raw=b"{\n")
        self.run_inproc(self.args())  # MALFORMED
        self.assertEqual(open_fds(), before)


class Decoys(Base):
    def test_fields_other_than_the_read_ones_are_not_read(self):
        decoy = self.rec(effort="low", requestedModel="claude-fable-5-1", advisorModel="claude-fable-5-1",
                         version="not a version", tools=["x"])
        decoy["api-request"] = {"params": {"model": "claude-fable-5-1", "effort": "max"}}
        decoy["message"]["content"] = [{"type": "text", "text": '"effort":"max" "model":"claude-fable-5-1"'}]
        api = {"type": "api-request", "params": {"model": "claude-fable-5-1", "effort": "max"}}
        user = {"type": "user", "effort": "max", "message": {"model": "claude-fable-5-1"}}
        self.write([api, user, decoy])
        self.assertLine(result("PASS", "opus", 3, "low"))

    def test_requested_and_advisor_model_do_not_raise_the_model(self):
        record = self.rec(model="claude-haiku-5-5", requestedModel=OPUS, advisorModel=OPUS)
        self.write([record])
        self.assertLine(result("BELOW", "haiku", 1, "high"))

    def test_capitalized_or_non_string_type_is_not_an_assistant_record(self):
        self.write([self.rec(type="Assistant", effort="low", agentId="x"), self.rec(type=["assistant"], effort=5),
                    {"effort": "low"}, self.rec(effort="max")])
        self.assertLine(result("PASS", "opus", 3, "max"))


class Appended(Base):
    def test_an_appended_higher_line_changes_nothing(self):
        path = self.write([self.rec(effort="medium")])
        with open(path, "ab") as fh:
            fh.write(json.dumps(self.rec(effort="max")).encode() + b"\n")
        self.assertLine(result("PASS", "opus", 3, "medium"))

    def test_an_appended_lower_line_lowers_the_result(self):
        path = self.write([self.rec(effort="high")])
        with open(path, "ab") as fh:
            fh.write(json.dumps(self.rec(effort="low")).encode() + b"\n")
        self.assertLine(result("BELOW", "opus", 3, "low", ("opus", "high")), self.args(("opus", "high")))

    def test_a_rewritten_line_passes(self):
        """A limit, not a protection (R-VER-1): a low line rewritten to a high value gives PASS."""
        self.write([self.rec(effort="low")])
        self.write([self.rec(effort="high")])  # the same file, its low line rewritten
        self.assertLine(result("PASS", "opus", 3, "high", ("opus", "high")), self.args(("opus", "high")))


class Types(Base):
    def test_effort_values(self):
        for effort, token in ((5, "MISSING_FIELD"), (None, "MISSING_FIELD"), ("High", "EFFORT_NOT_ALLOWED"),
                              ("\uff48\uff49\uff47\uff48", "EFFORT_NOT_ALLOWED"), (" high", "EFFORT_NOT_ALLOWED"),
                              ("high ", "EFFORT_NOT_ALLOWED"), ("ultra", "EFFORT_NOT_ALLOWED")):
            with self.subTest(effort=effort):
                self.write([self.rec(effort=effort, perTurnEffort=DROP)])
                self.assertStop(token)

    def test_missing_effort(self):
        self.write([self.rec(effort=DROP, perTurnEffort=DROP)])
        self.assertStop("MISSING_FIELD")

    def test_per_turn_effort(self):
        self.write([self.rec(perTurnEffort=DROP)])
        self.assertLine(result("PASS", "opus", 3, "high"))
        self.write([self.rec(perTurnEffort="xhigh")])
        self.assertStop("INCONSISTENT")
        self.write([self.rec(perTurnEffort=["high"])])
        self.assertStop("MISSING_FIELD")

    def test_is_sidechain_one(self):
        self.write([self.rec(isSidechain=1)])
        self.assertStop("BINDING_MISMATCH")

    def test_model_not_a_string_or_message_not_an_object(self):
        for message in ({"model": 5}, {"model": None}, {}, "claude-opus-5-5", None):
            with self.subTest(message=message):
                self.write([self.rec(message=message)])
                self.assertStop("MISSING_FIELD")
        self.write([self.rec(message=DROP)])
        self.assertStop("MISSING_FIELD")


class BadLines(Base):
    def malformed(self, raw):
        self.write(raw=raw)
        self.assertStop("MALFORMED")

    def good(self):
        return json.dumps(self.rec()).encode()

    def test_bad_lines(self):
        good = self.good()
        cases = {
            "truncated JSON": good[:-5] + b"\n",
            "duplicate key": b'{"type":"user","a":1,"a":2}\n',
            "escaped duplicate key": good[:-1] + b',"\\u0065ffort":"max"}\n',
            "NUL in a string": b'{"type":"user","a":"x\x00y"}\n',
            "NUL alone": b"\x00\n",
            "BOM": b"\xef\xbb\xbf" + good + b"\n",
            "empty line": good + b"\n\n" + good + b"\n",
            "only a newline": b"\n",
            "no final newline": good + b"\n" + good,
            "UTF-16": json.dumps(self.rec()).encode("utf-16") + b"\n",
            "invalid UTF-8": b'{"type":"user","a":"\xff"}\n',
            "NaN": b'{"type":"user","a":NaN}\n',
            "Infinity": b'{"type":"user","a":-Infinity}\n',
            "long integer": b'{"type":"user","a":1' + b"0" * 100 + b"}\n",
            "long float": b'{"type":"user","a":0.' + b"1" * 99 + b"}\n",
            "deep nesting": b'{"a":' * 100000 + b"1" + b"}" * 100000 + b"\n",
            "top-level array": b"[" + good + b"]\n",
            "top-level string": b'"assistant"\n',
            "spaces only": b"   \n",
        }
        for name, raw in cases.items():
            with self.subTest(name):
                self.malformed(raw)

    def test_number_at_the_length_limit_is_accepted(self):
        record = self.good()[:-1] + b',"n":1' + b"0" * 99 + b"}\n"
        self.write(raw=record)
        self.assertLine(result("PASS", "opus", 3, "high"))

    def test_u2028_is_content_not_a_line_break(self):
        record = self.rec()
        record["message"]["content"][0]["text"] = "a\u2028b\u2029c\x85d"
        self.write(raw=json.dumps(record, ensure_ascii=False).encode("utf-8") + b"\n")
        self.assertLine(result("PASS", "opus", 3, "high"))

    def test_empty_file_has_no_record(self):
        self.write(raw=b"")
        self.assertStop("NO_RECORD")

    def test_no_assistant_record(self):
        self.write([{"type": "user", "effort": "high"}, {"type": "assistant", "message": {"model": "<synthetic>"}}])
        self.assertStop("NO_RECORD")

    def test_truncated_during_the_read(self):
        path = self.write([self.rec(), self.rec()])
        size = os.path.getsize(path)
        real_read, calls = os.read, []

        def short_read(fd, n):
            calls.append(n)
            return real_read(fd, min(n, size // 2)) if len(calls) == 1 else b""

        with mock.patch.object(MOD, "read_config_file", return_value=SHIPPED_BYTES), \
                mock.patch.object(MOD.os, "read", short_read):
            self.assertStop("MALFORMED", inproc=True)


class Arguments(Base):
    def test_bad_agent_ids(self):
        self.write([self.rec()])
        for agent in (self.agent[:16], self.agent + "0", self.agent.upper(), "../" + self.agent[3:],
                      "g" * 17, self.agent + "\n", "", "-" + self.agent[1:]):
            with self.subTest(agent=agent):
                self.assertStop("BAD_ARGS", self.args(agent=agent))

    def test_nul_in_an_argument(self):
        self.write([self.rec()])
        self.assertStop("BAD_ARGS", self.args(projects=self.projects + "\x00x"), inproc=True)
        self.assertStop("BAD_ARGS", self.args(agent=self.agent[:16] + "\x00"), inproc=True)
        self.assertStop("BAD_ARGS", self.check_args(self.candidate() + "\x00"), inproc=True)

    def test_bad_option_use(self):
        self.write([self.rec()])
        base = self.args()
        bare = self.args(expect=())
        cases = {
            "repeated --agent-id": base + ["--agent-id", self.agent],
            "repeated --projects-dir": base + ["--projects-dir", self.projects],
            "repeated --expect-model": base + ["--expect-model", "opus"],
            "abbreviated --agent": ["subagent", "--projects-dir", self.projects, "--agent", self.agent] + base[5:],
            "abbreviated --projects": ["subagent", "--projects", self.projects, "--agent-id", self.agent] + base[5:],
            "abbreviated --config": base + ["--config", "a" * 40],
            "no expected values": bare,
            "only --expect-model": bare + ["--expect-model", "opus"],
            "only --expect-effort": bare + ["--expect-effort", "high"],
            "missing --agent-id": ["subagent", "--projects-dir", self.projects] + base[5:],
            "missing --projects-dir": ["subagent", "--agent-id", self.agent] + base[5:],
            "-h": ["-h"],
            "--help": ["--help"],
            "subagent -h": base + ["-h"],
            "subagent --help": base + ["--help"],
            "no subcommand": [],
            "options only": base[1:],
            "unknown subcommand": ["session"] + base[1:],
            "abbreviated subcommand": ["subagen"] + base[1:],
            "extra positional": base + ["extra-" + self.marker],
            "unknown option": base + ["--model", "opus"],
            "--candidate-config in subagent": base + ["--candidate-config", self.candidate()],
            "missing --floor": self.args(floor=None),
            "repeated --floor": base + ["--floor", "none"],
            "repeated --floor, another value": base + ["--floor", "work"],
            "--floor without a value": self.args(floor=None) + ["--floor"],
            "abbreviated --flo": self.args(floor=None) + ["--flo", "none"],
        }
        for name, argv in cases.items():
            with self.subTest(name):
                self.assertStop("BAD_ARGS", argv)

    def test_bad_expected_values(self):
        self.write([self.rec()])
        for expect in (("Opus", "high"), (OPUS, "high"), ("opus", "ultra"), ("opus", "High"), ("opus", ""),
                       ("inherit", "high"), ("unrecognized", "high"), ("mythos", "high"), ("", "high"),
                       ("opus ", "high")):
            with self.subTest(expect=expect):
                self.assertStop("BAD_ARGS", self.args(expect))

    def test_bad_floor_values(self):  # Issue #96 PR-2: only the five keys of FLOORS
        self.write([self.rec()])
        for floor in ("", "Work", "WORK", "work ", " work", "work\n", "review", "review_scan", "reviewscan",
                      "review-deep", "review-security", "scan", "light", "routine", "high", "max", "None", "null",
                      "unknown", "3", "review-light,work"):
            with self.subTest(floor=floor):
                self.assertStop("BAD_ARGS", self.args(floor=floor))
        for floor in ("work", "review-scan", "review-routine", "review-light", "none"):
            with self.subTest(floor=floor):  # a record below the expected values: BELOW with each floor
                self.assertLine(result("BELOW", "opus", 3, "high", ("opus", "max"), floor),
                                self.args(("opus", "max"), floor=floor))

    def test_expected_family_with_a_null_tier(self):  # Issue #96: a retired family is not a valid expected value
        self.write([self.rec()])
        script = self.make_pack(config_bytes(retire_sonnet))
        self.assertStop("BAD_ARGS", self.args(("sonnet", "medium")), script=script)
        self.assertLine(result("PASS", "opus", 3, "high", ("opus", "high")), self.args(("opus", "high")),
                        script=script)

    def test_bad_projects_dir(self):
        self.write([self.rec()])
        rel = os.path.relpath(self.projects, self.tmp)
        for projects in (rel, self.projects + "/", "/", self.projects + "/.", self.projects + "/../projects",
                         self.projects.replace("/projects", "//projects"), ""):
            with self.subTest(projects=projects):
                self.assertStop("BAD_ARGS", self.args(projects=projects))

    def test_projects_dir_is_a_symlink_a_file_or_missing(self):
        self.write([self.rec()])
        link = os.path.join(self.tmp, "link")
        os.symlink(self.projects, link)
        self.assertStop("SYMLINK", self.args(projects=link))
        path = os.path.join(self.tmp, "file")
        with open(path, "w") as fh:
            fh.write("x")
        self.assertStop("NOT_FOUND", self.args(projects=path))
        self.assertStop("NOT_FOUND", self.args(projects=os.path.join(self.tmp, "missing")))
        self.assertStop("NOT_FOUND", self.args(projects=os.path.join(path, "below")))


class Location(Base):
    def outside_tree(self):
        """A full slug/session/subagents tree with the target file, outside the projects directory."""
        outside = os.path.join(self.tmp, "outside")
        sub = os.path.join(outside, self.slug, self.session, "subagents")
        os.makedirs(sub)
        with open(os.path.join(sub, f"agent-{self.agent}.jsonl"), "wb") as fh:
            fh.write(json.dumps(self.rec()).encode() + b"\n")
        return outside

    def test_slug_symlink_is_skipped(self):
        outside = self.outside_tree()
        os.symlink(os.path.join(outside, self.slug), os.path.join(self.projects, self.slug))
        self.assertStop("NOT_FOUND")

    def test_session_symlink_is_skipped(self):
        outside = self.outside_tree()
        os.mkdir(os.path.join(self.projects, self.slug))
        os.symlink(os.path.join(outside, self.slug, self.session), os.path.join(self.projects, self.slug, self.session))
        self.assertStop("NOT_FOUND")

    def test_subagents_symlink_stops(self):
        outside = self.outside_tree()
        os.makedirs(os.path.join(self.projects, self.slug, self.session))
        os.symlink(os.path.join(outside, self.slug, self.session, "subagents"),
                   os.path.join(self.projects, self.slug, self.session, "subagents"))
        self.assertStop("SYMLINK")

    def test_target_symlink_stops(self):
        outside = self.outside_tree()
        os.symlink(os.path.join(outside, self.slug, self.session, "subagents", f"agent-{self.agent}.jsonl"),
                   self.target())
        self.assertStop("SYMLINK")

    def test_swapped_for_a_symlink_between_listing_and_open(self):
        self.write([self.rec()])
        real_open = os.open
        for level, err in ((self.slug, errno.ELOOP), (self.session, errno.ENOTDIR), ("subagents", errno.ELOOP),
                           (f"agent-{self.agent}.jsonl", errno.ELOOP)):
            def swapped(name, flags, mode=0o777, *, dir_fd=None, _level=level, _err=err):
                if name == _level:
                    raise OSError(_err, "swapped")
                return real_open(name, flags, mode, dir_fd=dir_fd)

            with self.subTest(level=level), mock.patch.object(MOD.os, "open", swapped):
                self.assertStop("SYMLINK", inproc=True)

    def test_errors_at_the_projects_dir_open_and_the_final_open(self):
        """Mocked os.open errors; no real swap between the lstat or the listing and the open (R-VER-1)."""
        self.write([self.rec()])
        real_open = os.open
        target = f"agent-{self.agent}.jsonl"
        for name, err, token in ((self.projects, errno.ELOOP, "SYMLINK"), (self.projects, errno.ENOTDIR, "SYMLINK"),
                                 (self.projects, errno.EIO, "INTERNAL"), (target, errno.ENOENT, "NOT_FOUND"),
                                 (target, errno.EIO, "INTERNAL")):
            def failing(path, flags, mode=0o777, *, dir_fd=None, _name=name, _err=err):
                if path == _name:
                    raise OSError(_err, "mocked")
                return real_open(path, flags, mode, dir_fd=dir_fd)

            before = open_fds()
            with self.subTest(name=os.path.basename(name), err=errno.errorcode[err]), \
                    mock.patch.object(MOD.os, "open", failing):
                self.assertStop(token, inproc=True)
            self.assertEqual(open_fds(), before)

    def test_wildcards_in_the_projects_dir_are_literal(self):
        wild = os.path.join(self.tmp, "p*j?[x]")
        os.mkdir(wild)
        self.write([self.rec()])
        os.rename(self.projects, os.path.join(self.tmp, "pAjBx"))
        self.assertStop("NOT_FOUND", self.args(projects=wild))
        os.rename(os.path.join(self.tmp, "pAjBx"), self.projects)
        os.rmdir(wild)
        os.rename(self.projects, wild)
        self.assertLine(result("PASS", "opus", 3, "high"), self.args(projects=wild))

    def test_two_sessions_with_the_same_agent_file(self):
        self.write([self.rec()])
        self.write([self.rec()], session=str(uuid.uuid4()))
        self.assertStop("AMBIGUOUS")

    def test_two_slugs_with_the_same_agent_file(self):
        self.write([self.rec()])
        self.write([self.rec()], slug="-other-" + secrets.token_hex(2))
        self.assertStop("AMBIGUOUS")

    def test_directories_with_names_out_of_format_are_not_entered(self):
        for slug, session in (("bad slug", self.session), ("slug~", self.session), (self.slug, self.session.upper()),
                              (self.slug, self.session + "x"), (self.slug, self.session.replace("-", ""))):
            with self.subTest(slug=slug, session=session):
                self.write([self.rec(sessionId=session)], slug=slug, session=session)
                self.assertStop("NOT_FOUND")
                shutil.rmtree(os.path.join(self.projects, slug))

    def test_subagents_is_a_file(self):
        os.makedirs(os.path.join(self.projects, self.slug, self.session))
        with open(os.path.join(self.projects, self.slug, self.session, "subagents"), "w") as fh:
            fh.write(json.dumps(self.rec()))
        self.assertStop("NOT_FOUND")

    def test_other_agent_file_only(self):
        self.write([self.rec(agentId=DROP)], agent=self.other_agent())
        self.assertStop("NOT_FOUND")


class Files(Base):
    def test_fifo_does_not_block(self):
        os.mkfifo(self.target())
        self.assertStop("NOT_REGULAR")

    def test_unix_socket(self):
        short = os.path.join(self.tmp, "s")
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.addCleanup(server.close)
        server.bind(short)
        os.rename(short, self.target())
        self.assertStop("NOT_REGULAR")

    def test_directory(self):
        os.mkdir(self.target())
        self.assertStop("NOT_REGULAR")

    def test_hardlink(self):
        path = self.write([self.rec()])
        os.link(path, os.path.join(self.tmp, "second-name"))
        self.assertStop("LINK_COUNT")

    def test_file_over_the_size_limit(self):
        path = self.write([self.rec()])
        with open(path, "r+b") as fh:
            fh.truncate(MOD.MAX_FILE_BYTES + 1)
        self.assertStop("TOO_LARGE")

    def test_line_over_the_length_limit(self):
        record = self.rec()
        record["pad"] = "x" * MOD.MAX_LINE_BYTES
        self.write([record])
        self.assertStop("TOO_LARGE")

    def test_line_count_limit(self):
        self.write(raw=b"{}\n" * MOD.MAX_LINES)
        self.assertStop("NO_RECORD")
        self.write(raw=b"{}\n" * (MOD.MAX_LINES + 1))
        self.assertStop("TOO_LARGE")

    def test_owner(self):
        """The transcript of another user; the configuration file is read with the real user ID."""
        self.write([self.rec()])
        with other_user():
            self.assertStop("OWNER", inproc=True)

    @unittest.skipIf(IS_ROOT, "root reads a file or directory with mode 000")
    def test_permission(self):
        path = self.write([self.rec()])
        for where in (path, os.path.dirname(path), os.path.join(self.projects, self.slug)):
            with self.subTest(where=os.path.relpath(where, self.projects)):
                mode = stat.S_IMODE(os.stat(where).st_mode)
                os.chmod(where, 0)
                try:
                    self.assertStop("PERMISSION")
                finally:
                    os.chmod(where, mode)

    def test_permission_error_on_open(self):
        self.write([self.rec()])
        real_open = os.open

        def denied(name, flags, mode=0o777, *, dir_fd=None):
            if name == f"agent-{self.agent}.jsonl":
                raise PermissionError(errno.EACCES, "denied")
            return real_open(name, flags, mode, dir_fd=dir_fd)

        with mock.patch.object(MOD.os, "open", denied):
            self.assertStop("PERMISSION", inproc=True)


class Binding(Base):
    def test_binding(self):
        for name, fields in (("agentId differs", {"agentId": self.other_agent()}),
                             ("sessionId differs", {"sessionId": str(uuid.uuid4())}),
                             ("isSidechain false", {"isSidechain": False}),
                             ("isSidechain string", {"isSidechain": "true"}),
                             ("agentId missing", {"agentId": DROP}),
                             ("sessionId missing", {"sessionId": DROP}),
                             ("isSidechain missing", {"isSidechain": DROP})):
            with self.subTest(name):
                self.write([self.rec(), self.rec(**fields)])
                self.assertStop("BINDING_MISMATCH")


class Models(Base):
    """The classification of Issue #96 (card I96-R2-C1 (a)) with the shipped configuration file."""

    def outcome(self, models, expect=("opus", "high"), effort="high", hidden=()):
        self.write([self.rec(model=model, effort=effort) for model in models])
        return self.run_script(self.args(expect), hidden=hidden)

    def test_listed_and_version_ids(self):
        for models, expect, want in (
                ([OPUS], ("opus", "high"), result("PASS", "opus", 3, "high", ("opus", "high"))),
                (["claude-opus-6-0"], ("opus", "high"), result("WARN", "opus", 3, "high", ("opus", "high"))),
                (["claude-opus-4-8"], ("opus", "high"), result("WARN", "opus", 3, "high", ("opus", "high"))),
                (["claude-opus-6"], ("opus", "high"), result("WARN", "opus", 3, "high", ("opus", "high"))),
                (["claude-sonnet-5-5"], ("opus", "high"), result("BELOW", "sonnet", 2, "high", ("opus", "high"))),
                (["claude-sonnet-5-5"], ("sonnet", "medium"),
                 result("WARN", "sonnet", 2, "high", ("sonnet", "medium"))),
                (["claude-haiku-5-5"], ("haiku", "low"), result("WARN", "haiku", 1, "high", ("haiku", "low"))),
                (["claude-fable-5-1"], ("opus", "high"), result("WARN", "fable", 4, "high", ("opus", "high"))),
                (["claude-fable-5-1"], ("fable", "high"), result("WARN", "fable", 4, "high", ("fable", "high"))),
                ([OPUS], ("fable", "high"), result("BELOW", "opus", 3, "high", ("fable", "high")))):
            with self.subTest(models=models, expect=expect):
                self.assertEqual(self.outcome(models, expect), want)

    def test_lower_family_words(self):
        """Step 3: a word that names a family below the expected one gives BELOW, whatever the separators."""
        for model, family in (("anthropic.claude-sonnet-5-5", "sonnet"), ("claude-haiku\u00a05-5", "haiku"),
                              ("claude\u2011haiku\u20115\u20115", "haiku"), ("claude\u00b7haiku\u00b75\u00b75", "haiku"),
                              ("CLAUDE-HAIKU-5-5", "haiku"), ("haiku", "haiku"), ("x sonnet4 y", "sonnet"),
                              ("claude-sonnet-5-5 claude-haiku-5-5", "haiku"), ("claude-sonnet-5-5\n", "sonnet")):
            with self.subTest(model=model):
                self.assertEqual(self.outcome([model], hidden=(model,) if len(model) > 6 else ()),
                                 result("BELOW", family, TIERS[family], "high", ("opus", "high")))

    def test_unrecognized_values_stop(self):
        for model, expect in (
                ("", ("opus", "high")), ("   ", ("opus", "high")), ("unknown", ("opus", "high")),
                ("opus", ("opus", "high")), ("claude-opus-6-0\n", ("opus", "high")),
                ("claude-opus-5-5\x07", ("opus", "high")), ("claude-opus-5-5\x00", ("opus", "high")),
                ("Claude-Opus-5-5", ("opus", "high")), (" claude-opus-5-5", ("opus", "high")),
                ("claude-opus-5-5[1m]", ("opus", "high")), ("claude-opus-5-5-v1:0", ("opus", "high")),
                ("arn:aws:bedrock:us-east-1:000000000000:inference-profile/us.anthropic.claude-opus-5-5-v1:0",
                 ("opus", "high")),
                ("anthropic.claude-sonnet-5-5", ("sonnet", "medium")), ("claude-mythos-1-0", ("opus", "high")),
                ("claude-opus-" + "5" * 100, ("opus", "high")), ("x" * 10000, ("opus", "high")),
                ("x" * 200 + "-haiku", ("opus", "high"))):
            with self.subTest(model=model[:40], expect=expect):
                self.assertEqual(self.outcome([model], expect, hidden=(model,) if len(model) > 6 else ()),
                                 "STOP MODEL_NOT_RECOGNIZED")

    def test_mixed_records(self):
        """rev9 section 2: more than one family gives BELOW when a record is below, else STOP; one family aggregates."""
        for models, efforts, want in (
                ([OPUS, "claude-opus-6-0"], ("high", "high"), result("WARN", "opus", 3, "high", ("opus", "high"))),
                ([OPUS, "claude-sonnet-5-5"], ("high", "high"), result("BELOW", "sonnet", 2, "high", ("opus", "high"))),
                ([OPUS, "claude-fable-5-1"], ("high", "high"), "STOP MODEL_NOT_RECOGNIZED"),
                ([OPUS, "unknown"], ("high", "high"), "STOP MODEL_NOT_RECOGNIZED"),
                (["unknown", OPUS], ("high", "high"), "STOP MODEL_NOT_RECOGNIZED"),
                (["unknown"], ("low",), result("BELOW", "unrecognized", "none", "low", ("opus", "high"))),
                ([OPUS, "unknown"], ("low", "high"), result("BELOW", "unrecognized", "none", "low", ("opus", "high"))),
                ([OPUS, "unknown"], ("high", "low"), result("BELOW", "unrecognized", "none", "low", ("opus", "high"))),
                ([OPUS, OPUS], ("high", "medium"), result("BELOW", "opus", 3, "medium", ("opus", "high"))),
                (["claude-opus-6-0", "claude-sonnet-5-5", "claude-haiku-5-5"], ("max", "max", "max"),
                 result("BELOW", "haiku", 1, "max", ("opus", "high")))):
            with self.subTest(models=models, efforts=efforts):
                self.write([self.rec(model=m, effort=e) for m, e in zip(models, efforts)])
                self.assertEqual(self.run_script(self.args(("opus", "high"))), want)

    def test_immediate_stops_come_before_the_aggregate(self):
        for records, token in (
                ([self.rec(model="unknown"), self.rec(effort="ultra", perTurnEffort=DROP)], "EFFORT_NOT_ALLOWED"),
                ([self.rec(model="claude-sonnet-5-5"), self.rec(isSidechain=False)], "BINDING_MISMATCH"),
                ([self.rec(model="claude-haiku-5-5"), self.rec(perTurnEffort="max")], "INCONSISTENT"),
                ([self.rec(model="unknown"), self.rec(effort=DROP, perTurnEffort=DROP)], "MISSING_FIELD"),
                ([self.rec(model="claude-sonnet-5-5", effort="low"), self.rec(model=5)], "MISSING_FIELD")):
            with self.subTest(token=token):
                self.write(records)
                self.assertStop(token, self.args(("opus", "high")))

    def test_retired_family(self):
        """A family with a null tier never meets an expected value: its listed and version IDs give BELOW."""
        script = self.make_pack(config_bytes(retire_sonnet))
        for model in ("claude-sonnet-5-5", "claude-sonnet-6-0", "x.sonnet"):
            with self.subTest(model=model):
                self.write([self.rec(model=model, effort="max")])
                self.assertLine(result("BELOW", "sonnet", "null", "max", ("haiku", "low")), self.args(("haiku", "low")),
                                script=script)

    def test_lowest_prefers_a_version_record_on_a_tie(self):
        self.assertEqual(MOD.lowest([("listed", "opus", 3), ("version", "opus", 3)]), 1)
        self.assertEqual(MOD.lowest([("version", "opus", 3), ("listed", "sonnet", 2)]), 1)
        self.assertEqual(MOD.lowest([("listed", "opus", 3), ("unrecognized", None, -1), ("lower", "x", 0)]), 1)
        self.assertEqual(MOD.lowest([("listed", "opus", 3), ("listed", "opus", 3)]), 0)


class Floors(Base):
    """--floor (Issue #96 PR-2, design d5 section 2): the check order and the floor of each value."""

    def outcome(self, records, expect, floor, script=COPY):
        self.write([self.rec(model=model, effort=effort) for model, effort in records])
        return self.run_script(self.args(expect, floor=floor), script=script)

    def test_the_examples_of_the_design(self):
        fable = "claude-fable-5-1"
        sonnet = "claude-sonnet-5-5"
        for records, expect, floor, want in (
                ([(OPUS, "xhigh")], ("opus", "xhigh"), "review-scan",
                 result("PASS", "opus", 3, "xhigh", ("opus", "xhigh"), "review-scan")),
                ([(OPUS, "high")], ("opus", "high"), "review-scan",  # step 4
                 result("BELOW", "opus", 3, "high", ("opus", "high"), "review-scan")),
                ([(sonnet, "medium")], ("sonnet", "medium"), "review-light",
                 result("WARN", "sonnet", 2, "medium", ("sonnet", "medium"), "review-light")),
                ([(sonnet, "medium")], ("sonnet", "medium"), "review-routine",  # step 4
                 result("BELOW", "sonnet", 2, "medium", ("sonnet", "medium"), "review-routine")),
                ([("claude-haiku-5-5", "high")], ("opus", "high"), "work",  # step 3
                 result("BELOW", "haiku", 1, "high", ("opus", "high"), "work")),
                ([(OPUS, "xhigh"), (fable, "xhigh")], ("opus", "xhigh"), "review-scan",  # step 5
                 "STOP MODEL_NOT_RECOGNIZED"),
                ([(OPUS, "xhigh"), (fable, "xhigh")], ("opus", "high"), "review-scan",  # step 4 comes first
                 result("BELOW", "opus", 3, "xhigh", ("opus", "high"), "review-scan")),
                ([("unknown", "high")], ("opus", "high"), "none", "STOP MODEL_NOT_RECOGNIZED")):
            with self.subTest(records=records, expect=expect, floor=floor):
                self.assertEqual(self.outcome(records, expect, floor), want)

    def test_the_same_records_without_a_floor(self):  # the BELOW lines of step 4 above come from the floor alone
        for records, expect, want in (
                ([(OPUS, "high")], ("opus", "high"), result("PASS", "opus", 3, "high", ("opus", "high"))),
                ([("claude-sonnet-5-5", "medium")], ("sonnet", "medium"),
                 result("WARN", "sonnet", 2, "medium", ("sonnet", "medium"))),
                ([(OPUS, "xhigh"), ("claude-fable-5-1", "xhigh")], ("opus", "high"), "STOP MODEL_NOT_RECOGNIZED")):
            with self.subTest(records=records, expect=expect):
                self.assertEqual(self.outcome(records, expect, "none"), want)

    def test_each_floor_at_and_below(self):
        family_of = {1: "haiku", 2: "sonnet", 3: "opus"}
        for floor, (tier, effort) in (("work", (3, "high")), ("review-scan", (3, "xhigh")),
                                      ("review-routine", (3, "high")), ("review-light", (2, "medium"))):
            lower_effort = MOD.EFFORT_ORDER[MOD.EFFORT_ORDER.index(effort) - 1]
            for expect, word in (((family_of[tier], effort), "PASS"), ((family_of[tier], "max"), "PASS"),
                                 (("fable", effort), "BELOW"),  # step 3: the opus record is below fable
                                 ((family_of[tier - 1], effort), "BELOW"), ((family_of[tier], lower_effort), "BELOW"),
                                 ((family_of[tier - 1], "max"), "BELOW")):
                with self.subTest(floor=floor, expect=expect):
                    self.assertEqual(self.outcome([(OPUS, "max")], expect, floor),
                                     result(word, "opus", 3, "max", expect, floor))
        for expect in (("haiku", "low"), ("opus", "max")):
            with self.subTest(floor="none", expect=expect):
                self.assertEqual(self.outcome([(OPUS, "max")], expect, "none"),
                                 result("PASS", "opus", 3, "max", expect, "none"))

    def test_the_floor_uses_the_tiers_of_the_file_of_this_call(self):
        def swap(config):  # opus tier 2 and sonnet tier 3 in this copy only
            config["families"]["opus"]["tier"], config["families"]["sonnet"]["tier"] = 2, 3
        script = self.make_pack(config_bytes(swap))
        self.assertEqual(self.outcome([(OPUS, "high")], ("opus", "high"), "work", script),
                         "BELOW model=opus tier=2 effort=high expected=opus/high expected_tier=2 floor=work")
        self.assertEqual(self.outcome([("claude-sonnet-5-5", "high")], ("sonnet", "high"), "work", script),
                         "WARN model=sonnet tier=3 effort=high expected=sonnet/high expected_tier=3 floor=work")

    def test_immediate_stops_come_before_the_floor(self):
        self.write([self.rec(model="claude-haiku-5-5", effort="low"), self.rec(isSidechain=False)])
        self.assertStop("BINDING_MISMATCH", self.args(("haiku", "low"), floor="review-scan"))
        self.assertStop("CONFIG", self.args(("haiku", "low"), floor="review-scan"), script=self.make_pack(b"{}"))


class Validator(unittest.TestCase):
    """validate_config: each rule of the design (rev7 section 3.1, rev8 section 2.1) with a positive and a negative case."""

    def bad(self, data, name=None):
        with self.subTest(name or repr(data[:60])):
            with self.assertRaises(MOD.Stop) as caught:
                MOD.validate_config(data)
            self.assertEqual(caught.exception.reason, "CONFIG")

    def good(self, data, name=None):
        with self.subTest(name or repr(data[:60])):
            self.assertIsInstance(MOD.validate_config(data), dict)

    def change(self, fn, ok, name):
        (self.good if ok else self.bad)(config_bytes(fn), name)

    def test_the_shipped_file_passes(self):
        self.assertEqual(MOD.validate_config(SHIPPED_BYTES), SHIPPED)

    def test_shipped_content(self):  # rev7 section 2: the content of the file, value by value
        self.assertEqual(SHIPPED["schema"], 1)
        self.assertEqual({n: (f["tier"], f["ids"]) for n, f in SHIPPED["families"].items()},
                         {"haiku": (1, []), "sonnet": (2, []), "opus": (3, [OPUS]), "fable": (4, [])})
        self.assertEqual(list(SHIPPED["roles"]), list(MOD.ROLE_NAMES))
        for name, role in SHIPPED["roles"].items():  # Issue #96 PR-2: a review or a scan uses its row value
            with self.subTest(role=name):
                if name.startswith(("review-", "scan")):
                    self.assertEqual(role["effort"][0], role["effort"][1])
                else:
                    self.assertEqual(role["effort"][1], "max")
        self.assertEqual({name: role["effort"] for name, role in SHIPPED["roles"].items()}, {
            "orchestration": ["high", "max"], "explore": ["low", "max"], "explore-synthesis": ["medium", "max"],
            "implement": ["high", "max"], "implement-reduced": ["medium", "max"], "review-routine": ["high", "high"],
            "review-routine-light": ["medium", "medium"], "review-deep": ["xhigh", "xhigh"],
            "review-security": ["xhigh", "xhigh"], "scan": ["xhigh", "xhigh"]})

    def test_strict_json(self):
        good = SHIPPED_BYTES
        self.bad(good.decode().encode("utf-16"), "UTF-16")
        self.bad(b"\xef\xbb\xbf" + good, "BOM")
        self.bad(good.replace(b'"schema": 1,', b'"schema": 1, "schema": 1,'), "duplicate key")
        self.bad(good.replace(b'"schema": 1,', b'"schema": 1, "sch\\u0065ma": 1,'), "escaped duplicate key")
        self.bad(good.replace(b'"schema": 1', b'"schema": NaN'), "NaN")
        self.bad(good.replace(b'"schema": 1', b'"schema": Infinity'), "Infinity")
        self.bad(good.replace(b'"schema": 1', b'"schema": 1' + b"0" * 100), "long number")
        self.bad(good.replace(b'"schema": 1', b'"schema": 0.' + b"1" * 100), "long float")
        self.bad(good[:-3], "cut short")
        self.bad(good + b"x", "trailing text")
        self.bad(good.replace(b"Opus 5.5", b"Opus \xff"), "invalid UTF-8")
        self.bad(b"", "empty")
        self.bad(b"[]", "array")
        self.bad(good.decode(), "str, not bytes")
        self.bad(bytearray(good), "bytearray, not bytes")
        self.bad(b"[" * 30000 + b"]" * 30000, "deep nesting")

    def test_size_limit(self):
        pad = MOD.MAX_CONFIG_BYTES - len(SHIPPED_BYTES)
        at_limit = SHIPPED_BYTES.replace(b'"Claude 5.5 (Opus 5.5)"', b'"Claude 5.5 (Opus 5.5)' + b"x" * pad + b'"')
        self.assertEqual(len(at_limit), MOD.MAX_CONFIG_BYTES)
        self.good(at_limit, "at the size limit")
        self.bad(at_limit.replace(b'x"', b'xx"', 1), "one byte over the size limit")

    def test_depth_limit(self):
        self.assertEqual(MOD.MAX_CONFIG_DEPTH, 8)
        with mock.patch.object(MOD, "MAX_CONFIG_DEPTH", 4):
            self.good(SHIPPED_BYTES, "depth 4 is the depth of the shipped file")
        with mock.patch.object(MOD, "MAX_CONFIG_DEPTH", 3):
            self.bad(SHIPPED_BYTES, "over the depth limit")

    def test_closed_key_sets(self):
        cases = [
            (lambda c: c.update(extra=1), "extra top-level key"),
            (lambda c: c.pop("responsibility"), "missing top-level key"),
            (lambda c: c["validated_with"].update(by="x"), "extra validated_with key"),
            (lambda c: c["validated_with"].pop("note"), "missing validated_with key"),
            (lambda c: c["families"]["opus"].update(line="x"), "extra family key"),
            (lambda c: c["families"]["opus"].pop("basis"), "missing family key"),
            (lambda c: c["roles"]["scan"].update(model="opus"), "extra role key"),
            (lambda c: c["roles"]["scan"].pop("effort"), "role without effort"),
            (lambda c: c["roles"]["orchestration"].pop("family"), "role without family"),
            (lambda c: c.update(validated_with="x"), "validated_with not an object"),
            (lambda c: c["validated_with"].update(note=["x"]), "validated_with note not a string"),
            (lambda c: c.update(responsibility=None), "responsibility not a string"),
            (lambda c: c.update(families=[]), "families not an object"),
            (lambda c: c.update(families={}), "no family"),
            (lambda c: c.update(roles=[]), "roles not an object"),
            (lambda c: c["roles"].update(scan=["opus"]), "role not an object"),
            (lambda c: c["families"].update(opus=[3]), "family not an object"),
        ]
        for fn, name in cases:
            self.change(fn, False, name)
        self.change(lambda c: c["roles"]["scan"].pop("agent"), True, "a role without an agent")

    def test_schema(self):
        for value in (2, 0, "1", 1.0, True, None):
            self.change(lambda c, v=value: c.update(schema=v), False, f"schema {value!r}")

    def test_family_names(self):
        def add(name, tier=5):
            return lambda c: c["families"].update({name: {"tier": tier, "ids": [], "basis": "x"}})
        for name in ("Mythos", "my-thos", "my_thos", "mythos5", "", "a" * 21, "m\u00fdthos", " mythos"):
            self.change(add(name), False, f"family name {name!r}")
        for name in ("unrecognized", "none", "null", "unknown", "inherit", "default", *MOD.EFFORT_ORDER):
            self.change(add(name), False, f"reserved family name {name!r}")
        self.change(add("a" * 20), True, "a family name of 20 letters")
        self.change(add("mythos", None), True, "a new family with a null tier")

    def test_tiers(self):
        for value in (True, False, 0, 100, -1, 1.0, "3", [3]):
            self.change(lambda c, v=value: c["families"]["fable"].update(tier=v), False, f"tier {value!r}")
        self.change(lambda c: c["families"]["fable"].update(tier=99), True, "tier 99")
        self.change(lambda c: c["families"]["fable"].update(tier=None), True, "tier null")
        self.change(lambda c: c["families"]["fable"].update(tier=3), False, "two equal tiers")
        self.change(lambda c: (c["families"]["fable"].update(tier=None), c["families"].update(
            mythos={"tier": None, "ids": [], "basis": "x"})), True, "two null tiers")

    def test_ids(self):
        def ids(family, values):
            return lambda c: c["families"][family].update(ids=values)
        for values, name in (("claude-opus-5-5", "ids not a list"), ([5], "an ID not a string"), ([None], "null ID"),
                             (["claude-Opus-5-5"], "an upper-case ID"), (["claude_opus_5_5"], "underscore"),
                             (["claude-opus-5-5 "], "space"), (["claude-opus-5-5\n"], "newline"),
                             (["claude-opus/5"], "slash"), (["claude-opus-5:0"], "colon"),
                             (["claude-opus-\u0665"], "non-ASCII digit"), ([""], "empty ID"),
                             (["claude-opus-" + "5" * 89], "101 characters"),
                             ([OPUS, OPUS], "the same ID twice in a family"),
                             (["claude-5-5"], "no word of its own family"), (["claude-opu-5"], "a shorter word"),
                             (["claude-opusx-5"], "a longer word"),
                             (["claude-opus-sonnet-5"], "a word of another family"),
                             (["claude-opus-haiku4-5"], "a word of another family with digits"),
                             ([OPUS, "fable.opus.1"], "a second ID with another family word")):
            self.change(ids("opus", values), False, name)
        self.change(lambda c: c["families"]["sonnet"].update(ids=[OPUS]), False, "an ID in two families")
        for values, name in ((["claude-opus-" + "5" * 88], "100 characters"), ([OPUS, "claude-opus4.5"], "opus4"),
                             (["claude-opus-5-5", "bedrock.opus.v1-0"], "dots"), ([], "no ID")):
            self.change(ids("opus", values), True, name)

    def test_basis(self):
        for value in ("", None, 5, ["x"]):
            self.change(lambda c, v=value: c["families"]["opus"].update(basis=v), False, f"basis {value!r}")
        self.change(lambda c: c["families"]["opus"].update(basis="x"), True, "a short basis")

    def test_roles(self):
        self.change(lambda c: c["roles"].pop("scan"), False, "a role missing")
        self.change(lambda c: c["roles"].update(extra={"family": "opus", "effort": ["high", "high"]}), False,
                    "an extra role")
        self.change(lambda c: c["roles"]["scan"].update(family="mythos"), False, "an unknown family")
        self.change(lambda c: c["roles"]["scan"].update(family=["opus"]), False, "a family that is not a string")
        self.change(lambda c: c["families"]["sonnet"].update(tier=None), False, "a role on a retired family")
        self.change(retire_sonnet, True, "retired with the roles moved")
        for value in ("high", ["high"], ["high", "high", "high"], ["high", 5], ["high", "ultra"], ["High", "high"],
                      ["xhigh", "high"], ["max", "low"], None):
            self.change(lambda c, v=value: c["roles"]["scan"].update(effort=v), False, f"effort {value!r}")
        for value in (["high", "xhigh"], ["low", "max"], ["max", "max"]):
            self.change(lambda c, v=value: c["roles"]["scan"].update(effort=v), True, f"effort {value!r}")

    def test_agents(self):
        for value in ("general-purpose", "Dev-Reviewer", "", None, ["dev-reviewer"]):
            self.change(lambda c, v=value: c["roles"]["scan"].update(agent=v), False, f"agent {value!r}")
        for value in (False, 1, "true", None):
            self.change(lambda c, v=value: c["roles"]["review-routine"].update(agent_default=v), False,
                        f"agent_default {value!r}")
        self.change(lambda c: c["roles"]["orchestration"].update(agent_default=True), False,
                    "agent_default without an agent")
        self.change(lambda c: c["roles"]["review-deep"].update(agent_default=True), False,
                    "two agent_default roles of one agent")
        self.change(lambda c: c["roles"]["review-routine"].pop("agent_default"), True,
                    "an agent without an agent_default role (check_pack requires it, not the validator)")
        self.change(lambda c: c["roles"]["review-routine"].update(family="haiku", effort=["low", "low"]), True,
                    "a role under a floor (card I96-C4 (a): not a validator error)")

    def test_pure(self):
        """No file, process or argument is read while the module loads or validates (rev7 section 3.1)."""
        with mock.patch.object(subprocess, "Popen", side_effect=AssertionError("Popen")):
            module = load_script()
        with mock.patch.object(module.subprocess, "Popen", side_effect=AssertionError("Popen")), \
                mock.patch.object(module.os, "open", side_effect=AssertionError("open")), \
                mock.patch.object(module.os, "read", side_effect=AssertionError("read")), \
                mock.patch.object(module.sys, "argv", ["-", "subagent"]), \
                mock.patch.object(module, "from_stdin", side_effect=AssertionError("from_stdin")):
            self.assertEqual(module.validate_config(SHIPPED_BYTES), SHIPPED)


class PathForm(Base):
    """A run by its path reads the model-config.json next to its scripts folder, opened as strictly as the transcript."""

    def setUp(self):
        super().setUp()
        self.write([self.rec()])

    def pack_config(self, script):
        return os.path.join(os.path.dirname(os.path.dirname(script)), "model-config.json")

    def test_a_copy_reads_its_own_file(self):
        self.assertLine(result("PASS", "opus", 3, "high"), script=self.make_pack())
        self.assertStop("CONFIG", script=self.make_pack(b"{}"))
        self.assertStop("CONFIG", script=self.make_pack(None))

    def test_wrong_name_or_parent(self):
        for script, parent in (("readback.py", "scripts"), ("model_effort_readback.py", "bin"),
                               ("model_effort_readback.py", "Scripts")):
            with self.subTest(script=script, parent=parent):
                self.assertStop("BAD_ARGS", script=self.make_pack(script=script, parent=parent))
        with mock.patch.object(MOD, "__file__", os.path.join(self.tmp, "x", "model_effort_readback.py")):
            self.assertStop("BAD_ARGS", inproc=True)

    def test_symlink(self):
        script = self.make_pack(None)
        real = self.candidate()
        os.symlink(real, self.pack_config(script))
        self.assertStop("CONFIG", script=script)

    def test_hard_link(self):
        script = self.make_pack()
        os.link(self.pack_config(script), os.path.join(self.tmp, "second-name"))
        self.assertStop("CONFIG", script=script)

    def test_other_owner(self):
        with mock.patch.object(MOD.os, "getuid", return_value=os.getuid() + 1):
            self.assertStop("CONFIG", inproc=True)

    def test_size(self):
        pad = MOD.MAX_CONFIG_BYTES - len(SHIPPED_BYTES)
        at_limit = SHIPPED_BYTES.replace(b'"Claude 5.5 (Opus 5.5)"', b'"Claude 5.5 (Opus 5.5)' + b"x" * pad + b'"')
        self.assertLine(result("PASS", "opus", 3, "high"), script=self.make_pack(at_limit))
        self.assertStop("CONFIG", script=self.make_pack(at_limit + b"\n"))
        script = self.make_pack()
        with open(self.pack_config(script), "r+b") as fh:
            fh.truncate(MOD.MAX_FILE_BYTES + 1)
        self.assertStop("CONFIG", script=script)

    def test_not_a_regular_file(self):
        script = self.make_pack(None)
        os.mkfifo(self.pack_config(script))
        self.assertStop("CONFIG", script=script)  # no block
        os.unlink(self.pack_config(script))
        os.mkdir(self.pack_config(script))
        self.assertStop("CONFIG", script=script)

    def test_config_base_by_path(self):
        self.assertStop("BAD_ARGS", self.args(base="a" * 40))
        self.assertStop("BAD_ARGS", self.args(base="a" * 64))

    def test_config_is_read_before_the_transcript(self):
        shutil.rmtree(self.projects)
        self.assertStop("CONFIG", script=self.make_pack(b"{}"))


class RealPath(Base):
    """IR1-S-05 (Issue #96 PR-2): a run by its path reads the model-config.json next to the scripts folder of the real
    path of the script. Each case runs the script in a subprocess with the literal ${skill}/../dev-core/scripts/...
    form of the rules, `..` included. OTHER gives WARN for the opus record, the shipped file gives PASS, so the two
    readings differ."""

    OTHER = config_bytes(lambda c: c["families"]["opus"].update(ids=[]))
    PASS = result("PASS", "opus", 3, "high")
    WARN = result("WARN", "opus", 3, "high")

    def setUp(self):
        super().setUp()
        self.write([self.rec()])

    def skills(self, name, config=SHIPPED_BYTES, script=True, gate=True):
        """<tmp>/<name>-*/ with dev-gate/ and dev-core/model-config.json (config None: none) and, when script is
        True, dev-core/scripts/model_effort_readback.py."""
        root = tempfile.mkdtemp(prefix=name + "-", dir=self.tmp)
        os.makedirs(os.path.join(root, "dev-core"))
        if gate:
            os.mkdir(os.path.join(root, "dev-gate"))
        if script:
            os.mkdir(os.path.join(root, "dev-core", "scripts"))
            shutil.copy(SCRIPT, os.path.join(root, "dev-core", "scripts", "model_effort_readback.py"))
        if config is not None:
            with open(os.path.join(root, "dev-core", "model-config.json"), "wb") as fh:
                fh.write(config)
        return root

    def literal(self, root):
        """The path form of the rules: ${CLAUDE_SKILL_DIR}/../dev-core/scripts/model_effort_readback.py."""
        return os.path.join(root, "dev-gate") + "/../dev-core/scripts/model_effort_readback.py"

    def outcome(self, root):
        return self.run_script(self.args(), script=self.literal(root))

    def test_the_literal_form_of_real_directories(self):  # the same file name in another scripts folder
        self.assertEqual(self.outcome(self.skills("plain")), self.PASS)
        self.assertEqual(self.outcome(self.skills("other", self.OTHER)), self.WARN)

    def test_skill_directory_is_a_symlink(self):
        real = self.skills("real")
        shown = self.skills("shown", self.OTHER, gate=False)
        os.symlink(os.path.join(real, "dev-gate"), os.path.join(shown, "dev-gate"))
        self.assertEqual(self.outcome(shown), self.PASS)  # the file next to the real location, not the literal one
        shown_only = self.skills("shown-only", self.OTHER, script=False, gate=False)
        os.symlink(os.path.join(real, "dev-gate"), os.path.join(shown_only, "dev-gate"))
        self.assertEqual(self.outcome(shown_only), self.PASS)

    def test_configuration_file_at_the_real_location_is_a_symlink(self):
        real = self.skills("real", None)
        os.symlink(self.candidate(), os.path.join(real, "dev-core", "model-config.json"))
        shown = self.skills("shown", gate=False)
        os.symlink(os.path.join(real, "dev-gate"), os.path.join(shown, "dev-gate"))
        self.assertEqual(self.outcome(shown), "STOP CONFIG")
        self.assertEqual(self.outcome(real), "STOP CONFIG")

    def test_scripts_folder_is_a_symlink(self):
        for name, want in (("scripts", self.PASS), ("bin", "STOP BAD_ARGS")):
            with self.subTest(target=name):
                target = tempfile.mkdtemp(prefix="target-", dir=self.tmp)
                os.mkdir(os.path.join(target, name))
                shutil.copy(SCRIPT, os.path.join(target, name, "model_effort_readback.py"))
                with open(os.path.join(target, "model-config.json"), "wb") as fh:
                    fh.write(SHIPPED_BYTES)
                shown = self.skills("shown", self.OTHER, script=False)
                os.symlink(os.path.join(target, name), os.path.join(shown, "dev-core", "scripts"))
                self.assertEqual(self.outcome(shown), want)  # PASS: the parent of the target, not dev-core

    def test_script_file_is_a_symlink(self):
        for name, want in (("readback.py", "STOP BAD_ARGS"), ("model_effort_readback.py", self.PASS)):
            with self.subTest(target=name):
                target = tempfile.mkdtemp(prefix="target-", dir=self.tmp)
                os.mkdir(os.path.join(target, "scripts"))
                shutil.copy(SCRIPT, os.path.join(target, "scripts", name))
                with open(os.path.join(target, "model-config.json"), "wb") as fh:
                    fh.write(SHIPPED_BYTES)
                shown = self.skills("shown", self.OTHER, script=False)
                os.mkdir(os.path.join(shown, "dev-core", "scripts"))
                os.symlink(os.path.join(target, "scripts", name),
                           os.path.join(shown, "dev-core", "scripts", "model_effort_readback.py"))
                self.assertEqual(self.outcome(shown), want)  # PASS: the file next to the other scripts folder


class FakeGit(Base):
    """The git calls of the stdin form, with a fake git in this process (Issue #96, rev8 section 4.1)."""

    BASE = "c" * 40

    def setUp(self):
        super().setUp()
        self.write([self.rec()])
        self.bin = os.path.join(self.tmp, "bin")
        os.mkdir(self.bin)
        self.log = os.path.join(self.tmp, "argv.log")
        self.config = self.candidate()

    def fake(self, rev_parse, cat_file):
        """A fake git: logs its arguments, then runs the shell text for the subcommand."""
        path = os.path.join(self.bin, "git")
        with open(path, "w") as fh:
            fh.write(f'#!/bin/sh\nfor a in "$@"; do printf "%s\\n" "$a" >> "{self.log}"; done\n'
                     f'case "$2" in\n  rev-parse) {rev_parse} ;;\n  cat-file) {cat_file} ;;\nesac\nexit 99\n')
        os.chmod(path, 0o755)

    def run_stdin(self, argv=None, timeout=None):
        argv = self.args(base=self.BASE) if argv is None else argv
        patches = [mock.patch.object(MOD, "from_stdin", return_value=True),
                   mock.patch.dict(os.environ, {"PATH": self.bin})]
        if timeout is not None:
            patches.append(mock.patch.object(MOD, "GIT_TIMEOUT", timeout))
        with contextlib.ExitStack() as stack:
            for patch in patches:
                stack.enter_context(patch)
            start = time.monotonic()
            line = self.run_inproc(argv, hidden=(self.BASE,))
        return line, time.monotonic() - start

    def ok_rev_parse(self, code=0):
        return f'printf "%s\\n" "{self.BASE}"; exit {code}'

    def ok_cat_file(self, code=0):
        return f'{shutil.which("cat")} "{self.config}"; exit {code}'

    def test_two_calls_with_literal_arguments(self):
        self.fake(self.ok_rev_parse(), self.ok_cat_file())
        self.assertEqual(self.run_stdin()[0], result("PASS", "opus", 3, "high"))
        with open(self.log) as fh:
            self.assertEqual(fh.read().split("\n")[:-1], [
                "--no-replace-objects", "rev-parse", "--verify", "--quiet", self.BASE + "^{commit}",
                "--no-replace-objects", "cat-file", "blob", self.BASE + ":" + CONFIG_IN_REPO])

    def test_an_exit_code_other_than_0_with_output(self):
        for rev_parse, cat_file in ((self.ok_rev_parse(1), self.ok_cat_file()),
                                    (self.ok_rev_parse(), self.ok_cat_file(1)),
                                    (self.ok_rev_parse(), self.ok_cat_file(128))):
            with self.subTest(rev_parse=rev_parse[-6:], cat_file=cat_file[-8:]):
                self.fake(rev_parse, cat_file)
                self.assertEqual(self.run_stdin()[0], "STOP CONFIG")

    def test_rev_parse_output_must_be_the_literal(self):
        for output in ("d" * 40 + "\\n", self.BASE, self.BASE + "\\n" + self.BASE + "\\n", " " + self.BASE + "\\n",
                       self.BASE.upper() + "\\n", self.BASE + "\\r\\n", ""):
            with self.subTest(output=output):
                self.fake(f"printf '{output}'; exit 0", self.ok_cat_file())
                self.assertEqual(self.run_stdin()[0], "STOP CONFIG")
        self.fake(f"printf '{self.BASE}\\n'; exit 0", self.ok_cat_file())  # the same form, with the literal
        self.assertEqual(self.run_stdin()[0], result("PASS", "opus", 3, "high"))

    def test_git_missing(self):
        self.assertEqual(self.run_stdin()[0], "STOP CONFIG")  # no git in PATH

    def test_timeout_kills_the_process_group(self):
        pidfile = os.path.join(self.tmp, "pid")
        self.fake(f'{shutil.which("sleep")} 30 & echo $! > "{pidfile}"; wait', self.ok_cat_file())
        line, elapsed = self.run_stdin(timeout=1)
        self.assertEqual(line, "STOP CONFIG")
        self.assertLess(elapsed, 10)
        with open(pidfile) as fh:
            pid = int(fh.read())
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                break
            time.sleep(0.05)
        else:
            self.fail("the child of the fake git still runs")

    def test_the_time_budget_is_shared_by_both_calls(self):
        self.fake(f'{shutil.which("sleep")} 0.6; ' + self.ok_rev_parse(), f'{shutil.which("sleep")} 0.6; '
                  + self.ok_cat_file())
        self.assertEqual(self.run_stdin(timeout=1)[0], "STOP CONFIG")
        self.assertEqual(self.run_stdin(timeout=5)[0], result("PASS", "opus", 3, "high"))

    def test_overflow_kills_the_call(self):
        self.fake(self.ok_rev_parse(), f'exec {shutil.which("yes")}')
        line, elapsed = self.run_stdin()
        self.assertEqual(line, "STOP CONFIG")
        self.assertLess(elapsed, 10)
        big = self.candidate(b" " * MOD.MAX_CONFIG_BYTES + SHIPPED_BYTES, "big.json")
        self.fake(self.ok_rev_parse(), f'{shutil.which("cat")} "{big}"; exit 0')
        self.assertEqual(self.run_stdin()[0], "STOP CONFIG")

    def test_an_exception_is_config(self):
        self.fake(self.ok_rev_parse(), self.ok_cat_file())
        with mock.patch.object(MOD.select, "select", side_effect=OSError(errno.EINTR, "x")):
            self.assertEqual(self.run_stdin()[0], "STOP CONFIG")
        with mock.patch.object(MOD.subprocess, "Popen", side_effect=ValueError("x")):
            self.assertEqual(self.run_stdin()[0], "STOP CONFIG")

    def test_from_stdin_needs_config_base(self):
        self.fake(self.ok_rev_parse(), self.ok_cat_file())
        self.assertEqual(self.run_stdin(self.args())[0], "STOP BAD_ARGS")
        self.assertFalse(os.path.exists(self.log))  # no git call

    def test_from_stdin_needs_floor(self):  # Issue #96 PR-2: the call form without --floor fails closed
        self.fake(self.ok_rev_parse(), self.ok_cat_file())
        self.assertEqual(self.run_stdin(self.args(base=self.BASE, floor=None))[0], "STOP BAD_ARGS")
        self.assertEqual(self.run_stdin(self.args(base=self.BASE, floor="review"))[0], "STOP BAD_ARGS")
        self.assertFalse(os.path.exists(self.log))  # no git call


@unittest.skipIf(GIT is None, "git is not installed")
class ConfigBase(Base):
    """The stdin form against real Git repositories (Issue #96, rev7 section 6, rev8 section 4.1)."""

    def setUp(self):
        super().setUp()
        self.write([self.rec()])
        self.home = os.path.join(self.tmp, "home")
        os.mkdir(self.home)
        self.env = {"PATH": os.path.dirname(GIT)}

    def git(self, repo, *args, data=None):
        command = [GIT, "-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false",
                   "-c", "tag.gpgsign=false", "-c", "init.defaultBranch=main", *args]
        p = subprocess.run(command, cwd=repo, input=data, capture_output=True, timeout=60,
                           env={"PATH": os.path.dirname(GIT), "HOME": self.home, "GIT_CONFIG_NOSYSTEM": "1"})
        self.assertEqual(p.returncode, 0, p.stderr)
        return p.stdout.decode("ascii").strip()

    def repo(self, config=SHIPPED_BYTES, object_format=None):
        """A repository with one commit that holds `config` at skills/dev-core/model-config.json; its commit ID."""
        repo = tempfile.mkdtemp(prefix="repo-", dir=self.tmp)
        self.git(repo, "init", "-q", *(["--object-format=" + object_format] if object_format else []))
        os.makedirs(os.path.join(repo, "skills", "dev-core"))
        with open(os.path.join(repo, CONFIG_IN_REPO), "wb") as fh:
            fh.write(config)
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", "x")
        return repo, self.git(repo, "rev-parse", "HEAD")

    def stdin(self, repo, base, argv=None):
        argv = self.args(base=base) if argv is None else argv
        return self.run_script(argv, hidden=(base,) if base else (), cwd=repo, env=self.env, stdin=True)

    def test_the_literal_commit_passes(self):
        repo, base = self.repo()
        self.assertEqual(self.stdin(repo, base), result("PASS", "opus", 3, "high"))
        with open(os.path.join(repo, CONFIG_IN_REPO), "wb") as fh:
            fh.write(b"{}")  # the work tree does not count; the commit does
        self.assertEqual(self.stdin(repo, base), result("PASS", "opus", 3, "high"))

    def test_other_objects_and_missing_commits(self):
        repo, base = self.repo()
        tree = self.git(repo, "rev-parse", "HEAD^{tree}")
        blob = self.git(repo, "rev-parse", "HEAD:" + CONFIG_IN_REPO)
        self.git(repo, "tag", "-a", "v1", "-m", "v1")
        tag = self.git(repo, "rev-parse", "v1")
        self.assertNotEqual(tag, base)
        missing = secrets.token_hex(20)
        for name, literal in (("tree", tree), ("blob", blob), ("annotated tag", tag), ("missing commit", missing)):
            with self.subTest(name):
                self.assertEqual(self.stdin(repo, literal), "STOP CONFIG")

    def test_literals_out_of_format(self):
        repo, base = self.repo()
        for literal in (base[:7], base[:39], base + "0", base + "-x", base.upper(), "HEAD", "main", "v1",
                        base + "^{commit}", base[:20] + " " + base[21:], "", "-" + base[1:]):
            with self.subTest(literal=literal):
                self.assertEqual(self.stdin(repo, base, self.args(base=literal)), "STOP BAD_ARGS")

    def test_sha256_repository(self):
        try:
            repo, base = self.repo(object_format="sha256")
        except AssertionError:
            self.skipTest("git cannot make a SHA-256 repository")
        self.assertEqual(len(base), 64)
        self.assertEqual(self.stdin(repo, base), result("PASS", "opus", 3, "high"))
        self.assertEqual(self.stdin(repo, base[:40]), "STOP CONFIG")  # an abbreviation in the 40-digit format

    def test_commit_without_or_with_a_bad_file(self):
        repo, base = self.repo()
        os.remove(os.path.join(repo, CONFIG_IN_REPO))
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-q", "-m", "removed")
        self.assertEqual(self.stdin(repo, self.git(repo, "rev-parse", "HEAD")), "STOP CONFIG")
        for config in (b"{}", config_bytes(lambda c: c.update(schema=2)), b" " * MOD.MAX_CONFIG_BYTES + SHIPPED_BYTES):
            with self.subTest(size=len(config)):
                bad_repo, bad = self.repo(config)
                self.assertEqual(self.stdin(bad_repo, bad), "STOP CONFIG")

    def test_replace_objects_are_not_used(self):
        repo, base = self.repo()
        blob = self.git(repo, "rev-parse", "HEAD:" + CONFIG_IN_REPO)
        other = self.git(repo, "hash-object", "-w", "--stdin", data=b"{}")
        self.git(repo, "replace", blob, other)
        self.assertEqual(self.git(repo, "cat-file", "blob", "HEAD:" + CONFIG_IN_REPO), "{}")
        self.assertEqual(self.stdin(repo, base), result("PASS", "opus", 3, "high"))

    def test_not_a_repository_or_no_git(self):
        repo, base = self.repo()
        outside = tempfile.mkdtemp(prefix="plain-", dir=self.tmp)
        self.assertEqual(self.run_script(self.args(base=base), hidden=(base,), cwd=outside, env=self.env, stdin=True),
                         "STOP CONFIG")
        no_git = tempfile.mkdtemp(prefix="bin-", dir=self.tmp)  # without PATH, the default search path finds git
        self.assertEqual(self.run_script(self.args(base=base), hidden=(base,), cwd=repo, env={"PATH": no_git},
                                         stdin=True), "STOP CONFIG")

    def test_from_stdin_without_config_base(self):
        repo, _ = self.repo()
        self.assertEqual(self.stdin(repo, "", self.args()), "STOP BAD_ARGS")

    def test_check_mode_refuses_config_base(self):
        repo, base = self.repo()
        self.assertEqual(self.stdin(repo, base, self.check_args(self.candidate()) + ["--config-base", base]),
                         "STOP BAD_ARGS")

    def test_floor_in_the_stdin_form(self):  # Issue #96 PR-2: the call form of the rules, with --floor
        repo, base = self.repo()
        for expect, floor, want in (
                (("opus", "high"), "work", result("PASS", "opus", 3, "high", ("opus", "high"), "work")),
                (("opus", "high"), "review-scan", result("BELOW", "opus", 3, "high", ("opus", "high"), "review-scan")),
                (("sonnet", "medium"), "review-light",
                 result("PASS", "opus", 3, "high", ("sonnet", "medium"), "review-light"))):
            with self.subTest(floor=floor):
                self.assertEqual(self.stdin(repo, base, self.args(expect, base=base, floor=floor)), want)
        self.assertEqual(self.stdin(repo, base, self.args(base=base, floor=None)), "STOP BAD_ARGS")


def lies_in_no_repository(folder):
    """Whether no folder from `folder` up to / has an entry named `.git` (os.lstat, as the script)."""
    level = os.path.realpath(folder)
    while True:
        if os.path.lexists(os.path.join(level, ".git")):
            return False
        if os.path.dirname(level) == level:
            return True
        level = os.path.dirname(level)


class CopyOutsideTheRepository(unittest.TestCase):
    """Issue #96 PR-3: the copy that the path form and the in-process cases run is the file of the repository."""

    def test_the_copy_equals_the_repository_file(self):
        with open(COPY, "rb") as fh:
            self.assertEqual(fh.read(), SOURCE)
        with open(os.path.join(COPY_ROOT, "model-config.json"), "rb") as fh:
            self.assertEqual(fh.read(), SHIPPED_BYTES)
        self.assertEqual(MOD.__file__, COPY)

    def test_precondition_the_temporary_folders_lie_in_no_repository(self):  # design d5 section 3
        self.assertTrue(lies_in_no_repository(COPY_ROOT), "the temporary folder lies in a Git repository")
        self.assertTrue(lies_in_no_repository(tempfile.gettempdir()))


@unittest.skipIf(GIT is None, "git is not installed")
class RepoCheck(Base):
    """The repository check of a run by its path (Issue #96 PR-3; design d1 section 4, d3 section 3, d4 section 2,
    d5 section 3) against real Git repositories and worktrees in a temporary folder. The script folder and the working
    directory lie at different depths. git runs with HOME set to a temporary folder and without the system Git
    configuration (git 2.54.0 on macOS when the tests were written)."""

    PASS = result("PASS", "opus", 3, "high")
    STOPS = ("STOP IN_REPO", "STOP REPO_CHECK")

    def setUp(self):
        super().setUp()
        self.write([self.rec()])
        self.root = os.path.realpath(self.tmp)
        self.assertTrue(lies_in_no_repository(self.root))
        self.home = os.path.join(self.root, "home")
        os.mkdir(self.home)
        self.env = {"PATH": os.path.dirname(GIT), "HOME": self.home, "GIT_CONFIG_NOSYSTEM": "1"}

    def git(self, cwd, *args, env=None):
        command = [GIT, "-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false",
                   "-c", "init.defaultBranch=main", *args]
        return subprocess.run(command, cwd=cwd, capture_output=True, timeout=60, env=env or self.env)

    def ok(self, cwd, *args):
        p = self.git(cwd, *args)
        self.assertEqual(p.returncode, 0, p.stderr)

    def repo(self, name="repo"):
        """A repository with one commit at <root>/<name>-*."""
        repo = tempfile.mkdtemp(prefix=name + "-", dir=self.root)
        self.ok(repo, "init", "-q")
        with open(os.path.join(repo, "file"), "w") as fh:
            fh.write("x")
        self.ok(repo, "add", "file")
        self.ok(repo, "commit", "-q", "-m", "x")
        return repo

    def linked(self, repo):
        """A linked worktree of `repo` at <root>/linked-*."""
        path = os.path.join(self.root, "linked-" + secrets.token_hex(4))
        self.ok(repo, "worktree", "add", "-q", path)
        return path

    def folder(self, *parts):
        path = os.path.join(*parts)
        os.makedirs(path, exist_ok=True)
        return path

    def pack_in(self, folder, config=True, name="model_effort_readback.py"):
        """A copy of the script at <folder>/skills/dev-core/scripts/<name>, with the configuration file next to its
        scripts folder unless config is False."""
        scripts = self.folder(folder, "skills", "dev-core", "scripts")
        shutil.copyfile(SCRIPT, os.path.join(scripts, name))
        if config:
            shutil.copyfile(CONFIG, os.path.join(os.path.dirname(scripts), "model-config.json"))
        return os.path.join(scripts, name)

    def outcome(self, script, cwd, argv=None, **variables):
        return self.run_script(self.args() if argv is None else argv, script=script, cwd=cwd,
                               env=dict(self.env, **variables))

    def test_the_same_worktree(self):
        repo = self.repo()
        script = self.pack_in(repo)
        self.assertEqual(self.outcome(script, repo), "STOP IN_REPO")
        self.assertEqual(self.outcome(script, self.folder(repo, "c")), "STOP IN_REPO")
        self.assertEqual(self.outcome(script, os.path.dirname(script)), "STOP IN_REPO")

    def test_main_and_linked_worktrees(self):
        repo = self.repo()
        first, second = self.linked(repo), self.linked(repo)
        self.assertEqual(self.outcome(self.pack_in(repo), first), "STOP IN_REPO")
        self.assertEqual(self.outcome(self.pack_in(first), self.folder(repo, "c")), "STOP IN_REPO")
        self.assertEqual(self.outcome(self.pack_in(second), first), "STOP IN_REPO")

    def test_two_repositories(self):
        script = self.pack_in(self.repo("one"))
        self.assertEqual(self.outcome(script, self.repo("two")), self.PASS)
        self.assertEqual(self.outcome(script, self.folder(self.repo("three"), "c")), self.PASS)

    def test_one_side_or_no_side_in_a_repository(self):  # card I96-P3-C1 (b)
        repo, plain = self.repo(), self.folder(self.root, "plain")
        self.assertEqual(self.outcome(self.pack_in(self.folder(self.root, "outside")), repo), self.PASS)
        self.assertEqual(self.outcome(self.pack_in(repo), plain), "STOP REPO_CHECK")
        self.assertEqual(self.outcome(COPY, plain), self.PASS)

    def test_git_dir_or_common_dir_of_the_working_directory(self):  # design d3 section 3, two repositories
        script, other = self.pack_in(self.repo("one")), self.repo("two")
        for name in ("GIT_DIR", "GIT_COMMON_DIR"):
            with self.subTest(name=name):
                self.assertIn(self.outcome(script, other, **{name: os.path.join(other, ".git")}), self.STOPS)

    def test_relative_or_empty_variables_do_not_pass(self):  # design d4 section 2
        repo = self.repo()
        script = self.pack_in(repo)
        setups = ((script, repo), (script, self.linked(repo)), (self.pack_in(self.repo("one")), self.repo("two")))
        for name, value in (("GIT_DIR", ".git"), ("GIT_COMMON_DIR", ".git"), ("GIT_DIR", ""),
                            ("GIT_WORK_TREE", "")):
            for script, cwd in setups:
                with self.subTest(name=name, value=value, cwd=os.path.basename(cwd)):
                    self.assertIn(self.outcome(script, cwd, **{name: value}), self.STOPS)

    def test_ceiling_directories_stop_either_side(self):
        repo = self.repo()
        linked = self.linked(repo)
        script = self.pack_in(repo)
        self.assertEqual(self.outcome(script, linked, GIT_CEILING_DIRECTORIES=repo), "STOP REPO_CHECK")
        self.assertEqual(self.outcome(script, self.folder(linked, "c", "d"), GIT_CEILING_DIRECTORIES=linked),
                         "STOP REPO_CHECK")

    def test_work_tree_and_discovery_variables_keep_the_same_repository_stopped(self):
        repo, other = self.repo(), self.repo("other")
        linked = self.linked(repo)
        script = self.pack_in(repo)
        for name, value in (("GIT_WORK_TREE", other), ("GIT_WORK_TREE", self.root),
                            ("GIT_DISCOVERY_ACROSS_FILESYSTEM", "1"), ("GIT_DISCOVERY_ACROSS_FILESYSTEM", "0")):
            with self.subTest(name=name, value=os.path.basename(value)):
                self.assertIn(self.outcome(script, linked, **{name: value}), self.STOPS)

    def test_residual_risk_23_a_worktree_without_a_git_entry_passes(self):
        """A limit, not a protection (residual risk 23, card I96-P3-C2 (a)): GIT_DIR and GIT_WORK_TREE point to a
        worktree that has no `.git` entry, the copy lies in it, and the check does not see it."""
        repo = self.repo()
        gitdir = os.path.join(self.root, "gitdir")
        os.rename(os.path.join(repo, ".git"), gitdir)
        self.assertTrue(lies_in_no_repository(repo))
        self.assertEqual(self.outcome(self.pack_in(repo), repo, GIT_DIR=gitdir, GIT_WORK_TREE=repo), self.PASS)

    def test_relative_git_common_dir_is_the_exception_of_card_c2(self):
        """The exception to the reasoning of card I96-P3-C2 (a) (card I96-P3-R2-C2 (a), residual risk 23): a relative
        GIT_COMMON_DIR that is valid in the script folder. git joins it wrongly there, ends with exit code 0 and
        prints a path that does not exist; the expected STOP comes from the os.stat of step 7. The argv is that of
        design d4 and d5 (no --path-format)."""
        repo = self.repo()
        linked = self.linked(repo)
        script = self.pack_in(repo)
        here = os.path.dirname(script)
        relative = os.path.relpath(os.path.join(repo, ".git"), here)
        p = self.git(here, "--no-replace-objects", "rev-parse", "--git-common-dir",
                     env=dict(self.env, GIT_COMMON_DIR=relative))
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertFalse(os.path.exists(os.path.join(here, p.stdout.decode().rstrip("\n"))))
        self.assertEqual(self.outcome(script, linked, GIT_COMMON_DIR=relative), "STOP REPO_CHECK")

    def test_a_git_file_that_is_not_valid(self):
        broken = self.folder(self.root, "broken")
        with open(os.path.join(broken, ".git"), "w") as fh:
            fh.write("not a gitdir line\n")
        self.assertEqual(self.outcome(self.pack_in(broken), self.repo()), "STOP REPO_CHECK")

    def test_a_dangling_git_symlink(self):  # found by os.lstat; os.stat would not see it and give PASS
        dangling = self.folder(self.root, "dangling")
        os.symlink(os.path.join(self.root, "missing-" + secrets.token_hex(4)), os.path.join(dangling, ".git"))
        self.assertEqual(self.outcome(self.pack_in(dangling), self.repo()), "STOP REPO_CHECK")

    def test_a_skill_folder_that_is_a_symlink_into_the_repository(self):
        repo = self.repo()
        linked = self.linked(repo)
        real = os.path.dirname(os.path.dirname(self.pack_in(repo)))  # <repo>/skills/dev-core
        shown = self.folder(self.root, "shown", "skills")
        os.symlink(real, os.path.join(shown, "dev-core"))
        self.assertTrue(lies_in_no_repository(shown))
        self.assertEqual(self.outcome(os.path.join(shown, "dev-core", "scripts", "model_effort_readback.py"), linked),
                         "STOP IN_REPO")

    @unittest.skipUnless(sys.platform == "darwin" and CASE_INSENSITIVE, "needs a file system that ignores case")
    def test_a_script_path_in_another_letter_case(self):  # design d5 section 2: the inode comparison is needed
        repo = self.repo()
        linked = self.linked(repo)
        script = self.pack_in(repo)
        shown = os.path.join(os.path.dirname(repo), os.path.basename(repo).upper()) + script[len(repo):]
        self.assertNotEqual(os.path.realpath(shown), script)  # the strings differ, the files are the same
        self.assertTrue(os.path.samefile(shown, script))
        self.assertEqual(self.outcome(shown, linked), "STOP IN_REPO")

    def test_the_order_of_the_checks(self):  # design d5 section 2: after BAD_ARGS, before the configuration file
        repo, plain = self.repo(), self.folder(self.root, "plain")
        script = self.pack_in(repo)
        self.assertEqual(self.outcome(script, plain, self.args(base="a" * 40)), "STOP BAD_ARGS")
        self.assertEqual(self.outcome(self.pack_in(self.folder(repo, "x"), name="readback.py"), plain),
                         "STOP BAD_ARGS")
        no_config = self.pack_in(self.folder(repo, "y"), config=False)
        self.assertEqual(self.outcome(no_config, plain), "STOP REPO_CHECK")
        self.assertEqual(self.outcome(no_config, repo), "STOP IN_REPO")
        self.assertEqual(self.outcome(self.pack_in(self.folder(self.root, "z"), config=False), repo), "STOP CONFIG")

    def test_check_mode_does_not_run_it(self):
        script = self.pack_in(self.repo())
        self.assertEqual(self.outcome(script, self.folder(self.root, "plain"), self.check_args(self.candidate())),
                         "CHECK model=opus match=listed tier=3 effort=high records=1")


class RepoCheckInProcess(Base):
    """The repository check with a fake git and patched os functions in this process (Issue #96 PR-3; design d4
    section 2, d5 section 3). Both folders have a `.git` directory; the fake git prints by its working directory."""

    PASS = result("PASS", "opus", 3, "high")

    def setUp(self):
        super().setUp()
        self.write([self.rec()])
        root = os.path.realpath(self.tmp)
        self.folder_s = os.path.join(root, "s")  # the script copy at s/x/skills/dev-core/scripts
        os.makedirs(os.path.join(self.folder_s, ".git"))
        scripts = os.path.join(self.folder_s, "x", "skills", "dev-core", "scripts")
        os.makedirs(scripts)
        shutil.copyfile(CONFIG, os.path.join(os.path.dirname(scripts), "model-config.json"))
        self.script, self.here = os.path.join(scripts, "model_effort_readback.py"), scripts
        os.makedirs(os.path.join(root, "c", ".git"))
        self.cwd = os.path.join(root, "c", "z")  # the working directory at c/z
        os.mkdir(self.cwd)
        self.common, self.other = os.path.join(root, "common"), os.path.join(root, "other")
        os.mkdir(self.common)
        os.mkdir(self.other)
        self.bin = os.path.join(root, "bin")
        os.mkdir(self.bin)
        self.log = os.path.join(root, "argv.log")

    def fake(self, here, cwd):
        """A fake git that logs its folder and arguments, then runs `here` in the script folder, else `cwd`."""
        path = os.path.join(self.bin, "git")
        with open(path, "w") as fh:
            fh.write(f'#!/bin/sh\nprintf "%s %s\\n" "$(pwd -P)" "$*" >> "{self.log}"\n'
                     f'case "$(pwd -P)" in\n  "{self.here}") {here} ;;\n  *) {cwd} ;;\nesac\n')
        os.chmod(path, 0o755)

    def prints(self, path):
        return f'printf "%s\\n" "{path}"; exit 0'

    def patches(self, timeout=None):
        stack = contextlib.ExitStack()
        stack.enter_context(mock.patch.dict(os.environ, {"PATH": self.bin}))
        stack.enter_context(mock.patch.object(MOD, "__file__", self.script))
        stack.enter_context(mock.patch.object(MOD.os, "getcwd", return_value=self.cwd))
        if timeout is not None:
            stack.enter_context(mock.patch.object(MOD, "GIT_TIMEOUT", timeout))
        return stack

    def outcome(self, timeout=None):
        with self.patches(timeout):
            return self.run_inproc(self.args())

    def test_two_calls_in_the_two_folders(self):
        self.fake(self.prints(self.common), self.prints(self.other))
        self.assertEqual(self.outcome(), self.PASS)
        with open(self.log) as fh:
            self.assertEqual(fh.read().splitlines(), [
                self.here + " --no-replace-objects rev-parse --git-common-dir",
                self.cwd + " --no-replace-objects rev-parse --git-common-dir"])

    def test_the_same_directory(self):
        relative = os.path.relpath(self.common, self.here)
        for here, cwd in ((self.common, self.common), (relative, self.common), (self.common + "/.", self.common),
                          (os.path.join(self.other, "..", "common"), self.common)):
            with self.subTest(here=here):
                self.fake(self.prints(here), self.prints(cwd))
                self.assertEqual(self.outcome(), "STOP IN_REPO")

    def test_output_rules(self):
        ok = self.prints(self.common)
        two = os.path.join(self.common, "two\nlines")  # a folder whose name holds a newline: two lines that exist
        os.mkdir(two)
        inner = os.path.join(self.common, "inner\nnewline")  # one newline, not at the end: only endswith stops it
        os.mkdir(inner)
        for name, here in (("two lines", f'printf "%s\\n%s\\n" "{self.common}" "{self.common}"'),
                           ("two lines that name a folder", self.prints(two)),
                           ("an empty line", 'printf "\\n"'), ("no output", "exit 0"),
                           ("NUL", f'printf "{self.common}\\000\\n"'),
                           ("no final newline", f'printf "%s" "{self.common}"'),
                           ("one newline, not the final byte", f'printf "%s" "{inner}x"'),  # IR-P3-S-06
                           ("not UTF-8", f'printf "{self.common}\\377\\n"'),
                           ("a path that does not exist", self.prints(os.path.join(self.missing(), ".git"))),
                           ("a relative path that does not exist", self.prints("../missing/.git")),
                           ("exit code 1", f'printf "%s\\n" "{self.common}"; exit 1'),
                           ("exit code 128", "exit 128")):
            with self.subTest(name):
                self.fake(here, ok)
                self.assertEqual(self.outcome(), "STOP REPO_CHECK")
                self.fake(ok, here)  # the same output in the working directory
                self.assertEqual(self.outcome(), "STOP REPO_CHECK")

    def missing(self):
        return os.path.join(os.path.realpath(self.tmp), "missing-" + secrets.token_hex(4))

    def test_git_missing(self):
        self.assertEqual(self.outcome(), "STOP REPO_CHECK")  # no git in PATH

    def test_timeout(self):
        self.fake(f'{shutil.which("sleep")} 30', self.prints(self.common))
        start = time.monotonic()
        self.assertEqual(self.outcome(timeout=1), "STOP REPO_CHECK")
        self.assertLess(time.monotonic() - start, 10)

    def test_the_time_budget_is_shared_by_both_calls(self):
        sleep = f'{shutil.which("sleep")} 0.6; '
        self.fake(sleep + self.prints(self.common), sleep + self.prints(self.other))
        self.assertEqual(self.outcome(timeout=1), "STOP REPO_CHECK")
        self.assertEqual(self.outcome(timeout=5), self.PASS)

    def test_one_deadline_for_both_calls(self):  # a mocked time.monotonic: one GIT_TIMEOUT for the two calls
        calls = []

        def record(argv, deadline, *, cwd=None):
            calls.append((argv, deadline, cwd))
            return os.fsencode(self.common if cwd == self.here else self.other) + b"\n"

        with self.patches(), mock.patch.object(MOD, "run_git", side_effect=record), \
                mock.patch.object(MOD.time, "monotonic", return_value=1000.0):
            self.assertIsNone(MOD.repo_check())
        argv = ["git", "--no-replace-objects", "rev-parse", "--git-common-dir"]
        self.assertEqual(calls, [(argv, 1000.0 + MOD.GIT_TIMEOUT, self.here),
                                 (argv, 1000.0 + MOD.GIT_TIMEOUT, self.cwd)])

    def test_the_same_inode_with_other_strings(self):  # design d5 section 3: portable, with a mocked os.stat
        self.fake(self.prints(self.common), self.prints(self.other))
        real_stat = os.stat

        def same(path, *args, **kwargs):
            return real_stat(self.common) if path in (self.common, self.other) else real_stat(path, *args, **kwargs)

        with mock.patch.object(MOD.os, "stat", same):
            self.assertEqual(self.outcome(), "STOP IN_REPO")

    def test_stat_errors(self):
        self.fake(self.prints(self.common), self.prints(self.other))
        real_stat = os.stat
        for target in ("common", "other"):
            def failing(path, *args, _target=os.path.join(os.path.realpath(self.tmp), target), **kwargs):
                if path == _target:
                    raise PermissionError(errno.EACCES, "mocked")
                return real_stat(path, *args, **kwargs)

            with self.subTest(target=target), mock.patch.object(MOD.os, "stat", failing):
                self.assertEqual(self.outcome(), "STOP REPO_CHECK")

    def test_lookup_errors(self):
        self.fake(self.prints(self.common), self.prints(self.other))
        real_lstat = os.lstat
        for side in (self.folder_s, os.path.dirname(self.cwd)):
            for err in (errno.EACCES, errno.EPERM, errno.ENAMETOOLONG, errno.ELOOP, errno.EIO):
                def failing(path, *args, _path=os.path.join(side, ".git"), _err=err, **kwargs):
                    if path == _path:
                        raise OSError(_err, "mocked")
                    return real_lstat(path, *args, **kwargs)

                with self.subTest(side=os.path.basename(side), err=errno.errorcode[err]), \
                        mock.patch.object(MOD.os, "lstat", failing):
                    self.assertEqual(self.outcome(), "STOP REPO_CHECK")

    def test_enotdir_and_enoent_go_on_upwards(self):
        self.fake(self.prints(self.common), self.prints(self.common))
        real_lstat = os.lstat
        for err in (errno.ENOENT, errno.ENOTDIR):
            def absent(path, *args, _path=os.path.join(self.folder_s, ".git"), _err=err, **kwargs):
                if path == _path:
                    raise OSError(_err, "mocked")
                return real_lstat(path, *args, **kwargs)

            with self.subTest(err=errno.errorcode[err]), mock.patch.object(MOD.os, "lstat", absent):
                self.assertEqual(self.outcome(), self.PASS)  # the copy lies in no repository: no git call
        self.assertFalse(os.path.exists(self.log))

    def test_both_sides_are_looked_up_first(self):  # design d5 section 2, step 2: before the copy ends the check
        real_lstat = os.lstat

        def failing(path, *args, **kwargs):
            if path == os.path.join(self.folder_s, ".git"):
                raise OSError(errno.ENOENT, "mocked")  # the copy lies in no repository
            if path == os.path.join(os.path.dirname(self.cwd), ".git"):
                raise OSError(errno.EACCES, "mocked")
            return real_lstat(path, *args, **kwargs)

        with mock.patch.object(MOD.os, "lstat", failing):
            self.assertEqual(self.outcome(), "STOP REPO_CHECK")

    def test_the_working_directory_cannot_be_read(self):
        self.fake(self.prints(self.common), self.prints(self.common))
        for exc in (FileNotFoundError(errno.ENOENT, "x"), PermissionError(errno.EACCES, "x"), OSError(errno.EIO, "x")):
            with self.subTest(exc=type(exc).__name__), self.patches(), \
                    mock.patch.object(MOD.os, "getcwd", side_effect=exc):
                self.assertEqual(self.run_inproc(self.args()), "STOP REPO_CHECK")

    def test_check_mode_and_the_stdin_form_do_not_run_it(self):
        self.fake(self.prints(self.common), self.prints(self.common))
        with self.patches(), mock.patch.object(MOD, "repo_check", side_effect=AssertionError("repo_check")):
            self.assertEqual(self.run_inproc(self.check_args(self.candidate())),
                             "CHECK model=opus match=listed tier=3 effort=high records=1")
            with mock.patch.object(MOD, "from_stdin", return_value=True), \
                    mock.patch.object(MOD, "config_from_git", return_value=SHIPPED_BYTES):
                self.assertEqual(self.run_inproc(self.args(base="c" * 40), hidden=("c" * 40,)), self.PASS)
        self.assertFalse(os.path.exists(self.log))
        with self.patches():  # the same patches without the mock give the result of the check
            self.assertEqual(self.run_inproc(self.args()), "STOP IN_REPO")


class CheckMode(Base):
    """`check` (card I96-C5 (a), rev7 section 5.8, rev8 section 4.3): a CHECK line, exit code 5, never PASS, WARN or BELOW."""

    def outcome(self, models, config=SHIPPED_BYTES, efforts=None, stdin=False):
        self.write([self.rec(model=m, effort=e) for m, e in zip(models, efforts or ["high"] * len(models))])
        return self.run_script(self.check_args(self.candidate(config)), stdin=stdin)

    def test_both_forms(self):
        for stdin in (False, True):
            with self.subTest(stdin=stdin):
                self.assertEqual(self.outcome([OPUS], stdin=stdin),
                                 "CHECK model=opus match=listed tier=3 effort=high records=1")

    def test_classification(self):
        for models, config, want in (
                (["claude-opus-6-0"], SHIPPED_BYTES, "model=opus match=version tier=3"),
                (["claude-sonnet-5-5"], SHIPPED_BYTES, "model=sonnet match=version tier=2"),
                (["anthropic.claude-sonnet-5-5"], SHIPPED_BYTES, "model=sonnet match=name tier=2"),
                (["us.anthropic.claude-opus-5-5-v1:0"], SHIPPED_BYTES, "model=opus match=name tier=3"),
                (["unknown"], SHIPPED_BYTES, "model=unrecognized match=none tier=none"),
                ([OPUS, "claude-sonnet-5-5"], SHIPPED_BYTES, "model=sonnet match=version tier=2"),
                (["claude-opus-6-0", "claude-sonnet-5-5"], SHIPPED_BYTES, "model=sonnet match=version tier=2"),
                ([OPUS, "unknown"], SHIPPED_BYTES, "model=unrecognized match=none tier=none"),
                (["claude-sonnet-5-5"], config_bytes(retire_sonnet), "model=sonnet match=listed tier=null"),
                (["claude-sonnet-5-5"], config_bytes(lambda c: c["families"]["sonnet"].update(ids=["claude-sonnet-5-5"])),
                 "model=sonnet match=listed tier=2")):
            with self.subTest(models=models):
                self.assertEqual(self.outcome(models, config), f"CHECK {want} effort=high records={len(models)}")

    def test_never_a_gate_result(self):
        for models in ([OPUS], ["claude-sonnet-5-5"], ["claude-opus-6-0"], ["unknown"], [OPUS, "claude-haiku-5-5"]):
            for efforts in (["low"] * len(models), ["max"] * len(models)):
                with self.subTest(models=models, efforts=efforts):
                    line = self.outcome(models, efforts=efforts)
                    self.assertTrue(line.startswith("CHECK "), line)
                    self.assertNotRegex(line, "PASS|WARN|BELOW")

    def test_candidate_file(self):
        self.write([self.rec()])
        self.assertStop("CONFIG", self.check_args(self.candidate(b"{}")))
        self.assertStop("CONFIG", self.check_args(self.candidate(config_bytes(lambda c: c.update(schema=2)))))
        self.assertStop("CONFIG", self.check_args(os.path.join(self.tmp, "missing.json")))
        link = os.path.join(self.tmp, "link.json")
        os.symlink(self.candidate(), link)
        self.assertStop("CONFIG", self.check_args(link))
        hard = os.path.join(self.tmp, "hard.json")
        os.link(self.candidate(name="other.json"), hard)
        self.assertStop("CONFIG", self.check_args(hard))
        self.assertStop("CONFIG", self.check_args(self.candidate(SHIPPED_BYTES + b" " * MOD.MAX_CONFIG_BYTES)))

    def test_bad_arguments(self):
        self.write([self.rec()])
        candidate = self.candidate()
        base = self.check_args(candidate)
        for name, argv in (("--config-base", base + ["--config-base", "a" * 40]),
                           ("--floor none", base + ["--floor", "none"]), ("--floor work", base + ["--floor", "work"]),
                           ("--expect-model", base + ["--expect-model", "opus"]),
                           ("--expect-effort", base + ["--expect-effort", "high"]),
                           ("no candidate", base[:-2]), ("repeated candidate", base + ["--candidate-config", candidate]),
                           ("abbreviated --candidate", base[:-2] + ["--candidate", candidate])):
            with self.subTest(name):
                self.assertStop("BAD_ARGS", argv)

    def test_transcript_stops_still_apply(self):
        self.write([self.rec(effort="ultra", perTurnEffort=DROP)])
        self.assertStop("EFFORT_NOT_ALLOWED", self.check_args(self.candidate()))
        self.write(raw=b"")
        self.assertStop("NO_RECORD", self.check_args(self.candidate()))


class Internal(Base):
    def test_an_unexpected_exception_is_internal(self):
        self.write([self.rec()])
        with mock.patch.object(MOD, "read_back", side_effect=RuntimeError(self.marker)):
            self.assertStop("INTERNAL", inproc=True)

    def test_a_reason_outside_the_closed_set_is_internal(self):
        self.write([self.rec()])
        with mock.patch.object(MOD, "read_back", side_effect=MOD.Stop("NEW_" + self.marker)):
            self.assertStop("INTERNAL", inproc=True)

    def test_a_missing_open_flag_is_internal(self):
        self.write([self.rec()])
        for flag in ("O_NOFOLLOW", "O_DIRECTORY", "O_NONBLOCK", "O_NOCTTY"):
            with self.subTest(flag), mock.patch.dict(MOD.os.__dict__):
                del MOD.os.__dict__[flag]
                self.assertStop("INTERNAL", inproc=True)
        self.assertLine(result("PASS", "opus", 3, "high"), inproc=True)

    def test_a_closed_stdout_gives_no_traceback(self):
        self.write([self.rec()])
        closed, err = io.StringIO(), io.StringIO()
        closed.close()
        with contextlib.redirect_stdout(closed), contextlib.redirect_stderr(err):
            code = MOD.main(self.args())
        self.assertEqual((code, err.getvalue()), (2, ""))

    def test_a_broken_pipe_on_stdout_gives_an_empty_stderr(self):
        self.write([self.rec()])
        self.assertLine(result("PASS", "opus", 3, "high"))  # the same call reaches the output line (Issue #96 PR-3)
        read_end, write_end = os.pipe()
        os.close(read_end)
        try:
            p = subprocess.run([sys.executable, "-I", "-B", COPY, *self.args()], cwd=self.tmp, env={},
                               stdout=write_end, stderr=subprocess.PIPE, timeout=10)
        finally:
            os.close(write_end)
        self.assertEqual((p.returncode, p.stderr), (2, b""))


class TokenCoverage(Base):
    """Every token of the closed set is produced by at least one fixture, here in one place."""

    def test_every_token_is_produced(self):
        real_open = os.open

        def denied(name, flags, mode=0o777, *, dir_fd=None):
            if name == f"agent-{self.agent}.jsonl":
                raise PermissionError(errno.EACCES, "denied")
            return real_open(name, flags, mode, dir_fd=dir_fd)

        def fresh():
            shutil.rmtree(self.projects)
            os.mkdir(self.projects)

        def symlink():
            os.symlink(self.write([self.rec()], agent=self.other_agent()), self.target())

        def big():
            with open(self.write([self.rec()]), "r+b") as fh:
                fh.truncate(MOD.MAX_FILE_BYTES + 1)

        def hardlink():
            os.link(self.write([self.rec()]), os.path.join(self.tmp, "link-" + secrets.token_hex(4)))

        missing = os.path.join(self.tmp, "missing-" + secrets.token_hex(4) + ".json")
        producers = {  # token -> (fixture, argv or None, in process, patch)
            "BAD_ARGS": (lambda: None, ["subagent"], False, None),
            "CONFIG": (lambda: self.write([self.rec()]), None, True,
                       mock.patch.object(MOD, "own_config_path", return_value=missing)),
            "NOT_FOUND": (lambda: None, None, False, None),
            "AMBIGUOUS": (lambda: (self.write([self.rec()]), self.write([self.rec()], session=str(uuid.uuid4()))),
                          None, False, None),
            "SYMLINK": (symlink, None, False, None),
            "NOT_REGULAR": (lambda: os.mkfifo(self.target()), None, False, None),
            "OWNER": (lambda: self.write([self.rec()]), None, True, other_user()),
            "LINK_COUNT": (hardlink, None, False, None),
            "PERMISSION": (lambda: self.write([self.rec()]), None, True, mock.patch.object(MOD.os, "open", denied)),
            "TOO_LARGE": (big, None, False, None),
            "MALFORMED": (lambda: self.write(raw=b"{\n"), None, False, None),
            "BINDING_MISMATCH": (lambda: self.write([self.rec(isSidechain=False)]), None, False, None),
            "MISSING_FIELD": (lambda: self.write([self.rec(effort=DROP)]), None, False, None),
            "INCONSISTENT": (lambda: self.write([self.rec(perTurnEffort="low")]), None, False, None),
            "NO_RECORD": (lambda: self.write(raw=b""), None, False, None),
            "MODEL_NOT_RECOGNIZED": (lambda: self.write([self.rec(model="unknown")]), None, False, None),
            "EFFORT_NOT_ALLOWED": (lambda: self.write([self.rec(effort="High", perTurnEffort=DROP)]), None, False,
                                   None),
            "INTERNAL": (lambda: self.write([self.rec()]), None, True,
                         mock.patch.object(MOD, "read_back", side_effect=RuntimeError("x"))),
            "IN_REPO": (lambda: self.write([self.rec()]), None, True, same_repository(self.tmp)),
            "REPO_CHECK": (lambda: self.write([self.rec()]), None, True,
                           mock.patch.object(MOD.os, "getcwd", side_effect=FileNotFoundError(errno.ENOENT, "x"))),
        }
        self.assertEqual(set(producers), TOKENS)
        for token, (fixture, argv, inproc, patch) in producers.items():
            with self.subTest(token):
                fresh()
                fixture()
                with patch if patch is not None else contextlib.nullcontext():
                    self.assertStop(token, argv, inproc=inproc)


@contextlib.contextmanager
def same_repository(common):
    """Both folders of the repository check lie in a Git repository whose common Git directory is `common`."""
    with mock.patch.object(MOD, "has_git_entry", return_value=True), \
            mock.patch.object(MOD, "run_git", return_value=os.fsencode(common) + b"\n"):
        yield


@contextlib.contextmanager
def other_user():
    """Another user ID for the transcript check; the configuration file is given as read."""
    with mock.patch.object(MOD, "read_config_file", return_value=SHIPPED_BYTES), \
            mock.patch.object(MOD.os, "getuid", return_value=os.getuid() + 1):
        yield


def popen_problems(tree) -> list:
    """The subprocess.Popen Attribute nodes that are not the func of a call, and a count other than one (IR1-S-06)."""
    funcs = [node.func for node in ast.walk(tree) if isinstance(node, ast.Call)]
    attrs = [node for node in ast.walk(tree) if isinstance(node, ast.Attribute) and node.attr == "Popen"
             and isinstance(node.value, ast.Name) and node.value.id == "subprocess"]
    problems = [ast.unparse(node) for node in attrs if not any(node is func for func in funcs)]
    return problems + ([f"{len(attrs)} subprocess.Popen nodes"] if len(attrs) != 1 else [])


def underscore_attribute_problems(tree) -> list:
    """The attributes that start with `_`, except __init__ (IR1-S-06)."""
    return sorted({node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
                   and node.attr.startswith("_") and node.attr != "__init__"})


def underscore_name_problems(tree) -> list:
    """The names that start with `_`, except _, __file__ and __name__ (IR1-S-06)."""
    return sorted({node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
                   and node.id.startswith("_") and node.id not in ("_", "__file__", "__name__")})


def bare_module_problems(tree) -> list:
    """The os and sys names that are not the value of an Attribute (IR1-S-06)."""
    values = [node.value for node in ast.walk(tree) if isinstance(node, ast.Attribute)]
    return [f"{node.id} at line {node.lineno}" for node in ast.walk(tree) if isinstance(node, ast.Name)
            and node.id in ("os", "sys") and not any(node is value for value in values)]


OS_PATH_ATTRS = {"abspath", "basename", "dirname", "isabs", "join", "normpath", "realpath"}


def os_path_problems(tree) -> list:
    """The os.path nodes that are not the value of an Attribute in OS_PATH_ATTRS (IR1-S-06)."""
    paths = [node for node in ast.walk(tree) if isinstance(node, ast.Attribute) and node.attr == "path"
             and isinstance(node.value, ast.Name) and node.value.id == "os"]
    outer = [node for node in ast.walk(tree) if isinstance(node, ast.Attribute)
             and any(node.value is path for path in paths)]
    unused = [f"os.path at line {path.lineno}" for path in paths if not any(o.value is path for o in outer)]
    return unused + sorted({"os.path." + o.attr for o in outer if o.attr not in OS_PATH_ATTRS})


class Static(unittest.TestCase):
    """Regression guards on the script text; the same PR can change the script and these tests."""

    IMPORTS = {"argparse", "errno", "json", "os", "re", "select", "signal", "stat", "subprocess", "sys", "time"}
    MODULE_ATTRS = {  # the only names that the script takes from these modules
        "os": {"open", "close", "read", "fstat", "stat", "lstat", "scandir", "getuid", "fspath", "path", "killpg",
               "getcwd"},  # getcwd: the repository check (Issue #96 PR-3)
        "subprocess": {"Popen", "DEVNULL", "PIPE"},
        "signal": {"SIGKILL"},
        "select": {"select"},
        "time": {"monotonic"},
    }
    FORBIDDEN = {"eval", "exec", "compile", "__import__", "getattr", "setattr", "globals", "vars", "importlib",
                 "open", "environ", "getenv", "expanduser", "socket", "system", "popen", "spawn", "fork"}
    FORBIDDEN_TEXT = ("environ", "getenv", "expanduser", "socket", "O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC",
                      "O_APPEND", "sys.modules", "shell=", "env=", "executable=", "preexec_fn=")
    POPEN_KEYWORDS = {"stdin": "subprocess.DEVNULL", "stdout": "subprocess.PIPE", "stderr": "subprocess.DEVNULL",
                      "start_new_session": "True", "cwd": "cwd"}  # cwd: the parameter of run_git (Issue #96 PR-3)
    GIT_CALLS = {(("git", "--no-replace-objects", "rev-parse", "--verify", "--quiet"), "^{commit}"),
                 (("git", "--no-replace-objects", "cat-file", "blob"), ":skills/dev-core/model-config.json")}
    REPO_GIT_CALL = ["git", "--no-replace-objects", "rev-parse", "--git-common-dir"]  # Issue #96 PR-3, design d4 1.1

    @classmethod
    def setUpClass(cls):
        with open(SCRIPT, encoding="utf-8") as fh:
            cls.source = fh.read()
        cls.tree = ast.parse(cls.source)

    def test_imports(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertIn(alias.name, self.IMPORTS)
                    self.assertIsNone(alias.asname)
            elif isinstance(node, ast.ImportFrom):
                self.assertEqual((node.module, node.level, [a.name for a in node.names]),
                                 ("__future__", 0, ["annotations"]))

    def test_module_attributes(self):
        for module, allowed in self.MODULE_ATTRS.items():
            with self.subTest(module=module):
                attrs = [node for node in ast.walk(self.tree) if isinstance(node, ast.Attribute)
                         and isinstance(node.value, ast.Name) and node.value.id == module]
                used = {node.attr for node in attrs}
                if module == "os":
                    self.assertEqual({a for a in used if a not in allowed and not a.startswith("O_")}, set())
                    self.assertEqual({a for a in used if a.startswith("O_")} - {
                        "O_RDONLY", "O_DIRECTORY", "O_NOFOLLOW", "O_NONBLOCK", "O_NOCTTY"}, set())
                else:
                    self.assertEqual(used - allowed, set())
                    bare = [node for node in ast.walk(self.tree) if isinstance(node, ast.Name) and node.id == module]
                    self.assertEqual(len(bare), len(attrs))  # the module name is used only to take an allowed name

    def test_forbidden_names(self):
        names = {node.id for node in ast.walk(self.tree) if isinstance(node, ast.Name)}
        names |= {node.attr for node in ast.walk(self.tree) if isinstance(node, ast.Attribute)}
        names |= {node.name for node in ast.walk(self.tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
        self.assertEqual(names & self.FORBIDDEN - {"open"}, set())
        builtin_open = [node for node in ast.walk(self.tree) if isinstance(node, ast.Name) and node.id == "open"]
        self.assertEqual(builtin_open, [])
        self.assertEqual([word for word in self.FORBIDDEN_TEXT if word in self.source], [])

    def test_one_subprocess_call_and_three_git_calls(self):
        calls = [node for node in ast.walk(self.tree) if isinstance(node, ast.Call)]
        popen = [c for c in calls if isinstance(c.func, ast.Attribute) and isinstance(c.func.value, ast.Name)
                 and c.func.value.id == "subprocess"]
        self.assertEqual(len(popen), 1)
        call = popen[0]
        self.assertEqual(call.func.attr, "Popen")
        self.assertEqual([(type(a), getattr(a, "id", None)) for a in call.args], [(ast.Name, "argv")])
        self.assertEqual({k.arg: ast.unparse(k.value) for k in call.keywords}, self.POPEN_KEYWORDS)
        owner = [f.name for f in ast.walk(self.tree) if isinstance(f, ast.FunctionDef) and call in ast.walk(f)]
        self.assertEqual(owner, ["run_git"])
        run_git = self.function("run_git")  # cwd is a keyword-only parameter with the default None
        self.assertEqual(([a.arg for a in run_git.args.args], [a.arg for a in run_git.args.kwonlyargs],
                          [ast.unparse(d) for d in run_git.args.kw_defaults]), (["argv", "deadline"], ["cwd"], ["None"]))
        git_calls = [c for c in calls if isinstance(c.func, ast.Name) and c.func.id == "run_git"]
        self.assertEqual(len(git_calls), 3)
        found, repo_calls = set(), []
        for c in git_calls:
            argv = c.args[0]
            self.assertIsInstance(argv, ast.List)
            if all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in argv.elts):
                repo_calls.append(c)  # the repository check: every element is a string constant
                continue
            *head, last = argv.elts
            self.assertTrue(all(isinstance(e, ast.Constant) and isinstance(e.value, str) for e in head))
            self.assertIsInstance(last, ast.BinOp)
            self.assertIsInstance(last.op, ast.Add)
            self.assertEqual((type(last.left), last.left.id), (ast.Name, "base"))
            self.assertIsInstance(last.right, ast.Constant)
            self.assertEqual(c.keywords, [])  # config_from_git passes no cwd
            found.add((tuple(e.value for e in head), last.right.value))
        self.assertEqual(found, self.GIT_CALLS)
        self.assertEqual(len(repo_calls), 1)
        self.assertEqual([e.value for e in repo_calls[0].args[0].elts], self.REPO_GIT_CALL)
        config_from_git = self.function("config_from_git")
        self.assertEqual(sorted(c.lineno for c in git_calls if c in ast.walk(config_from_git)),
                         sorted(c.lineno for c in git_calls if c is not repo_calls[0]))
        refs = [n for n in ast.walk(self.tree) if isinstance(n, ast.Name) and n.id == "run_git"]
        self.assertEqual(len(refs), 3)  # run_git is never passed on or renamed

    def function(self, name):
        found = [f for f in ast.walk(self.tree) if isinstance(f, ast.FunctionDef) and f.name == name]
        self.assertEqual(len(found), 1, name)
        return found[0]

    def test_the_repository_check_runs_git_in_the_folders_of_step_1(self):  # design d5 sections 2 and 3
        check = self.function("repo_check")
        calls = [c for c in ast.walk(check) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                 and c.func.id == "run_git"]
        self.assertEqual(len(calls), 1)
        self.assertEqual([(k.arg, ast.unparse(k.value)) for k in calls[0].keywords], [("cwd", "folder")])
        cwd_keywords = [c for c in ast.walk(self.tree) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                        and c.func.id == "run_git" and any(k.arg == "cwd" for k in c.keywords)]
        self.assertEqual(cwd_keywords, calls)  # cwd= only in the call of the repository check
        loops = [n for n in ast.walk(check) if isinstance(n, ast.For) and calls[0] in ast.walk(n)]
        self.assertEqual(len(loops), 1)  # folder takes the two variables of step 1, not the variable of the lookup
        self.assertEqual((ast.unparse(loops[0].target), ast.unparse(loops[0].iter)), ("folder", "(here, cwd)"))
        assigned = {ast.unparse(t): ast.unparse(n.value) for n in ast.walk(check) if isinstance(n, ast.Assign)
                    for t in n.targets}
        self.assertEqual((assigned["cwd"], assigned["here"]),
                         ("os.path.realpath(os.getcwd())", "os.path.dirname(os.path.realpath(__file__))"))
        stores = [n.id for n in ast.walk(check) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)]
        self.assertEqual((stores.count("cwd"), stores.count("here"), stores.count("folder")), (1, 1, 1))
        joins = [c for c in ast.walk(check) if isinstance(c, ast.Call) and ast.unparse(c.func) == "os.path.join"]
        self.assertEqual([ast.unparse(c.args[0]) for c in joins], ["folder"])  # a relative value joins to folder
        getcwd = [n for n in ast.walk(self.tree) if isinstance(n, ast.Attribute) and n.attr == "getcwd"]
        self.assertEqual(len(getcwd), 1)
        self.assertIn(getcwd[0], list(ast.walk(check)))
        lookup = self.function("has_git_entry")  # os.lstat, never os.stat: a dangling `.git` symlink counts
        self.assertEqual(sorted({ast.unparse(c.func) for c in ast.walk(lookup) if isinstance(c, ast.Call)
                                 and ast.unparse(c.func).startswith("os.")}),
                         ["os.lstat", "os.path.dirname", "os.path.join"])
        called = [c for c in ast.walk(self.tree) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                  and c.func.id == "repo_check"]
        self.assertEqual(len(called), 1)
        self.assertIn(called[0], list(ast.walk(self.function("run"))))

    def test_no_env_keyword(self):  # Issue #96 PR-3, card I96-P3-C2 (a): git gets the variables of the caller
        self.assertEqual([ast.unparse(c) for c in ast.walk(self.tree) if isinstance(c, ast.Call)
                          and any(k.arg == "env" for k in c.keywords)], [])

    def test_no_alias_of_popen_os_or_sys(self):  # IR1-S-06 (Issue #96 PR-2)
        for check in (popen_problems, underscore_attribute_problems, underscore_name_problems, bare_module_problems,
                      os_path_problems):
            with self.subTest(check=check.__name__):
                self.assertEqual(check(self.tree), [])

    def test_alias_mutations_fail(self):  # IR1-S-06: each mutation of the source in memory is found; no file
        cases = {
            popen_problems: ("P = subprocess.Popen", "run = [subprocess.Popen][0]", "def f(p=subprocess.Popen): pass",
                             "x = subprocess.Popen.__call__", "x = subprocess.Popen(argv)"),
            underscore_attribute_problems: ("x = os._exit", "x = sys._getframe", "x = ().__class__",
                                            "x = re.__dict__", "x = subprocess._args_from_interpreter_flags",
                                            "x = Stop.__subclasses__"),
            underscore_name_problems: ("x = __builtins__", "_x = 1", "x = __loader__", "x = __spec__",
                                       "__import__('os')", "x = __cached__"),
            bare_module_problems: ("m = os", "m = sys", "f(os)", "os = None", "x = [sys][0]", "x = {'m': os}"),
            os_path_problems: ("p = os.path", "f(os.path)", "x = os.path.exists('x')", "x = os.path.expanduser",
                               "x = os.path.islink", "x = [os.path][0].join"),
        }
        for check, mutations in cases.items():
            for mutation in mutations:
                with self.subTest(check=check.__name__, mutation=mutation):
                    self.assertNotEqual(check(ast.parse(self.source + "\n" + mutation + "\n")), [])

    def test_type_is_not_banned(self):  # IR1-S-06: the validator checks types with `type(x) is int`
        self.assertIn("type", {node.id for node in ast.walk(self.tree) if isinstance(node, ast.Name)})

    def test_validator_reads_nothing(self):
        func = [f for f in ast.walk(self.tree) if isinstance(f, ast.FunctionDef) and f.name == "validate_config"]
        self.assertEqual(len(func), 1)
        names = {n.id for n in ast.walk(func[0]) if isinstance(n, ast.Name)}
        self.assertEqual(names & {"os", "sys", "subprocess", "select", "signal", "time", "__file__", "from_stdin",
                                  "run_git", "config_from_git", "read_config_file", "own_config_path", "open_at"},
                         set())

    def test_python_39_grammar(self):
        ast.parse(self.source, feature_version=(3, 9))
        annotations = [node.returns for node in ast.walk(self.tree) if isinstance(node, ast.FunctionDef)]
        annotations += [node.annotation for node in ast.walk(self.tree) if isinstance(node, (ast.arg, ast.AnnAssign))]
        unions = [node for annotation in annotations if annotation is not None for node in ast.walk(annotation)
                  if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr)]
        self.assertEqual(unions, [])  # no PEP 604 union: Python 3.9 cannot evaluate one

    def test_pinned_constants(self):
        self.assertFalse(hasattr(MOD, "MODEL_ALLOWLIST"))  # replaced by the configuration file (Issue #96)
        self.assertFalse(hasattr(MOD, "MODEL_ORDER"))
        self.assertEqual(MOD.EFFORT_ORDER, ("low", "medium", "high", "xhigh", "max"))
        self.assertEqual(MOD.FLOORS, {"work": (3, "high"), "review-scan": (3, "xhigh"), "review-routine": (3, "high"),
                                      "review-light": (2, "medium"), "none": None})  # Issue #96 PR-2
        self.assertEqual(MOD.ROLE_NAMES, ("orchestration", "explore", "explore-synthesis", "implement",
                                          "implement-reduced", "review-routine", "review-routine-light",
                                          "review-deep", "review-security", "scan"))
        self.assertEqual(MOD.AGENT_NAMES, ("dev-explorer", "dev-implementer", "dev-reviewer",
                                           "dev-security-reviewer"))
        self.assertEqual(MOD.RESERVED_FAMILY_NAMES, {"unrecognized", "none", "null", "unknown", "inherit", "default",
                                                     "low", "medium", "high", "xhigh", "max"})
        self.assertEqual(MOD.REASONS, TOKENS)
        self.assertEqual((MOD.MAX_FILE_BYTES, MOD.MAX_LINE_BYTES, MOD.MAX_LINES, MOD.MAX_NUMBER_CHARS),
                         (64 * 1024 * 1024, 1024 * 1024, 200000, 100))
        self.assertEqual((MOD.MAX_CONFIG_BYTES, MOD.MAX_CONFIG_DEPTH, MOD.MAX_TIER, MOD.MAX_ID_CHARS,
                          MOD.MAX_SCAN_CHARS, MOD.GIT_TIMEOUT), (64 * 1024, 8, 99, 100, 200, 20))
        self.assertEqual((MOD.BASE_RE, MOD.FAMILY_RE, MOD.MODEL_ID_RE, MOD.VERSION_RE, MOD.WORD_SPLIT_RE),
                         (r"(?:[0-9a-f]{40}|[0-9a-f]{64})", r"[a-z]{1,20}", r"[a-z0-9.-]{1,100}",
                          r"claude-([a-z]+)-[0-9]+(?:-[0-9]+)*", r"[^a-z0-9]+"))
        for token in TOKENS:
            self.assertIn(token, MOD.__doc__)
        MOD.set_flags()
        self.assertEqual(MOD.DIR_FLAGS, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        self.assertEqual(MOD.FILE_FLAGS, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_NOCTTY)

    def test_every_open_at_call_passes_a_pinned_flag_name(self):
        calls = [node for node in ast.walk(self.tree) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Name) and node.func.id == "open_at"]
        self.assertGreater(len(calls), 0)
        for call in calls:
            flags = call.args[1:2] + [k.value for k in call.keywords if k.arg == "flags"]
            self.assertEqual(len(flags), 1, ast.dump(call))
            self.assertIsInstance(flags[0], ast.Name, ast.dump(call))
            self.assertIn(flags[0].id, {"DIR_FLAGS", "FILE_FLAGS"})


if __name__ == "__main__":
    unittest.main()
