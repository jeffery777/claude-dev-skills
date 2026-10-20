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
        self.edit("SOURCE_MAP", "| `workflow.md#wf-writing` | R-WRT-1 | covered | |\n", "")
        code, out = run(self.mod)
        self.assertEqual(code, 1)
        self.assertIn("anchor without source-map row: workflow.md#wf-writing", out)

    def test_not_applicable_needs_reason(self):
        self.edit("SOURCE_MAP", "| `workflow.md#wf-writing` | R-WRT-1 | covered | |",
                  "| `workflow.md#wf-writing` | | not-applicable | |")
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
        entries = mod.sources(mod.front_block(os.path.join(ROOT, "skills", "dev-plan", "templates", "REQ-template.md")))
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
