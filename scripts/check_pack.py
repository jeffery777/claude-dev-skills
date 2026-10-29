#!/usr/bin/env python3
"""Structural checks for the skill pack (stdlib only).

- closed world (CB-7): the plugin root holds only the names in ROOT_NAMES (exact case);
  .claude-plugin/ holds exactly plugin.json and marketplace.json, both valid JSON; skills/
  holds only non-hidden real directories, each with a regular file named exactly SKILL.md;
  agents/ holds only non-hidden regular files named *.md; no two names in one directory under
  skills/, agents/ or vendor/ differ only in case. Hidden names count (os.listdir). Every
  SKILL.md, agent file and *.md file under a skill directory is a readable regular file in
  valid UTF-8 (a directory named *.md fails), and a manifest that does not parse (deep
  nesting included) is an error, not a traceback;
- every skills/<dir>/SKILL.md has name == <dir> and a description of at most 1,024 characters;
- every skills/<dir>/SKILL.md has allowed-tools as a list of exactly the two pack Read rules
  in SKILL_ALLOWED_TOOLS: no bare tool, no other rule or tool, no string form (CB-7);
- the raw front matter text of every skills/<dir>/SKILL.md is printable ASCII with LF line
  ends, and each line is a column-0 `key: value` line with a key from SKILL_KEYS, used once,
  or one of the two allowed-tools item lines right after `allowed-tools:`; every other value
  follows the closed value grammar: one space after the colon, then a non-empty YAML plain
  scalar that does not start with a space or a character of PLAIN_START_BANNED, holds no
  `: `, ` #` or `---`, and does not end with `:` or a space, so no quote, tag, anchor, alias,
  flow or block value (CB-7). The parsed check above uses a permissive subset parser; this
  raw check is the guard;
- the raw front matter text of every agents/*.md follows the same text rules, with a key
  from AGENT_KEYS, used once (CB-7);
- the keys of .claude-plugin/plugin.json, of .claude-plugin/marketplace.json and of its
  plugins[] entry stay inside the allowlists in MANIFEST_KEYS, so no manifest key points at
  other component paths, and marketplace.json has exactly one plugins[] entry, with name
  dev-skills and source ./ (CB-7);
- skills/, agents/ and vendor/ are not symlinks; no symlink and no hardlinked regular file
  under skills/ or vendor/ (CB-7);
- every agents/*.md has name == file stem, a description, a model alias and an effort level;
- every read-only or pinned agent file (stem in REQUIRED_AGENTS) is at most AGENT_MAX_BYTES bytes, this
  repository's own lower limit; Claude Code skips an agent file over 1,048,576 bytes (inferred
  from reading the Claude Code 2.1.310 code, not run; Issue #69 R69S1-002);
- the read-only and pinned agents in REQUIRED_AGENTS exist as regular files named in exact case, no other
  agent file stem equals one of their names after agent_key normalization (NFKC, casefold, no
  whitespace, `_` or Pd dash; inferred from reading the Claude Code 2.1.310 code, not run: when
  no agent has the exact dispatch name and exactly one agent matches after normalization, Claude
  Code dispatches that agent; Issue #69 R69S1-002),
  and the raw `tools` and `disallowedTools` values of each equal the pinned strings exactly
  (absent where pinned to None), so no other spelling (a space-separated write tool, `*`, a
  specifier) and no removed `disallowedTools` passes, whatever split rule Claude Code uses
  (Issue #69, MR67V-001). They keep Bash; read-only Bash use is enforced by instructions, not
  by this check (CB-5);
- the raw `model` and `effort` values of each agent in PINNED_AGENT_SETTINGS equal the pinned
  values exactly, so a lower and a higher value both fail (R-DEL-2, Issue #77). This checks the
  file text only; whether the host applies the values rests on the controlled test that REQ-009
  records;
- every ${CLAUDE_SKILL_DIR}/... path named in a skill exists;
- every REQ file in docs/requirements/ has closed front matter, an id matching its
  name, a valid status, typed relations as REQ-id lists, and sources entries with
  type, locator and quote; relations resolve and depends_on is acyclic.

This is a schema check of this repository's own files. The semantic requirements
lint (contradictions, orphans, stale requirements) is Phase 2 (D-008).
"""

