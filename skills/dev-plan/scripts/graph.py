#!/usr/bin/env python3
"""G0 task graph tool for claude-dev-skills (stdlib only).

The graph is coordination data (CB-1). It never proves completion or grants
authority (R-AUTH-1); completion evidence stays in Git, verification output, and
independent review (Core exact-head-and-evidence.md#exact-identity).

Commands:
  validate <graph.json> [--requirements-dir DIR]
  ready <graph.json> [--requirements-dir DIR]
  transition <graph.json> <node> <status> (--evidence TEXT | --evidence-file PATH)
             [--actor NAME] [--requirements-dir DIR]

--evidence-file never copies file content into events.jsonl, which is
committed by default (CB-1). The file must be a regular file inside the project root,
and the last component of its path must not be a symlink. The event records
"file:<relative path> sha256:<hex>". A refused file exits 2 with
EVIDENCE_FILE_REFUSED. A graph without a project root cannot use it.

`ready` lists nodes whose dependencies are satisfied; a listed node that is
still `planned` must move to `ready` before `in_progress`. `transition`
re-validates the resulting graph and refuses a change that would leave it
invalid.

Requirement files are always checked. Without --requirements-dir the tool
finds the project root (the nearest ancestor of the graph file that holds
.git or .dev/) and uses "requirements_dir" from <root>/.dev/config.json, else
<root>/docs/requirements/. The directory, including one given with
--requirements-dir, must stay inside the project root (D-003, D-008).

Exit codes: 0 ok, 1 graph/transition errors, 2 usage or unreadable input.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import posixpath
import re
import stat
import sys
import tempfile
from typing import Any

try:
    import fcntl
except ImportError:  # pragma: no cover - non-POSIX platforms
    fcntl = None  # type: ignore[assignment]

SCHEMA = "claude-dev-graph/v1"
KINDS = {"explore", "implement", "docs", "verify", "review", "gate", "human_gate"}
WRITE_KINDS = {"implement", "docs"}
RISKS = {"low", "medium", "high", "unknown"}
REVIEWS = {"none", "routine", "deep", "security"}
RIGORS = {"standard", "strict"}
STATUSES = {"planned", "ready", "in_progress", "blocked", "reviewing", "done", "accepted", "cancelled"}
SATISFIED = {"done", "accepted"}
STARTED = {"in_progress", "reviewing", "done", "accepted"}
TRANSITIONS = {
    "planned": {"ready", "blocked", "cancelled"},
    "ready": {"in_progress", "blocked", "cancelled"},
    "in_progress": {"ready", "reviewing", "blocked"},
    "blocked": {"planned", "ready", "cancelled"},
    "reviewing": {"in_progress", "done", "blocked"},
    "done": {"accepted", "ready"},
    "accepted": set(),
    "cancelled": set(),
}
REQ_RE = re.compile(r"^REQ-[0-9]{3,}$")
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*$")
REQ_RELATIONS = ("depends_on", "refines", "conflicts_with", "superseded_by")


class Issue(dict):
    def __init__(self, code: str, message: str, node: str | None = None):
        super().__init__(code=code, message=message)
        if node is not None:
            self["node"] = node


def load(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("graph root must be a JSON object")
    return data


def _str_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(v, str) and v for v in value)


def _prefix(pattern: str) -> list[str]:
    """Normalized literal path segments before the first wildcard (conservative).

    "", ".", "/" and "./" mean the whole repository and return [].
    """
    norm = posixpath.normpath("/" + pattern.replace("\\", "/")).lstrip("/")
    segments: list[str] = []
    for seg in norm.split("/") if norm else []:
        if any(ch in seg for ch in "*?[{"):
            break
        segments.append(seg)
    return segments


def patterns_overlap(a: str, b: str) -> bool:
    pa, pb = [s.casefold() for s in _prefix(a)], [s.casefold() for s in _prefix(b)]  # case-insensitive file systems
    n = min(len(pa), len(pb))
    return pa[:n] == pb[:n]


def check_schema(g: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if g.get("schema") != SCHEMA:
        issues.append(Issue("SCHEMA", f"schema must be {SCHEMA!r}"))
    obj = g.get("objective")
    if not isinstance(obj, dict):
        issues.append(Issue("SCHEMA", "objective must be an object"))
    else:
        for key in ("id", "title"):
            if not isinstance(obj.get(key), str) or not obj.get(key):
                issues.append(Issue("SCHEMA", f"objective.{key} must be a non-empty string"))
        if not isinstance(obj.get("rigor"), str) or obj.get("rigor") not in RIGORS:
            issues.append(Issue("SCHEMA", f"objective.rigor must be one of {sorted(RIGORS)}"))
        if not _str_list(obj.get("requirements")) or not obj.get("requirements"):
            issues.append(Issue("SCHEMA", "objective.requirements must be a non-empty list"))
        else:
            for req in obj["requirements"]:
                if not REQ_RE.match(req):
                    issues.append(Issue("SCHEMA", f"bad requirement id {req!r}"))
    nodes = g.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        issues.append(Issue("SCHEMA", "nodes must be a non-empty list"))
        return issues
    for i, n in enumerate(nodes):
        if not isinstance(n, dict):
            issues.append(Issue("SCHEMA", f"nodes[{i}] must be an object"))
            continue
        nid = n.get("id") if isinstance(n.get("id"), str) else f"nodes[{i}]"
        if not isinstance(n.get("id"), str) or not ID_RE.match(n["id"]):
            issues.append(Issue("SCHEMA", "id must match " + ID_RE.pattern, nid))
        if not isinstance(n.get("title"), str) or not n.get("title"):
            issues.append(Issue("SCHEMA", "title must be a non-empty string", nid))
        for key, allowed in (("kind", KINDS), ("risk", RISKS), ("review", REVIEWS), ("status", STATUSES)):
            if not isinstance(n.get(key), str) or n.get(key) not in allowed:
                issues.append(Issue("SCHEMA", f"{key} must be one of {sorted(allowed)}", nid))
        for key in ("requirements", "owns", "dod", "verify"):
            if not isinstance(n.get(key), list) or (n.get(key) and not _str_list(n.get(key))):
                issues.append(Issue("SCHEMA", f"{key} must be a list of strings", nid))
        deps = n.get("depends_on")
        if not isinstance(deps, list):
            issues.append(Issue("SCHEMA", "depends_on must be a list", nid))
        else:
            for d in deps:
                if not isinstance(d, dict) or not isinstance(d.get("node"), str):
                    issues.append(Issue("SCHEMA", "depends_on entries need a 'node' string", nid))
        is_writer = isinstance(n.get("kind"), str) and n["kind"] in WRITE_KINDS
        if is_writer and isinstance(n.get("dod"), list) and not n.get("dod"):
            issues.append(Issue("SCHEMA", "write nodes need at least one DoD item", nid))
        for pattern in n.get("owns") if _str_list(n.get("owns")) else []:
            norm = pattern.replace("\\", "/")
            if norm.startswith("/") or re.match(r"^[A-Za-z]:", norm) or ".." in norm.split("/"):
                issues.append(Issue("SCHEMA", f"owns path {pattern!r} must be repository-relative without '..'", nid))
    return issues


def _node_map(g: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {n["id"]: n for n in g["nodes"]}


def _reachable(nodes: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    """Map node -> transitive dependencies through non-cancelled nodes (graph must be acyclic)."""
    memo: dict[str, set[str]] = {}

    def visit(nid: str) -> set[str]:
        if nid not in memo:
            acc: set[str] = set()
            for d in nodes[nid]["depends_on"]:
                dep = d["node"]
                if nodes[dep]["status"] != "cancelled":
                    acc |= {dep} | visit(dep)
            memo[nid] = acc
        return memo[nid]

    for nid in nodes:
        visit(nid)
    return memo


def find_cycle(nodes: dict[str, dict[str, Any]]) -> list[str] | None:
    color = {nid: 0 for nid in nodes}
    path: list[str] = []

    def dfs(nid: str) -> list[str] | None:
        color[nid] = 1
        path.append(nid)
        for d in nodes[nid]["depends_on"]:
            dep = d["node"]
            if dep not in nodes:
                continue
            if color[dep] == 1:
                return path[path.index(dep):] + [dep]
            if color[dep] == 0:
                found = dfs(dep)
                if found:
                    return found
        path.pop()
        color[nid] = 2
        return None

    for nid in sorted(nodes):
        if color[nid] == 0:
            found = dfs(nid)
            if found:
                return found
    return None


def frontmatter_lines(path: str) -> list[str] | None:
    """Lines between the opening and closing '---', or None when either is missing."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[1:i]
    return None


