"""Issue #104: the moved text is reachable, and each decision has its rule sentence (D-031, DL-048, DL-049)."""

import os
import re
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return " ".join(fh.read().split())


CORE = ("skills", "dev-core", "SKILL.md")
GATE = ("skills", "dev-core", "references", "readback-gate.md")
PUSH = ("skills", "dev-core", "references", "push-scan.md")
AGENT = ("agents", "dev-security-reviewer.md")


def rule(text, rule_id):
    """The text of one rule of dev-core, up to the next rule."""
    start = text.index(f"**{rule_id}**")
    following = re.search(r" - \*\*(R|CB)-[A-Z0-9-]+\*\* ", text[start + 1:])
    return text[start:start + 1 + following.start()] if following else text[start:]


class Moved(unittest.TestCase):
    def test_rule_points_to_each_reference(self):
        core = read(*CORE)
        for name in ("readback-gate.md", "push-scan.md"):
            self.assertIn(f"`${{CLAUDE_SKILL_DIR}}/../dev-core/references/{name}`", core)
            self.assertTrue(os.path.isfile(os.path.join(ROOT, "skills", "dev-core", "references", name)))
        self.assertIn(f"Before a read-back, read `${{CLAUDE_SKILL_DIR}}/../dev-core/references/readback-gate.md` in full", core)
        self.assertIn("references/push-scan.md`. Read that file in full first", core)

    def test_rule_keeps_the_read_back_command(self):
        self.assertIn("| python3 -I - subagent --config-base <full base ID> --floor review-scan", read(*CORE))

    def test_push_steps_are_in_the_reference_only(self):
        self.assertNotIn("The real push has only this form", read(*CORE))
        self.assertIn("The real push has only this form", read(*PUSH))
        self.assertIn("Not covered: the scans cover", read(*PUSH))
        self.assertIn("references/push-scan.md", read("skills", "dev-implement", "SKILL.md"))


class Decisions(unittest.TestCase):
    def test_q1_r_ver_2_is_at_the_core_level(self):
        text = rule(read(*CORE), "R-VER-2")
        self.assertIn("It stops for the user, with a decision card (R-AUTH-6), only on a `MUST-FIX`, a requirement "
                      "change or a loosening; otherwise the work continues.", text)
        self.assertNotIn("stop the fix loop", text)
        for parts in (CORE, ("skills", "dev-deliver", "SKILL.md"), ("skills", "dev-review", "SKILL.md"),
                      ("skills", "dev-review", "references", "review-report.md")):
            self.assertNotIn("stop rule", read(*parts), parts)

    def test_q2_only_the_three_dispatches_are_read_back(self):
        core = read(*CORE)
        self.assertIn("No other dispatch is read back: its `recorded` value is `unknown` with the case `not read back`.",
                      core)
        self.assertIn("No other dispatch is read back.", read(*GATE))
        self.assertNotIn("For a dispatch of work under the floor", read(*GATE))
        for parts in (("skills", "dev-implement", "SKILL.md"), ("skills", "dev-continue", "SKILL.md")):
            self.assertNotIn("does not count by R-DEL-2", read(*parts), parts)

    def test_q2_keeps_the_floor_check_and_the_session_rule(self):
        core = read(*CORE)
        self.assertIn("A review or scan counts only in the session that dispatched it as a subagent", core)
        self.assertIn("This check runs at the `dev-deliver` Dispatch step", core)

    def test_q3_scan_target(self):
        self.assertIn("for private data only", rule(read(*CORE), "R-REV-9"))
        self.assertIn("It does not judge whether a fact is precise", rule(read(*CORE), "R-REV-9"))
        self.assertIn("It does not judge whether a fact is precise", read(*AGENT))

    def text_check(self, content):
        command = re.search(r"`(LC_ALL=C awk '[^`]*\{print NR\}') <text file>`", read(*CORE)).group(1)
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "text")
            with open(path, "wb") as fh:
                fh.write(content)
            return subprocess.run(["bash", "-c", f"{command} '{path}'"], capture_output=True)

    def test_q3_check_prints_only_line_numbers(self):
        samples = [b"/" + b"Users/someone/x", b"/" + b"home/someone/x", b"a.b" + b"@example.invalid",
                   b"gh" + b"p_abc", b"github" + b"_pat_abc", b"AK" + b"IAABC", b"-----BEGIN " + b"RSA PRIVATE KEY"]
        for sample in samples:
            with self.subTest(sample=sample):
                result = self.text_check(b"clean\n" + sample + b"\n")
                self.assertEqual((result.returncode, result.stdout), (0, b"2\n"))

    def test_q3_check_passes_clean_text_and_survives_a_nul_byte(self):
        self.assertEqual(self.text_check(b"Closes #104\nskills/dev-core/SKILL.md\n").stdout, b"")
        self.assertEqual(self.text_check(b"a\0b\n" + b"x" + b"@example.invalid\n").stdout, b"2\n")

    def test_r_rev_4_order(self):
        text = rule(read(*CORE), "R-REV-4")
        order = [text.index(words) for words in ("is it in the threat model", "does a requirement cover it",
                                                 "only then fix, and prefer deletion")]
        self.assertEqual(order, sorted(order))
        self.assertIn("This order does not lower a Core blocker", text)

    def test_accepted_residual_risk(self):
        self.assertIn("A residual risk that the user has accepted is not raised again in later PRs of the same work",
                      rule(read(*CORE), "R-REV-3"))

    def test_platform_signature_is_recorded_only(self):
        words = "created (committer `GitHub <noreply@github.com>`) is recorded only"
        for parts in (CORE, PUSH, AGENT):
            self.assertIn(words, read(*parts), parts)
        self.assertIn("A signature on the user's own commits before a push still goes to the user", read(*CORE))
        self.assertIn("a signature that R-REV-9 step 8 reports as blocking stops the push",
                      read("skills", "dev-implement", "SKILL.md"))


if __name__ == "__main__":
    unittest.main()
