"""Negative tests for scripts/check_core_coverage.py and scripts/verify_core.py."""

import contextlib
import glob
import importlib.util
import io
import json
import os
import re
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
    def test_duplicate_req_file_fails(self):
        mod = load("check_pack")
        tmp = tempfile.mkdtemp()
        try:
            req_dir = os.path.join(tmp, "docs", "requirements")
            shutil.copytree(os.path.join(ROOT, "docs", "requirements"), req_dir)
            shutil.copy(os.path.join(req_dir, "REQ-001-claude-skill-pack.md"), os.path.join(req_dir, "REQ-001-dup.md"))
            for sub in ("skills", "agents", ".claude-plugin"):
                shutil.copytree(os.path.join(ROOT, sub), os.path.join(tmp, sub))
            mod.ROOT = tmp
            code, out = run(mod)
            self.assertEqual(code, 1)
            self.assertIn("REQ-001 has several files", out)
        finally:
            shutil.rmtree(tmp)


class FrontMatterGuards(unittest.TestCase):
    """check_pack rejects a bad agent model or effort and a bad REQ status (PR-C2 A3), and any skill
    allowed-tools value other than the two pack Read rules, any skill or agent front matter text
    outside the raw line format, any name outside the closed-world allowlists of the root,
    .claude-plugin/, skills/ and agents/, a manifest key outside its allowlist or another
    marketplace entry, or a symlink or hardlink under skills/ or vendor/ (CB-7)."""

    def check(self, rel, old, new, same_file=False, count=1):
        def edit(tmp):
            path = os.path.join(tmp, rel)
            with open(path, encoding="utf-8", newline="") as fh:
                text = fh.read()
            self.assertIn(old, text)
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(text.replace(old, new, 1))
        return self.check_tree(edit, rel if same_file else None, count=count)

    def check_tree(self, change, same_file=None, count=1, restore=None, patch=None):
        mod = load("check_pack")
        tmp = tempfile.mkdtemp()
        try:
            for sub in ("skills", "agents", "vendor", os.path.join("docs", "requirements"), ".claude-plugin"):
                shutil.copytree(os.path.join(ROOT, sub), os.path.join(tmp, sub))
            change(tmp)
            mod.ROOT = tmp
            if patch:  # a change of a constant of check_pack itself
                patch(mod)
            code, out = run(mod)
            if same_file:  # the edit may be reported by both skill checks, but by nothing else
                problems = [line for line in out.splitlines() if line.startswith("  - ")]
                self.assertTrue(problems and all(p.startswith(f"  - {same_file}: ") for p in problems), out)
            else:
                self.assertEqual(out.count("\n  - "), count, out)  # the edit is the only problem, or gives `count`
            return code, out
        finally:
            if restore:  # Issue #66 MR67B-001: undo a change such as chmod 0 before the tree is removed
                restore(tmp)
            shutil.rmtree(tmp)

    AGENT_DEFAULT = "of the agent_default role in skills/dev-core/model-config.json is needed for"  # Issue #96

    def test_bad_model_fails(self):  # the agent_default check of Issue #96 fires as well
        code, out = self.check(os.path.join("agents", "dev-explorer.md"), "\nmodel: haiku\n", "\nmodel: claude-haiku-5-5\n",
                               count=2)
        self.assertEqual(code, 1)
        self.assertIn("agents/dev-explorer.md: model must be an alias", out)
        self.assertIn(f"agents/dev-explorer.md: the line 'model: haiku' {self.AGENT_DEFAULT} model", out)

    def test_bad_effort_fails(self):  # the agent_default check of Issue #96 fires as well
        code, out = self.check(os.path.join("agents", "dev-explorer.md"), "\neffort: low\n", "\neffort: think-harder\n",
                               count=2)
        self.assertEqual(code, 1)
        self.assertIn("agents/dev-explorer.md: effort must be one of", out)
        self.assertIn(f"agents/dev-explorer.md: the line 'effort: low' {self.AGENT_DEFAULT} effort", out)

    def test_empty_values_fail_without_crash(self):  # MR4-02: an empty value parsed as a list crashed with TypeError
        for rel, old, new, message in (
                (os.path.join("agents", "dev-explorer.md"), "\nmodel: haiku\n", "\nmodel:\n", "model must be an alias"),
                (os.path.join("agents", "dev-explorer.md"), "\neffort: low\n", "\neffort:\n", "effort must be one of"),
                (os.path.join("docs", "requirements", "REQ-001-claude-skill-pack.md"), "\nstatus: active\n", "\nstatus:\n",
                 "status must be one of")):
            with self.subTest(rel=rel, field=new.strip()):
                code, out = self.check(rel, old, new, same_file=True)  # an agent file also fails the value grammar
                self.assertEqual(code, 1)
                self.assertIn(message, out)

    def test_bad_req_status_fails(self):
        code, out = self.check(os.path.join("docs", "requirements", "REQ-001-claude-skill-pack.md"), "\nstatus: active\n", "\nstatus: finished\n")
        self.assertEqual(code, 1)
        self.assertIn("REQ-001-claude-skill-pack.md: status must be one of", out)


    RULES = ("allowed-tools:\n  - Read(/${CLAUDE_PLUGIN_ROOT}/skills/**)\n"
             "  - Read(/${CLAUDE_PLUGIN_ROOT}/vendor/engineering-workflow-core/contracts/**)\n")

    def test_skill_read_grant_is_exactly_two_rules(self):  # CB-7, Issue #66 card A1
        skill = os.path.join("skills", "dev-core", "SKILL.md")
        rules = self.RULES
        for case, new in (
                ("bare Read item", rules.replace("  - Read(/${CLAUDE_PLUGIN_ROOT}/skills/**)\n", "  - Read\n")),
                ("bare Read string", "allowed-tools: Read\n"),
                ("string form", "allowed-tools: Read(/${CLAUDE_PLUGIN_ROOT}/skills/**) "
                                "Read(/${CLAUDE_PLUGIN_ROOT}/vendor/engineering-workflow-core/contracts/**)\n"),
                ("whole plugin root", rules.replace("/${CLAUDE_PLUGIN_ROOT}/skills/**", "/${CLAUDE_PLUGIN_ROOT}/**")),
                ("no leading slash", rules.replace("(/${CLAUDE_PLUGIN_ROOT}/skills/", "(${CLAUDE_PLUGIN_ROOT}/skills/")),
                ("extra Grep", rules + "  - Grep\n"),
                ("empty list", "allowed-tools:\n")):
            with self.subTest(case=case):
                code, out = self.check(skill, "\n" + rules, "\n" + new, same_file=True)
                self.assertEqual(code, 1)
                self.assertIn("skills/dev-core/SKILL.md: allowed-tools must be a YAML list of exactly", out)
        code, out = self.check(skill, "\n" + rules, "\n", same_file=True)
        self.assertEqual(code, 1)
        self.assertIn("skills/dev-core/SKILL.md: allowed-tools missing", out)
        self.assertIn("skills/dev-core/SKILL.md: front matter has no 'allowed-tools:' line", out)

    def test_real_pack_front_matter_passes(self):  # CB-7, Issue #66 I66R1-001
        mod = load("check_pack")
        for skill_md in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
            with self.subTest(skill=skill_md):
                self.assertIsNone(mod.raw_front_matter_problem(skill_md, mod.SKILL_KEYS))
        for agent_md in sorted(glob.glob(os.path.join(ROOT, "agents", "*.md"))):
            with self.subTest(agent=agent_md):
                self.assertIsNone(mod.raw_front_matter_problem(agent_md, mod.AGENT_KEYS))
        self.assertEqual(run(mod)[0], 0)

    def test_raw_front_matter_outside_the_line_format_fails(self):  # CB-7, Issue #66 I66R1-001 / I66S1-001
        skill = os.path.join("skills", "dev-core", "SKILL.md")
        item1 = "  - Read(/${CLAUDE_PLUGIN_ROOT}/skills/**)\n"
        item2 = "  - Read(/${CLAUDE_PLUGIN_ROOT}/vendor/engineering-workflow-core/contracts/**)\n"
        rules = self.RULES
        for case, old, new, message in (
                ("continuation after item 2", rules, rules + "    Bash\n", "'    Bash' is not a column-0"),
                ("continuation after item 1", item1, item1 + "    Bash\n", "allowed-tools must be the line"),
                ("tab-led line", rules, rules + "\tBash\n", "only printable ASCII is allowed, found '\\t'"),
                ("item ends with '  Bash'", item2, item2[:-1] + "  Bash\n", "allowed-tools must be the line"),
                ("item ends with U+0085", item2, item2[:-1] + "\x85Bash\n", "only printable ASCII is allowed"),
                ("item ends with form feed", item2, item2[:-1] + "\x0cBash\n", "only printable ASCII is allowed"),
                ("U+2028 in a value", "name: dev-core\n", "name: dev-core\u2028\n", "only printable ASCII is allowed"),
                ("duplicate key before the list", rules, "allowed-tools: Bash\n" + rules, "allowed-tools must be the line"),
                ("duplicate list after the list", rules, rules + rules, "key 'allowed-tools' appears twice"),
                ("duplicate name", rules, rules + "name: dev-core\n", "key 'name' appears twice"),
                ("quoted key after the list", rules, rules + '"allowed-tools": Bash\n', "is not a column-0"),
                ("complex key", rules, rules + "? allowed-tools\n: Bash\n", "is not a column-0"),
                ("underscore key", rules, rules + "allowed_tools: Bash\n", "is not a column-0"),
                ("hooks key", rules, rules + "hooks:\n", "is not a column-0"),
                ("extra third item", rules, rules + "  - Bash\n", "'  - Bash' is not a column-0"),
                ("items swapped", item1 + item2, item2 + item1, "allowed-tools must be the line")):
            with self.subTest(case=case):
                code, out = self.check(skill, old, new, same_file=True)
                self.assertEqual(code, 1)
                self.assertIn("skills/dev-core/SKILL.md: front matter line", out)
                self.assertIn(message, out)

    def test_agent_front_matter_outside_the_key_allowlist_fails(self):  # CB-7, Issue #66 I66S1-002, card I66-R1-C1 (a)
        agent = os.path.join("agents", "dev-reviewer.md")
        for case, new, message in (
                ("permissionMode key", "permissionMode: bypassPermissions\n", "'permissionMode: bypassPermissions' is not a column-0"),
                ("hooks key", "hooks:\n", "'hooks:' is not a column-0"),
                ("mcpServers key", "mcpServers: x\n", "is not a column-0"),
                ("skills key", "skills: dev-core\n", "is not a column-0"),
                ("indented continuation", "    Bash\n", "'    Bash' is not a column-0"),
                ("duplicate tools", "tools: Read, Grep, Glob, Bash, Edit\n", "key 'tools' appears twice"),
                ("non-ASCII", "color: yellow\u2028\n", "only printable ASCII is allowed")):
            with self.subTest(case=case):
                code, out = self.check(agent, "\ncolor: yellow\n", "\ncolor: yellow\n" + new, same_file=True)
                self.assertEqual(code, 1)
                self.assertIn("agents/dev-reviewer.md: front matter line", out)
                self.assertIn(message, out)

    def test_read_only_agent_tools_are_pinned(self):  # CB-5, Issue #69 (MR67V-001): no split rule to imitate
        explorer, reviewer, security = (os.path.join("agents", n + ".md")
                                        for n in ("dev-explorer", "dev-reviewer", "dev-security-reviewer"))
        tools, denied = "\ntools: Read, Grep, Glob, Bash\n", "\ndisallowedTools: Edit, Write, NotebookEdit\n"
        for case, rel, old, new in (
                ("space-separated write tool", explorer, tools, "\ntools: Read, Grep, Glob, Bash Edit\n"),
                ("comma-separated write tool", explorer, tools, "\ntools: Read, Grep, Glob, Bash, Edit\n"),
                ("'*' in the list", reviewer, tools, "\ntools: Read, Grep, Glob, Bash, *\n"),
                ("write tool with a specifier", explorer, tools, "\ntools: Read, Grep, Glob, Bash, Write(docs/**)\n"),
                ("Agent tool", security, tools, "\ntools: Read, Grep, Glob, Bash, Agent\n"),
                ("no spaces", explorer, tools, "\ntools: Read,Grep,Glob,Bash\n"),
                ("tools removed", explorer, tools, "\n"),
                ("disallowedTools removed", reviewer, denied, "\n"),
                ("disallowedTools removed", security, denied, "\n"),
                ("disallowedTools without NotebookEdit", security, denied, "\ndisallowedTools: Edit, Write\n"),
                ("disallowedTools space-separated", reviewer, denied, "\ndisallowedTools: Edit Write NotebookEdit\n"),
                ("disallowedTools added", explorer, tools, tools + "disallowedTools: Edit\n")):
            with self.subTest(case=case, rel=rel):
                code, out = self.check(rel, old, new)  # check_tree asserts that this is the only problem
                self.assertEqual(code, 1)
                self.assertIn(f"  - {rel}: read-only agent must have ", out)
        code, out = self.check(explorer, tools, "\ntools: *\n", same_file=True)  # the value grammar also fails
        self.assertEqual(code, 1)
        self.assertIn("  - agents/dev-explorer.md: read-only agent must have the line 'tools: Read, Grep, Glob, Bash' "
                      "for tools, found '*'", out)
        code, out = self.check_tree(lambda tmp: os.remove(os.path.join(tmp, security)))
        self.assertEqual(code, 1)
        self.assertIn("  - agents/dev-security-reviewer.md: missing; the read-only agents", out)

    def test_read_only_agent_name_variants_fail(self):  # CB-5, Issue #69 R69R1-001, R69S1-002
        def write(name, text):
            def change(tmp):
                with open(os.path.join(tmp, "agents", name), "w", encoding="utf-8", newline="") as fh:
                    fh.write(text)
            return change
        with open(os.path.join(ROOT, "agents", "dev-reviewer.md"), encoding="utf-8", newline="") as fh:
            reviewer = fh.read()
        def rename(tmp):  # a case-only rename works on a case-insensitive file system too
            os.rename(os.path.join(tmp, "agents", "dev-reviewer.md"), os.path.join(tmp, "agents", "Dev-Reviewer.md"))
            write("Dev-Reviewer.md", reviewer.replace("\nname: dev-reviewer\n", "\nname: Dev-Reviewer\n", 1))(tmp)
        code, out = self.check_tree(rename, count=2)
        self.assertEqual(code, 1)
        self.assertIn("  - agents/dev-reviewer.md: missing; the read-only agents", out)
        self.assertIn("  - agents/Dev-Reviewer.md: the name equals the read-only agent 'dev-reviewer'", out)
        name_line = "\nname: dev-reviewer\n"
        code, out = self.check_tree(write("dev_reviewer.md", reviewer.replace(name_line, "\nname: dev_reviewer\n", 1)))
        self.assertEqual(code, 1)
        self.assertIn("  - agents/dev_reviewer.md: the name equals the read-only agent 'dev-reviewer'", out)
        code, out = self.check_tree(write("dev reviewer.md", reviewer.replace(name_line, "\nname: dev reviewer\n", 1)))
        self.assertEqual(code, 1)  # whitespace is dropped (Issue #69 R69S2-001)
        self.assertIn("  - agents/dev reviewer.md: the name equals the read-only agent 'dev-reviewer'", out)
        for name in ("dev\u2013reviewer.md", "\uff44\uff45\uff56\uff0dreviewer.md"):  # en dash; fullwidth letters and dash
            with self.subTest(name=name):
                rel = os.path.join("agents", name)
                code, out = self.check_tree(write(name, reviewer.replace(name_line, f"\nname: {name[:-3]}\n", 1)),
                                            same_file=rel)  # the non-ASCII name line is reported too
                self.assertEqual(code, 1)
                self.assertIn(f"  - {rel}: the name equals the read-only agent 'dev-reviewer'", out)
        code, out = self.check_tree(write("dev-reviewer.md", reviewer + "x" * 65536 + "\n"))  # past AGENT_MAX_BYTES
        self.assertEqual(code, 1)
        self.assertIn("  - agents/dev-reviewer.md: larger than AGENT_MAX_BYTES (65536 bytes)", out)

    def test_pinned_agent_settings(self):  # R-DEL-2, Issue #77 (cards I77-C1 (a), I77-C5 (a); S3-06, S3-07, S3-08)
        self.assertEqual(load("check_pack").PINNED_AGENT_SETTINGS, {
            "dev-implementer": {"model": "opus", "effort": "high"},
            "dev-reviewer": {"model": "opus", "effort": "high"},
            "dev-security-reviewer": {"model": "opus", "effort": "xhigh"}})
        pins = {"dev-implementer": "high", "dev-reviewer": "high", "dev-security-reviewer": "xhigh"}
        for stem, effort in pins.items():
            rel = os.path.join("agents", stem + ".md")
            for model in ("sonnet", "haiku", "fable", "inherit"):  # lower, other and inherited models
                with self.subTest(stem=stem, model=model):  # the agent_default check of Issue #96 fires as well
                    code, out = self.check(rel, "\nmodel: opus\n", f"\nmodel: {model}\n", count=2)
                    self.assertEqual(code, 1)
                    self.assertIn(f"  - {rel}: pinned agent must have the line 'model: opus' for model, found "
                                  f"{model!r}", out)
                    self.assertIn(f"  - {rel}: the line 'model: opus' {self.AGENT_DEFAULT} model", out)
            for level in ("low", "medium", "high", "xhigh", "max"):  # a lower and a higher value both fail
                if level == effort:
                    continue
                with self.subTest(stem=stem, effort=level):
                    code, out = self.check(rel, f"\neffort: {effort}\n", f"\neffort: {level}\n", count=2)
                    self.assertEqual(code, 1)
                    self.assertIn(f"  - {rel}: pinned agent must have the line 'effort: {effort}' for effort", out)
                    self.assertIn(f"  - {rel}: the line 'effort: {effort}' {self.AGENT_DEFAULT} effort", out)
        implementer = os.path.join("agents", "dev-implementer.md")
        for case, old, new in (
                ("full model ID", "\nmodel: opus\n", "\nmodel: claude-opus-5-5\n"),
                ("model line removed", "\nmodel: opus\n", "\n"),
                ("effort line removed", "\neffort: high\n", "\n"),
                ("duplicate key, lower value last", "\nmodel: opus\n", "\nmodel: opus\nmodel: sonnet\n"),
                ("quote over the pinned lines", "\ndescription: Bounded", "\ndescription: \"Bounded"),
                ("trailing comment", "\neffort: high\n", "\neffort: high # pinned\n"),
                ("CRLF on a pinned line", "\neffort: high\n", "\neffort: high\r\n")):
            with self.subTest(case=case):
                code, out = self.check(implementer, old, new, same_file=True)
                self.assertEqual(code, 1)
        with open(os.path.join(ROOT, implementer), encoding="utf-8", newline="") as fh:
            text = fh.read()
        low = text.replace("\nmodel: opus\neffort: high\n", "\nmodel: sonnet\neffort: medium\n", 1)
        self.assertNotEqual(low, text)
        def write(name, body):
            def change(tmp):
                with open(os.path.join(tmp, "agents", name), "w", encoding="utf-8", newline="") as fh:
                    fh.write(body)
            return change
        # a quote that opens in the description and closes after the pinned lines, with lower values after it:
        # a YAML reader takes opus/high as part of the description; raw_values reads opus/high, so the value
        # grammar must stop it at the opening quote (round 2 findings I77-R2-01, I77-RS2-01)
        hidden = text.replace("\ndescription: Bounded", "\ndescription: \"Bounded", 1).replace(
            "\neffort: high\n", "\neffort: high\ncolor: green\"\nmodel: sonnet\neffort: medium\n", 1)
        self.assertEqual(hidden.split("\n---\n", 1)[0].count("\""), 2)  # both quotes are in the front matter
        code, out = self.check_tree(write("dev-implementer.md", hidden), same_file=implementer)
        self.assertEqual(code, 1)
        self.assertIn(f"  - {implementer}: front matter line 3: a value must not start with", out)
        def remove(tmp):
            os.remove(os.path.join(tmp, implementer))
        code, out = self.check_tree(remove)  # one error for the missing pinned agent
        self.assertEqual(code, 1)
        self.assertIn("  - agents/dev-implementer.md: missing; the read-only agents", out)
        def rename_case(tmp):
            remove(tmp)
            write("Dev-Implementer.md", text.replace("\nname: dev-implementer\n", "\nname: Dev-Implementer\n", 1))(tmp)
        code, out = self.check_tree(rename_case, count=2)
        self.assertEqual(code, 1)
        self.assertIn("  - agents/dev-implementer.md: missing; the read-only agents", out)
        self.assertIn("  - agents/Dev-Implementer.md: the name equals the pinned agent 'dev-implementer'", out)
        code, out = self.check_tree(write("dev_implementer.md", low.replace(
            "\nname: dev-implementer\n", "\nname: dev_implementer\n", 1)))
        self.assertEqual(code, 1)
        self.assertIn("  - agents/dev_implementer.md: the name equals the pinned agent 'dev-implementer'", out)
        def moved(tmp):  # another file name that keeps the dispatch name, with lower values
            remove(tmp)
            write("implementer.md", low)(tmp)
        code, out = self.check_tree(moved, count=2)
        self.assertEqual(code, 1)
        self.assertIn("  - agents/dev-implementer.md: missing; the read-only agents", out)
        self.assertIn("  - agents/implementer.md: name must equal the file name", out)
        code, out = self.check_tree(write("other.md", low),  # a second file with the same dispatch name
                                    same_file=os.path.join("agents", "other.md"))
        self.assertEqual(code, 1)
        code, out = self.check_tree(write("dev-implementer.md", text + "x" * 65536 + "\n"))  # past AGENT_MAX_BYTES
        self.assertEqual(code, 1)
        self.assertIn("  - agents/dev-implementer.md: larger than AGENT_MAX_BYTES (65536 bytes)", out)
        outside = tempfile.mkdtemp()  # the link target is outside the tree, so only the link is reported
        self.addCleanup(shutil.rmtree, outside)
        def symlinked(tmp):
            path = os.path.join(tmp, implementer)
            os.rename(path, os.path.join(outside, "dev-implementer.md"))
            os.symlink(os.path.join(outside, "dev-implementer.md"), path)
        code, out = self.check_tree(symlinked, same_file=implementer)
        self.assertEqual(code, 1)

    MODEL_CONFIG = os.path.join("skills", "dev-core", "model-config.json")

    def config_change(self, fn):
        """A change of the configuration file of the tree: fn(config) edits the parsed JSON in place."""
        def change(tmp):
            path = os.path.join(tmp, self.MODEL_CONFIG)
            with open(path, encoding="utf-8") as fh:
                config = json.load(fh)
            fn(config)
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(config, fh)
        return change

    def test_model_config_pins(self):  # Issue #96 (cards I96-C12 (a), I96-R4-C1 (a); rev8 section 2.2)
        mod = load("check_pack")
        self.assertEqual(mod.PINNED_FAMILY_TIERS, {"haiku": 1, "sonnet": 2, "opus": 3, "fable": 4})
        with open(os.path.join(ROOT, self.MODEL_CONFIG), "rb") as fh:
            config = mod.readback.validate_config(fh.read())  # the shipped file passes the script's validator
        self.assertEqual(config["roles"], mod.PINNED_ROLE_VALUES)
        self.assertEqual(list(mod.PINNED_ROLE_VALUES), list(mod.readback.ROLE_NAMES))
        self.assertEqual({n: f["tier"] for n, f in config["families"].items()}, mod.PINNED_FAMILY_TIERS)
        self.assertEqual(sorted(mod.EFFORTS), sorted(mod.readback.EFFORT_ORDER))
        self.assertEqual(mod.PINNED_FLOORS, {"work": (3, "high"), "review-scan": (3, "xhigh"),  # Issue #96 PR-2
                                             "review-routine": (3, "high"), "review-light": (2, "medium"),
                                             "none": None})
        self.assertEqual(mod.readback.FLOORS, mod.PINNED_FLOORS)
        self.assertEqual({role: value["effort"] for role, value in mod.PINNED_ROLE_VALUES.items()}, {
            "orchestration": ["high", "max"], "explore": ["low", "max"], "explore-synthesis": ["medium", "max"],
            "implement": ["high", "max"], "implement-reduced": ["medium", "max"], "review-routine": ["high", "high"],
            "review-routine-light": ["medium", "medium"], "review-deep": ["xhigh", "xhigh"],
            "review-security": ["xhigh", "xhigh"], "scan": ["xhigh", "xhigh"]})
        self.assertEqual(mod.MODELS, {"haiku", "sonnet", "opus", "fable", "inherit"})  # unchanged by Issue #96
        self.assertEqual(mod.readback.__name__, "model_effort_readback")
        self.assertEqual(os.path.normpath(mod.readback.__file__),
                         os.path.join(ROOT, "skills", "dev-core", "scripts", "model_effort_readback.py"))

    def test_family_tiers_are_pinned(self):  # Issue #96, card I96-C12 (a): a tier equals its pin or is null
        config = self.MODEL_CONFIG
        code, out = self.check_tree(self.config_change(lambda c: c["families"]["opus"].update(tier=5)))
        self.assertEqual(code, 1)
        self.assertIn(f"  - {config}: the tier of 'opus' must be 3 or null, found 5", out)
        def swap(c):
            c["families"]["haiku"]["tier"], c["families"]["sonnet"]["tier"] = 2, 1
        code, out = self.check_tree(self.config_change(swap), count=2)
        self.assertEqual(code, 1)
        self.assertIn(f"  - {config}: the tier of 'haiku' must be 1 or null, found 2", out)
        self.assertIn(f"  - {config}: the tier of 'sonnet' must be 2 or null, found 1", out)
        code, out = self.check_tree(self.config_change(lambda c: c["families"].pop("fable")))
        self.assertEqual(code, 1)
        self.assertIn(f"  - {config}: the families must be exactly ['fable', 'haiku', 'opus', 'sonnet'], found", out)
        code, out = self.check_tree(self.config_change(
            lambda c: c["families"].update(mythos={"tier": 5, "ids": [], "basis": "x"})))
        self.assertEqual(code, 1)
        self.assertIn(f"  - {config}: the families must be exactly", out)
        code, out = self.check_tree(self.config_change(lambda c: c["families"]["fable"].update(tier=None)), count=0)
        self.assertEqual(code, 0)  # retired: null is allowed

    def test_role_values_are_pinned(self):  # Issue #96 PR-2: exact values, keys included
        config = self.MODEL_CONFIG
        for case, fn, role in (
                ("lower effort", lambda c: c["roles"]["review-deep"].update(effort=["high", "high"]), "review-deep"),
                ("lower family", lambda c: c["roles"]["scan"].update(family="sonnet"), "scan"),
                ("higher family", lambda c: c["roles"]["explore"].update(family="sonnet"), "explore"),
                ("wider range of a review", lambda c: c["roles"]["review-routine-light"].update(
                    effort=["medium", "high"]), "review-routine-light"),
                ("wider range of a scan", lambda c: c["roles"]["scan"].update(effort=["xhigh", "max"]), "scan"),
                ("the PR-1 value", lambda c: c["roles"]["implement"].update(effort=["high", "high"]), "implement"),
                ("narrower range", lambda c: c["roles"]["explore-synthesis"].update(effort=["medium", "xhigh"]),
                 "explore-synthesis"),
                ("lower minimum", lambda c: c["roles"]["orchestration"].update(effort=["medium", "max"]),
                 "orchestration"),
                ("higher minimum", lambda c: c["roles"]["implement-reduced"].update(effort=["high", "max"]),
                 "implement-reduced"),
                ("key added", lambda c: c["roles"]["orchestration"].update(agent="dev-implementer"), "orchestration"),
                ("other agent", lambda c: c["roles"]["explore-synthesis"].update(agent="dev-implementer"),
                 "explore-synthesis"),
                ("agent removed", lambda c: c["roles"]["scan"].pop("agent"), "scan")):
            with self.subTest(case=case):
                table = {"other agent": 1, "agent removed": 2}.get(case, 0)  # rows of the routing table check (PR-3)
                code, out = self.check_tree(self.config_change(fn),
                                            count=(2 if case == "higher family" else 1) + table)
                self.assertEqual(code, 1)
                self.assertIn(f"  - {config}: role {role!r} must be ", out)
                self.assertIn("(PINNED_ROLE_VALUES, Issue #96 PR-2)", out)
                if table:
                    self.assertIn(f"names the role {role!r}, whose agent in {config} is ", out)

    def test_agent_default_roles(self):  # Issue #96: one agent_default role per agent, equal to the agent file
        config = self.MODEL_CONFIG
        code, out = self.check_tree(self.config_change(lambda c: c["roles"]["implement"].pop("agent_default")),
                                    count=2)
        self.assertEqual(code, 1)
        self.assertIn(f"  - {config}: agent 'dev-implementer' must have exactly one agent_default role, found 0", out)
        self.assertIn(f"  - {config}: role 'implement' must be ", out)
        explorer = os.path.join("agents", "dev-explorer.md")
        for old, new, key, want in (("\nmodel: haiku\n", "\nmodel: sonnet\n", "model", "haiku"),
                                    ("\nmodel: haiku\n", "\nmodel: opus\n", "model", "haiku"),
                                    ("\neffort: low\n", "\neffort: medium\n", "effort", "low")):
            with self.subTest(new=new.strip()):  # dev-explorer has no PINNED_AGENT_SETTINGS entry: only this check
                code, out = self.check(explorer, old, new)
                self.assertEqual(code, 1)
                self.assertIn(f"  - {explorer}: the line '{key}: {want}' {self.AGENT_DEFAULT} {key}", out)
        def move(c):  # the default of dev-explorer moves to its synthesis role
            c["roles"]["explore"].pop("agent_default")
            c["roles"]["explore-synthesis"]["agent_default"] = True
        code, out = self.check_tree(self.config_change(move), count=4)
        self.assertEqual(code, 1)
        self.assertIn(f"  - {explorer}: the line 'model: sonnet' {self.AGENT_DEFAULT} model", out)
        self.assertIn(f"  - {explorer}: the line 'effort: medium' {self.AGENT_DEFAULT} effort", out)

    def test_invalid_or_missing_config(self):  # Issue #96: the shipped file must pass the script's validator
        config = self.MODEL_CONFIG
        for case, fn in (("schema 2", lambda c: c.update(schema=2)),
                         ("retired family still used", lambda c: c["families"]["sonnet"].update(tier=None)),
                         ("upper-case ID", lambda c: c["families"]["opus"].update(ids=["claude-Opus-5-5"])),
                         ("two agent_default roles", lambda c: c["roles"]["review-deep"].update(agent_default=True))):
            with self.subTest(case=case):
                code, out = self.check_tree(self.config_change(fn))
                self.assertEqual(code, 1)
                self.assertIn(f"  - {config}: the read-back script gives STOP CONFIG for it", out)
        ref = "${CLAUDE_SKILL_DIR}/../dev-core/model-config.json"  # Issue #96 PR-2: the rules name this path
        docs = []
        for doc in sorted(glob.glob(os.path.join(ROOT, "skills", "**", "*.md"), recursive=True)):
            with open(doc, encoding="utf-8") as fh:
                if ref in fh.read():
                    docs.append(os.path.relpath(doc, ROOT))
        code, out = self.check_tree(lambda tmp: os.remove(os.path.join(tmp, config)), count=1 + len(docs))
        self.assertEqual(code, 1)
        self.assertIn(f"  - {config}: missing or not a regular file (Issue #96)", out)
        for doc in docs:  # every other problem is a reference to the removed file
            self.assertIn(f"  - {doc}: referenced path does not exist: {ref}\n", out)
        def duplicate_key(tmp):
            path = os.path.join(tmp, config)
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text.replace('"schema": 1,', '"schema": 1, "schema": 1,', 1))
        code, out = self.check_tree(duplicate_key)
        self.assertEqual(code, 1)
        self.assertIn(f"  - {config}: the read-back script gives STOP CONFIG for it", out)

    def test_efforts_equal_effort_order(self):  # Issue #96: check_pack's EFFORTS is the script's EFFORT_ORDER
        def drop_max(mod):
            mod.EFFORTS = {"low", "medium", "high", "xhigh"}
        code, out = self.check_tree(lambda tmp: None, patch=drop_max)
        self.assertEqual(code, 1)
        self.assertIn("  - scripts/check_pack.py: EFFORTS ['high', 'low', 'medium', 'xhigh'] must equal EFFORT_ORDER", out)

    def test_floors_equal_pinned_floors(self):  # Issue #96 PR-2: FLOORS of the read-back script is pinned
        script = "skills/dev-core/scripts/model_effort_readback.py"
        def floors(value):
            def patch(mod):
                mod.readback.FLOORS = value
            return patch
        def removed(mod):
            del mod.readback.FLOORS
        pinned = {"work": (3, "high"), "review-scan": (3, "xhigh"), "review-routine": (3, "high"),
                  "review-light": (2, "medium"), "none": None}
        for case, patch in (
                ("lower effort", floors({**pinned, "review-scan": (3, "high")})),
                ("lower tier", floors({**pinned, "review-light": (1, "medium")})),
                ("a floor for none", floors({**pinned, "none": (1, "low")})),
                ("key missing", floors({k: v for k, v in pinned.items() if k != "review-light"})),
                ("key added", floors({**pinned, "review-deep": (3, "xhigh")})),
                ("a list, not a tuple", floors({**pinned, "work": [3, "high"]})),
                ("not a dict", floors(list(pinned.items()))),
                ("removed", removed)):
            with self.subTest(case=case):
                code, out = self.check_tree(lambda tmp: None, patch=patch)
                self.assertEqual(code, 1)
                self.assertIn(f"  - {script}: FLOORS must equal PINNED_FLOORS", out)
                self.assertIn("(Issue #96 PR-2)", out)

    def test_fu033_cases(self):  # CB-7, FU-033: cases that REQ-028 acceptance names; each gives one clear error
        agent, skill = os.path.join("agents", "dev-reviewer.md"), os.path.join("skills", "dev-core", "SKILL.md")
        market = os.path.join(".claude-plugin", "marketplace.json")
        color = "\ncolor: yellow\n"
        for case, rel, old, new, message, same_file in (
                ("CR line end", agent, color, "\ncolor: yellow\r\n", "only printable ASCII is allowed, found '\\r'", False),
                ("tab", agent, color, "\ncolor:\tyellow\n", "only printable ASCII is allowed, found '\\t'", False),
                ("U+0085", agent, color, "\ncolor: yellow\u0085\n", "only printable ASCII is allowed, found '\\x85'", False),
                ("quoted key", agent, color, '\n"color": yellow\n', "is not a column-0 'key: value' line", False),
                ("allowed-tools item names Grep", skill, "  - Read(/${CLAUDE_PLUGIN_ROOT}/skills/**)\n",
                 "  - Grep(/${CLAUDE_PLUGIN_ROOT}/skills/**)\n", "allowed-tools must be", True)):
            with self.subTest(case=case):
                code, out = self.check(rel, old, new, same_file=same_file)
                self.assertEqual(code, 1)
                self.assertIn(f"  - {rel}: ", out)
                self.assertIn(message, out)
        def empty_plugins(tmp):
            path = os.path.join(tmp, market)
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            data["plugins"] = []
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(data, fh)
        code, out = self.check_tree(empty_plugins)
        self.assertEqual(code, 1)
        self.assertIn(f"  - {market}: plugins must be a list of exactly one", out)
        def nest(tmp):
            with open(os.path.join(tmp, market), "w", encoding="utf-8") as fh:
                fh.write("[" * 100000 + "]" * 100000)
        code, out = self.check_tree(nest)
        self.assertEqual(code, 1)
        self.assertIn(".claude-plugin/marketplace.json: not valid JSON in UTF-8 without a BOM", out)
        code, out = self.check_tree(lambda tmp: os.mkdir(os.path.join(tmp, "agents", "x.md")))
        self.assertEqual(code, 1)
        self.assertIn("  - agents/x.md: agents/ may hold only", out)

    def test_root_outside_the_allowlist_fails(self):  # CB-7, Issue #66 review round 2, card I66-R2-C1 (a)
        def touch(path):
            open(path, "w", encoding="utf-8").close()
        for name, make in (("hooks", os.mkdir), ("commands", os.mkdir), ("monitors", os.mkdir), ("bin", os.mkdir),
                           ("workflows", os.mkdir), ("output-styles", os.mkdir), ("themes", os.mkdir), ("Hooks", os.mkdir),
                           (".mcp.json", touch), (".lsp.json", touch), ("settings.json", touch), ("plugin.json", touch),
                           ("SKILL.md", touch), ("README.MD", touch), (".DS_Store", touch)):
            with self.subTest(path=name):
                code, out = self.check_tree(lambda tmp: make(os.path.join(tmp, name)))
                self.assertEqual(code, 1)
                self.assertIn(f"  - {name}: not in the root allowlist ROOT_NAMES", out)
                self.assertIn("a new plugin component needs a change of check_pack.py with review; "
                              "a local file such as .DS_Store must be removed (CB-7)", out)  # Issue #66 I66R3-003, I66S3-007
        code, out = self.check_tree(lambda tmp: os.rename(os.path.join(tmp, "skills"), os.path.join(tmp, "Skills")))
        self.assertEqual(code, 1)
        self.assertIn("  - Skills: not in the root allowlist ROOT_NAMES (case differs from 'skills')", out)

    def test_claude_plugin_dir_and_marketplace_entry_are_pinned(self):  # CB-7, Issue #66 review round 2, card I66-R2-C1 (a)
        market = os.path.join(".claude-plugin", "marketplace.json")
        code, out = self.check_tree(lambda tmp: open(os.path.join(tmp, ".claude-plugin", "extra.json"), "w").close())
        self.assertEqual(code, 1)
        self.assertIn(".claude-plugin/extra.json: only ['plugin.json', 'marketplace.json'] are allowed", out)
        code, out = self.check_tree(lambda tmp: os.remove(os.path.join(tmp, market)))
        self.assertEqual(code, 1)
        self.assertIn(".claude-plugin/marketplace.json: missing", out)
        for case, old, new in (("BOM", '{\n  "name"', '\ufeff{\n  "name"'), ("invalid JSON", '"plugins": [', '"plugins": [,')):
            with self.subTest(case=case):
                code, out = self.check(market, old, new)
                self.assertEqual(code, 1)
                self.assertIn(".claude-plugin/marketplace.json: not valid JSON in UTF-8 without a BOM", out)
        entry = '      "name": "dev-skills",\n      "source": "./",\n'
        for case, new in (("two entries", None), ("source ./other", entry.replace('"./"', '"./other"')),
                          ("source object", entry.replace('"./"', '{"source": "github", "repo": "x/y"}')),
                          ("other name", entry.replace('"dev-skills"', '"other"'))):
            with self.subTest(case=case):
                if new is None:
                    def change(tmp):
                        path = os.path.join(tmp, market)
                        with open(path, encoding="utf-8") as fh:
                            data = json.load(fh)
                        data["plugins"].append(dict(data["plugins"][0]))
                        with open(path, "w", encoding="utf-8") as fh:
                            json.dump(data, fh)
                    code, out = self.check_tree(change)
                else:
                    code, out = self.check(market, entry, new)
                self.assertEqual(code, 1)
                self.assertIn(".claude-plugin/marketplace.json: plugins must be a list of exactly one entry", out)

    SKILL_TEXT = ("---\nname: dev-x\ndescription: x\nallowed-tools:\n  - Read(/${CLAUDE_PLUGIN_ROOT}/skills/**)\n"
                  "  - Read(/${CLAUDE_PLUGIN_ROOT}/vendor/engineering-workflow-core/contracts/**)\n---\n")

    def test_skills_and_agents_outside_the_allowlist_fail(self):  # CB-7, Issue #66 review round 2, card I66-R2-C1 (a)
        def write(rel, text=self.SKILL_TEXT):
            def change(tmp):
                os.makedirs(os.path.dirname(os.path.join(tmp, rel)), exist_ok=True)
                with open(os.path.join(tmp, rel), "w", encoding="utf-8") as fh:
                    fh.write(text)
            return change
        with open(os.path.join(ROOT, "agents", "dev-explorer.md"), encoding="utf-8") as fh:
            explorer = fh.read()
        for rel, change, message in (
                ("skills/.x", write(os.path.join("skills", ".x", "SKILL.md")), "hidden names under skills/ are not allowed"),
                ("skills/SKILL.md", write(os.path.join("skills", "SKILL.md")), "every entry under skills/ must be a skill directory"),
                ("skills/file.txt", write(os.path.join("skills", "file.txt"), "x\n"), "every entry under skills/ must be a skill directory"),
                ("skills/dev-x", write(os.path.join("skills", "dev-x", "skill.md")), "has no regular file named exactly SKILL.md"),
                ("agents/sub", lambda tmp: os.mkdir(os.path.join(tmp, "agents", "sub")), "agents/ may hold only"),
                ("agents/.x.md", write(os.path.join("agents", ".x.md"), explorer), "agents/ may hold only"),
                ("agents/x.MD", write(os.path.join("agents", "x.MD"), explorer), "agents/ may hold only"),
                ("agents/notes.txt", write(os.path.join("agents", "notes.txt"), "x\n"), "agents/ may hold only")):
            with self.subTest(rel=rel):
                code, out = self.check_tree(change)
                self.assertEqual(code, 1)
                self.assertIn(f"  - {rel}: {message}", out)

    def test_case_colliding_names_fail(self):  # CB-7, Issue #66 review round 2, card I66-R2-C1 (a)
        mod = load("check_pack")
        self.assertEqual(mod.casefold_duplicates(["dev-core", "Dev-Core", "SKILL.md", "skill.md", "x"]), ["dev-core", "skill.md"])
        if not self.case_sensitive_fs():
            self.skipTest(self.CASE_SKIP)
        code, out = self.check_tree(lambda tmp: shutil.copy(os.path.join(tmp, "skills", "dev-core", "SKILL.md"),
                                                             os.path.join(tmp, "skills", "dev-core", "skill.md")))
        self.assertEqual(code, 1)
        self.assertIn("skills/dev-core/skill.md: another name in this directory differs only in case", out)

    CASE_SKIP = "a tree with two names that differ only in case can only be made on a case-sensitive file system"

    @staticmethod
    def case_sensitive_fs():
        tmp = tempfile.mkdtemp()  # the file system of the trees that check_tree makes
        try:
            os.mkdir(os.path.join(tmp, "a"))
            return not os.path.exists(os.path.join(tmp, "A"))
        finally:
            shutil.rmtree(tmp)

    def test_agent_names_differing_only_in_case_fail(self):  # CB-7, Issue #66 I66R3-001, I66S3-005
        if not self.case_sensitive_fs():
            self.skipTest(self.CASE_SKIP)
        def change(tmp):
            with open(os.path.join(tmp, "agents", "dev-explorer.md"), encoding="utf-8") as fh:
                text = fh.read()
            for name in ("x", "X"):  # each file name matches its own name key
                with open(os.path.join(tmp, "agents", name + ".md"), "w", encoding="utf-8") as fh:
                    fh.write(text.replace("\nname: dev-explorer\n", f"\nname: {name}\n", 1))
        code, out = self.check_tree(change)
        self.assertEqual(code, 1)
        self.assertIn("  - agents/x.md: another name in this directory differs only in case", out)

    def test_vendor_names_differing_only_in_case_fail(self):  # CB-7, Issue #66 MR67-001
        if not self.case_sensitive_fs():
            self.skipTest(self.CASE_SKIP)
        contracts = os.path.join("vendor", "engineering-workflow-core", "contracts")
        code, out = self.check_tree(lambda tmp: shutil.copy(os.path.join(tmp, contracts, "workflow.md"),
                                                             os.path.join(tmp, contracts, "Workflow.md")))
        self.assertEqual(code, 1)
        self.assertIn(f"  - {contracts}/workflow.md: another name in this directory differs only in case", out)

    def check_edits(self, rel, *pairs, count=1):  # several replacements in one file; the result must give `count` problems
        def change(tmp):
            path = os.path.join(tmp, rel)
            with open(path, encoding="utf-8", newline="") as fh:
                text = fh.read()
            for old, new in pairs:
                self.assertIn(old, text)
                text = text.replace(old, new, 1)
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(text)
        return self.check_tree(change, count=count)

    VALUE_SCOPES = ((os.path.join("skills", "dev-retro", "SKILL.md"), "disable-model-invocation", "true",
                     "\ndisallowed-tools: Write, Edit, MultiEdit, NotebookEdit\n"),
                    (os.path.join("agents", "dev-reviewer.md"), "color", "yellow",
                     "\ndisallowedTools: Edit, Write, NotebookEdit\n"))

    def test_front_matter_value_grammar(self):  # CB-7, Issue #66 card I66-M3 (a): MR67C-001, MR67U-001, MR67U-002, FU-032
        start = "a value must not start with any of "
        forms = [("two spaces", "  x", "exactly one space must follow the colon"),
                 ("empty value", "", "a value must not be empty"),
                 ("space, then empty", " ", "a value must not be empty"),
                 ("inner ': '", " a: b", "a value must not contain ': ' or ' #'"),
                 ("inner ' #'", " a #b", "a value must not contain ': ' or ' #'"),
                 ("trailing ':'", " a:", "a value must not end with ':' or a space"),
                 ("trailing space", " a ", "a value must not end with ':' or a space"),
                 ("'---' inside", " a --- b", "a value must not contain '---'")]
        forms += [(f"first character {ch!r}", " " + ch + "x", start) for ch in "-?:,[]{}#&*!|>'\"%@`"]  # not from check_pack
        for rel, key, value, _ in self.VALUE_SCOPES:
            for case, new, message in forms:
                with self.subTest(rel=rel, case=case):
                    code, out = self.check(rel, f"\n{key}: {value}\n", f"\n{key}:{new}\n")
                    self.assertEqual(code, 1)  # check_tree asserts that this is the only problem
                    self.assertIn(f"  - {rel}: front matter line ", out)
                    self.assertIn(message, out)
        for rel, key, value, later in self.VALUE_SCOPES:  # an unclosed quote that closes on a later key line
            with self.subTest(rel=rel, case="unclosed quote spanning lines"):
                pinned = rel.startswith("agents")  # `later` is the pinned disallowedTools line (Issue #69)
                code, out = self.check_edits(rel, (f"\n{key}: {value}\n", f'\n{key}: "{value}\n'),
                                             (later, later[:-1] + '"\n'), count=2 if pinned else 1)
                self.assertEqual(code, 1)
                if pinned:
                    self.assertIn(f"  - {rel}: read-only agent must have the line 'disallowedTools: ", out)
                self.assertIn(f"  - {rel}: front matter line ", out)
                self.assertIn(start, out)

    def test_front_matter_value_bypasses_from_review(self):  # CB-7, Issue #66 card I66-M3 (a): the reviewers' inputs
        start = "a value must not start with any of "
        agent = os.path.join("agents", "dev-reviewer.md")
        skill = os.path.join("skills", "dev-retro", "SKILL.md")
        tools = "\ntools: Read, Grep, Glob, Bash\n"
        color = "\ncolor: yellow\n"
        for case, rel, pairs, message in (
                ("MR67C-001 two spaces hide \\x45dit", agent,
                 [(tools, '\ntools:  "Read, Grep, Glob, Bash, \\x45dit"\n')], "exactly one space must follow the colon"),
                ("MR67U-001 tag before a quote that closes on a later key line", agent,
                 [("\ndescription: ", '\ndescription: !!str "'), (color, '\ncolor: yellow"\n')], start),
                ("MR67U-001 anchor before a quote that closes on a later key line", agent,
                 [("\ndescription: ", '\ndescription: &d "'), (color, '\ncolor: yellow"\n')], start),
                ("MR67U-002 tag hides Edit", agent, [(tools, "\ntools: !!str Edit, Read, Grep, Glob, Bash\n")], start),
                ("MR67U-002 anchor and alias hide Edit", agent,
                 [(tools, "\ntools: [Read, Grep, Glob, Bash, *e]\n"), (color, "\ncolor: &e Edit\n")], start),
                ("MR67C-001 skill quote after two spaces closes on disallowed-tools", skill,
                 [("\ndescription: Lessons", '\ndescription:  "Lessons'),
                  ("NotebookEdit\n", 'NotebookEdit"\n')], "exactly one space must follow the colon")):
            with self.subTest(case=case):
                pinned = any(old == tools for old, _ in pairs)  # the pinned tools line also fails (Issue #69)
                code, out = self.check_edits(rel, *pairs, count=2 if pinned else 1)
                self.assertEqual(code, 1)  # check_tree asserts that these are the only problems
                self.assertIn(f"  - {rel}: front matter line ", out)
                self.assertIn(message, out)
                if pinned:
                    self.assertIn(f"  - {rel}: read-only agent must have the line 'tools: ", out)

    def test_manifest_key_outside_the_allowlist_fails(self):  # CB-7, Issue #66 review round 1 (main agent addition, now part of card I66-R2-C1 (a))
        plugin = os.path.join(".claude-plugin", "plugin.json")
        market = os.path.join(".claude-plugin", "marketplace.json")
        for manifest, old, key, part in (
                (plugin, '  "name": "dev-skills",\n', "agents", "top level"),
                (plugin, '  "name": "dev-skills",\n', "hooks", "top level"),
                (market, '  "name": "dev-skills",\n  "owner"', "agents", "top level"),
                (market, '  "name": "dev-skills",\n  "owner"', "hooks", "top level"),
                (market, '      "name": "dev-skills",\n', "mcpServers", "plugins[] entry"),
                (market, '      "name": "dev-skills",\n', "agents", "plugins[] entry")):
            with self.subTest(manifest=manifest, key=key, part=part):
                head = old.split("\n")[0] + "\n"
                code, out = self.check(manifest, old, head + f'  "{key}": {{}},\n' + old[len(head):])
                self.assertEqual(code, 1)
                self.assertIn(f"{manifest}: {part} keys ['{key}'] are not in the allowlist", out)

    def test_crlf_front_matter_fails(self):  # CB-7, Issue #66 I66R1-001
        def change(tmp):
            path = os.path.join(tmp, "skills", "dev-core", "SKILL.md")
            with open(path, encoding="utf-8", newline="") as fh:
                text = fh.read()
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(text.replace("\n", "\r\n"))
        code, out = self.check_tree(change, os.path.join("skills", "dev-core", "SKILL.md"))
        self.assertEqual(code, 1)
        self.assertIn("skills/dev-core/SKILL.md: front matter must open and close with a line that is exactly '---'", out)

    def test_symlink_under_skills_or_vendor_fails(self):  # CB-7, Issue #66 card A1, I66S1-005
        for rel, target in ((os.path.join("skills", "dev-core", "link.txt"), "outside"),
                            (os.path.join("vendor", "engineering-workflow-core", "contracts", "linkdir"), "outside"),
                            (os.path.join("skills", "dev-core", "file-link.md"), "outside.md"),
                            (os.path.join("vendor", "engineering-workflow-core", "contracts", "broken.md"), "missing"),
                            (os.path.join("skills", "dev-core", "broken.md"), "missing")):
            with self.subTest(rel=rel, target=target):
                def change(tmp):
                    outside = os.path.join(tmp, "docs", target)  # docs/ is in the root allowlist and not walked
                    if target == "outside":
                        os.mkdir(outside)
                    elif target == "outside.md":
                        with open(outside, "w", encoding="utf-8") as fh:
                            fh.write("outside\n")
                    os.symlink(outside, os.path.join(tmp, rel))
                code, out = self.check_tree(change)
                self.assertEqual(code, 1)
                self.assertIn(f"{rel}: symlink under {rel.split(os.sep)[0]}/ is not allowed", out)

    def test_hardlink_under_skills_or_vendor_fails(self):  # CB-7, Issue #66 I66S1-005
        for rel in (os.path.join("skills", "dev-core", "hard.md"),
                    os.path.join("vendor", "engineering-workflow-core", "contracts", "hard.md")):
            with self.subTest(rel=rel):
                def change(tmp):
                    outside = os.path.join(tmp, "docs", "outside.md")  # docs/ is in the root allowlist and not walked
                    with open(outside, "w", encoding="utf-8") as fh:
                        fh.write("outside\n")
                    os.link(outside, os.path.join(tmp, rel))
                code, out = self.check_tree(change)
                self.assertEqual(code, 1)
                self.assertIn(f"{rel}: hardlinked file under {rel.split(os.sep)[0]}/ is not allowed", out)

    def test_symlinked_skill_entries_fail(self):  # CB-7, Issue #66 I66R3-001, I66S3-005
        def outside_skill(tmp):  # a directory with a valid SKILL.md; docs/ is in the root allowlist and not walked
            outside = os.path.join(tmp, "docs", "dev-x")
            os.mkdir(outside)
            with open(os.path.join(outside, "SKILL.md"), "w", encoding="utf-8") as fh:
                fh.write(self.SKILL_TEXT)
            return outside
        code, out = self.check_tree(lambda tmp: os.symlink(outside_skill(tmp), os.path.join(tmp, "skills", "dev-x")),
                                    os.path.join("skills", "dev-x"))
        self.assertEqual(code, 1)  # two independent checks fire
        self.assertIn("  - skills/dev-x: every entry under skills/ must be a skill directory, not a file or symlink", out)
        self.assertIn("  - skills/dev-x: symlink under skills/ is not allowed", out)

        def link_skill_md(tmp):
            os.mkdir(os.path.join(tmp, "skills", "dev-x"))
            os.symlink(os.path.join(outside_skill(tmp), "SKILL.md"), os.path.join(tmp, "skills", "dev-x", "SKILL.md"))
        code, out = self.check_tree(link_skill_md, count=2)
        self.assertEqual(code, 1)  # two independent checks fire
        self.assertIn("  - skills/dev-x: has no regular file named exactly SKILL.md", out)
        self.assertIn("  - skills/dev-x/SKILL.md: symlink under skills/ is not allowed", out)

        code, out = self.check_tree(lambda tmp: os.makedirs(os.path.join(tmp, "skills", "dev-x", "SKILL.md")))
        self.assertEqual(code, 1)
        self.assertIn("  - skills/dev-x: has no regular file named exactly SKILL.md", out)

    def test_agent_and_top_level_symlinks_fail(self):  # CB-7, Issue #66 I66R3-001, I66S3-001, I66S3-005
        def link_agent(tmp):
            outside = os.path.join(tmp, "docs", "dev-x.md")  # docs/ is in the root allowlist and not walked
            shutil.copy(os.path.join(tmp, "agents", "dev-explorer.md"), outside)
            os.symlink(outside, os.path.join(tmp, "agents", "dev-x.md"))
        code, out = self.check_tree(link_agent)
        self.assertEqual(code, 1)
        self.assertIn("  - agents/dev-x.md: agents/ may hold only non-hidden regular files named *.md", out)
        for top in ("skills", "agents", "vendor"):
            with self.subTest(top=top):
                def change(tmp):
                    os.rename(os.path.join(tmp, top), os.path.join(tmp, "docs", top))
                    os.symlink(os.path.join(tmp, "docs", top), os.path.join(tmp, top))
                code, out = self.check_tree(change)
                self.assertEqual(code, 1)
                self.assertIn(f"  - {top}: symlink is not allowed", out)

    def test_non_utf8_file_fails(self):  # CB-7, Issue #66 I66S3-004
        for rel in (os.path.join("skills", "dev-core", "SKILL.md"), os.path.join("agents", "dev-reviewer.md"),
                    os.path.join("skills", "dev-core", "deltas.md")):
            with self.subTest(rel=rel):
                def change(tmp):
                    with open(os.path.join(tmp, rel), "ab") as fh:
                        fh.write(b"\xff\n")
                code, out = self.check_tree(change)
                self.assertEqual(code, 1)
                self.assertIn(f"  - {rel}: not valid UTF-8 (CB-7)", out)

    def test_markdown_path_that_is_not_a_readable_file_fails(self):  # CB-7, Issue #66 MR67S-002
        def directory(tmp):
            os.makedirs(os.path.join(tmp, "skills", "dev-core", "x.md"))
            with open(os.path.join(tmp, "skills", "dev-core", "x.md", "inner.txt"), "w", encoding="utf-8") as fh:
                fh.write("x\n")
        code, out = self.check_tree(directory)
        self.assertEqual(code, 1)
        self.assertIn("  - skills/dev-core/x.md: not a regular file (CB-7)", out)
        if os.geteuid() == 0:
            self.skipTest("root reads a file without read permission")
        for rel in ("skills/dev-core/deltas.md", "skills/dev-core/SKILL.md", "agents/dev-reviewer.md"):  # MR67B-001
            with self.subTest(rel=rel):
                code, out = self.check_tree(lambda tmp: os.chmod(os.path.join(tmp, rel), 0),
                                            restore=lambda tmp: os.chmod(os.path.join(tmp, rel), 0o644))
                self.assertEqual(code, 1)  # check_tree asserts that this is the only problem
                self.assertIn(f"  - {rel}: cannot be read: Permission denied (CB-7)", out)

    def test_missing_or_non_utf8_manifest_fails(self):  # CB-7, Issue #66 MR67S-005
        plugin = os.path.join(".claude-plugin", "plugin.json")
        code, out = self.check_tree(lambda tmp: os.remove(os.path.join(tmp, plugin)))
        self.assertEqual(code, 1)
        self.assertIn("  - .claude-plugin/plugin.json: missing (CB-7)", out)
        for name in ("plugin.json", "marketplace.json"):
            with self.subTest(name=name):
                def change(tmp):
                    with open(os.path.join(tmp, ".claude-plugin", name), "ab") as fh:
                        fh.write(b"\xff\n")
                code, out = self.check_tree(change)
                self.assertEqual(code, 1)
                self.assertIn(f"  - .claude-plugin/{name}: not valid JSON in UTF-8 without a BOM", out)

    def test_deeply_nested_manifest_fails(self):  # CB-7, Issue #66 I66S3-004
        def change(tmp):
            with open(os.path.join(tmp, ".claude-plugin", "plugin.json"), "w", encoding="utf-8") as fh:
                fh.write("[" * 100000 + "]" * 100000)
        code, out = self.check_tree(change)
        self.assertEqual(code, 1)
        self.assertIn(".claude-plugin/plugin.json: not valid JSON in UTF-8 without a BOM", out)