def strip_comment(value: str) -> str:
    """Remove a trailing ` # comment` from a YAML scalar (quoted text is kept whole)."""
    value = value.strip()
    if value.startswith("#"):
        return ""
    if value.startswith("["):
        quote = ""
        for i, ch in enumerate(value):  # a flow list ends at its unquoted bracket
            if quote:
                quote = "" if ch == quote else quote
            elif ch in "'\"":
                quote = ch
            elif ch == "]":
                return value[:i + 1]
        return value
    if value[:1] in {"'", '"'}:
        i = 1
        while i < len(value):
            if value[i] == value[0]:
                if value[0] == "'" and value[i + 1:i + 2] == "'":
                    i += 2  # '' is an escaped quote inside single quotes
                    continue
                return value[:i + 1]
            i += 1
        return value
    m = re.search(r"\s+#", value)
    return value[:m.start()].rstrip() if m else value


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        inner = value[1:-1]
        return inner.replace("''", "'") if value[0] == "'" else inner
    return value


def frontmatter(path: str) -> dict[str, Any]:
    """Top-level keys of a Markdown front matter block (a small YAML subset).

    Supported subset (REQ, SKILL.md and agent front matter must stay inside it):

    - Block: the first line is `---` and the next line that is `---` closes
      it. A missing delimiter yields {}.
    - Keys: a line at column 0 of the form `key:` or `key: value`, where key
      matches [A-Za-z_][A-Za-z0-9_-]*. A repeated key keeps its last value.
      Comment-only lines are skipped (except inside a block scalar).
    - Plain or quoted scalar -> str. A trailing ` # comment` is removed, then
      one pair of matching outer quotes. Inside single quotes `''` is `'`.
      Indented lines that follow are appended with one space.
    - `null` or `~` -> None. No other type conversion: `true` and `12` stay str.
    - Flow list on one line, `[a, "b, c"]` -> list of str (no nesting).
    - Empty value, then `- item` lines (any indent) -> list of str. Without
      items the value is [], or the str on the next indented line.
    - Block scalar `>` or `|` (chomping indicators ignored) -> the following
      lines, stripped and joined with spaces; `|` does not keep newlines.

    Not supported: double-quote escapes (`\\"` ends the string), flow lists
    over several lines (they become a str), nested mappings (a `- key: v` item
    becomes the str "key: v" and its other lines are dropped; check_pack.sources
    reads `sources` entries itself), anchors, aliases, tags, flow mappings and
    several documents. Input outside the subset raises no error and may parse
    wrongly; that is a format limit of this parser, not a defect.
    """
    lines = frontmatter_lines(path)
    if lines is None:
        return {}
    result: dict[str, Any] = {}
    key: str | None = None
    folded: list[str] | None = None
    for line in lines:
        if line.strip().startswith("#") and folded is None:
            continue  # comment-only line
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):(?:\s+(.*))?$", line)
        if m:
            if folded is not None and key:
                result[key] = " ".join(folded).strip()
            folded = None
            key, value = m.group(1), strip_comment(m.group(2) or "")
            if value in {">", "|", ">-", "|-", ">+", "|+"}:
                folded = []
            elif value.startswith("[") and value.endswith("]"):
                items = re.findall(r'\s*(?:"[^"]*"|\'[^\']*\'|[^,]+)', value[1:-1])
                result[key] = [_unquote(v) for v in items if v.strip()]
            elif value == "":
                result[key] = []
            elif value in {"null", "~"}:
                result[key] = None
            else:
                result[key] = _unquote(value)
            continue
        if folded is not None:
            folded.append(line.strip())
            continue
        item = re.match(r"^\s*-\s+(.*?)\s*$", line)
        if key and item and isinstance(result.get(key), list):
            result[key].append(_unquote(strip_comment(item.group(1))))
        elif key and line[:1].isspace() and line.strip() and isinstance(result.get(key), str):
            result[key] = _unquote(result[key] + " " + strip_comment(line))  # continued plain scalar
        elif key and line[:1].isspace() and line.strip() and result.get(key) == []:
            result[key] = _unquote(strip_comment(line))  # scalar starting on the next line
    if folded is not None and key:
        result[key] = " ".join(folded).strip()
    return result


