"""Issue #106 PR-1: the acceptance D-032 names the pinned reviewer tools, and R-REV-1 holds its check (DL-004).

A co-change check only: it proves no runtime tool limit and no new acceptance of the user.
Only a new, quoted decision of the user changes D-032 (R-REV-1).
"""

import importlib.util
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECK = ('`test "$(gh api user --jq .login 2>/dev/null)" = jeffery777 && test "$(gh repo view --json nameWithOwner'
         ' --jq .nameWithOwner 2>/dev/null)" = jeffery777/claude-dev-skills && echo PASS || echo STOP`')
REVIEWERS = ("dev-reviewer", "dev-security-reviewer")


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as fh:
        return fh.read()


def load_check_pack():
    spec = importlib.util.spec_from_file_location("check_pack", os.path.join(ROOT, "scripts", "check_pack.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def section(text, heading):
    """The text from one `### ` heading up to the next heading of level 1 to 3, or a closing `</details>`."""
    start = text.index(heading)
    end = re.compile(r"\n(#{1,3} |</details>)").search(text, start + len(heading))
    return text[start:end.start() if end else len(text)]


class Acceptance(unittest.TestCase):
    def setUp(self):
        self.proposal = read("docs", "design-proposal.md")
        self.english = section(self.proposal, "### D-032 One-time acceptance of the reviewer write channel")

    def test_record_in_both_languages(self):
        self.assertEqual(self.proposal.count("### D-032 "), 2)
        self.assertIn("### D-032 reviewer 寫入通道的一次性接受", self.proposal)

    def test_record_names_the_pinned_tools(self):
        pins = load_check_pack().READ_ONLY_AGENTS
        for stem in REVIEWERS:
            self.assertIn(f"`tools: {pins[stem]['tools']}`", self.english, stem)
            self.assertIn(f"`disallowedTools: {pins[stem]['disallowedTools']}`", self.english, stem)

    def test_record_and_rule_hold_the_same_check(self):
        self.assertIn(CHECK, self.english)
        self.assertIn(CHECK, section(self.proposal, "### D-032 reviewer 寫入通道的一次性接受"))
        core = read("skills", "dev-core", "SKILL.md")
        rev1 = core[core.index("- **R-REV-1**"):core.index("- **R-REV-2**")]
        self.assertIn(CHECK, rev1)
        self.assertIn("D-032", rev1)
        self.assertIn("never change it to make a test pass", rev1)

    def test_record_has_the_core_fields(self):
        for field in ("- Origin:", "- Bound environment:", "- Protected resources:", "- Rules covered:",
                      "- Write channels:", "- Reason:", "- Substitute detection:", "- Not covered by the detection:",
                      "- Not exempted:", "- End and change:"):
            self.assertIn(field, self.english, field)
        self.assertIn("never recorded as technical read-only", self.english)


if __name__ == "__main__":
    unittest.main()
