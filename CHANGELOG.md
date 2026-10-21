# Changelog

All notable changes to this project are recorded in this file. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Every entry names the upstream `engineering-workflow-core` version that the
pack follows. Every change of the Core pin gets its own entry. No version is
released yet: the first tagged release waits for FU-001 (GitHub Issue #3,
Cowork runtime test). At that release,
`[Unreleased]` becomes `[0.1.0] - <date>` and serves as the release notes.

## [Unreleased]

### Added

- Upstream: `engineering-workflow-core` v0.1.1
  (`jeffery777/engineering-workflow-core`), tag object
  `7ce698fa853106c8ef44c4240c9334762da5ffb0`, commit
  `7b66978a76597d09be1b55ad199a969b4ee59c0f`. The pin is in
  `vendor/engineering-workflow-core.lock.json` and is checked by
  `scripts/verify_core.py`.
- Phase 1 (PR #2, Issue #1):
  - The vendored Core v0.1.1 (14 files) with a digest lock.
  - `dev-core`: an execution digest of Core whose rules cite Core anchors,
    with a source map, deltas and a coverage check of all 21 anchors.
  - Skills `dev-plan`, `dev-implement`, `dev-review`, `dev-gate`,
    `dev-docs`, `dev-continue` and `dev-deliver`.
  - Agents `dev-explorer`, `dev-implementer`, `dev-reviewer` and
    `dev-security-reviewer`. The reviewers have no Edit or Write tools;
    read-only Bash use is enforced by instructions only.
  - The G0 task graph: `graph.py` (Python standard library only) with schema,
    cycle, ownership, requirement-anchor and REQ-relation checks, and locked
    transitions.
  - Requirements wiki templates and REQ-001 to REQ-010.
  - Plugin `dev-skills` 0.1.0, the marketplace manifest and
    `scripts/validate.sh`.
- Security review before every commit and push (PR #5, Issue #4; D-015,
  REQ-011): a `dev-security-reviewer` scan of the staged diff and the commit
  identity and message before every commit, of everything a push sends
  before every push, of PR text before it is posted, and of every commit and
  the merge or squash commit at merge (R-REV-9, DL-010).
- Review convergence, decision cards and requirement relation (PR #7,
  Issue #6; D-013, D-014, D-016, REQ-012 to REQ-014): severity thresholds,
  classification before fixing, a narrow confirmation before a push, a stop
  rule for the fix loop, review records stored without a new head, a fixed
  decision card, `requirement_relation` and the `REQ-GAP` category.
- Decisions D-009 to D-012 (PR-C1, Issue #8; REQ-002, REQ-015 to REQ-019):
  graph engineering in stages, no agent memory, a deployment and measurement
  plan, and the handoff evaluation in `dev-continue`. Also this changelog and
  `docs/core-feedback.md`.

### Changed

- R-REV-1: a required security review uses `dev-security-reviewer`, never
  `dev-reviewer` (PR #5).
- Design principle 1 no longer states an unmeasured context cost; D-011
  measures it (PR-C1).
- Cleanups (PR-C2, Issue #10): wording that now matches the code and the
  records, notes on superseded review records, and follow-up FU-007.

### Fixed

- `scripts/check_pack.py` reads `>+` and `|+` block scalars in REQ `sources`
  (PR-C2), with regression tests for the agent model and effort checks and
  the REQ status check.

### Security

- `graph.py transition --evidence-file` records only the project-relative
  path and the SHA-256 of a regular file inside the project, never its
  content (PR #5, FU-003).