def _relation_ids(meta: dict[str, Any], field: str) -> list[str]:
    value = meta.get(field)
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def check_requirement_relations(metas: dict[str, dict[str, Any]], known: set[str] | None = None) -> list[Issue]:
    """Typed REQ relations must point at existing REQs; depends_on must be acyclic."""
    errors: list[Issue] = []
    known = set(metas) if known is None else known
    for rid, meta in sorted(metas.items()):
        for field in REQ_RELATIONS:
            for target in _relation_ids(meta, field):
                if target not in known:
                    errors.append(Issue("REQ_RELATION_UNKNOWN", f"{rid}.{field} points to missing {target}"))
    dep_nodes = {rid: {"depends_on": [{"node": d} for d in _relation_ids(m, "depends_on") if d in metas]}
                 for rid, m in metas.items()}
    cycle = find_cycle(dep_nodes)
    if cycle:
        errors.append(Issue("REQ_DEPENDENCY_CYCLE", "requirement depends_on cycle: " + " -> ".join(cycle)))
    return errors


REQ_STATUSES = {"proposed", "active", "conflict", "done", "superseded", "dropped"}
REQ_FILE_RE = re.compile(r"^(REQ-[0-9]{3,})(-.*)?\.md$")


def load_requirements(requirements_dir: str) -> tuple[dict[str, list[str]], dict[str, dict[str, Any]], dict[str, Any]]:
    """Parse every REQ file once.

    Returns (REQ id -> file names, REQ id -> front matter for a unique file whose
    id matches, file name -> front matter id as found).
    """
    by_id: dict[str, list[str]] = {}
    metas: dict[str, dict[str, Any]] = {}
    found_ids: dict[str, Any] = {}
    for name in sorted(os.listdir(requirements_dir)):
        m = REQ_FILE_RE.match(name)
        if not m:
            continue
        by_id.setdefault(m.group(1), []).append(name)
        meta = frontmatter(os.path.join(requirements_dir, name))
        found_ids[name] = meta.get("id")
        if meta.get("id") == m.group(1) and len(by_id[m.group(1)]) == 1:
            metas[m.group(1)] = meta
        else:
            metas.pop(m.group(1), None)
    return by_id, metas, found_ids


