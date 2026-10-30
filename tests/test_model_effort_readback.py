"""Tests for skills/dev-core/scripts/model_effort_readback.py (Issue #89, Issue #79 slice B; REQ-009).

Synthetic fixtures only: every tree, file and ID is made in a temporary directory at run time. No test reads a real
transcript or the home directory. Of the environment and process data, the tests read only the user ID and the
effective user ID (os.getuid, os.geteuid), the list of open file descriptors in /dev/fd, and the TMPDIR, TEMP or TMP
variable that tempfile reads to find the temporary directory. The script runs as `sys.executable -I -B` with a
timeout and an empty environment; the cases that a subprocess cannot make (an argument with NUL, a patched
allowlist, a patched os.getuid, os.read or os.open, a missing open flag, a closed stdout, an exception) call its
main() in this process. These fixtures prove only the outcomes that they list (R-VER-1).
"""

import ast
import contextlib
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
import unittest
import uuid
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "skills", "dev-core", "scripts", "model_effort_readback.py")
OPUS = "claude-opus-5-5"
TOKENS = {
    "BAD_ARGS", "NOT_FOUND", "AMBIGUOUS", "SYMLINK", "NOT_REGULAR", "OWNER", "LINK_COUNT", "PERMISSION", "TOO_LARGE",
    "MALFORMED", "BINDING_MISMATCH", "MISSING_FIELD", "INCONSISTENT", "NO_RECORD", "MODEL_NOT_ALLOWED",
    "EFFORT_NOT_ALLOWED", "INTERNAL"}
ALIAS = "(haiku|sonnet|opus)"
LEVEL = "(low|medium|high|xhigh|max)"
GRAMMAR = [  # (line pattern, exit code)
    (re.compile(f"OK model={ALIAS} effort={LEVEL} records=[1-9][0-9]*"), 0),
    (re.compile(f"PASS model={ALIAS} effort={LEVEL} expected={ALIAS}/{LEVEL}"), 0),
    (re.compile(f"BELOW model={ALIAS} effort={LEVEL} expected={ALIAS}/{LEVEL}"), 3),
    (re.compile("STOP (" + "|".join(sorted(TOKENS)) + ")"), 2),
]
DROP = object()  # a record field to leave out
IS_ROOT = hasattr(os, "geteuid") and os.geteuid() == 0


def load_script():
    """The script as a module, without writing bytecode next to it."""
    spec = importlib.util.spec_from_file_location("model_effort_readback", SCRIPT)
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

    def args(self, expect=None, projects=None, agent=None):
        argv = ["subagent", "--projects-dir", projects or self.projects, "--agent-id", agent or self.agent]
        if expect:
            argv += ["--expect-model", expect[0], "--expect-effort", expect[1]]
        return argv

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

    def run_script(self, argv, hidden=()):
        p = subprocess.run([sys.executable, "-I", "-B", SCRIPT, *argv], cwd=self.tmp, env={}, capture_output=True,
                           timeout=10)
        return self.check(p.returncode, p.stdout.decode("ascii"), p.stderr.decode("ascii"), hidden)

    def run_inproc(self, argv, hidden=()):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = MOD.main(argv)
        return self.check(code, out.getvalue(), err.getvalue(), hidden)

    def assertStop(self, token, argv=None, inproc=False, hidden=()):
        argv = self.args() if argv is None else argv
        line = (self.run_inproc if inproc else self.run_script)(argv, hidden)
        self.assertEqual(line, "STOP " + token)

    def assertLine(self, want, argv=None, inproc=False):
        argv = self.args() if argv is None else argv
        self.assertEqual((self.run_inproc if inproc else self.run_script)(argv), want)