class RoutingNamesRoles(unittest.TestCase):
    """The family-name lint and the routing table check of check_pack (Issue #96 PR-3, design d1 section 3): one
    counterexample for each rule and each exception, on small trees in a temporary directory. Each tree passes before
    its one change, so that the change alone gives the problem."""

    DELIVER = os.path.join("skills", "dev-deliver", "SKILL.md")
    REVIEW = os.path.join("skills", "dev-review", "SKILL.md")
    DELIVER_TABLE = (
        "   | Node | Agent | Role |\n"
        "   | --- | --- | --- |\n"
        "   | explore | `dev-explorer` | role `explore`; role `explore-synthesis` for synthesis |\n"
        "   | implement, docs | `dev-implementer` | `light`: role `implement-reduced`; `strict`: role `implement` |\n"
        "   | review (routine) | `dev-reviewer` | role `review-routine`; `light`: role `review-routine-light` |\n"
        "   | review (deep) | `dev-reviewer` | role `review-deep` |\n"
        "   | review (security) | `dev-security-reviewer` | role `review-security`; a higher effort only when the user"
        " asks |\n"
        "   | commit / push scan | `dev-security-reviewer` | role `scan` |\n")
    REVIEW_TABLE = (
        "| Mode | When | Reviewer |\n"
        "| --- | --- | --- |\n"
        "| routine | low or medium risk | `dev-reviewer`, role `review-routine`; at the `light` tier, role "
        "`review-routine-light` |\n"
        "| security | trust boundaries (R-REV-7) | `dev-security-reviewer`, role `review-security` |\n")

    def setUp(self):
        self.mod = load("check_pack")
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp)
        self.mod.ROOT = self.tmp
        self.roles = self.mod.PINNED_ROLE_VALUES
        self.reset()
        self.write(os.path.join("agents", "dev-x.md"), "---\nname: dev-x\nmodel: opus\neffort: high\n---\nBody.\n")
        self.assertEqual(self.mod.family_name_problems(), [])
        self.assertEqual(self.mod.routing_table_problems(self.roles), [])

    def reset(self):
        """The two passing tables."""
        self.write(self.DELIVER, "# dev-deliver\n\n" + self.DELIVER_TABLE + "\nText after the table.\n")
        self.write(self.REVIEW, "# dev-review\n\n" + self.REVIEW_TABLE + "\nText after the table.\n")

    def write(self, rel, text):
        path = os.path.join(self.tmp, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(text)

    def edit(self, rel, old, new):
        with open(os.path.join(self.tmp, rel), encoding="utf-8", newline="") as fh:
            text = fh.read()
        self.assertEqual(text.count(old), 1, old)
        self.write(rel, text.replace(old, new))

    def lint(self):
        return self.mod.family_name_problems()

    def tables(self):
        return self.mod.routing_table_problems(self.roles)

    # the family-name lint

    def test_each_family_in_any_case_and_as_part_of_an_id(self):
        for line in ("model opus", "`sonnet`/`medium`", "Haiku", "FABLE 5.1", "claude-opus-5-5", "x.opus.y",
                     "(opus)", "opus/high"):
            with self.subTest(line=line):
                self.write(os.path.join("skills", "dev-x", "SKILL.md"), f"# x\n\n{line}\n")
                problems = self.lint()
                self.assertEqual(len(problems), 1, problems)
                self.assertTrue(problems[0].startswith("skills/dev-x/SKILL.md:3: names the model family "), problems)
                self.assertIn("(family-name lint, Issue #96 PR-3)", problems[0])

    def test_a_longer_word_is_not_a_family(self):  # a whole word: no ASCII letter or digit before or after it
        self.write(os.path.join("skills", "dev-x", "SKILL.md"), "opus4 opuses magnumopus sonnets haikus 5fable\n")
        self.assertEqual(self.lint(), [])

    def test_scope(self):
        for rel in (os.path.join("skills", "dev-x", "references", "deep", "notes.md"),
                    os.path.join("skills", "dev-core", "references", "other.md"), os.path.join("agents", "dev-y.md")):
            with self.subTest(rel=rel):
                self.write(rel, "uses opus\n")
                self.assertEqual([p.split(":")[0] for p in self.lint()], [rel])
                os.remove(os.path.join(self.tmp, rel))
        for rel in ("README.md", os.path.join("docs", "notes.md"), os.path.join(".dev", "plan.md"),
                    os.path.join("skills", "dev-x", "notes.txt"), os.path.join("agents", "sub", "dev-z.md")):
            with self.subTest(rel=rel):  # outside the scope of the lint
                self.write(rel, "uses opus\n")
                self.assertEqual(self.lint(), [])

    def test_the_two_exempt_files(self):
        for rel in self.mod.FAMILY_LINT_EXCEPTIONS:
            self.write(rel, "opus/high, sonnet/medium\n")
        self.assertEqual(self.lint(), [])
        self.assertEqual(self.mod.FAMILY_LINT_EXCEPTIONS, (os.path.join("skills", "dev-core", "deltas.md"), os.path.join(
            "skills", "dev-core", "references", "model-effort-readback.md")))
        for rel in (os.path.join("skills", "dev-review", "deltas.md"),  # the same name in another place counts
                    os.path.join("skills", "dev-core", "model-effort-readback.md")):
            with self.subTest(rel=rel):
                self.write(rel, "opus/high\n")
                self.assertEqual([p.split(":")[0] for p in self.lint()], [rel])
                os.remove(os.path.join(self.tmp, rel))

    def test_only_the_model_line_of_an_agent_front_matter(self):
        agent = os.path.join("agents", "dev-x.md")
        for old, new, line in (("Body.\n", "Body.\nmodel: opus\n", 7),  # after the front matter
                               ("name: dev-x\n", "name: dev-x\ndescription: an opus agent\n", 3),
                               ("effort: high\n", "effort: high\nmodels: opus\n", 5)):
            with self.subTest(new=new):
                self.edit(agent, old, new)
                self.assertEqual([p.split(": names")[0] for p in self.lint()], [f"{agent}:{line}"])
                self.edit(agent, new, old)
        skill = os.path.join("skills", "dev-x", "SKILL.md")  # a skill front matter has no exempt model: line
        self.write(skill, "---\nname: dev-x\nmodel: opus\n---\n")
        self.assertEqual([p.split(": names")[0] for p in self.lint()], [f"{skill}:3"])

    def test_the_shipped_agent_files_name_families_only_on_the_model_line(self):
        self.mod.ROOT = ROOT
        self.assertEqual([p for p in self.lint() if p.startswith("agents/")], [])

    # the routing table check

    def test_each_table_exactly_once(self):
        for rel, table in ((self.DELIVER, self.DELIVER_TABLE), (self.REVIEW, self.REVIEW_TABLE)):
            header = table.split("\n")[0]
            with self.subTest(rel=rel, case="missing"):
                self.edit(rel, header, header.replace("| Role |", "| Model / effort |").replace(
                    "| Reviewer |", "| Model |"))
                self.assertIn(f"{rel}: the table {header.strip()!r} must appear exactly once, found 0 (Issue #96 PR-3)",
                              self.tables())
                self.write(rel, "# x\n\n" + table)
            with self.subTest(rel=rel, case="twice"):
                self.write(rel, "# x\n\n" + table + "\n" + table)
                self.assertIn(f"{rel}: the table {header.strip()!r} must appear exactly once, found 2 (Issue #96 PR-3)",
                              self.tables())
                self.write(rel, "# x\n\n" + table)
            with self.subTest(rel=rel, case="no file"):
                os.remove(os.path.join(self.tmp, rel))
                self.assertIn(f"{rel}: the table {header.strip()!r} is needed, but the file is missing or not readable "
                              f"(Issue #96 PR-3)", self.tables())
                self.write(rel, "# x\n\n" + table)
        self.assertEqual(self.tables(), [])

    def test_a_row_without_a_role(self):
        self.edit(self.DELIVER, "| role `review-deep` |", "| the deep reviewer |")
        self.assertEqual([p.split(": ", 1)[1] for p in self.tables()], [
            "a row of the table '| Node | Agent | Role |' names no role in its third column (Issue #96 PR-3)",
            "the role 'review-deep' of skills/dev-core/model-config.json is named in no row of the table "
            "'| Node | Agent | Role |' (Issue #96 PR-3)"])

    def test_a_name_that_is_not_a_role(self):
        for rel, old in ((self.DELIVER, "role `review-deep` |"), (self.REVIEW, "role `review-security` |")):
            with self.subTest(rel=rel):
                self.edit(rel, old, old[:-2] + ", role `review-extra` |")
                self.assertEqual([p.split(": ", 1)[1] for p in self.tables()], [
                    f"a row of the table {self.header(rel)!r} names 'review-extra', which is not a role of "
                    "skills/dev-core/model-config.json (Issue #96 PR-3)"])
                self.edit(rel, old[:-2] + ", role `review-extra` |", old)

    def header(self, rel):
        return "| Node | Agent | Role |" if rel == self.DELIVER else "| Mode | When | Reviewer |"

    def test_an_effort_value_in_the_role_column(self):
        for effort in ("low", "medium", "high", "xhigh", "max", "High"):
            for rel, old in ((self.DELIVER, "role `review-deep` |"), (self.REVIEW, "role `review-security` |")):
                with self.subTest(effort=effort, rel=rel):
                    new = old[:-2] + f" at {effort} |"
                    self.edit(rel, old, new)
                    self.assertEqual([p.split(": ", 1)[1] for p in self.tables()], [
                        f"a row of the table {self.header(rel)!r} names the effort {effort} in its third column; the "
                        "table names roles, not values (Issue #96 PR-3)"])
                    self.edit(rel, new, old)
        self.edit(self.REVIEW, "| routine | low or medium risk |", "| routine | low, medium or high risk |")
        self.assertEqual(self.tables(), [])  # only the third column is checked

    def test_the_agent_of_a_role_is_the_agent_of_the_row(self):
        for rel, old, new, agent in (
                (self.DELIVER, "| role `review-deep` |", "| role `scan` |", "dev-reviewer"),
                (self.DELIVER, "| `dev-reviewer` | role `review-deep` |", "| `dev-implementer` | role `review-deep` |",
                 "dev-implementer"),
                (self.REVIEW, "`dev-security-reviewer`, role `review-security`", "`dev-reviewer`, role `review-security`",
                 "dev-reviewer")):
            with self.subTest(rel=rel, new=new):
                self.edit(rel, old, new)
                role = re.findall(r"role `([^`]*)`", new)[0]
                problems = [p.split(": ", 1)[1] for p in self.tables()]
                self.assertIn(f"a row of the table {self.header(rel)!r} names the role {role!r}, whose agent in "
                              f"skills/dev-core/model-config.json is {self.roles[role]['agent']!r}, not the agent "
                              f"{agent!r} of the row (Issue #96 PR-3)", problems)
                self.reset()
        self.edit(self.DELIVER, "| explore | `dev-explorer` | role `explore`;",
                  "| explore | `dev-explorer` | role `explore`; role `orchestration`;")
        self.assertEqual([p.split(": ", 1)[1] for p in self.tables()], [
            "a row of the table '| Node | Agent | Role |' names the role 'orchestration', whose agent in "
            "skills/dev-core/model-config.json is None, not the agent 'dev-explorer' of the row (Issue #96 PR-3)"])

    def test_every_role_but_orchestration_is_in_the_first_table(self):
        self.assertNotIn("`orchestration`", self.DELIVER_TABLE)  # the passing tree of setUp has no orchestration row
        for role in sorted(set(self.roles) - {"orchestration"}):
            with self.subTest(role=role):  # the name in the row becomes a name of the text, not a role
                self.write(self.DELIVER, "# x\n\n" + self.DELIVER_TABLE.replace(f"role `{role}`", f"the {role} node"))
                missing = [p for p in self.tables() if "is named in no row" in p]
                self.assertEqual(missing, [
                    f"skills/dev-deliver/SKILL.md: the role {role!r} of skills/dev-core/model-config.json is named in "
                    "no row of the table '| Node | Agent | Role |' (Issue #96 PR-3)"])
        self.reset()
        self.edit(self.REVIEW, "role `review-security` |", "role `review-security`, role `scan` |")
        self.edit(self.DELIVER, "   | commit / push scan | `dev-security-reviewer` | role `scan` |\n", "")
        self.assertEqual([p.split(": ", 1)[1] for p in self.tables()], [  # the second table does not count
            "the role 'scan' of skills/dev-core/model-config.json is named in no row of the table "
            "'| Node | Agent | Role |' (Issue #96 PR-3)"])

    def test_the_form_of_the_table(self):
        self.edit(self.DELIVER, "   | --- | --- | --- |\n", "")
        self.assertIn("skills/dev-deliver/SKILL.md: the table '| Node | Agent | Role |' needs the line "
                      "'| --- | --- | --- |' right after its header (Issue #96 PR-3)", self.tables())
        self.write(self.DELIVER, "# x\n\n" + self.DELIVER_TABLE)
        self.edit(self.REVIEW, "| security | trust boundaries (R-REV-7) |", "| security | trust | boundaries |")
        self.assertEqual([p.split(": ", 1)[1] for p in self.tables()], [
            "a row of the table '| Mode | When | Reviewer |' must have 3 columns, found 4 (Issue #96 PR-3)"])
        self.write(self.REVIEW, "# x\n\n" + self.REVIEW_TABLE.split("| routine")[0] + "\ntext\n")
        self.assertEqual(self.tables(), [
            "skills/dev-review/SKILL.md: the table '| Mode | When | Reviewer |' has no row (Issue #96 PR-3)"])

    def test_main_runs_both_checks(self):  # the shipped tree with one more problem of each check
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp)
        for sub in ("skills", "agents", "vendor", os.path.join("docs", "requirements"), ".claude-plugin"):
            shutil.copytree(os.path.join(ROOT, sub), os.path.join(tmp, sub))
        with open(os.path.join(tmp, "skills", "dev-docs", "SKILL.md"), "a", encoding="utf-8") as fh:
            fh.write("\nAn added line that names sonnet.\n")
        review = os.path.join(tmp, self.REVIEW)
        with open(review, encoding="utf-8") as fh:
            text = fh.read()
        with open(review, "w", encoding="utf-8") as fh:
            fh.write(text.replace("| Mode | When | Reviewer |", "| Mode | When | Model |"))
        self.mod.ROOT = tmp
        code, out = run(self.mod)
        self.assertEqual(code, 1)
        self.assertRegex(out, r"\n  - skills/dev-docs/SKILL.md:[0-9]+: names the model family sonnet; ")
        self.assertIn("\n  - skills/dev-review/SKILL.md: the table '| Mode | When | Reviewer |' must appear exactly "
                      "once, found 0 (Issue #96 PR-3)", out)


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