def check_requirement_files(declared: set[str], nodes: dict[str, dict[str, Any]],
                            requirements_dir: str) -> tuple[list[Issue], list[Issue]]:
    """Every declared REQ must have exactly one file REQ-xxx*.md whose front matter id matches."""
    errors: list[Issue] = []
    warnings: list[Issue] = []
    if not os.path.isdir(requirements_dir):
        return [Issue("MISSING_REQUIREMENTS_DIR", f"requirements directory not found: {requirements_dir}")], warnings
    by_id, metas, found_ids = load_requirements(requirements_dir)
    errors += check_requirement_relations(metas, set(by_id))
    for req in sorted(declared):
        hits = by_id.get(req, [])
        if not hits:
            errors.append(Issue("MISSING_REQUIREMENT_FILE", f"no file for {req} in {requirements_dir}"))
            continue
        if len(hits) > 1:
            errors.append(Issue("DUPLICATE_REQUIREMENT_FILE", f"{req} has several files: {hits}"))
            continue
        meta = metas.get(req)
        if meta is None:
            errors.append(Issue("REQUIREMENT_ID_MISMATCH", f"{hits[0]} front matter id is {found_ids.get(hits[0])!r}, expected {req}"))
            continue
        if not isinstance(meta.get("status"), str) or meta.get("status") not in REQ_STATUSES:
            errors.append(Issue("BAD_REQUIREMENT_STATUS", f"{req} status {meta.get('status')!r} is not one of {sorted(REQ_STATUSES)}"))
            continue
        open_users = sorted(nid for nid, n in nodes.items()
                            if req in n["requirements"] and n["status"] not in SATISFIED | {"cancelled"})
        if meta.get("status") == "conflict":
            for nid in open_users:
                if nodes[nid]["kind"] in WRITE_KINDS:
                    errors.append(Issue("REQUIREMENT_CONFLICT", f"{req} has conflicting sources; the user must decide before this node proceeds", nid))
        elif meta.get("status") in {"dropped", "superseded"} and open_users:
            warnings.append(Issue("INACTIVE_REQUIREMENT", f"{req} is {meta['status']} but open nodes cite it: {open_users}"))
    return errors, warnings


