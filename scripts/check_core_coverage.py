#!/usr/bin/env python3
"""Check that skills/dev-core covers every anchor of the vendored Core (D-001).

Fails when:
- a Core anchor has no source-map row, or a row names an unknown anchor;
- a covered row lists a rule that does not exist or does not cite that anchor;
- a not-applicable row has no reason;
- a dev-core rule cites no anchor, an unknown anchor, or is missing from the map.
"""

from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTRACTS = os.path.join(ROOT, "vendor", "engineering-workflow-core", "contracts")
SKILL = os.path.join(ROOT, "skills", "dev-core", "SKILL.md")
SOURCE_MAP = os.path.join(ROOT, "skills", "dev-core", "source-map.md")

RULE_RE = re.compile(r"\*\*(R-[A-Z]+-\d+)\*\*")
CITE_RE = re.compile(r"\[core: ([^\]]+)\]")
ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|([^|]*)\|([^|]*)\|([^|]*)\|\s*$")


def core_anchors() -> set[str]:
    anchors = set()
    for name in sorted(os.listdir(CONTRACTS)):
        if name.endswith(".md"):
            with open(os.path.join(CONTRACTS, name), encoding="utf-8") as fh:
                for anchor in re.findall(r'<a id="([^"]+)"', fh.read()):
                    anchors.add(f"{name}#{anchor}")
    return anchors


def rules() -> dict[str, set[str]]:
    """Rule id -> cited anchors. A rule block runs until the next rule or heading."""
    with open(SKILL, encoding="utf-8") as fh:
        text = fh.read()
    result: dict[str, set[str]] = {}
    matches = list(RULE_RE.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        heading = re.compile(r"\n#{1,6} ").search(text, m.end(), end)
        block = text[m.end(): heading.start() if heading else end]
        if m.group(1) in result:
            result[m.group(1)] = {"__DUPLICATE__"}
            continue
        result[m.group(1)] = {a.strip() for c in CITE_RE.findall(block) for a in c.split(",")}
    return result


def source_map() -> dict[str, tuple[list[str], str, str]]:
    rows = {}
    with open(SOURCE_MAP, encoding="utf-8") as fh:
        for line in fh:
            m = ROW_RE.match(line.rstrip("\n"))
            if m and m.group(1) in rows:
                rows[m.group(1)] = ([], "__DUPLICATE_ROW__", "")
                continue
            if m:
                ids = [r.strip() for r in m.group(2).split(",") if r.strip()]
                rows[m.group(1)] = (ids, m.group(3).strip(), m.group(4).strip())
    return rows


def main() -> int:
    anchors, rule_map, rows = core_anchors(), rules(), source_map()
    errors = []
    if not anchors:
        errors.append("no Core anchors found; is vendor/ present?")
    for a in sorted(anchors - rows.keys()):
        errors.append(f"anchor without source-map row: {a}")
    for a in sorted(rows.keys() - anchors):
        errors.append(f"source-map row for unknown anchor: {a}")
    mapped: dict[str, set[str]] = {}
    for anchor, (ids, status, note) in rows.items():
        if status == "covered":
            if not ids:
                errors.append(f"{anchor}: covered but lists no rules")
            for rid in ids:
                mapped.setdefault(rid, set()).add(anchor)
                if "__DUPLICATE__" in rule_map.get(rid, set()):
                    continue  # reported once below as a duplicate
                if rid not in rule_map:
                    errors.append(f"{anchor}: rule {rid} does not exist in dev-core")
                elif anchor not in rule_map[rid]:
                    errors.append(f"{anchor}: rule {rid} does not cite this anchor")
        elif status == "__DUPLICATE_ROW__":
            errors.append(f"{anchor}: more than one source-map row")
        elif status == "not-applicable":
            if not note:
                errors.append(f"{anchor}: not-applicable without a reason")
        else:
            errors.append(f"{anchor}: unknown status {status!r}")
    for rid, cites in sorted(rule_map.items()):
        if "__DUPLICATE__" in cites:
            errors.append(f"{rid}: duplicate rule id")
            continue
        if not cites:
            errors.append(f"{rid}: cites no Core anchor")
        for a in sorted(cites - anchors):
            errors.append(f"{rid}: cites unknown anchor {a}")
        for a in sorted((cites & anchors) - mapped.get(rid, set())):
            errors.append(f"{rid}: cites {a} but source-map row does not list it")
    if errors:
        print("core coverage: FAIL")
        for e in errors:
            print("  - " + e)
        return 1
    print(f"core coverage: OK ({len(anchors)} anchors, {len(rule_map)} rules)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
