"""Issue #106 PR-1: the reviewer acceptance record, its check, and the version tie (R-REV-1, D-032, DL-004).

The tests prove the script outputs and the co-change tie only. They prove no runtime tool limit,
no new acceptance of a user, and nothing about a real user's record (they use a temporary home).
"""

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "skills", "dev-core", "scripts", "reviewer_acceptance.py")
REFERENCE = os.path.join(ROOT, "skills", "dev-core", "references", "reviewer-acceptance.md")
REVIEWERS = ("dev-reviewer", "dev-security-reviewer")

# SHA-256 of the pinned texts (see pinned_digest) for each ACCEPTANCE_VERSION. A change of a pinned
# text fails this test. Raise the version when the meaning or a tool line changes; update only the
# digest for a cite, a line number or a typo, with the reason in the version table of the reference.
# Both need a new decision of the user for that change (setup-change rule of the reference).
PINNED = {1: "b1e9b2973ccaf9f6706b5ee1ff182767b301f083d28b1db7702b838d51613499", 2: "b69a4a495498d5268dda4492d583c20f8ed9ee3942118265f2558115d5b1a7cf", 3: "b9e6b29eebb67fd3cc5e7130424e73a3c5971a8955e2651ec9b6d7fec61a0410"}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def lines_between(path, start_prefix, end_prefix):
    with open(path, "rb") as fh:
        lines = fh.read().split(b"\n")
    start = next(i for i, line in enumerate(lines) if line.startswith(start_prefix))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith(end_prefix))
    return b"\n".join(lines[start:end])


def pinned_digest():
    parts = []
    with open(REFERENCE, "rb") as fh:
        parts.append(fh.read())
    parts.append(lines_between(os.path.join(ROOT, "skills", "dev-core", "SKILL.md"), b"- **CB-4**", b"- **CB-6**"))
    parts.append(lines_between(os.path.join(ROOT, "skills", "dev-retro", "SKILL.md"), b"## Read-back", b"## capture"))
    for stem in REVIEWERS:
        with open(os.path.join(ROOT, "agents", stem + ".md"), "rb") as fh:
            parts.extend(line for line in fh.read().split(b"\n")
                         if line.startswith(b"tools:") or line.startswith(b"disallowedTools:"))
    digest = hashlib.sha256()
    for part in parts:
        digest.update(hashlib.sha256(part).digest())
    return digest.hexdigest()