def project_root(graph_path: str) -> str | None:
    """Nearest ancestor of the graph file that holds .git or .dev/."""
    current = os.path.dirname(os.path.abspath(graph_path))
    while True:
        if os.path.exists(os.path.join(current, ".git")) or os.path.isdir(os.path.join(current, ".dev")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def find_requirements_dir(graph_path: str, explicit: str | None = None) -> tuple[str | None, Issue | None]:
    """Resolve the requirements folder inside the project root (never above it).

    An explicit directory is used as given, but must also stay inside the
    project root when the graph has one.
    """
    root = project_root(graph_path)
    if explicit is not None:
        if root is not None and not _inside(root, explicit):
            return None, Issue("REQUIREMENTS_DIR_OUTSIDE", f"{explicit} resolves outside the project root {root}")
        return explicit, None
    if root is None:
        return None, Issue("MISSING_REQUIREMENTS_DIR", "no project root (.git or .dev/) above the graph file; pass --requirements-dir")
    candidate = os.path.join(root, "docs", "requirements")
    config = os.path.join(root, ".dev", "config.json")
    if os.path.isfile(config):
        try:
            with open(config, encoding="utf-8") as fh:
                configured = json.load(fh).get("requirements_dir")
        except (OSError, ValueError, AttributeError):
            return None, Issue("BAD_CONFIG", f"cannot read requirements_dir from {config}")
        if configured is not None:
            if not isinstance(configured, str) or not configured:
                return None, Issue("BAD_CONFIG", "requirements_dir must be a non-empty string")
            candidate = os.path.join(root, configured)
    if not _inside(root, candidate):
        return None, Issue("REQUIREMENTS_DIR_OUTSIDE", f"{candidate} resolves outside the project root {root}")
    return candidate, None


def _inside(root: str, path: str) -> bool:
    real_root, real = os.path.realpath(root), os.path.realpath(path)
    return os.path.commonpath([real_root, real]) == real_root


def check_graph(g: dict[str, Any], requirements_dir: str | None = None) -> tuple[list[Issue], list[Issue]]:
    """Validate a graph. Pass requirements_dir to also check the REQ files (the CLI always does)."""
    errors = check_schema(g)
    warnings: list[Issue] = []
    if errors:
        return errors, warnings

    seen: set[str] = set()
    for n in g["nodes"]:
        if n["id"] in seen:
            errors.append(Issue("DUP_ID", "duplicate node id", n["id"]))
        seen.add(n["id"])
    if errors:
        return errors, warnings
    nodes = _node_map(g)
    declared = set(g["objective"]["requirements"])

    for n in nodes.values():
        for d in n["depends_on"]:
            if d["node"] not in nodes:
                errors.append(Issue("UNKNOWN_DEP", f"depends on unknown node {d['node']!r}", n["id"]))
            # Fake-edge test: an edge must name the data that crosses it.
            if not isinstance(d.get("consumes"), str) or not d.get("consumes", "").strip():
                errors.append(Issue("FAKE_EDGE", f"edge to {d['node']!r} does not say what it consumes", n["id"]))
        # Requirement anchors: every write node traces to a declared requirement.
        if n["kind"] in WRITE_KINDS and not n["requirements"]:
            errors.append(Issue("NO_REQUIREMENT", "write node has no requirement anchor (possible scope creep)", n["id"]))
        for req in n["requirements"]:
            if req not in declared:
                errors.append(Issue("UNKNOWN_REQUIREMENT", f"{req} is not in objective.requirements", n["id"]))
        # Unknown is not low; high or unknown risk needs deep or security review.
        if n["kind"] in WRITE_KINDS and n["risk"] in {"high", "unknown"} and n["review"] in {"none", "routine"}:
            errors.append(Issue("RISK_REVIEW", f"risk {n['risk']} requires deep or security review", n["id"]))
        if n["kind"] in WRITE_KINDS and n["review"] == "none" and g["objective"]["rigor"] == "strict":
            errors.append(Issue("RISK_REVIEW", "strict rigor requires review on every write node", n["id"]))
        if n["kind"] in WRITE_KINDS and not n["owns"]:
            errors.append(Issue("NO_OWNERSHIP", "write node must declare owned paths", n["id"]))

    if requirements_dir is not None:
        req_errors, req_warnings = check_requirement_files(declared, nodes, requirements_dir)
        errors += req_errors
        warnings += req_warnings

    if any(e["code"] == "UNKNOWN_DEP" for e in errors):
        return errors, warnings
    cycle = find_cycle(nodes)
    if cycle:
        errors.append(Issue("CYCLE", "dependency cycle: " + " -> ".join(cycle)))
        return errors, warnings

    reach = _reachable(nodes)
    writers = sorted(nid for nid, n in nodes.items()
                     if n["kind"] in WRITE_KINDS and n["status"] not in SATISFIED | {"cancelled"})
    for i, a in enumerate(writers):
        for b in writers[i + 1:]:
            if a in reach[b] or b in reach[a]:
                continue  # ordered by a live dependency path, never concurrent
            for pa in nodes[a]["owns"]:
                for pb in nodes[b]["owns"]:
                    if patterns_overlap(pa, pb):
                        msg = f"{a} ({pa}) and {b} ({pb}) are not ordered and own overlapping paths"
                        errors.append(Issue("OWNERSHIP_OVERLAP", msg, a))
                        errors.append(Issue("OWNERSHIP_OVERLAP", msg, b))

    for n in nodes.values():
        if n["status"] in STARTED | {"ready"}:
            pending = [d["node"] for d in n["depends_on"] if nodes[d["node"]]["status"] not in SATISFIED]
            if pending:
                issue = Issue("STATUS_DEP", f"status {n['status']} but dependencies not satisfied: {pending}", n["id"])
                issue["pending"] = pending
                errors.append(issue)

    for n in nodes.values():
        if n["status"] not in SATISFIED | {"cancelled"}:
            dead = [d["node"] for d in n["depends_on"] if nodes[d["node"]]["status"] == "cancelled"]
            if dead:
                warnings.append(Issue("STRANDED", f"depends on cancelled {dead}; re-plan the edge or cancel this node", n["id"]))

    used = {r for n in nodes.values() for r in n["requirements"]}
    for req in sorted(declared - used):
        warnings.append(Issue("UNUSED_REQUIREMENT", f"{req} has no node; is it out of scope?"))
    return errors, warnings


def ready_nodes(g: dict[str, Any], waiting: set[str] | None = None) -> list[str]:
    """Nodes whose dependencies are satisfied, minus nodes waiting on a requirement conflict."""
    nodes = _node_map(g)
    waiting = waiting or set()
    return [
        nid for nid, n in nodes.items()
        if n["status"] in {"planned", "ready"} and nid not in waiting
        and all(nodes[d["node"]]["status"] in SATISFIED for d in n["depends_on"])
    ]


def _is_new_error(err: Issue, before: list[Issue]) -> bool:
    """True when `err` was not already present. A STATUS_DEP is new only if its pending set grew."""
    if err["code"] == "STATUS_DEP":
        old = [b for b in before if b["code"] == "STATUS_DEP" and b.get("node") == err.get("node")]
        return not old or not set(err.get("pending", [])) <= set(old[0].get("pending", []))
    return (err["code"], err.get("node"), err["message"]) not in {(b["code"], b.get("node"), b["message"]) for b in before}


def _refuse_symlink(path: str) -> Issue | None:
    if os.path.islink(path):
        return Issue("SYMLINK_REFUSED", f"{path} is a symlink; refusing to write through it")
    return None


def transition(path: str, node: str, to: str, evidence: str, actor: str,
               requirements_dir: str | None = None) -> list[Issue]:
    """Apply one status change under an exclusive lock: graph first, then the event."""
    if fcntl is None:
        return [Issue("LOCK_UNAVAILABLE", "this platform has no fcntl file locking; transition is supported on POSIX only")]
    folder = os.path.dirname(os.path.abspath(path))
    root = project_root(path)
    if root is not None and not _inside(root, folder):
        return [Issue("SYMLINK_REFUSED", f"{folder} resolves outside the project root {root} (symlinked parent folder)")]
    parts = folder.split(os.sep)
    if ".dev" in parts:  # no symlinked folder between the graph and its .dev folder
        dev = os.sep.join(parts[:len(parts) - parts[::-1].index(".dev")])
        current = folder
        while True:
            if os.path.islink(current):
                return [Issue("SYMLINK_REFUSED", f"{current} is a symlink; refusing to write through it")]
            if current == dev:
                break
            current = os.path.dirname(current)
    events_path = os.path.join(folder, "events.jsonl")
    lock_path = os.path.join(folder, ".graph.lock")
    for p in (path, events_path, lock_path):
        refused = _refuse_symlink(p)
        if refused:
            return [refused]
    lock_fd = os.open(lock_path, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        with open(path, encoding="utf-8") as fh:
            original_text = fh.read()
        g = json.loads(original_text)
        if not isinstance(g, dict):
            return [Issue("UNREADABLE", "graph root must be a JSON object")]
        before, _ = check_graph(g, requirements_dir)
        if any(e["code"] in {"SCHEMA", "DUP_ID", "UNKNOWN_DEP", "CYCLE"} for e in before):
            return [Issue("INVALID_GRAPH", "fix structural validate errors before transitions")] + before
        nodes = _node_map(g)
        if node not in nodes:
            return [Issue("UNKNOWN_NODE", f"no node {node!r}")]
        current = nodes[node]["status"]
        if to not in TRANSITIONS.get(current, set()):
            return [Issue("ILLEGAL_TRANSITION", f"{current} -> {to} is not allowed", node)]
        if not evidence.strip():
            return [Issue("NO_EVIDENCE", "every transition needs evidence text", node)]
        if to in STARTED | {"ready"}:
            pending = [d["node"] for d in nodes[node]["depends_on"] if nodes[d["node"]]["status"] not in SATISFIED]
            if pending:
                return [Issue("STATUS_DEP", f"dependencies not satisfied: {pending}", node)]
        if current == "done" and to == "ready":
            started = sorted(nid for nid, n in nodes.items()
                             if n["status"] not in {"planned", "ready", "cancelled"}
                             and any(d["node"] == node for d in n["depends_on"]))
            if started:
                return [Issue("ILLEGAL_REOPEN", f"dependents already past ready: {started}; move unfinished ones back to planned first, and for done or accepted ones add a new node instead of reopening", node)]
        # Moving forward needs a clean node and a clean graph; parking a node
        # (planned, blocked, cancelled) is allowed while other errors are open,
        # so a writer can be recorded as waiting on the user's decision.
        if to not in {"planned", "blocked", "cancelled"}:
            blocking = [e for e in before if e.get("node") in (None, node)]
            if blocking:
                return [Issue("INVALID_GRAPH", f"resolve these errors before moving {node} to {to}", node)] + blocking
        nodes[node]["status"] = to
        after, _ = check_graph(g, requirements_dir)
        new = [e for e in after if _is_new_error(e, before)]
        if new:
            return [Issue("TRANSITION_BREAKS_GRAPH", f"{current} -> {to} would add errors; re-plan first", node)] + new

        seq = 1
        if os.path.exists(events_path):
            with open(events_path, "rb") as fh:
                raw = fh.read()
            if raw and not raw.endswith(b"\n"):
                return [Issue("EVENTS_CORRUPT", "events.jsonl does not end with a newline (torn write); repair it before new transitions")]
            seq = sum(1 for line in raw.splitlines() if line.strip()) + 1
        event = {
            "seq": seq,
            "at": _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds"),
            "actor": actor,
            "node": node,
            "from": current,
            "to": to,
            "evidence": evidence,
        }
        _atomic_write(path, json.dumps(g, indent=2, ensure_ascii=False) + "\n")
        line = (json.dumps(event, ensure_ascii=False) + "\n").encode("utf-8")
        try:
            fd = os.open(events_path, os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o644)
            try:
                start = os.fstat(fd).st_size
                try:
                    view = memoryview(line)
                    while view:
                        written = os.write(fd, view)
                        if written <= 0:
                            raise OSError("short write to events.jsonl")
                        view = view[written:]
                    os.fsync(fd)
                except OSError:
                    os.ftruncate(fd, start)  # drop a partial or unsynced line
                    raise
            finally:
                os.close(fd)
        except OSError as exc:
            try:
                _atomic_write(path, original_text)  # keep graph and event log consistent
            except OSError as restore_exc:
                return [Issue("GRAPH_EVENT_MISMATCH",
                              f"event not recorded ({exc}) and graph restore failed ({restore_exc}); "
                              f"graph.json shows {node}={to} without an event. Fix by hand before continuing", node)]
            return [Issue("EVENT_WRITE_FAILED", f"event not recorded, graph restored: {exc}", node)]
        return []
    finally:
        os.close(lock_fd)


def evidence_file_ref(graph_path: str, file_path: str) -> tuple[str | None, Issue | None]:
    """Reference an evidence file by project-relative path and SHA-256, never by content.

    events.jsonl is committed by default, so copying file text into it could
    publish a private file, and an absolute or outside path could publish a
    private path (REQ-011, R-AUTH-7). Only a regular file inside the project
    root is accepted, and the last component of its path must not be a symlink.
    """
    def refuse(reason: str) -> tuple[None, Issue]:
        return None, Issue("EVIDENCE_FILE_REFUSED", f"{file_path}: {reason}")

    root = project_root(graph_path)
    if root is None:
        return refuse("no project root (.git or .dev/) above the graph file")
    if os.path.islink(file_path):
        return refuse("is a symlink")
    real = os.path.realpath(file_path)
    rel = os.path.relpath(real, os.path.realpath(root)).replace(os.sep, "/")
    if os.path.isabs(rel) or rel == ".." or rel.startswith("../"):
        return refuse("resolves outside the project root")
    try:
        if not stat.S_ISREG(os.lstat(real).st_mode):  # also keeps a FIFO from blocking the open
            return refuse("is not a regular file")
        digest = hashlib.sha256()
        with open(real, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 16), b""):
                digest.update(chunk)
    except OSError as exc:
        return refuse(f"cannot read ({exc.strerror})")
    return f"file:{rel} sha256:{digest.hexdigest()}", None


def _atomic_write(path: str, text: str) -> None:
    folder = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".graph-", suffix=".tmp", dir=folder)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            if os.path.exists(path):
                os.fchmod(fh.fileno(), os.stat(path).st_mode & 0o7777)  # keep the original mode
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def _emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("validate", "ready"):
        p = sub.add_parser(name)
        p.add_argument("graph")
        p.add_argument("--requirements-dir")
    p = sub.add_parser("transition")
    p.add_argument("graph")
    p.add_argument("node")
    p.add_argument("status", choices=sorted(STATUSES))
    ev = p.add_mutually_exclusive_group(required=True)
    ev.add_argument("--evidence", help="short reference: a commit SHA, a report path, a command")
    ev.add_argument("--evidence-file", help="record a project file as evidence by relative path and SHA-256 (never its content)")
    p.add_argument("--actor", default="main-agent")
    p.add_argument("--requirements-dir")
    args = parser.parse_args(argv)

    if not os.path.isfile(args.graph):
        print(json.dumps({"ok": False, "errors": [Issue("UNREADABLE", f"no graph file at {args.graph}")]}), file=sys.stderr)
        return 2
    req_dir, problem = find_requirements_dir(args.graph, args.requirements_dir)
    if problem:
        _emit({"ok": False, "errors": [problem]})
        return 1

    try:
        if args.cmd == "transition":
            evidence = args.evidence
            if args.evidence_file:
                evidence, refused = evidence_file_ref(args.graph, args.evidence_file)
                if refused:
                    print(json.dumps({"ok": False, "errors": [refused]}, ensure_ascii=False), file=sys.stderr)
                    return 2
            errs = transition(args.graph, args.node, args.status, evidence, args.actor, req_dir)
            if errs and errs[0]["code"] == "UNREADABLE":
                print(json.dumps({"ok": False, "errors": errs}, ensure_ascii=False), file=sys.stderr)
                return 2
            _emit({"ok": not errs, "errors": errs})
            return 1 if errs else 0
        g = load(args.graph)
    except RecursionError:
        print(json.dumps({"ok": False, "errors": [Issue("GRAPH_TOO_DEEP", "dependency chain too deep to check")]}), file=sys.stderr)
        return 2
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [Issue("UNREADABLE", str(exc))]}), file=sys.stderr)
        return 2

    try:
        errors, warnings = check_graph(g, req_dir)
    except RecursionError:
        print(json.dumps({"ok": False, "errors": [Issue("GRAPH_TOO_DEEP", "dependency chain too deep to check")]}), file=sys.stderr)
        return 2
    if args.cmd == "validate":
        _emit({"ok": not errors, "errors": errors, "warnings": warnings})
        return 1 if errors else 0
    # A writer parked (planned or blocked) on a conflicting REQ waits for the
    # user; it must not stall the rest of the graph. Any other error still stops.
    statuses = {n["id"]: n["status"] for n in g["nodes"]}
    waiting = {e["node"] for e in errors
               if e["code"] == "REQUIREMENT_CONFLICT" and statuses.get(e.get("node")) in {"planned", "blocked"}}
    other = [e for e in errors if not (e["code"] == "REQUIREMENT_CONFLICT" and e.get("node") in waiting)]
    if other:
        _emit({"ok": False, "errors": other})
        return 1
    print(json.dumps({"ready": ready_nodes(g, waiting), "waiting_on_conflict": sorted(waiting),
                      "warnings": warnings}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
