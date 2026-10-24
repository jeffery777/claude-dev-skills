# Requirements wiki format (D-003)

The requirements anchor the work against over-engineering. They are plain
Markdown in Git, so Claude, Codex and Grok Build can all read them without
extra tools. Obsidian is an optional viewer. Graphify is an optional index
and never the source.

## Where it lives

- Each target project keeps its own wiki. The default location is
  `docs/requirements/`; a project can set another one in `.dev/config.json`:
  `{"requirements_dir": "spec/requirements"}`.
  The same file holds `"commit_state"` (default `true`), which decides
  whether `.dev/<objective-id>/` state files are committed (CB-1),
  and the optional `"platform_profile"`, which selects a provider profile for
  the merge gate (`dev-gate/references/platform-profile.md`). Other top-level
  keys make the merge gate fail closed.
- Before you create the folder in a project for the first time, ask the user.
- When the project already has a formal requirements system (Jira,
  Confluence, a PRD), the wiki is an index only. Each REQ cites the original
  with `type: external` and a precise `locator` (issue key, page URL plus
  section, document version).
- Confidential text never leaves the project. Do not copy it into another
  repo, into memory, into briefs for external services, or into public
  artifacts. When you are unsure, record the `locator` and leave `quote` empty
  (`""`).

## Layout

```text
<requirements_dir>/
  index.md              # one row per requirement: ID, title, status, [[file]]
  log.md                # append-only change log
  REQ-001-login-rate-limit.md
```

Templates: `${CLAUDE_SKILL_DIR}/templates/` (`REQ-template.md`, `index.md`, `log.md`).

## Fields

| Field | Rule |
| --- | --- |
| `id` | `REQ-` plus at least three digits; it must match the file name prefix |
| `status` | `proposed`, `active`, `conflict`, `done`, `superseded`, `dropped` |
| `sources[]` | Each entry has `type` (`doc`, `chat`, `issue`, `commit`, `external`), a `locator` precise enough to find the original again, and a verbatim `quote` |
| `non_goals` | Exclusions stated in the sources |
| `depends_on`, `refines`, `conflicts_with`, `superseded_by` | Typed relations; each is a list of existing REQ ids. `graph.py validate` rejects unknown ids and `depends_on` cycles |
| `superseded_reason` | Required when the status is `superseded` |

Locator examples:

- `docs/prd.pdf p.12`
- `README.md#install`
- `Claude Code session 2026-10-20, user message 1`
- `https://github.com/org/repo/issues/42#issuecomment-123`
- `commit 3f2c9a1`
- `JIRA PROJ-881 v3`

The quotes are the originals and live only in `sources`. Your own summary
goes in the `Need` section. Never merge the two.

## Relations and views

The typed relation fields are the requirement graph. `[[wiki links]]` in the
body are for reading only. Obsidian's graph view can be used to browse the
folder, but its links have no types, so it cannot replace these fields.

Every rendering — Mermaid, HTML, an Artifact, Obsidian — is a projection
regenerated from the REQ files, `graph.json` and Git. A projection is never
authority or completion evidence (R-AUTH-1), and nobody edits it back into a source.

## Operations

- **Ingest.** Write each new need as a REQ file. Put the exact words in
  `sources[].quote` and the location in `locator`. Anything you inferred stays
  `proposed` until the user confirms it. If an existing REQ already covers the
  need, add the new source to that REQ instead of creating a duplicate.
- **Conflict.** When sources contradict each other, keep both, each with its
  locator, under `## Conflicts`, set `status: conflict`, and list the other REQ
  in `conflicts_with` when the conflict is between two requirements. Ask the user.
  Never pick a side or overwrite one. `graph.py` blocks open write tasks that
  cite a conflicting REQ.
- **Supersede.** Never delete a requirement. Set `status: superseded`, and
  fill in `superseded_by` (a list) and `superseded_reason`.
- **Log.** Record every change in `log.md` with the date, the REQ, the change
  and the source locator. Never rewrite earlier lines.
- **Query.** Read `index.md` first, then only the REQ files you need (R-EVD-2).
- **Lint** (manual in Phase 1; a script is planned for Phase 2). Check for
  contradictions, orphan pages, superseded REQs that open tasks still cite,
  and acceptance criteria that nothing verifies. Report what you find; do not
  silently fix it.

## Rule of use

A change that no `REQ-…` covers is either a missing requirement (ask the user)
or a `SCOPE-CREEP` finding (R-RIG-3). Never generalize a requirement on your
own.
