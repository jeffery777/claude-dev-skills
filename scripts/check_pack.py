#!/usr/bin/env python3
"""Structural checks for the skill pack (stdlib only).

- every skills/<dir>/SKILL.md has name == <dir> and a description of at most 1,024 characters;
- every agents/*.md has name == file stem, a description, a model alias and an effort level;
- read-only agents list their tools and expose no Edit, Write or NotebookEdit tool
  (they keep Bash; read-only Bash use is enforced by instructions, not by this check);
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
import os
import re
import sys
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS = {"haiku", "sonnet", "opus", "fable", "inherit"}
EFFORTS = {"low", "medium", "high", "xhigh", "max"}
WRITE_TOOLS = {"Edit", "MultiEdit", "Write", "NotebookEdit"}
READ_ONLY_AGENTS = {"dev-explorer", "dev-reviewer", "dev-security-reviewer"}
SOURCE_TYPES = {"doc", "chat", "issue", "commit", "external"}

_spec = importlib.util.spec_from_file_location("graph", os.path.join(ROOT, "skills", "dev-plan", "scripts", "graph.py"))
graph = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(graph)
REQ_ID = graph.REQ_RE


front_block = graph.frontmatter_lines


def tool_set(value: Any) -> set[str]:
    """Tool names, ignoring permission specifiers such as Write(docs/**)."""
    items = value if isinstance(value, list) else re.findall(r"[^,(]+(?:\([^)]*\))?", str(value or ""))
    return {graph._unquote(t.strip()).split("(", 1)[0].strip() for t in items if t.strip()}


def sources(block: list[str]) -> list[dict[str, str]]:
    """Entries of the `sources:` list (a list of type/locator/quote mappings).

    Items may start at column 0 or indented. A field value may continue on
    the following, deeper-indented lines, or be a `>`/`|` block scalar.
    """
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    field: str | None = None
    in_sources = False
    for line in block:
        if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:", line):
            in_sources = line.startswith("sources:") and graph.strip_comment(line[len("sources:"):]) == ""
            field = None
            continue
        if not in_sources or not line.strip():
            continue
        m = re.match(r"^\s*(-\s+)?(type|locator|quote):\s*(.*?)\s*$", line)
        if m:
            if m.group(1):
                current = {}
                entries.append(current)
            if current is None:
                continue
            field = m.group(2)
            value = graph.strip_comment(m.group(3))
            current[field] = "" if value in {">", "|", ">-", "|-"} else graph._unquote(value)
            continue
        if current is not None and field:  # continuation of the last field
            joined = (current[field] + " " + line.strip()).strip()
            current[field] = graph._unquote(joined)
    return entries


def main() -> int:
    errors: list[str] = []

    for skill_md in sorted(glob.glob(os.path.join(ROOT, "skills", "*", "SKILL.md"))):
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
        for doc in sorted(glob.glob(os.path.join(skill_dir, "**", "*.md"), recursive=True)):
            with open(doc, encoding="utf-8") as fh:
                text = fh.read()
            for ref in sorted(set(re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([^\s`'\")]+)", text))):
                if os.path.basename(skill_dir) == "dev-core" and not ref.startswith(("../dev-core/", "../../vendor/")):
                    errors.append(f"{os.path.relpath(doc, ROOT)}: dev-core is loaded by sibling skills; "
                                  f"write ${{CLAUDE_SKILL_DIR}}/../dev-core/... instead of ${{CLAUDE_SKILL_DIR}}/{ref}")
                target = ref.split("<")[0].rstrip("/.,:;")
                if target and not os.path.exists(os.path.normpath(os.path.join(skill_dir, target))):
                    errors.append(f"{os.path.relpath(doc, ROOT)}: referenced path does not exist: ${{CLAUDE_SKILL_DIR}}/{ref}")

    for agent_md in sorted(glob.glob(os.path.join(ROOT, "agents", "*.md"))):
        rel = os.path.relpath(agent_md, ROOT)
        stem = os.path.splitext(os.path.basename(agent_md))[0]
        if front_block(agent_md) is None:
            errors.append(f"{rel}: front matter is not closed with '---'")
            continue
        meta = graph.frontmatter(agent_md)
        if meta.get("name") != stem:
            errors.append(f"{rel}: name must equal the file name")
        if not meta.get("description"):
            errors.append(f"{rel}: description missing")
        if meta.get("model") not in MODELS:
            errors.append(f"{rel}: model must be an alias {sorted(MODELS)}")
        if meta.get("effort") not in EFFORTS:
            errors.append(f"{rel}: effort must be one of {sorted(EFFORTS)}")
        if stem in READ_ONLY_AGENTS:
            if not meta.get("tools"):
                errors.append(f"{rel}: read-only agent must list tools explicitly")
            exposed = tool_set(meta.get("tools")) & WRITE_TOOLS
            if exposed:
                errors.append(f"{rel}: read-only agent exposes write tools {sorted(exposed)}")

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
        if meta.get("status") not in graph.REQ_STATUSES:
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
        entries = sources(block)
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