from __future__ import annotations

import glob
import importlib.util
import json
import os
import re
import stat
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = {"haiku", "sonnet", "opus", "fable", "inherit"}
EFFORTS = {"low", "medium", "high", "xhigh", "max"}
READ_ONLY_AGENTS = {  # CB-5, DL-009: stem -> the exact raw tools and disallowedTools values (None: no such line);
    # a change needs a change of check_pack.py with review (Issue #69)
    "dev-explorer": {"tools": "Read, Grep, Glob, Bash", "disallowedTools": None},
    "dev-reviewer": {"tools": "Read, Grep, Glob, Bash", "disallowedTools": "Edit, Write, NotebookEdit"},
    "dev-security-reviewer": {"tools": "Read, Grep, Glob, Bash", "disallowedTools": "Edit, Write, NotebookEdit"},
}
PINNED_AGENT_SETTINGS = {  # R-DEL-2, Issue #77: stem -> the exact raw model and effort values; they protect a dispatch
    # that leaves out a value. A change needs a change of check_pack.py with review
    "dev-implementer": {"model": "opus", "effort": "high"},
    "dev-reviewer": {"model": "opus", "effort": "high"},
    "dev-security-reviewer": {"model": "opus", "effort": "xhigh"},
}
REQUIRED_AGENTS = sorted(set(READ_ONLY_AGENTS) | set(PINNED_AGENT_SETTINGS))
AGENT_MAX_BYTES = 65536  # Issue #69 R69S1-002: this repository's own lower limit for a read-only or pinned agent file (ours
# are < 10 KB); Claude Code skips an agent file over 1,048,576 bytes (inferred from reading the 2.1.310 code, not run)
SOURCE_TYPES = {"doc", "chat", "issue", "commit", "external"}
SKILL_ALLOWED_TOOLS = [  # CB-7: the only grant a skill declares; never widen it
    "Read(/${CLAUDE_PLUGIN_ROOT}/skills/**)",
    "Read(/${CLAUDE_PLUGIN_ROOT}/vendor/engineering-workflow-core/contracts/**)",
]
SKILL_KEYS = {"name", "description", "allowed-tools", "disable-model-invocation", "disallowed-tools"}
# AGENT_KEYS is part of the read-only guarantee (CB-5): a key such as `memory` can add tools to an agent (inferred
# from reading the Claude Code 2.1.310 code, not run), so adding a key needs a CB-5 review
AGENT_KEYS = {"name", "description", "model", "effort", "tools", "disallowedTools", "color"}  # the keys in use
PLAIN_START_BANNED = "-?:,[]{}#&*!|>'\"%@`"  # CB-7: YAML indicators; a value never starts with one (card I66-M3 (a))
ROOT_NAMES = {  # CB-7 closed world: the tracked root names, and .git and .claude (not plugin components;
    # .claude holds local session worktrees in this repository)
    ".claude-plugin", ".dev", ".github", ".gitignore", "CHANGELOG.md", "LICENSE", "README.md",
    "agents", "docs", "scripts", "skills", "tests", "vendor", ".git", ".claude"}
CLOSED_WORLD_HINT = ("a new plugin component needs a change of check_pack.py with review; a local file such as "
                     ".DS_Store must be removed (CB-7)")
MANIFEST_NAMES = ("plugin.json", "marketplace.json")  # the only files in .claude-plugin/
MANIFEST_KEYS = {  # the keys in use; (manifest, part) -> allowed keys
    (".claude-plugin/plugin.json", "top level"): {
        "name", "displayName", "version", "description", "author", "homepage", "repository", "license", "keywords"},
    (".claude-plugin/marketplace.json", "top level"): {"name", "owner", "description", "plugins"},
    (".claude-plugin/marketplace.json", "plugins[] entry"): {"name", "source", "description", "version"},
}

_spec = importlib.util.spec_from_file_location("graph", os.path.join(ROOT, "skills", "dev-plan", "scripts", "graph.py"))
graph = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(graph)
REQ_ID = graph.REQ_RE


front_block = graph.frontmatter_lines