class Normal(Base):
    def test_ok_takes_the_lowest_effort_over_all_records(self):
        self.write([self.rec(effort="xhigh"), self.rec(effort="high"), self.rec(effort="max")])
        self.assertLine("OK model=opus effort=high records=3")

    def test_synthetic_record_is_skipped_without_other_checks(self):
        synthetic = {"type": "assistant", "message": {"model": "<synthetic>"}, "agentId": "x", "effort": 1}
        self.write([self.rec(effort="xhigh"), synthetic])
        self.assertLine("OK model=opus effort=xhigh records=1")

    def test_pass_when_equal_or_above(self):
        self.write([self.rec(effort="xhigh")])
        self.assertLine("PASS model=opus effort=xhigh expected=opus/xhigh", self.args(("opus", "xhigh")))
        self.assertLine("PASS model=opus effort=xhigh expected=sonnet/medium", self.args(("sonnet", "medium")))

    def test_below_effort(self):
        self.write([self.rec(effort="xhigh"), self.rec(effort="medium")])
        self.assertLine("BELOW model=opus effort=medium expected=opus/high", self.args(("opus", "high")))

    def test_below_model_with_a_patched_allowlist(self):
        self.write([self.rec(model="test-model-sonnet", effort="max")])
        with mock.patch.dict(MOD.MODEL_ALLOWLIST, {"test-model-sonnet": "sonnet"}):
            self.assertLine("BELOW model=sonnet effort=max expected=opus/high", self.args(("opus", "high")),
                            inproc=True)

    def test_unrelated_symlinks_and_sessions_without_subagents_keep_ok(self):
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
        self.assertLine("OK model=opus effort=high records=1")

    def test_file_descriptors_are_closed(self):
        self.write([self.rec()])
        self.write([self.rec()], slug="second-slug")
        before = open_fds()
        self.run_inproc(self.args())  # AMBIGUOUS
        self.write([self.rec()], session=str(uuid.uuid4()), slug="third-slug", agent=self.other_agent())
        os.unlink(self.target(slug="second-slug"))
        self.run_inproc(self.args())  # OK
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
        self.assertLine("OK model=opus effort=low records=1")

    def test_requested_and_advisor_model_do_not_raise_the_model(self):
        record = self.rec(model="test-model-haiku", requestedModel=OPUS, advisorModel=OPUS)
        self.write([record])
        with mock.patch.dict(MOD.MODEL_ALLOWLIST, {"test-model-haiku": "haiku"}):
            self.assertLine("OK model=haiku effort=high records=1", inproc=True)

    def test_capitalized_or_non_string_type_is_not_an_assistant_record(self):
        self.write([self.rec(type="Assistant", effort="low", agentId="x"), self.rec(type=["assistant"], effort=5),
                    {"effort": "low"}, self.rec(effort="max")])
        self.assertLine("OK model=opus effort=max records=1")


class Appended(Base):
    def test_an_appended_higher_line_changes_nothing(self):
        path = self.write([self.rec(effort="medium")])
        with open(path, "ab") as fh:
            fh.write(json.dumps(self.rec(effort="max")).encode() + b"\n")
        self.assertLine("OK model=opus effort=medium records=2")

    def test_an_appended_lower_line_lowers_the_result(self):
        path = self.write([self.rec(effort="high")])
        with open(path, "ab") as fh:
            fh.write(json.dumps(self.rec(effort="low")).encode() + b"\n")
        self.assertLine("BELOW model=opus effort=low expected=opus/high", self.args(("opus", "high")))

    def test_a_rewritten_line_passes(self):
        """A limit, not a protection (R-VER-1): a low line rewritten to a high value gives PASS."""
        self.write([self.rec(effort="low")])
        self.write([self.rec(effort="high")])  # the same file, its low line rewritten
        self.assertLine("PASS model=opus effort=high expected=opus/high", self.args(("opus", "high")))


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
        self.assertLine("OK model=opus effort=high records=1")
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
        self.assertLine("OK model=opus effort=high records=1")

    def test_u2028_is_content_not_a_line_break(self):
        record = self.rec()
        record["message"]["content"][0]["text"] = "a\u2028b\u2029c\x85d"
        self.write(raw=json.dumps(record, ensure_ascii=False).encode("utf-8") + b"\n")
        self.assertLine("OK model=opus effort=high records=1")

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

        with mock.patch.object(MOD.os, "read", short_read):
            self.assertStop("MALFORMED", inproc=True)


