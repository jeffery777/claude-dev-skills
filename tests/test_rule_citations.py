"""Rule IDs cited in skills/ and agents/ exist in dev-core; skills/, agents/ and tests/ do not cite dev-core by
section number (REQ-022)."""

import glob
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORE = os.path.join(ROOT, "skills", "dev-core", "SKILL.md")
ID_RE = re.compile(r"\b(?:R-[A-Z]+-\d+|CB-\d+)\b")
DEFINED_RE = re.compile(r"\*\*((?:R-[A-Z]+-\d+|CB-\d+))\*\*")
# A citation of dev-core by section number, in any file.
SECTION_RE = re.compile(r"dev-core`?(?:'s)?\s*(?:section|§)\s*\d|(?:section|§)\s*\d+\s+(?:of|in)\s+`?dev-core"
                        r"|\(\s*(?:section|§)\s*\d+\s*\)", re.IGNORECASE)
# Inside dev-core's own folder, any section number is a citation of dev-core.
CORE_SECTION_RE = re.compile(r"\bsections?\s*\d|§\s*\d", re.IGNORECASE)


def files():
    return sorted(glob.glob(os.path.join(ROOT, "skills", "**", "*.md"), recursive=True)
                  + glob.glob(os.path.join(ROOT, "agents", "*.md")))


def section_hits(path):
    text = " ".join(read(path).split())
    if os.path.dirname(path) == os.path.dirname(CORE):
        return bool(CORE_SECTION_RE.search(text))
    return bool(SECTION_RE.search(text))


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


class RuleCitations(unittest.TestCase):
    def test_defined_ids_include_cb_1_to_cb_5(self):
        defined = DEFINED_RE.findall(read(CORE))
        self.assertEqual(len(defined), len(set(defined)))
        for n in range(1, 6):
            self.assertIn(f"CB-{n}", defined)

    def test_every_cited_id_exists_in_dev_core(self):
        defined = set(DEFINED_RE.findall(read(CORE)))
        missing = [(os.path.relpath(p, ROOT), rid) for p in files() for rid in sorted(set(ID_RE.findall(read(p))))
                   if rid not in defined]
        self.assertEqual(missing, [])

    def test_no_citation_by_section_number(self):
        tests = [p for p in glob.glob(os.path.join(ROOT, "tests", "*.py")) if os.path.basename(p) != "test_rule_citations.py"]
        hits = [os.path.relpath(p, ROOT) for p in files() + sorted(tests) if section_hits(p)]
        self.assertEqual(hits, [])

    def test_patterns_catch_bad_citations(self):
        defined = set(DEFINED_RE.findall(read(CORE)))
        self.assertNotIn("R-REV-99", defined)
        self.assertNotIn("CB-6", defined)
        self.assertTrue(ID_RE.search("cite R-REV-99 here"))
        self.assertTrue(ID_RE.search("cite CB-6 here"))
        for bad in ("(dev-core §8)", "(`dev-core` section 8)", "stops at the gate (section 8)", "(§8)",
                    "dev-core Section 8", "section 8 of dev-core", "dev-core's section 8", '"""dev-core section 8: x"""'):
            self.assertTrue(SECTION_RE.search(bad), bad)
        self.assertFalse(SECTION_RE.search("one writer (design section 6)"))
        for bad in ("| DL-009 | R-DEL-1, R-REV-1, section 8 |", "(§ 8)", "sections 4 and 8"):
            self.assertTrue(CORE_SECTION_RE.search(bad), bad)
        self.assertFalse(CORE_SECTION_RE.search("Other files cite the ID, never the section number."))


if __name__ == "__main__":
    unittest.main()