def raw_values(path: str) -> dict[str, str]:
    """The raw text after `key: ` of the first column-0 line of each key in the front matter (Issue #69).

    No YAML parsing: the pinned READ_ONLY_AGENTS and PINNED_AGENT_SETTINGS values are compared with this text, so the
    check does not depend on how Claude Code splits a tools list. raw_front_matter_problem
    reports duplicate keys and other line forms.
    """
    with open(path, encoding="utf-8", newline="") as fh:
        lines = fh.read().split("\n")
    end = lines.index("---", 1) if lines[0] == "---" and "---" in lines[1:] else 0
    values: dict[str, str] = {}
    for line in lines[1:end]:
        m = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):(?: (.*))?", line)
        if m:
            values.setdefault(m.group(1), m.group(2) or "")
    return values


def agent_key(stem: str) -> str:
    """The file stem after the normalization of Claude Code's fallback agent match (Issue #69 R69S1-002).

    Inferred from reading the Claude Code 2.1.310 code, not run: the fallback applies only when no
    agent has the exact dispatch name and exactly one agent matches after normalization. Claude
    Code normalizes the agent type `<plugin>:<name>` with the front matter `name` (NFKC,
    toLowerCase, drops White_Space, Pd and `_`); within this plugin the prefix is the same. This
    key on the file stem is equivalent here only because check_pack requires name == stem and
    printable ASCII front matter; on ASCII, isspace also drops 0x1c-0x1f, so it may report more
    matches, never fewer.
    """
    return "".join(c for c in unicodedata.normalize("NFKC", stem).casefold()
                   if not c.isspace() and c != "_" and unicodedata.category(c) != "Pd")


def casefold_duplicates(names: list[str]) -> list[str]:
    """The names that equal an earlier name in `names` after casefold (CB-7)."""
    seen: dict[str, str] = {}
    return [name for name in sorted(names) if seen.setdefault(name.casefold(), name) != name]


def utf8_problem(path: str) -> str | None:
    """Why `path` is not a readable regular file in UTF-8, or None, so a later read gives no traceback (CB-7)."""
    if not os.path.isfile(path):  # a directory or FIFO named *.md; checked first, so open() neither fails nor blocks
        return "not a regular file"
    try:
        with open(path, encoding="utf-8") as fh:
            fh.read()
    except UnicodeDecodeError:
        return "not valid UTF-8"
    except OSError as exc:
        return f"cannot be read: {exc.strerror or exc}"
    return None


def raw_front_matter_problem(path: str, keys: set[str]) -> str | None:
    """The first problem in the raw front matter text of a SKILL.md or agent file, or None (CB-7).

    Each line must be a column-0 `key: value` line with a key from `keys`, used once. When
    `keys` has allowed-tools (skills), that line must exist, be exactly `allowed-tools:` and
    be followed by the two SKILL_ALLOWED_TOOLS item lines. Every other value follows the
    closed value grammar of the module docstring. Reads with newline="" and splits
    on "\n" only, so CR, U+0085, U+2028 and other characters that a YAML reader or
    str.splitlines treats as a line break stay visible.
    """
    with open(path, encoding="utf-8", newline="") as fh:
        lines = fh.read().split("\n")
    end = lines.index("---", 1) if lines[0] == "---" and "---" in lines[1:] else None
    if end is None:
        return "front matter must open and close with a line that is exactly '---', with LF line ends"
    for i in range(1, end):
        bad = [ch for ch in lines[i] if not " " <= ch <= "~"]
        if bad:
            return f"front matter line {i + 1}: only printable ASCII is allowed, found {bad[0]!r}"
    seen: set[str] = set()
    i = 1
    while i < end:
        line = lines[i]
        m = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):(?: .*)?", line)
        if not m or m.group(1) not in keys:
            return (f"front matter line {i + 1}: {line!r} is not a column-0 'key: value' line with a key in "
                    f"{sorted(keys)}" + (" or an allowed-tools item right after 'allowed-tools:'"
                                         if "allowed-tools" in keys else ""))
        if m.group(1) in seen:
            return f"front matter line {i + 1}: key {m.group(1)!r} appears twice"
        seen.add(m.group(1))
        if m.group(1) == "allowed-tools":
            if line != "allowed-tools:" or lines[i + 1:i + 3] != ["  - " + rule for rule in SKILL_ALLOWED_TOOLS]:
                return (f"front matter line {i + 1}: allowed-tools must be the line 'allowed-tools:' followed "
                        f"directly by the item lines '  - ' + each of {SKILL_ALLOWED_TOOLS}, in this order")
            i += 2
        else:  # the closed value grammar: a restricted YAML plain scalar (Issue #66 card I66-M3 (a))
            value = line[len(m.group(1)) + 2:]
            where = f"front matter line {i + 1}: "
            if not value:
                return where + "a value must not be empty"
            if value[0] == " ":
                return where + "exactly one space must follow the colon"
            if value[0] in PLAIN_START_BANNED:
                return where + f"a value must not start with any of {PLAIN_START_BANNED!r}"
            if ": " in value or " #" in value:
                return where + "a value must not contain ': ' or ' #'"
            if value[-1] in ": ":
                return where + "a value must not end with ':' or a space"
            if "---" in value:
                return where + "a value must not contain '---'"
        i += 1
    if "allowed-tools" in keys and "allowed-tools" not in seen:
        return "front matter has no 'allowed-tools:' line"
    return None