class Arguments(Base):
    def test_bad_agent_ids(self):
        self.write([self.rec()])
        for agent in (self.agent[:16], self.agent + "0", self.agent.upper(), "../" + self.agent[3:],
                      "g" * 17, self.agent + "\n", "", "-" + self.agent[1:]):
            with self.subTest(agent=agent):
                self.assertStop("BAD_ARGS", ["subagent", "--projects-dir", self.projects, "--agent-id", agent])

    def test_nul_in_an_argument(self):
        self.write([self.rec()])
        self.assertStop("BAD_ARGS", ["subagent", "--projects-dir", self.projects + "\x00x", "--agent-id", self.agent],
                        inproc=True)
        self.assertStop("BAD_ARGS", ["subagent", "--projects-dir", self.projects, "--agent-id",
                                     self.agent[:16] + "\x00"], inproc=True)

    def test_bad_option_use(self):
        self.write([self.rec()])
        base = self.args()
        cases = {
            "repeated --agent-id": base + ["--agent-id", self.agent],
            "repeated --projects-dir": base + ["--projects-dir", self.projects],
            "repeated --expect-model": self.args(("opus", "high")) + ["--expect-model", "opus"],
            "abbreviated --agent": ["subagent", "--projects-dir", self.projects, "--agent", self.agent],
            "abbreviated --projects": ["subagent", "--projects", self.projects, "--agent-id", self.agent],
            "only --expect-model": base + ["--expect-model", "opus"],
            "only --expect-effort": base + ["--expect-effort", "high"],
            "missing --agent-id": ["subagent", "--projects-dir", self.projects],
            "missing --projects-dir": ["subagent", "--agent-id", self.agent],
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
        }
        for name, argv in cases.items():
            with self.subTest(name):
                self.assertStop("BAD_ARGS", argv)

    def test_bad_expected_values(self):
        self.write([self.rec()])
        for expect in (("fable", "high"), ("Opus", "high"), (OPUS, "high"), ("opus", "ultra"), ("opus", "High"),
                       ("opus", ""), ("inherit", "high")):
            with self.subTest(expect=expect):
                self.assertStop("BAD_ARGS", self.args(expect))

    def test_bad_projects_dir(self):
        self.write([self.rec()])
        rel = os.path.relpath(self.projects, self.tmp)
        for projects in (rel, self.projects + "/", "/", self.projects + "/.", self.projects + "/../projects",
                         self.projects.replace("/projects", "//projects"), ""):
            with self.subTest(projects=projects):
                self.assertStop("BAD_ARGS", ["subagent", "--projects-dir", projects, "--agent-id", self.agent])

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
        self.assertLine("OK model=opus effort=high records=1", self.args(projects=wild))

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
        path = self.write([self.rec()])
        other = os.stat(path).st_uid + 1
        with mock.patch.object(MOD.os, "getuid", return_value=other):
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
    def test_models_not_in_the_allowlist(self):
        for model in ("claude-opus-4-1", "claude-opus-5-5[1m]", "Claude-Opus-5-5", "opus", " claude-opus-5-5",
                      "arn:aws:bedrock:us-east-1:000000000000:inference-profile/us.anthropic.claude-opus-5-5-v1:0",
                      "claude-fable-5-1", "claude-sonnet-5-5", "claude-haiku-5-5", ""):
            with self.subTest(model=model):
                self.write([self.rec(), self.rec(model=model)])
                self.assertStop("MODEL_NOT_ALLOWED", hidden=(model,) if len(model) > 6 else ())


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
        self.assertLine("OK model=opus effort=high records=1", inproc=True)

    def test_a_closed_stdout_gives_no_traceback(self):
        self.write([self.rec()])
        closed, err = io.StringIO(), io.StringIO()
        closed.close()
        with contextlib.redirect_stdout(closed), contextlib.redirect_stderr(err):
            code = MOD.main(self.args())
        self.assertEqual((code, err.getvalue()), (2, ""))

    def test_a_broken_pipe_on_stdout_gives_an_empty_stderr(self):
        self.write([self.rec()])
        read_end, write_end = os.pipe()
        os.close(read_end)
        try:
            p = subprocess.run([sys.executable, "-I", "-B", SCRIPT, *self.args()], cwd=self.tmp, env={},
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

        producers = {  # token -> (fixture, argv or None, in process, patch)
            "BAD_ARGS": (lambda: None, ["subagent"], False, None),
            "NOT_FOUND": (lambda: None, None, False, None),
            "AMBIGUOUS": (lambda: (self.write([self.rec()]), self.write([self.rec()], session=str(uuid.uuid4()))),
                          None, False, None),
            "SYMLINK": (symlink, None, False, None),
            "NOT_REGULAR": (lambda: os.mkfifo(self.target()), None, False, None),
            "OWNER": (lambda: self.write([self.rec()]), None, True,
                      mock.patch.object(MOD.os, "getuid", return_value=os.getuid() + 1)),
            "LINK_COUNT": (hardlink, None, False, None),
            "PERMISSION": (lambda: self.write([self.rec()]), None, True, mock.patch.object(MOD.os, "open", denied)),
            "TOO_LARGE": (big, None, False, None),
            "MALFORMED": (lambda: self.write(raw=b"{\n"), None, False, None),
            "BINDING_MISMATCH": (lambda: self.write([self.rec(isSidechain=False)]), None, False, None),
            "MISSING_FIELD": (lambda: self.write([self.rec(effort=DROP)]), None, False, None),
            "INCONSISTENT": (lambda: self.write([self.rec(perTurnEffort="low")]), None, False, None),
            "NO_RECORD": (lambda: self.write(raw=b""), None, False, None),
            "MODEL_NOT_ALLOWED": (lambda: self.write([self.rec(model="claude-sonnet-5-5")]), None, False, None),
            "EFFORT_NOT_ALLOWED": (lambda: self.write([self.rec(effort="High", perTurnEffort=DROP)]), None, False,
                                   None),
            "INTERNAL": (lambda: self.write([self.rec()]), None, True,
                         mock.patch.object(MOD, "read_back", side_effect=RuntimeError("x"))),
        }
        self.assertEqual(set(producers), TOKENS)
        for token, (fixture, argv, inproc, patch) in producers.items():
            with self.subTest(token):
                fresh()
                fixture()
                with patch if patch is not None else contextlib.nullcontext():
                    self.assertStop(token, argv, inproc=inproc)


class Static(unittest.TestCase):
    """Regression guards on the script text; the same PR can change the script and these tests."""

    IMPORTS = {"argparse", "errno", "json", "os", "re", "stat", "sys"}
    OS_ATTRS = {"open", "close", "read", "fstat", "stat", "lstat", "scandir", "getuid", "fspath", "path"}
    FORBIDDEN = {"eval", "exec", "compile", "__import__", "getattr", "setattr", "globals", "vars", "importlib",
                 "open", "environ", "getenv", "expanduser", "subprocess", "socket"}
    FORBIDDEN_TEXT = ("environ", "getenv", "expanduser", "subprocess", "socket", "O_WRONLY", "O_RDWR", "O_CREAT",
                      "O_TRUNC", "O_APPEND", "sys.modules")

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

    def test_os_attributes(self):
        used = {node.attr for node in ast.walk(self.tree)
                if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "os"}
        self.assertEqual({a for a in used if a not in self.OS_ATTRS and not a.startswith("O_")}, set())
        self.assertEqual({a for a in used if a.startswith("O_")} - {"O_RDONLY", "O_DIRECTORY", "O_NOFOLLOW",
                                                                    "O_NONBLOCK", "O_NOCTTY"}, set())

    def test_forbidden_names(self):
        names = {node.id for node in ast.walk(self.tree) if isinstance(node, ast.Name)}
        names |= {node.attr for node in ast.walk(self.tree) if isinstance(node, ast.Attribute)}
        names |= {node.name for node in ast.walk(self.tree) if isinstance(node, (ast.FunctionDef, ast.ClassDef))}
        self.assertEqual(names & self.FORBIDDEN - {"open"}, set())
        builtin_open = [node for node in ast.walk(self.tree) if isinstance(node, ast.Name) and node.id == "open"]
        self.assertEqual(builtin_open, [])
        self.assertEqual([word for word in self.FORBIDDEN_TEXT if word in self.source], [])

    def test_python_39_grammar(self):
        ast.parse(self.source, feature_version=(3, 9))
        annotations = [node.returns for node in ast.walk(self.tree) if isinstance(node, ast.FunctionDef)]
        annotations += [node.annotation for node in ast.walk(self.tree) if isinstance(node, (ast.arg, ast.AnnAssign))]
        unions = [node for annotation in annotations if annotation is not None for node in ast.walk(annotation)
                  if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr)]
        self.assertEqual(unions, [])  # no PEP 604 union: Python 3.9 cannot evaluate one

    def test_pinned_constants(self):
        self.assertEqual(MOD.MODEL_ALLOWLIST, {"claude-opus-5-5": "opus"})
        self.assertEqual(MOD.MODEL_ORDER, ("haiku", "sonnet", "opus"))
        self.assertEqual(MOD.EFFORT_ORDER, ("low", "medium", "high", "xhigh", "max"))
        self.assertEqual(MOD.REASONS, TOKENS)
        self.assertEqual((MOD.MAX_FILE_BYTES, MOD.MAX_LINE_BYTES, MOD.MAX_LINES, MOD.MAX_NUMBER_CHARS),
                         (64 * 1024 * 1024, 1024 * 1024, 200000, 100))
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
