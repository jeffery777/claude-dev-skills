# Task graph schema (`claude-dev-graph/v1`)

The graph is coordination data (CB-1). It never proves completion and never grants
authority (R-AUTH-1, R-VER-1). Location: `.dev/<objective-id>/graph.json`.
`graph.py transition` appends to `events.jsonl` in the same folder.

```json
{
  "schema": "claude-dev-graph/v1",
  "objective": {
    "id": "OBJ-login-rate-limit",
    "title": "Rate-limit login attempts",
    "rigor": "standard",
    "requirements": ["REQ-001", "REQ-002"]
  },
  "nodes": [
    {
      "id": "T2",
      "title": "Add limiter middleware",
      "kind": "implement",
      "requirements": ["REQ-001"],
      "depends_on": [{"node": "T1", "consumes": "auth call-site list"}],
      "owns": ["src/auth/limiter/**"],
      "risk": "high",
      "review": "security",
      "status": "ready",
      "dod": ["6th attempt in 60s returns 429"],
      "verify": ["pytest tests/auth/test_limiter.py"]
    }
  ]
}
```

## Fields

| Field | Values | Notes |
| --- | --- | --- |
| `objective.rigor` | `standard`, `strict` | `light` work has no graph file (R-RIG-1) |
| `kind` | `explore`, `implement`, `docs`, `verify`, `review`, `gate`, `human_gate` | `implement` and `docs` are write nodes |
| `requirements` | `REQ-…` ids from `objective.requirements` | Required on write nodes |
| `depends_on[].consumes` | Text naming the data that crosses the edge | Missing means a fake edge |
| `owns` | Repository-relative path globs (no absolute paths, no `..`) | Required on write nodes; parallel writers must not overlap |
| `risk` | `low`, `medium`, `high`, `unknown` | `high` or `unknown` write nodes need `deep` or `security` review (R-REV-6) |
| `review` | `none`, `routine`, `deep`, `security` | `strict` forbids `none` on write nodes |
| `status` | `planned`, `ready`, `in_progress`, `blocked`, `reviewing`, `done`, `accepted`, `cancelled` | Change only through `graph.py transition`. Nodes and edges change by re-planning (`dev-plan`), followed by `validate` |

## Status transitions

```text
planned  -> ready | blocked | cancelled
ready    -> in_progress | blocked | cancelled
in_progress -> ready | reviewing | blocked
blocked  -> planned | ready | cancelled
reviewing -> in_progress | done | blocked
done     -> accepted | ready
accepted, cancelled: terminal
```

- `done` means the node's evidence is complete. `accepted` means a human or a
  formal gate accepted it. Never set `accepted` on your own judgment.
- A node can become `ready` or start only when every dependency is `done` or `accepted`. A cancelled dependency is never satisfied.
- `ready` lists nodes whose dependencies are satisfied. A listed node that is still `planned` moves to `ready` before `in_progress`.
- Every transition needs `--evidence` text. Point to the commit, the command
  output or the review report; the text itself is not evidence (CB-1).

## Error codes (`graph.py validate`)

| Code | Meaning |
| --- | --- |
| `SCHEMA` | Missing field or a value outside the enum |
| `DUP_ID` | Two nodes share an id |
| `UNKNOWN_DEP` | A dependency names a missing node |
| `CYCLE` | A dependency cycle; review and fix loops are not edges (Core default: re-assess after two unfinished rounds, R-VER-2) |
| `FAKE_EDGE` | An edge does not say what it consumes |
| `NO_REQUIREMENT` | A write node has no requirement anchor (possible scope creep; R-RIG-3) |
| `UNKNOWN_REQUIREMENT` | A node cites a requirement not in the objective |
| `MISSING_REQUIREMENTS_DIR` | No project root (`.git` or `.dev/`) above the graph file, or the resolved requirements folder does not exist (exit 1) |
| `MISSING_REQUIREMENT_FILE` | A declared requirement has no `REQ-xxx-*.md` file |
| `DUPLICATE_REQUIREMENT_FILE` | Several files claim the same requirement id |
| `REQUIREMENT_ID_MISMATCH` | The file name and the front matter `id` disagree |
| `REQ_RELATION_UNKNOWN` | A REQ relation field (`depends_on`, `refines`, `conflicts_with`, `superseded_by`) names a missing REQ |
| `REQ_DEPENDENCY_CYCLE` | REQ `depends_on` relations form a cycle |
| `REQUIREMENTS_DIR_OUTSIDE` | The requirements folder (configured, found, or given with `--requirements-dir`) resolves outside the project root |
| `BAD_CONFIG` | `.dev/config.json` cannot be read or has a bad `requirements_dir` (exit 1) |
| `BAD_REQUIREMENT_STATUS` | A cited REQ has a status outside the allowed set (statuses are case-sensitive) |
| `REQUIREMENT_CONFLICT` | An open write node cites a REQ whose status is `conflict`; the user must decide first. `validate` fails. `ready` still lists the other nodes when the only such errors are on writers parked as `planned` or `blocked`, and reports those writers under `waiting_on_conflict` |
| `RISK_REVIEW` | The review mode is too weak for the risk or the rigor |
| `NO_OWNERSHIP` | A write node declares no owned paths |
| `OWNERSHIP_OVERLAP` | Two unfinished writers with no live dependency path between them own overlapping paths, compared case-insensitively (reported on both nodes; finished writers are not compared) |
| `STATUS_DEP` | A node is `ready` or past it while a dependency is not `done` or `accepted` |

