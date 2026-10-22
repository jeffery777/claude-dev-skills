"""Negative tests for scripts/check_core_coverage.py and scripts/verify_core.py."""

import contextlib
import importlib.util
import io
import os
import shutil
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "scripts", name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run(mod):
    with contextlib.redirect_stdout(io.StringIO()) as out:
        code = mod.main()
    return code, out.getvalue()


class Coverage(unittest.TestCase):
    def setUp(self):
        self.mod = load("check_core_coverage")
        self.tmp = tempfile.mkdtemp()
        for name in ("SKILL", "SOURCE_MAP"):
            dst = os.path.join(self.tmp, os.path.basename(getattr(self.mod, name)))
            shutil.copy(getattr(self.mod, name), dst)
            setattr(self.mod, name, dst)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def edit(self, attr, old, new):
        path = getattr(self.mod, attr)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn(old, text)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text.replace(old, new, 1))

    def test_current_tree_passes(self):
        self.assertEqual(run(self.mod)[0], 0)

    def test_missing_anchor_row_fails(self):
        self.edit("SOURCE_MAP", "| `authorization-and-stops.md#auth-data` | R-AUTH-7 | covered | |\n", "")
        code, out = run(self.mod)
        self.assertEqual(code, 1)
        self.assertIn("anchor without source-map row: authorization-and-stops.md#auth-data", out)

    def test_not_applicable_needs_reason(self):
        self.edit("SOURCE_MAP", "| `authorization-and-stops.md#auth-data` | R-AUTH-7 | covered | |",
                  "| `authorization-and-stops.md#auth-data` | | not-applicable | |")
        code, out = run(self.mod)
        self.assertEqual(code, 1)
        self.assertIn("not-applicable without a reason", out)

    def test_rule_without_citation_fails(self):
        self.edit("SKILL", "[core: workflow.md#wf-writing]", "")
        code, out = run(self.mod)
        self.assertEqual(code, 1)
        self.assertIn("R-WRT-1: cites no Core anchor", out)


class TemplateParses(unittest.TestCase):
    def test_req_template_sources_parse(self):
        mod = load("check_pack")
        entries, _ = mod.sources(mod.front_block(os.path.join(ROOT, "skills", "dev-plan", "templates", "REQ-template.md")))
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["type"], "chat")


class PackChecks(unittest.TestCase):
    def test_tool_set_ignores_specifiers(self):
        mod = load("check_pack")
        self.assertEqual(mod.tool_set("Read, Write(docs/**), Bash"), {"Read", "Write", "Bash"})
        self.assertEqual(mod.tool_set(["Read", "MultiEdit"]), {"Read", "MultiEdit"})

    def test_duplicate_req_file_fails(self):
        mod = load("check_pack")
        tmp = tempfile.mkdtemp()
        try:
            req_dir = os.path.join(tmp, "docs", "requirements")
            shutil.copytree(os.path.join(ROOT, "docs", "requirements"), req_dir)
            shutil.copy(os.path.join(req_dir, "REQ-001-claude-skill-pack.md"), os.path.join(req_dir, "REQ-001-dup.md"))
            for sub in ("skills", "agents"):
                shutil.copytree(os.path.join(ROOT, sub), os.path.join(tmp, sub))
            mod.ROOT = tmp
            code, out = run(mod)
            self.assertEqual(code, 1)
            self.assertIn("REQ-001 has several files", out)
        finally:
            shutil.rmtree(tmp)


class FrontMatterGuards(unittest.TestCase):
    """check_pack rejects a bad agent model or effort and a bad REQ status (PR-C2 A3)."""

    def check(self, rel, old, new):
        mod = load("check_pack")
        tmp = tempfile.mkdtemp()
        try:
            for sub in ("skills", "agents", "vendor", os.path.join("docs", "requirements")):
                shutil.copytree(os.path.join(ROOT, sub), os.path.join(tmp, sub))
            path = os.path.join(tmp, rel)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            self.assertIn(old, text)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text.replace(old, new, 1))
            mod.ROOT = tmp
            code, out = run(mod)
            self.assertEqual(out.count("\n  - "), 1, out)  # the edit is the only problem
            return code, out
        finally:
            shutil.rmtree(tmp)

    def test_bad_model_fails(self):
        code, out = self.check(os.path.join("agents", "dev-explorer.md"), "\nmodel: haiku\n", "\nmodel: claude-haiku-5-5\n")
        self.assertEqual(code, 1)
        self.assertIn("agents/dev-explorer.md: model must be an alias", out)

    def test_bad_effort_fails(self):
        code, out = self.check(os.path.join("agents", "dev-explorer.md"), "\neffort: low\n", "\neffort: think-harder\n")
        self.assertEqual(code, 1)
        self.assertIn("agents/dev-explorer.md: effort must be one of", out)

    def test_empty_values_fail_without_crash(self):  # MR4-02: an empty value parsed as a list crashed with TypeError
        for rel, old, new, message in (
                (os.path.join("agents", "dev-explorer.md"), "\nmodel: haiku\n", "\nmodel:\n", "model must be an alias"),
                (os.path.join("agents", "dev-explorer.md"), "\neffort: low\n", "\neffort:\n", "effort must be one of"),
                (os.path.join("docs", "requirements", "REQ-001-claude-skill-pack.md"), "\nstatus: active\n", "\nstatus:\n",
                 "status must be one of")):
            with self.subTest(rel=rel, field=new.strip()):
                code, out = self.check(rel, old, new)
                self.assertEqual(code, 1)
                self.assertIn(message, out)

    def test_bad_req_status_fails(self):
        code, out = self.check(os.path.join("docs", "requirements", "REQ-001-claude-skill-pack.md"), "\nstatus: active\n", "\nstatus: finished\n")
        self.assertEqual(code, 1)
        self.assertIn("REQ-001-claude-skill-pack.md: status must be one of", out)


