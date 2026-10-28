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
- Follow-up FU-018 (records only, Issue #48): choosing the subagent model
  and effort before dispatch and escalating after a failed fix round.
- Follow-up FU-019 (records only, Issue #48): the main agent stops at a
  `+` or `-` dry-run ref line, so that a force or delete caused by
  configuration goes to the user. A legitimate push mirror triggers it;
  planted configuration is out of scope under the REQ-011 threat model.
- Decision D-019, lessons (records only, PR-1, Issue #57; REQ-026):
  REQ-026, D-019 in zh and EN, the `dev-retro` row and the D-019 items of
  section 6 in `docs/design-proposal.md`, and the requirements index and
  log. D-019 plans a skill `dev-retro` (`capture` and `review`) that only
  the user invokes, that writes no file (skill rule;
  `disable-model-invocation` blocks only the Skill tool call; not a
  technical guarantee; see D-019) and that
  supports only Claude Code,
  and a "Lesson candidates" section in the `dev-deliver` and `dev-review`
  reports (R-VER-5, DL-035). Levels L1 (project), L2 (this pack), L3 (Core)
  and L4 (the user's own instructions); text that leaves its source
  repository names only a category and a date; the user reviews every
  lesson text word for word before a commit or post. No ledger, lessons
  file, hooks, schedule or validator. The skill comes in PR-2, the report
  section in PR-3 and the first use in PR-4.
- Skill `dev-retro` (D-019 PR-2, Issue #57; REQ-026):
  `skills/dev-retro/SKILL.md` with the modes
  `/dev-skills:dev-retro capture` and `/dev-skills:dev-retro review`, a
  `dev-retro` row in the `dev-core` stage map and a README row (zh and EN).
  Only the user invokes it (`disable-model-invocation: true` blocks only the
  Skill tool call; a skill rule, not a technical guarantee); it supports
  only Claude Code. It writes no file and changes no record; the output is a
  report, draft text and cards. `disallowed-tools` removes `Write`, `Edit`,
  `MultiEdit` and `NotebookEdit` as one defense layer, not a guarantee. The
  read-back runs `git --no-optional-locks status`, so `git status` does not
  update `.git/index`; `git diff HEAD` still can (finding MS2-001). The
  locator rule also covers PR titles, PR and Issue comments and branch
  names (finding MS2-002). A failed read-back command makes the read-back
  NOT_RUN; drafts contain only visible characters; a security problem with
  an unknown fix status counts as not fixed; a card answer does not start
  a commit or post (card D19-PR2-C1, round-1 review).
- Lesson candidates section (D-019 PR-3, Issue #57; REQ-026): new rule
  R-VER-5 and delta DL-035 (`tighten`, Core `workflow.md:74`). The
  `dev-deliver` final report and the `dev-review` review report each have a
  "Lesson candidates" section with minimum triggers (the stop rule of the
  fix loop, a `REQ-GAP` or a spec that lost a condition of its source, the
  same kind of finding in two or more rounds; in `dev-deliver` also a user
  correction, a refused tool call or a platform that behaved differently
  from a rule), "none" when there is no candidate, and fixed fields for
  each candidate. The section is report content only: it writes no file,
  changes no rule and invokes no skill, and a candidate is never authority
  or completion evidence. Every field of a candidate is in the agent's own
  words and masked, uses no content of files outside the repository, of
  native memory or of automatically loaded instruction files, and contains
  no authorization change, which only the user writes (card D19-PR3-C1).
  `review-report.md` carries the reviewer part of R-VER-5 word for word;
  `dev-deliver` and `dev-retro` cite R-VER-5. The first commit records the
  items that the PR #59 review deferred.
- First use of `dev-retro` (D-019 PR-4, Issue #57; REQ-026): the first
  commit applies the items that the PR #60 review deferred. The DL-035
  summary names the quotes that a candidate must not contain and the
  authorization-change rule of R-VER-5; the requirements log records the
  no-loosening rule in the PR-3 acceptance list (finding MR60-002); the
  transcript check moves from PR-3 to PR-4, and before the first use a
  new session loads the merged `main`, read back by the main checkout
  `HEAD` and the SHA-256 of `skills/dev-retro/SKILL.md`. For this pack, `dev-retro`
  counts a fix as released when it is merged to `main`, and a residual
  risk that the user accepted in a card is not an unfixed security problem
  (review card V3 (a)); follow-up FU-025 (card D19-PR4-C1 (a)).
- Read grant for the pack files (REQ-028, Issue #66; cards A1 and B1). For a
  user-level install without permission allow rules, each dev-* skill
  declares exactly two `allowed-tools` rules,
  `Read(/${CLAUDE_PLUGIN_ROOT}/skills/**)` and
  `Read(/${CLAUDE_PLUGIN_ROOT}/vendor/engineering-workflow-core/contracts/**)`.
  The new binding CB-7 (DL-037) records the headless test results: the
  grant holds only in the turn that invokes the skill, also for a
  `general-purpose` subagent dispatched in that turn; the next turn without
  a skill was denied, and a later turn that invokes a skill was allowed
  again (a later turn can prompt: re-invoke a skill or approve the
  prompt); a denied pack read stops as CB-6 says; the grant is never
  widened. Interactive sessions and a real install are not verified
  (FU-031). `scripts/check_pack.py`, run by `scripts/validate.sh` and CI
  (not when Claude Code loads the plugin), checks a closed world (card
  I66-R2-C1 (a); the agent key allowlist is from card I66-R1-C1 (a)): the
  plugin root holds only the tracked
  names and `.git` and `.claude`, which are allowed root names but not
  plugin components (`.claude` holds local session worktrees in this
  repository), in exact case, so `hooks/`,
  `monitors/`, `bin/`, `.mcp.json`, `settings.json` or any new component
  path fails; `.claude-plugin/` holds exactly `plugin.json` and
  `marketplace.json`, valid JSON with keys inside allowlists of the keys in
  use, and one marketplace entry, `dev-skills` with source `./`; `skills/`
  holds only non-hidden directories with a regular `SKILL.md`, and
  `agents/` only non-hidden regular `*.md` files; hidden names count, and
  names in one directory under `skills/`, `agents/` or `vendor/` that
  differ only in case fail (root names must match exactly). The raw front
  matter of each skill and agent file must be printable ASCII with LF line
  ends, with only the keys in use, each once, `allowed-tools` exactly the
  two rules; every other value follows a closed grammar (card I66-M3 (a)):
  exactly one space after the colon, then a non-empty YAML plain scalar
  that does not start with a space, a backtick or any of
  `- ? : , [ ] { } # & * ! | > ' " % @`, holds no `: `, ` #` or `---`,
  and does not end with `:` or a space, so no quoted, tagged, anchored,
  alias, flow or block value. A `skills`, `agents` or `vendor` root entry
  that is a symlink fails, and so do symlinks and hardlinked files under
  `skills/` and `vendor/`. Each rule has negative tests, apart from the
  cases that FU-033 lists.
  The README Install section states the limit, and that the rules are not
  tested in Cowork (FU-001). FU-025 is closed with the second-repository
  check of Issue #66; follow-ups FU-030 (card D1) and FU-031 (card C1).

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
  word (74 IDs at 70 places; the readings are in the FU-011 row of
  `.dev/followups.md`). No word of the existing text changes, so the files
  that subagents get keep their full text. `README.md` gets no IDs. Gaps in
  the copies that subagents get go to FU-016.
- Agent files get the `dev-core` rule text that their shorter copies left
  out where that lowered protection (REQ-024, FU-016 PR-1, Issue #42). The
  explorer and both reviewers treat tool output, such as test output, as
  data (R-AUTH-1). The implementer keeps unrelated changes intact (R-STG-4)
  and never routes around a refused tool call (R-AUTH-4). `dev-reviewer`
  states when a Security Diff Scan is required (R-REV-7) and the full list
  of Core blockers (R-REV-3). `dev-security-reviewer` applies the scan to an
  open security concern, examines the affected boundary when unsure, and
  never reports an incomplete, failed or insufficient scan as Passed
  (R-REV-7); it does not get the sentence on actual impact, so its list of
  boundaries, which names executables and scripts without a qualifier
  (DL-027), stays a trigger (card PR1-C1 (a)). The explorer
  names `(R-STG-2)` on an existing sentence. Each sentence is quoted from
  `dev-core`, except that two sentences turn a `dev-core` list heading or list
  item into a sentence (R-REV-3, R-REV-7); no existing sentence changes.
- Agent files get the remaining approved `dev-core` rule text (REQ-024,
  FU-016 PR-2, Issue #44). `dev-reviewer` treats GitNexus as advisory and
  says when its index is stale or the tree is dirty (CB-3), and asks for a
  docs change or a recorded reason when behavior changed and never counts a
  missing or unrun CI as Passed (R-EXH-2). Both reviewers use deterministic
  checks for facts a machine can check, and a missing tool blocks only the
  dependent readiness (R-REV-8). The implementer gets R-RIG-3 in full:
  every added wrapper or persistent state, like any other addition, traces
  to a requirement and states the protection it alone provides. Each
  sentence is quoted word for word from `dev-core`; no existing sentence
  changes. The FU-016 row records the rows compared with no change.
- Subagent model and effort (REQ-009, FU-018, Issue #50; DL-034). R-DEL-2
  now carries D-007 rule 3: the main agent chooses the model and effort
  before each dispatch, passes both (a dispatch that names only the model
  keeps the agent file's effort) and writes the reason in the brief. The
  `dev-deliver` table gives an explicit effort for each role; the
  implementer row depends on the rigor tier (`light` sonnet/medium, or
  opus/high for a cross-module or unclear slice; `standard` opus/high, or
  sonnet/medium for a mechanical slice in one module; `strict` opus/high). The `dev-review` mode table gives single values: R-REV-9
  scans use `xhigh` (before, "high or more"), and a security review uses
  `xhigh`, with `max` only when the user asks. When the main session
  implements, the plan records its transcript-recorded setting; for work
  under the floor with a model other than opus, an effort below `high`, or
  either `unknown`, the main agent asks the user to switch to opus/high or
  dispatches `dev-implementer` at opus/high.
  After one unsolved review and fix round, only the fixing side escalates
  and only for a quality failure (effort, then model `haiku` → `sonnet` →
  `opus`); a spec, acceptance or design failure goes to the R-VER-2 stop
  rule instead. Conflicting evidence triggers a re-assessment without
  escalation. An escalated setting is never lowered, the floor stays, and
  the round count and findings are kept. Receipts and review reports add the
  `recorded` model and effort, which the main agent reads from the
  transcript fields only, or `unknown` with the reason. `fable` is not in
  the escalation order; its evaluation is deferred to FU-020. Agent file
  defaults do not change.

- `dev-plan` (Issue #62; REQ-027): step 2 adds the source trace (FU-022;
  cards D19-PR2-C1 (4b) and FU022-C1 (a)): for every spec or REQ from a
  user decision, a `dev-retro` card included, each rule sentence names the
  user sentence that it comes from, and every condition of those words has
  a place; a condition that the spec does not keep is listed with its
  reason and shown to the user; the review of the spec checks the trace. Step 6 keeps the smallest coherent
  slices and adds review units chosen by risk and review cost: a unit is
  one write node of the task graph that lists the DoD, verification and
  requirements of each of its slices; in a `strict` objective, and for a
  high-risk slice, each slice is a unit of its own with the early reviews
  and scans of R-REV-6; in a `light` or `standard` objective, slices that
  are not high risk with a close review scope may be reviewed together and
  delivered as one change; when joining adds risk or is unclear, a
  decision card goes to the user; the mapping to issues, branches and
  change requests follows the project's own rules (card FU022-R2-C1 (a)).
  `dev-review` step 2 tells the reviewer to check the source trace. The
  `.dev/followups.md` header prefers card IDs, rule IDs or section names to
  line numbers (card FU022-C2 (a)).
- R-REV-9 push pre-check and scan views (REQ-011, REQ-012, D-021, Issue
  #68; user decisions E1 A and E2, cards I68-C7a and I68-R1-C1a; fallback
  (c) with option (c1) after review round 3). Push step 4a runs the new
  `skills/dev-gate/scripts/push_precheck.py verify` on the saved dry-run
  output and the step-6 ID list: the source checks of step 7, exit 0 (the
  checks passed) or 2 (`STOP <reason>`, the push stops). Exit 0 replaces no
  scan: steps 6 to 8 always run, and the reviewer still scans everything
  the push sends. The commit-scan view adds
  `--ignore-submodules=none --submodule=short`, and the `log -p` commands
  of push step 8 and the merge-readiness range scan add
  `--ignore-submodules=none`, so that a gitlink change stays visible; the
  commit-scan hash command of `dev-gate` and `review-report.md` adds
  `--ignore-submodules=none --submodule=short` too (S4-002).
  `deltas.md` adds the no-regression definition for changes to project
  tightenings (card I68-C7a). R-EXH-3 binds reusable content evidence to
  the tree and the diff: when a new head differs from a reviewed head only
  in identities or messages (the same base, the same number of commits and
  equal trees one by one), its content evidence may be reused; the new
  review still binds the exact base, head and merge-base and gives its own
  verdict (E2). Temporary-repository tests in `tests/test_push_precheck.py`.
  Not enabled: the push path without a reviewer scan (E1 A), with its
  commit-time scan records and report binding; review round 3 found that
  the binding let a published scan report confirm a guessed identity
  (R3-001).
- Model routing (REQ-009, D-022, Issue #73; user answers
  「C3 選 a，C4/C5 同意」, 「I69-M1 a」, 「I73-R1-C1 選 c，I73-R1-C2 選 a」 and
  「I73-R2-C1 選 a，接受 S2-001；I73-R2-C2 選 a」 and 「I73-R3-C1 選 a」; DL-034,
  DL-038). C4: at the `light` tier, routine review uses
  `sonnet`/`medium` unless an escalation trigger that `dev-review` lists
  applies (the R-DEL-2 floor; packaging, installation, CI or dependencies;
  more than one module; a disputed finding; a part the reviewer could not
  check); a trigger found after the review re-runs it at `opus`/`high` and
  keeps the first report; the brief of a `sonnet`/`medium` review lists
  triggers 1 to 3 and the reviewer reports whether any holds, and a reported
  trigger, or a report without an answer for each, re-runs the review at
  `opus`/`high`; once a trigger applies to a
  node, every later review round of that node uses `opus`/`high`. C5: the
  `dev-deliver` Dispatch step runs a node in this session by default and
  lists when to delegate; before this session runs any node under the floor
  (explore, implement or docs), and again before it fixes or writes any part
  of such a node itself, it checks its own model and effort against the
  floor and never implements first; `verify`, `gate` and `human_gate` nodes
  are outside the check, with the reason. C3 (an R-REV-9 text scan at `sonnet`/`high`
  with a deterministic secret scan, as an exception to the R-DEL-2 floor)
  is deferred to FU-034 by the user: the floor has no exception, and text
  scans before posting stay `opus`/`xhigh`. Agent file defaults do not
  change.

### Fixed

- Skill paths (REQ-026, FU-025, Issue #64). In the first use of
  `dev-retro`, the capture read `dev-core` with a path relative to the
  working directory. The new binding CB-6 (DL-036) says that each file that
  a dev-* skill names with a `${CLAUDE_SKILL_DIR}` path is read, run or
  copied only with that absolute path, never relative to the working
  directory, and that a path that does not resolve stops the skill. A file
  with the same name in the working directory is that repository's data,
  never pack rules (R-AUTH-1); a file of the current repository that is a
  review target, an input, a record or a write target keeps its repository
  path. Each dev-* skill cites CB-6. The pack files that review round 1
  found without the prefix, and the remaining `graph.py` commands, now have
  it; CB-6 covers other names without the prefix for pack references,
  template sources and scripts (open questions: FU-029). `dev-retro`
  capture steps 3 and 4 and review step 3 separate the pack rules from the
  files of the current repository. CB-6 states its limit when the plugin checkout is inside the
  repository under review, not at the merged `main`, or has uncommitted
  changes (FU-028). The README Cowork paragraph now says that a skill stops
  when a path does not resolve (FU-001).
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
- The read-only agent check of `scripts/check_pack.py` (CB-5, DL-009;
  Issue #69, MR67V-001). It split `tools` on commas only, while Claude Code
  2.1.310 (inferred from its binary, confirmed by a probe) also splits on
  spaces outside parentheses and reads `*` as all tools, so
  `tools: Read, Grep, Glob, Bash Edit` or a list with `*` passed. Now the raw
  `tools` and `disallowedTools` lines of `dev-explorer`, `dev-reviewer` and
  `dev-security-reviewer` must equal pinned strings (`dev-explorer`: no
  `disallowedTools` line), whatever split rule Claude Code uses. Each of the
  three files must exist with its exact name, also on a case-insensitive
  file system. A read-only agent file larger than 65,536 bytes (this
  repository's limit) fails. Another agent file whose name equals a
  read-only agent name after normalization (case, `_`, dashes, spaces,
  NFKC) fails. Reason for the last two (inferred from the Claude Code
  2.1.310 code, not run): Claude Code skips an agent file over 1,048,576
  bytes, and when no agent has the exact name, it can pick the one agent
  whose name matches after normalization.
  A change of these values needs a change of `check_pack.py` with review.
  Negative tests cover a space-separated write tool, `*`, a specifier, an
  added tool, a removed or changed `disallowedTools`, a missing or renamed
  file, an oversized file and a name collision. The cases of FU-033 also
  get negative tests. The agent files do not change.

### Security

- The push scan and the merge-readiness scan stop at commit and tag
  signatures (REQ-011, FU-017, Issue #54). A signature can carry a name or
  email that the headers do not show (the certificate of an x509
  signature, the signer's user ID of an OpenPGP signature). In R-REV-9
  and `dev-security-reviewer`: when the scan view has a `gpgsig `,
  `gpgsig-sha256 ` or `mergetag ` commit header, or a scanned tag has a
  line that starts with `gpgsig` or `-----END ` or contains `-----BEGIN `
  (a tag message without a trailing newline puts the signature block
  inside the last message line; card FU017-R2-C2a), the reviewer reports a
  blocking finding with the disposition Needs Human Decision. It lists
  each such commit or tag and the kind of signature, and it does not
  decode the signature (card FU017-C1b). The checks use `awk`, because
  `grep` can treat a view with a NUL byte as binary. The main agent stops
  the push (also in `dev-implement`), and the user decides whether the
  identity of the signing key may be published. When the user allows it,
  the main agent records the signature finding as `Rejected`, with the
  user's answer as the source and the reason; the answer covers only that
  push, or at merge readiness that range. When the scan has no other
  open finding, the scan counts as passed (card FU017-R2-C3a). The
  R-REV-9 "Not covered" list names the decoded content of signatures and
  signatures that the platform adds at merge or squash, and an `encoding`
  header that names an encoding that is not ASCII-compatible (UTF-16,
  EBCDIC), for which the view can show no readable identity or signature
  header (card FU017-R1-C1a).
- The push stops, within the coverage that R-REV-9 states, at a force or
  delete that configuration causes, and the
  error output of the URL check, `ls-remote`, the dry-run and the push stays
  out of records (REQ-011, FU-019, Issue #52). In R-REV-9 and
  `dev-implement`: before the dry-run, the main agent stops and asks the
  user when the configuration of the remote sets a push mirror or a
  `remote.<name>.push` refspec that starts with `+` or is `:<dst>`
  (card RB-C2b: a remote ref that changes after the dry-run could otherwise
  still be force-updated or deleted); it also stops when the dry-run lists
  a `+` (forced update) or `-` (delete) ref line. Both stops work within
  the coverage that R-REV-9 states: the configuration check does not cover
  the `GIT_CONFIG` environment variable, legacy `$GIT_DIR/remotes/` and
  `$GIT_DIR/branches/` files, or Git before 2.18 (card RB-C3a). The URL
  check sends the error output of `git remote get-url` to `/dev/null` (a
  `transfer.credentialsInUrl` warning can show the user name and host) and
  counts the fetch URL lines too (`$(…)` drops trailing newlines). The error
  output of `ls-remote`, the dry-run and the push goes into no brief, record
  or post. The REQ-011 threat model says that this pack does not implement
  inbound controls apart from R-AUTH-1. The reviewer agent file does not
  repeat the new checks; this is an author decision that follows card
  PR2-C2a (the push form). FU-017 (commit and tag signatures) moves to a
  separate Issue and PR after this one (card RB-C1b).
- The push scan checks the push destination and its own input, and states
  what it does not cover (REQ-011, FU-015 PR-2, Issue #48). In R-REV-9,
  `dev-implement` and `dev-security-reviewer`: before `ls-remote`, the main
  agent checks that the fetch and push URLs of `<remote>` are one and the
  same (it prints only PASS or STOP). The real push has one closed form
  that names `<remote>`, so `remote.pushDefault` and
  `branch.<name>.pushRemote` choose no other remote, and allows no other
  option (no `-q`, no later `--recurse-submodules=<value>`, nothing between
  `git` and `push`); the main agent checks the form, and no independent
  check repeats it. The reviewer blocks an empty dry-run list, an ID or a
  source with unexpected characters before it goes into a command, a
  source outside `refs/heads/` and `refs/tags/` that is not a full object
  ID, and an updated ref whose old value is not a listed ID. The
  merge-readiness range scan has a command with the push scan view.
  R-REV-9 lists what the scans do not cover; REQ-011 and DL-010 claim
  only that coverage. REQ-011 gets a threat model: R-REV-9 addresses
  accidental leaks under the developer's own legitimate configuration,
  within the coverage it states; deliberately malicious configuration and
  hooks that someone else planted (`git clone`, `fetch` and `pull` do not
  transfer `.git/config` or `.git/hooks`) are inbound controls (review of
  install steps after a clone or sync, R-AUTH-1), not a scan.
- Push and commit scans no longer change with the listed configuration
  (REQ-011, FU-015 PR-1, Issue #46). In R-REV-9 and
  `dev-security-reviewer`, the scan and read-back commands run as
  `git --no-replace-objects`; the `git diff` and `git log` scan commands add
  `--no-relative` and `-c core.quotePath=false`; the push scan uses `git log --format=raw
  --no-mailmap --no-show-signature --encoding=UTF-8 --root`. The read-back
  after a commit uses `git cat-file commit HEAD` (also in `dev-implement`),
  and the `dev-gate` commit binding hashes the same view. So `.mailmap`,
  replace refs, `log.showRoot`, `diff.relative`, `core.quotePath`,
  `log.showSignature` and `i18n.logOutputEncoding` no longer hide what is
  sent, and the scan no longer runs `gpg.program`. The real push and its
  dry-run include `--no-recurse-submodules` (a later `--recurse-submodules=`
  value is left for FU-015 PR-2). The main agent checks the remote
  names, that the dry-run exits 0 and lists at least one ref line, and the
  dry-run names before they go into a command; the reviewer scans the source
  side of each ref line and blocks a ref that is not a commit or a tag of a
  commit. Other configuration and objects are left for FU-015 PR-2. New
  follow-up FU-017: commit and tag signatures.
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