Transition errors:

- `ILLEGAL_TRANSITION`, `NO_EVIDENCE`, `UNKNOWN_NODE`, `UNREADABLE` (exit 2), `GRAPH_TOO_DEEP` (exit 2)
- `INVALID_GRAPH`: structural errors (schema, duplicate ids, unknown dependencies, cycles) block every transition; other errors block moving a node forward when they concern that node or the whole graph. Moving a node to `planned`, `blocked` or `cancelled` stays possible, so a writer can wait for the user's decision on a `REQUIREMENT_CONFLICT`
- `ILLEGAL_REOPEN`: moving a `done` node back to `ready` while a dependent is past `ready` (including `blocked`)
- `TRANSITION_BREAKS_GRAPH`: the transition would add errors, for example cancelling the only node that orders two overlapping writers, or reopening a node while a dependent is `ready`; re-plan or move the dependent back first
- `SYMLINK_REFUSED`: the graph, event log or lock is a symlink, a folder between the graph and its `.dev` folder is a symlink, or the graph's folder resolves outside the project root
- `LOCK_UNAVAILABLE`: no `fcntl` file locking (non-POSIX platform); transitions are supported on POSIX only
- `EVENTS_CORRUPT`: `events.jsonl` ends with a torn line; repair it first
- `EVENT_WRITE_FAILED`: the event could not be written completely; the partial line was removed and the graph restored
- `GRAPH_EVENT_MISMATCH`: the event failed and the restore failed too; fix by hand before continuing

Warnings:

- `UNUSED_REQUIREMENT`: a declared requirement has no node.
- `INACTIVE_REQUIREMENT`: an open node cites a `dropped` or `superseded` requirement.
- `STRANDED`: an open node depends on a cancelled node, so it can never become ready; re-plan the edge or cancel the node.

Every command checks the requirement files. The folder is resolved inside the
project root (the nearest ancestor of the graph file that holds `.git` or
`.dev/`): `requirements_dir` from `<root>/.dev/config.json`, else
`<root>/docs/requirements/`. The search never climbs above the project root,
and a configured path that resolves outside it is refused.

REQ front matter is read with a small YAML subset. The `frontmatter`
docstring in `scripts/graph.py` lists what is supported; input outside the
subset is a format limit, not a defect.

A crash between the graph write and the event append can leave a status change
without its event (an accepted trade-off of writing the graph first). Compare
`graph.json` with the last events after an interrupted run.

`transition` runs the same checks, including `REQUIREMENT_CONFLICT`, under an
exclusive lock (`.graph.lock`). It refuses to write through symlinks, writes
`graph.json` atomically through a temporary file, then appends the event. If the
event cannot be written, the graph is restored. Add `.dev/**/.graph.lock` and
`.dev/**/.graph-*.tmp` to the project's `.gitignore` so that the lock and
temporary files are never committed (CB-1).

## Commands

```bash
python3 graph.py validate <graph> [--requirements-dir DIR]
python3 graph.py ready <graph> [--requirements-dir DIR]     # {ready, waiting_on_conflict, warnings}
python3 graph.py transition <graph> <node> <status> --evidence 'abc1234 tests pass' [--actor NAME]
python3 graph.py transition <graph> <node> <status> --evidence-file <path>   # records file:<relative path> sha256:<hex>
```

Pass evidence as a short reference in single quotes (a commit SHA, a report
path, a command name). Never paste receipt or tool text into a double-quoted
shell argument. For longer evidence, save it as a report in the project (for
example under `.dev/<objective-id>/reviews/`) and pass `--evidence-file`.
`events.jsonl` is committed by default (CB-1), so `--evidence-file` never copies the
file's content: it records the project-relative path and the SHA-256. It
refuses a path whose last component is a symlink, a file that is not a regular file (such as a FIFO), a
missing file, and a path that resolves outside the project root
(`EVIDENCE_FILE_REFUSED`, exit 2) (REQ-011). It needs a project root. Do not
point it at a secret file: the hash of a short, guessable file can be guessed
offline.

Requires a shell with Python 3. Where no shell is available (for example a
Cowork session without code execution), apply the same rules by hand: check
each error code in the table above against `graph.json` and the REQ files, and
record status changes and evidence in `events.jsonl` yourself. Say in the
report that the checks were manual.