def clean_env(home):
    """No GIT_* variable and no global or system Git config (as tests/test_push_precheck.py)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_") and k != "XDG_CONFIG_HOME"}
    env.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null", GIT_CONFIG_NOSYSTEM="1", HOME=home)
    return env


def git(home, *args):
    subprocess.run(["git", "-c", "commit.gpgsign=false", *args], env=clean_env(home), check=True,
                   stdin=subprocess.DEVNULL, capture_output=True)


def run(args, cwd, home, stdin=subprocess.DEVNULL):
    env = clean_env(home)
    return subprocess.run([sys.executable, "-I", SCRIPT] + args, cwd=cwd, env=env, stdin=stdin,
                          capture_output=True, text=True, timeout=60)


class Check(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.home = os.path.join(self.tmp.name, "home")
        self.repo = os.path.join(self.tmp.name, "repo")
        os.makedirs(self.home)
        git(self.home, "init", "-q", self.repo)
        self.mod = load("reviewer_acceptance", SCRIPT)
        cwd = os.getcwd()
        os.chdir(self.repo)
        try:
            with mock.patch.dict(os.environ, clean_env(self.home), clear=True):
                self.cid = self.mod.clone_id()
        finally:
            os.chdir(cwd)
        self.folder = os.path.join(self.home, ".claude", "dev-skills", "reviewer-acceptance")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, text):
        os.makedirs(self.folder, exist_ok=True)
        with open(os.path.join(self.folder, self.cid + ".json"), "w", encoding="utf-8") as fh:
            fh.write(text)

    def check(self, cwd=None):
        proc = run(["check"], cwd or self.repo, self.home)
        self.assertEqual(proc.stderr, "")
        return proc.stdout, proc.returncode

    def test_no_record(self):
        self.assertEqual(self.check(), ("STOP NO_RECORD\n", 1))

    def test_pass(self):
        self.write(json.dumps({"version": self.mod.ACCEPTANCE_VERSION, "decision": "I accept", "date": "2026-11-09"}))
        self.assertEqual(self.check(), ("PASS\n", 0))

    def test_bad_records(self):
        v = self.mod.ACCEPTANCE_VERSION
        for text in ("not json",
                     '{"version": %d, "decision": "a", "decision": "b", "date": "d"}' % v,
                     json.dumps({"version": True, "decision": "a", "date": "d"}),
                     json.dumps({"version": v, "decision": " ", "date": "d"}),
                     json.dumps({"version": v, "decision": "a", "date": "d", "extra": 1}),
                     json.dumps({"version": v, "decision": "a"}),
                     json.dumps([v, "a", "d"])):
            self.write(text)
            self.assertEqual(self.check(), ("STOP BAD_RECORD\n", 1), text)

    def test_old_version(self):
        for version in (self.mod.ACCEPTANCE_VERSION - 1, self.mod.ACCEPTANCE_VERSION + 1):  # SEC108-02: older and newer
            with self.subTest(version=version):
                self.write(json.dumps({"version": version, "decision": "a", "date": "d"}))
                self.assertEqual(self.check(), ("STOP VERSION\n", 1))

    def test_outside_a_repository(self):
        outside = os.path.join(self.tmp.name, "plain")
        os.makedirs(outside)
        self.assertEqual(self.check(outside), ("STOP GIT\n", 1))

    def test_subfolder_and_worktree_share_the_record(self):
        self.write(json.dumps({"version": self.mod.ACCEPTANCE_VERSION, "decision": "a", "date": "d"}))
        sub = os.path.join(self.repo, "sub")
        os.makedirs(sub)
        self.assertEqual(self.check(sub), ("PASS\n", 0))
        git(self.home, "-C", self.repo, "-c", "user.name=t", "-c", "user.email=t@example.invalid",
            "commit", "-q", "--allow-empty", "-m", "init")
        wt = os.path.join(self.tmp.name, "wt")
        git(self.home, "-C", self.repo, "worktree", "add", "-q", wt)
        self.assertEqual(self.check(wt), ("PASS\n", 0))

    def test_another_clone_has_no_record(self):
        self.write(json.dumps({"version": self.mod.ACCEPTANCE_VERSION, "decision": "a", "date": "d"}))
        other = os.path.join(self.tmp.name, "other")
        git(self.home, "init", "-q", other)
        self.assertEqual(self.check(other), ("STOP NO_RECORD\n", 1))

    def test_relative_or_root_home_gives_no_record(self):
        self.write(json.dumps({"version": self.mod.ACCEPTANCE_VERSION, "decision": "a", "date": "d"}))
        for home in (".", "rel", ""):
            proc = run(["check"], self.repo, home)
            self.assertEqual((proc.stdout, proc.returncode, proc.stderr), ("STOP NO_RECORD\n", 1, ""), home)

    def test_written_record_passes_and_is_shown(self):
        cwd = os.getcwd()
        os.chdir(self.repo)
        patch = mock.patch.dict(os.environ, clean_env(self.home), clear=True)
        patch.start()
        try:
            self.assertEqual(self.mod.existing_record_line(), "This clone has no record yet.")
            self.mod.write_record("  I accept the residual risk  ")
            self.assertEqual(self.mod.existing_record_line().split(": ", 1)[1], "I accept the residual risk")
            path = os.path.join(self.folder, self.cid + ".json")
            self.assertEqual(os.stat(path).st_mode & 0o777, 0o600)
        finally:
            patch.stop()
            os.chdir(cwd)
        self.assertEqual(self.check(), ("PASS\n", 0))

    def test_key_has_no_device_number(self):
        proc = subprocess.run(["git", "-C", self.repo, "rev-parse", "--path-format=absolute", "--git-common-dir"],
                              env=clean_env(self.home), capture_output=True, text=True, check=True)
        real = os.path.realpath(proc.stdout.strip())
        want = hashlib.sha256(f"{real}\0{os.stat(real).st_ino}".encode("utf-8", "surrogateescape")).hexdigest()
        self.assertEqual(self.cid, want)  # card I106-C10 (a): st_dev can change at a reboot

    def test_bad_arguments(self):
        proc = run(["check", "--base", "x"], self.repo, self.home)
        self.assertEqual((proc.stdout, proc.returncode, proc.stderr), ("STOP BAD_ARGS\n", 2, ""))


class Accept(unittest.TestCase):
    def test_refuses_without_a_terminal(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = os.path.join(tmp, "home")
            repo = os.path.join(tmp, "repo")
            os.makedirs(home)
            git(home, "init", "-q", repo)
            proc = run(["accept"], repo, home)
            self.assertEqual((proc.stdout, proc.returncode, proc.stderr), ("STOP NO_TTY\n", 1, ""))
            self.assertFalse(os.path.exists(os.path.join(home, ".claude")))

    def test_decision_needs_words_and_exact_yes(self):
        mod = load("reviewer_acceptance", SCRIPT)
        self.assertTrue(mod.decide("I accept the residual risk", "yes"))
        for words, answer in (("I accept", "y"), ("I accept", "Yes please"), ("I accept", ""), ("", "yes"),
                              ("  ", "yes"), ("不接受", "no")):
            self.assertFalse(mod.decide(words, answer), (words, answer))

    def test_accepted_text_is_the_reference_section(self):
        mod = load("reviewer_acceptance", SCRIPT)
        text = mod.accepted_text()
        self.assertTrue(text.startswith(f"## Accepted text (version {mod.ACCEPTANCE_VERSION})"))
        self.assertIn("Write channels:", text)
        self.assertIn("Not covered by the detection:", text)
        self.assertNotIn("## The record", text)


class Version(unittest.TestCase):
    def test_pinned_texts_match_the_version(self):
        mod = load("reviewer_acceptance", SCRIPT)
        self.assertEqual(max(PINNED), mod.ACCEPTANCE_VERSION)
        self.assertEqual(pinned_digest(), PINNED[mod.ACCEPTANCE_VERSION])

    def test_reference_names_the_pinned_tool_lines(self):
        pins = load("check_pack", os.path.join(ROOT, "scripts", "check_pack.py")).READ_ONLY_AGENTS
        with open(REFERENCE, encoding="utf-8") as fh:
            ref = fh.read()
        for stem in REVIEWERS:
            self.assertIn(f"`tools: {pins[stem]['tools']}`", ref, stem)
            self.assertIn(f"`disallowedTools: {pins[stem]['disallowedTools']}`", ref, stem)


class Rules(unittest.TestCase):
    def test_rule_points_to_the_reference_and_names_no_binding(self):
        with open(os.path.join(ROOT, "skills", "dev-core", "SKILL.md"), encoding="utf-8") as fh:
            core = fh.read()
        rev1 = core[core.index("- **R-REV-1**"):core.index("- **R-REV-2**")]
        self.assertIn("the check that `${CLAUDE_SKILL_DIR}/../dev-core/references/reviewer-acceptance.md` gives prints `PASS`", rev1)
        with open(REFERENCE, encoding="utf-8") as fh:
            ref = fh.read()
        for sentence in ("The agent never creates, edits, moves or deletes the user's record",
                         "keeps the review incomplete and the\ndependent gate stopped",
                         "or a case where\nthe record does not apply",
                         "quoted with its date and\nthe change it was given for, and recorded in this change"):
            self.assertIn(sentence, ref)
        for path in (os.path.join(ROOT, "skills", "dev-core", "SKILL.md"), REFERENCE, SCRIPT,
                     os.path.join(ROOT, "skills", "dev-core", "deltas.md")):
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            for name in ("gh api user", "nameWithOwner", "reviewer-acceptance.json"):
                self.assertNotIn(name, text, (path, name))
        for path in (os.path.join(ROOT, "skills", "dev-core", "SKILL.md"), REFERENCE, SCRIPT):
            with open(path, encoding="utf-8") as fh:
                self.assertNotIn("jeffery777", fh.read(), path)  # the login of this repository's owner


if __name__ == "__main__":
    unittest.main()
