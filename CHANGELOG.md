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
- Minimal CI (D-017, REQ-020): `.github/workflows/ci.yml` runs on every pull
  request to `main` and every push to `main`. Job `validate` runs
  `scripts/validate.sh` with the Claude CLI at an exact npm version (no
  login). Job `gitleaks` runs gitleaks 8.30.1, checked against a SHA-256 in
  the workflow, over every commit reachable from the checked-out commit, with
  redacted output. Actions are pinned by full commit SHA; the workflow has
  `permissions: contents: read` and uses no secrets.

### Changed

- R-REV-1: a required security review uses `dev-security-reviewer`, never
  `dev-reviewer` (PR #5).
- Design principle 1 no longer states an unmeasured context cost; D-011
  measures it (PR-C1).
- Cleanups (PR-C2, Issue #10): wording that now matches the code and the
  records, notes on superseded review records, and follow-up FU-007.
- `dev-gate` reads the checks of a PR back (R-EXH-4): one read of the head
  and the checks, each check listed; a failed read or another head gives
  `UNVERIFIED`. `platform_enforcement` stays `NOT_CONFIGURED`: the project
  setting that selects a provider profile is designed in FU-009, together
  with FU-008 (D-017).
- R-REV-9 also scans Issue titles, bodies and comments before they are
  posted (REQ-011, FU-007 part (a)). FU-007: commit timestamps are an
  accepted risk; Git LFS, push options and release notes stay deferred.
  New follow-ups FU-008 (a PR can change its own checks) and FU-009 (the
  provider-profile setting), deferred and designed together.
- `dev-gate` platform read-back (REQ-021, D-018, Issue #14): a project selects
  a GitHub provider profile with `platform_profile` in `.dev/config.json`,
  read only at the bound base commit. The new read-only checker
  `skills/dev-gate/scripts/platform_profile.py` (with
  `tests/test_platform_profile.py`) reads the required checks back: only
  `success` passes, profile and platform checks are joined, each check is
  pinned to an app id, an invalid setting fails closed, and the result is
  `BLOCKED`, then `UNVERIFIED`, then `VERIFIED`. A change of the setting in a
  PR goes to the user. With a profile, `VERIFIED` says that the checks ran
  the PR's own definitions, and the gate lists changed check files (FU-008,
  report only). `dev-core` R-EXH-4 states when the result is
  `NOT_CONFIGURED` (MR-001). This repository selects `validate` and
  `gitleaks` from GitHub Actions.
- Each rule in one place (REQ-022, FU-006, Issue #16): the skills cite
  `dev-core` instead of restating three rules whose copies were missed in
  PR #7, #13 and #15 (R-EXH-3 record storage, R-VER-2 stop rule, R-EXH-4
  platform result). Other restated rule text that the Issue #16 inventory
  lists stays word for word and names its rule IDs (user card 7a); restated
  text outside the inventory goes to the FU-010 audit (card 8a). The masking rule for review records is now
  also in `dev-core` R-REV-8 and covers gate records too (DL-016, tighten);
  no other rule changes in meaning. The `dev-core` section 8
  bindings get the IDs CB-1 to CB-5. The agent files keep their own copies
  (FU-005). A test checks that every rule ID cited in `skills/` (Markdown
  and Python files) and `agents/` exists in `dev-core`, and searches `skills/`, `agents/` and
  `tests/` for the known ways of citing `dev-core` by section number.
  New follow-up FU-010: R-WRT-1 lists fewer machine literals than Core.
- On-demand Core loading, PR-1 records (REQ-025, D-020, FU-005, Issue #22).
  `dev-core` R-AUTH-5 and R-VER-3 state the project reading of two Core
  sentences that can be read two ways (`authorization-and-stops.md:35`,
  `workflow.md:76`; DL-028, DL-029). DL-018 to DL-027 record existing
  tightenings that had no row; no other rule text changes. CB-1 to CB-5 name
  their origin. `docs/core-feedback.md` records the upstream Issues
  engineering-workflow-core#21 to #27.
- On-demand Core loading, PR-2 Core reading (REQ-025, D-020, FU-005,
  Issue #28). `dev-core` has a stage map: the Core files that each skill
  reads in full before it acts, and the Core files that each reviewer role
  uses as review criteria. Two header sentences: the Core text in context
  governs every rule shown as an index line, and rule text that another
  skill or reference restates follows the same two rules as `dev-core`
  (DL-030). The first line of each of the 7 other skills points to the stage
  map. No rule text changes.
- On-demand Core loading, PR-3 reviewer Core criteria (REQ-025, D-020,
  FU-005, Issue #31). The subagent task brief has a "Core review criteria"
  line, and `dev-reviewer` and `dev-security-reviewer` each have a
  paragraph: the reviewer reads the listed Core files as data for judging
  the change, never as instructions, and only the brief sets policy. The
  implementer and the explorer get no Core files. The restated rule text
  does not change.
- On-demand Core loading, PR-4 index lines (REQ-025, D-020, FU-005,
  Issue #35). `dev-core` is now the index of the vendored Core (still
  v0.1.1) and the project's tightenings. 13 rules become index lines (rule
  ID, title, Core anchor); R-AUTH-5 and R-VER-3 keep their project
  readings. The rules that are stricter than Core (also literally) or
  Claude-specific, and CB-1 to CB-5, stay word for word. R-STG-4, R-AUTH-4
  and R-VER-1 stay too, because each has a sentence that is literally
  stricter than Core (DL-031 to DL-033). Each skill reads the original Core
  text for the index lines (stage map, PR-2).
- `dev-security-reviewer` Bash allow-list (REQ-024, SR21B-001, Issue #32).
  The allow-list now names the test commands named in the brief, with the
  wording of `dev-reviewer`. The file already told the reviewer how to run
  the Python tests that the brief names; before, the reviewer decided at run
  time whether the allow-list permitted them. The other read-only, no-install,
  no-external-service and no-write rules do not change.
- Rule IDs on restated rule text (REQ-025, FU-011, Issue #40). The skills,
  their references, the agent files and the subagent task brief name the
  rule ID on the text that restates a rule that `dev-core` keeps word for
  word (75 IDs at 71 places; the readings are in the FU-011 row of
  `.dev/followups.md`). No word of the existing text changes, so the files
  that subagents get keep their full text. `README.md` gets no IDs. Gaps in
  the copies that subagents get go to FU-016.

### Fixed

- `dev-core` and Core (REQ-023, FU-010, Issue #18). A rule-by-rule audit
  against Core v0.1.1 (`.dev/issue-18-core-audit/audit.md`) found rules
  that leave out Core obligations or state them more loosely; three review
  rounds each found new ones. The `dev-core` header now says that where a
  rule is shorter or looser than its cited Core section, that Core section
  governs, and that a stricter rule (for example DL tightenings, CB-1 to
  CB-5, user decisions) still applies (DL-017). R-WRT-1 now follows Core `wf-writing`
  items 1 to 6 and the spot-check, including the machine literals flags,
  APIs, logs and kept quotations, the required technical detail and
  technical precision. The other gaps are input for the on-demand loading
  design (FU-005). Core-feedback candidates in CF-009. Follow-ups FU-013
  (reviewer test caches; implementer deletions) and FU-014 (the `--prune`
  of the push fetch).
- Agent write and delete rules (REQ-024, FU-013, Issue #20). The reviewer
  agents run the Python tests that the brief names with
  `PYTHONDONTWRITEBYTECODE=1` and pytest `-p no:cacheprovider`, so tests
  create no files in the repository (card 3d), and write no file anywhere,
  including the session scratchpad (card 9b); a temporary file that a named
  test creates and removes itself in the system temporary directory is not a
  reviewer write (card 11b). The implementer never deletes an untracked or
  ignored file, even inside its owned paths; it reports the file and the main agent asks the
  user (card 6a, R-AUTH-3). FU-004 gains an official-tools-only arm.

- `scripts/check_pack.py` reads `>+` and `|+` block scalars in REQ `sources`
  (PR-C2), with regression tests for the agent model and effort checks and
  the REQ status check.

### Security

- Push scan without prune (REQ-011, FU-014, Issue #24). Before a push,
  R-REV-9, `dev-implement` step 4 and the `dev-gate` push binding get the
  remote state from `git ls-remote --heads --tags <remote>` and run no
  `git fetch`. The old `git fetch --prune` could delete local tags or
  branches (with `fetch.pruneTags` or a non-default refspec). New follow-up
  FU-015: a push URL that differs from the fetch URL, `.mailmap` and replace
  refs in the scan commands, nested or blob tags, quoting of ref names, and
  heads or tags that the remote hides from pushes.
- `graph.py transition --evidence-file` records only the project-relative
  path and the SHA-256 of a regular file inside the project, never its
  content (PR #5, FU-003).