def sources(block: list[str]) -> tuple[list[dict[str, str]], list[str]]:
    """Entries of the `sources:` list and any problems found while parsing.

    Items may start at column 0 or indented. A field value may continue on
    following lines indented deeper than the field's key, or be a `>`/`|`
    block scalar with an optional `-` or `+` chomping indicator. Any other
    key inside an item is reported as a problem.
    """
    entries: list[dict[str, str]] = []
    problems: list[str] = []
    current: dict[str, str] | None = None
    field: str | None = None
    field_indent = 0
    block_scalar = False
    in_sources = False
    for line in block:
        if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:", line):
            in_sources = line.startswith("sources:") and graph.strip_comment(line[len("sources:"):]) == ""
            field = None
            continue
        indent = len(line) - len(line.lstrip())
        in_block = bool(current is not None and field and block_scalar and indent > field_indent)
        if not in_sources or not line.strip() or (line.strip().startswith("#") and not in_block):
            continue  # comment-only lines are skipped, except inside a block scalar (as in graph.frontmatter)
        m = re.match(r"^(\s*)(-\s+)?([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$", line)
        if m and not (field and indent > field_indent):
            if m.group(2):
                current = {}
                entries.append(current)
            if current is None:
                continue
            if m.group(3) not in {"type", "locator", "quote"}:
                problems.append(f"unknown key {m.group(3)!r} in a sources entry")
                field = None
                continue
            field = m.group(3)
            field_indent = len(m.group(1)) + (len(m.group(2)) if m.group(2) else 0)
            value = graph.strip_comment(m.group(4))
            block_scalar = value in {">", "|", ">-", "|-", ">+", "|+"}
            current[field] = "" if block_scalar else graph._unquote(value)
            continue
        if current is not None and field and indent > field_indent:  # continuation of the last field
            current[field] = graph._unquote((current[field] + " " + line.strip()).strip())
        else:
            problems.append(f"unexpected line in sources: {line.strip()!r}")
    return entries, problems