class SourcesParser(unittest.TestCase):
    def test_variants(self):
        mod = load("check_pack")
        block = ["id: REQ-001", "sources:", "- type: chat", "  locator: \"x\"", "  quote:", "    long quote",
                 "  - type: doc", "    locator: y", "    quote: >", "      folded text", "non_goals: []"]
        self.assertEqual(mod.sources(block), ([
            {"type": "chat", "locator": "x", "quote": "long quote"},
            {"type": "doc", "locator": "y", "quote": "folded text"}], []))

    def test_sibling_key_is_not_a_quote(self):
        mod = load("check_pack")
        entries, problems = mod.sources(["sources:", "  - type: chat", "    locator: x", "    quote:", "    note: anything"])
        self.assertEqual(entries[0]["quote"], "")
        self.assertEqual(problems, ["unknown key 'note' in a sources entry"])

    def test_hash_line_inside_block_scalar_is_content(self):  # MR5-01
        mod = load("check_pack")
        block = ["sources:", "  - type: chat", "    locator: x", "    quote: |", "      # Heading", "      line two",
                 "  - type: doc", "    locator: y", "    quote: >", "      one", "      # two", "      three"]
        self.assertEqual(mod.sources(block), ([
            {"type": "chat", "locator": "x", "quote": "# Heading line two"},
            {"type": "doc", "locator": "y", "quote": "one # two three"}], []))

    def test_keep_chomping_block_scalar(self):  # PR-C2 A4: the old parser kept "|+" as text and skipped "# a"
        mod = load("check_pack")
        block = ["sources:", "  - type: chat", "    locator: x", "    quote: |+", "      # a", "      b",
                 "  - type: doc", "    locator: y", "    quote: >+", "      c"]
        self.assertEqual(mod.sources(block), ([
            {"type": "chat", "locator": "x", "quote": "# a b"},
            {"type": "doc", "locator": "y", "quote": "c"}], []))

    def test_comment_line_outside_block_scalar_is_skipped(self):
        mod = load("check_pack")
        block = ["sources:", "  - type: chat", "    locator: x", "    quote: q", "      # a comment",
                 "  # between entries", "  - type: doc", "    locator: y", "    quote: >", "      text", "  # after"]
        self.assertEqual(mod.sources(block), ([
            {"type": "chat", "locator": "x", "quote": "q"},
            {"type": "doc", "locator": "y", "quote": "text"}], []))


class ReviewerBinding(unittest.TestCase):
    """dev-core CB-4: no write-capable substitute for a required review (PR #2 decision 3)."""

    def setUp(self):
        with open(os.path.join(ROOT, "skills", "dev-core", "SKILL.md"), encoding="utf-8") as fh:
            text = fh.read()
        self.text = text
        self.section = text[text.index("## 8. Claude-specific bindings"):]

    def test_fingerprint_script_removed(self):
        self.assertFalse(os.path.exists(os.path.join(ROOT, "skills", "dev-core", "scripts", "tree_fingerprint.py")))
        self.assertNotIn("tree_fingerprint", self.section)

    def test_required_review_stops_without_read_only_agent(self):
        self.assertNotIn("When a named agent is unavailable, use a general-purpose subagent", self.section)
        self.assertIn("do not substitute an agent that has write tools for a required review", self.section)
        self.assertIn("Stop at that gate", self.section)
        self.assertNotIn("general-purpose substitute counts as the independent reviewer", self.text)
        self.assertNotIn("tree check", self.text)

    def test_accidental_edit_check_is_stated(self):
        self.assertIn("git rev-parse HEAD", self.section)
        self.assertIn("git status --porcelain=v1 --untracked-files=all", self.section)
        self.assertIn("git diff HEAD --binary", self.section)
        self.assertIn("It is not isolation", self.section)

    def test_commit_state_setting(self):
        self.assertIn('`"commit_state"` in `.dev/config.json`. The default is `true`', self.section)


class VendorLock(unittest.TestCase):
    def setUp(self):
        self.mod = load("verify_core")
        self.tmp = tempfile.mkdtemp()
        vendor = os.path.join(self.tmp, "core")
        shutil.copytree(self.mod.VENDOR, vendor)
        self.mod.VENDOR = vendor

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_current_tree_passes(self):
        self.assertEqual(run(self.mod)[0], 0)

    def test_tampered_file_fails(self):
        with open(os.path.join(self.mod.VENDOR, "contracts", "workflow.md"), "a", encoding="utf-8") as fh:
            fh.write("\nrelaxed rule\n")
        code, out = run(self.mod)
        self.assertEqual(code, 1)
        self.assertIn("digest or size mismatch: contracts/workflow.md", out)

    def test_upstream_flag_needs_value(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(self.mod.main(["--upstream"]), 2)

    def test_extra_file_fails(self):
        with open(os.path.join(self.mod.VENDOR, "extra.md"), "w"):
            pass
        code, out = run(self.mod)
        self.assertEqual(code, 1)
        self.assertIn("not in lock: extra.md", out)


if __name__ == "__main__":
    unittest.main()
