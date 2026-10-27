"""Negative tests for scripts/check_core_coverage.py and scripts/verify_core.py."""

import contextlib
import glob
import importlib.util
import io
import json
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

    def check(self, rel, old, new, same_file=False):
        def edit(tmp):
            path = os.path.join(tmp, rel)
            with open(path, encoding="utf-8", newline="") as fh:
                text = fh.read()
            self.assertIn(old, text)
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(text.replace(old, new, 1))
        return self.check_tree(edit, rel if same_file else None)

    def check_tree(self, change, same_file=None, count=1, restore=None):
        mod = load("check_pack")
        tmp = tempfile.mkdtemp()
        try:
            for sub in ("skills", "agents", "vendor", os.path.join("docs", "requirements"), ".claude-plugin"):
                shutil.copytree(os.path.join(ROOT, sub), os.path.join(tmp, sub))
            change(tmp)
            mod.ROOT = tmp
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