def main() -> int:
    errors: list[str] = []

    for name in sorted(os.listdir(ROOT)):  # CB-7 closed world; hidden names included
        if name not in ROOT_NAMES:
            same = [n for n in sorted(ROOT_NAMES) if n.casefold() == name.casefold()]
            errors.append(f"{name}: not in the root allowlist ROOT_NAMES" + (f" (case differs from {same[0]!r})" if same else "")
                          + "; " + CLOSED_WORLD_HINT)

    skill_mds: list[str] = []
    skills_dir = os.path.join(ROOT, "skills")
    for name in sorted(os.listdir(skills_dir)) if os.path.isdir(skills_dir) else []:
        path = os.path.join(skills_dir, name)
        if name.startswith("."):
            errors.append(f"skills/{name}: hidden names under skills/ are not allowed; " + CLOSED_WORLD_HINT)
        elif os.path.islink(path) or not os.path.isdir(path):
            errors.append(f"skills/{name}: every entry under skills/ must be a skill directory, not a file or symlink; "
                          + CLOSED_WORLD_HINT)
        elif "SKILL.md" not in os.listdir(path) or not stat.S_ISREG(os.lstat(os.path.join(path, "SKILL.md")).st_mode):
            errors.append(f"skills/{name}: has no regular file named exactly SKILL.md (CB-7)")
        elif problem := utf8_problem(os.path.join(path, "SKILL.md")):
            errors.append(f"skills/{name}/SKILL.md: {problem} (CB-7)")
        else:
            skill_mds.append(os.path.join(path, "SKILL.md"))

    for skill_md in skill_mds:
        skill_dir = os.path.dirname(skill_md)
        rel = os.path.relpath(skill_md, ROOT)
        if front_block(skill_md) is None:
            errors.append(f"{rel}: front matter is not closed with '---'")
            continue
        meta = graph.frontmatter(skill_md)
        if meta.get("name") != os.path.basename(skill_dir):
            errors.append(f"{rel}: name must equal the directory name")
        if not meta.get("description"):
            errors.append(f"{rel}: description missing")
        elif len(meta["description"]) > 1024:
            errors.append(f"{rel}: description longer than 1024 characters (Cowork limit)")
        if "allowed-tools" not in meta:
            errors.append(f"{rel}: allowed-tools missing; it must be the list {SKILL_ALLOWED_TOOLS} (CB-7)")
        elif meta["allowed-tools"] != SKILL_ALLOWED_TOOLS:
            errors.append(f"{rel}: allowed-tools must be a YAML list of exactly {SKILL_ALLOWED_TOOLS}, "
                          f"found {meta['allowed-tools']!r} (CB-7)")
        raw_problem = raw_front_matter_problem(skill_md, SKILL_KEYS)
        if raw_problem:
            errors.append(f"{rel}: {raw_problem} (CB-7)")
        for doc in sorted(glob.glob(os.path.join(skill_dir, "**", "*.md"), recursive=True)):
            if os.path.islink(doc):
                continue  # reported by the symlink check below; a broken link must not crash this loop
            if problem := utf8_problem(doc):
                errors.append(f"{os.path.relpath(doc, ROOT)}: {problem} (CB-7)")
                continue
            with open(doc, encoding="utf-8") as fh:
                text = fh.read()
            for ref in sorted(set(re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([^\s`'\")]+)", text))):
                if os.path.basename(skill_dir) == "dev-core" and not ref.startswith(("../dev-core/", "../../vendor/")):
                    errors.append(f"{os.path.relpath(doc, ROOT)}: dev-core is loaded by sibling skills; "
                                  f"write ${{CLAUDE_SKILL_DIR}}/../dev-core/... instead of ${{CLAUDE_SKILL_DIR}}/{ref}")
                target = ref.split("<")[0].rstrip("/.,:;")
                if target and not os.path.exists(os.path.normpath(os.path.join(skill_dir, target))):
                    errors.append(f"{os.path.relpath(doc, ROOT)}: referenced path does not exist: ${{CLAUDE_SKILL_DIR}}/{ref}")

    for top in ("skills", "agents", "vendor"):
        if os.path.islink(os.path.join(ROOT, top)):
            errors.append(f"{top}: symlink is not allowed (CB-7)")
    for top in ("skills", "vendor"):
        top_dir = os.path.join(ROOT, top)
        if os.path.islink(top_dir):
            continue  # reported above
        for dirpath, dirnames, filenames in os.walk(top_dir):  # does not follow links
            for name in sorted(dirnames + filenames):
                path = os.path.join(dirpath, name)
                st = os.lstat(path)
                if stat.S_ISLNK(st.st_mode):
                    errors.append(f"{os.path.relpath(path, ROOT)}: symlink under {top}/ is not allowed (CB-7)")
                elif stat.S_ISREG(st.st_mode) and st.st_nlink > 1:
                    errors.append(f"{os.path.relpath(path, ROOT)}: hardlinked file under {top}/ is not allowed (CB-7)")

    for top in ("skills", "agents", "vendor"):
        for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, top)):
            for name in casefold_duplicates(dirnames + filenames):
                errors.append(f"{os.path.relpath(os.path.join(dirpath, name), ROOT)}: another name in this "
                              f"directory differs only in case (CB-7)")

    plugin_dir = os.path.join(ROOT, ".claude-plugin")
    present = os.listdir(plugin_dir) if os.path.isdir(plugin_dir) else []
    for name in sorted(set(present) - set(MANIFEST_NAMES)):
        errors.append(f".claude-plugin/{name}: only {list(MANIFEST_NAMES)} are allowed in .claude-plugin/; "
                      + CLOSED_WORLD_HINT)
    for name in MANIFEST_NAMES:
        manifest = ".claude-plugin/" + name
        path = os.path.join(ROOT, manifest)
        if name not in present or not os.path.isfile(path):
            errors.append(f"{manifest}: missing (CB-7)")
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except (ValueError, RecursionError) as exc:  # JSONDecodeError, a UTF-8 BOM, UnicodeDecodeError, deep nesting
            errors.append(f"{manifest}: not valid JSON in UTF-8 without a BOM: {exc} (CB-7)")
            continue
        parts = [("top level", data)]
        if name == "marketplace.json":
            plugins = data.get("plugins") if isinstance(data, dict) else None
            if not (isinstance(plugins, list) and len(plugins) == 1 and isinstance(plugins[0], dict)
                    and plugins[0].get("name") == "dev-skills" and plugins[0].get("source") == "./"):
                errors.append(f"{manifest}: plugins must be a list of exactly one entry with name 'dev-skills' "
                              f"and source './', found {plugins!r} (CB-7)")
            parts += [("plugins[] entry", entry) for entry in plugins] if isinstance(plugins, list) else []
        for part, value in parts:
            allowed = MANIFEST_KEYS[(manifest, part)]
            extra = sorted(set(value) - allowed) if isinstance(value, dict) else [f"<not an object: {value!r}>"]
            if extra:
                errors.append(f"{manifest}: {part} keys {extra} are not in the allowlist {sorted(allowed)} (CB-7)")

    agent_mds: list[str] = []
    agents_dir = os.path.join(ROOT, "agents")
    agent_names = sorted(os.listdir(agents_dir)) if os.path.isdir(agents_dir) else []
    for stem in REQUIRED_AGENTS:  # CB-4 names in exact case (Issue #69 R69R1-001; Issue #77); a missing file is reported
        if stem + ".md" not in agent_names or not stat.S_ISREG(os.lstat(os.path.join(agents_dir, stem + ".md")).st_mode):
            errors.append(f"agents/{stem}.md: missing; the read-only agents {sorted(READ_ONLY_AGENTS)} and the pinned "
                          f"agents {sorted(PINNED_AGENT_SETTINGS)} must exist (CB-4, Issue #77)")
    required_keys = {agent_key(stem): stem for stem in REQUIRED_AGENTS}
    for name in agent_names:
        path = os.path.join(agents_dir, name)
        stem = name[:-3] if name.endswith(".md") else name
        if stem not in REQUIRED_AGENTS and agent_key(stem) in required_keys:  # Issue #69 R69S1-002; Issue #77
            match = required_keys[agent_key(stem)]
            role, rule = ("read-only agent", "CB-5") if match in READ_ONLY_AGENTS else ("pinned agent", "R-DEL-2, Issue #77")
            errors.append(f"agents/{name}: the name equals the {role} {match!r} after "
                          f"normalization (case, NFKC, whitespace, '_', dashes); Claude Code may dispatch it ({rule})")
        if name.startswith(".") or not name.endswith(".md") or not stat.S_ISREG(os.lstat(path).st_mode):
            errors.append(f"agents/{name}: agents/ may hold only non-hidden regular files named *.md; " + CLOSED_WORLD_HINT)
        elif stem in REQUIRED_AGENTS and os.lstat(path).st_size > AGENT_MAX_BYTES:
            errors.append(f"agents/{name}: larger than AGENT_MAX_BYTES ({AGENT_MAX_BYTES} bytes), this repository's "
                          f"limit for a read-only or pinned agent file; Claude Code skips an agent file over 1,048,576 bytes "
                          f"(inferred from the 2.1.310 code, not run; Issue #69 R69S1-002)")
        elif problem := utf8_problem(path):
            errors.append(f"agents/{name}: {problem} (CB-7)")
        else:
            agent_mds.append(path)

    for agent_md in agent_mds:
        rel = os.path.relpath(agent_md, ROOT)
        stem = os.path.splitext(os.path.basename(agent_md))[0]
        if front_block(agent_md) is None:
            errors.append(f"{rel}: front matter is not closed with '---'")
            continue
        raw_problem = raw_front_matter_problem(agent_md, AGENT_KEYS)
        if raw_problem:
            errors.append(f"{rel}: {raw_problem} (CB-7)")
        meta = graph.frontmatter(agent_md)
        if meta.get("name") != stem:
            errors.append(f"{rel}: name must equal the file name")
        if not meta.get("description"):
            errors.append(f"{rel}: description missing")
        if not isinstance(meta.get("model"), str) or meta.get("model") not in MODELS:
            errors.append(f"{rel}: model must be an alias {sorted(MODELS)}")
        if not isinstance(meta.get("effort"), str) or meta.get("effort") not in EFFORTS:
            errors.append(f"{rel}: effort must be one of {sorted(EFFORTS)}")
        if stem in READ_ONLY_AGENTS:
            raw = raw_values(agent_md)
            for key, pinned in READ_ONLY_AGENTS[stem].items():
                if raw.get(key) != pinned:
                    want = "no line" if pinned is None else f"the line '{key}: {pinned}'"
                    errors.append(f"{rel}: read-only agent must have {want} for {key}, found "
                                  f"{raw.get(key)!r} (CB-5, Issue #69)")
        if stem in PINNED_AGENT_SETTINGS:
            raw = raw_values(agent_md)
            for key, pinned in PINNED_AGENT_SETTINGS[stem].items():
                if raw.get(key) != pinned:
                    errors.append(f"{rel}: pinned agent must have the line '{key}: {pinned}' for {key}, found "
                                  f"{raw.get(key)!r} (R-DEL-2, Issue #77)")

    req_dir = os.path.join(ROOT, "docs", "requirements")
    for req in sorted(p for p in glob.glob(os.path.join(req_dir, "REQ-*.md")) if graph.REQ_FILE_RE.match(os.path.basename(p))):
        rel = os.path.relpath(req, ROOT)
        block = front_block(req)
        if block is None:
            errors.append(f"{rel}: front matter is not closed with '---'")
            continue
        meta = graph.frontmatter(req)
        prefix = re.match(r"^(REQ-\d{3,})", os.path.basename(req))
        if not prefix or meta.get("id") != prefix.group(1):
            errors.append(f"{rel}: front matter id must match the file name")
        if not isinstance(meta.get("status"), str) or meta.get("status") not in graph.REQ_STATUSES:
            errors.append(f"{rel}: status must be one of {sorted(graph.REQ_STATUSES)}")
        for field in graph.REQ_RELATIONS:
            value = meta.get(field)
            if not isinstance(value, list) or not all(REQ_ID.match(v) for v in value):
                errors.append(f"{rel}: {field} must be a list of REQ ids, e.g. [] or [REQ-001]")
        if meta.get("status") == "superseded":
            if not meta.get("superseded_by"):
                errors.append(f"{rel}: superseded requires superseded_by")
            if not meta.get("superseded_reason"):
                errors.append(f"{rel}: superseded requires superseded_reason")
        entries, problems = sources(block)
        errors += [f"{rel}: {p}" for p in problems]
        if not entries:
            errors.append(f"{rel}: sources must list at least one entry")
        for i, e in enumerate(entries):
            if e.get("type") not in SOURCE_TYPES:
                errors.append(f"{rel}: sources[{i}].type must be one of {sorted(SOURCE_TYPES)}")
            if not e.get("locator"):
                errors.append(f"{rel}: sources[{i}].locator missing")
            if "quote" not in e or (not e["quote"] and e.get("type") != "external"):
                errors.append(f"{rel}: sources[{i}].quote missing (only external sources may leave it empty)")

    if os.path.isdir(req_dir):
        by_id, metas, _ = graph.load_requirements(req_dir)
        for rid, names in sorted(by_id.items()):
            if len(names) > 1:
                errors.append(f"docs/requirements: {rid} has several files: {names}")
        errors += [f"docs/requirements: {e['code']}: {e['message']}"
                   for e in graph.check_requirement_relations(metas, set(by_id))]

    if errors:
        print("pack structure: FAIL")
        for e in errors:
            print("  - " + e)
        return 1
    print("pack structure: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
