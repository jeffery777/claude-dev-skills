# Issue #69 plan: read-only agent tools check (MR67V-001)

- Objective: Issue #69. The read-only agent check of `scripts/check_pack.py`
  (CB-5, DL-009) must not pass a `tools` value that gives a read-only agent a
  write tool. Found as MR67V-001 (SHOULD-FIX, Deferred) in the Merge Review of
  PR #67; it was on `main` before that PR.
- Rigor `standard` (Issue #69, Process): the change is a lint of this
  repository's own files. It changes no agent file, no permission and no
  runtime behavior of the pack. It touches the guard of a permission boundary
  (R-REV-7), so the review is deep and a Security Diff Scan runs in each
  round that reviews a code change (round 3 changed records only after the
  code check; its scan runs with the R-REV-9 commit scan).
- Requirement trace: REQ-028 (the closed-world guard of the agent front
  matter, CB-7), DL-009 and CB-5 (read-only reviewer agents). Issue #69 is the
  source of this change. The only requirement text change is one line of the
  REQ-028 acceptance (the FU-033 exception, finding R69R1-005), with one row
  of `docs/requirements/log.md`.
- Review units: one unit (task node T1), alone in this PR (Issue #69: one PR,
  separate from the R-REV-9 cost change of Issue #68). This PR does not touch
  `skills/dev-core/SKILL.md`, `skills/dev-core/deltas.md` or
  `docs/design-proposal.md` (Issue #68). It overlaps with Issue #68 only in
  `docs/requirements/` (one REQ-028 line and one appended row of
  `docs/requirements/log.md`, where both PRs may append rows: a possible
  merge conflict), one row of `.dev/followups.md` (FU-033) and one
  `CHANGELOG.md` entry.

## Design

Two options in Issue #69, Change 1:

1. Pin the raw `tools` and `disallowedTools` values of the three read-only
   agents to exact strings.
2. Split like Claude Code (commas and spaces outside parentheses) and fail
   on `*`.

Decision: option 1. Reasons:

- It is simpler and fails closed. Any value other than the pinned string
  fails, whatever split rule Claude Code uses now or later. Option 2 copies a
  parser that is inferred from a binary and can change in another version
  (lesson candidate of MR67V-001: a lint that imitates the platform parser
  must follow the real parser). With option 1 there is no parser to follow.
- It also catches values that option 2 would pass: a new read tool that is
  not a write tool, for example `Agent` (a subagent can dispatch a writer) or
  an MCP tool.
- The cost: a change of a read-only agent's tools needs a change of
  `check_pack.py` with review. Such a change is a change of the CB-5 trust
  boundary and needs that review anyway.

This is not a trade-off for the user (Issue #69 lets the design pick one), so
no decision card.

Details:

- `READ_ONLY_AGENTS` maps each stem to its pinned raw values. `None` means
  "no such line": `dev-explorer` has no `disallowedTools` now, and an added
  line fails too (closed world; a change needs review).
- The check compares the raw text after `key: ` (new `raw_values`), not the
  value of the permissive subset parser `graph.frontmatter`. The closed value
  grammar (card I66-M3 (a)) already refuses quoted, tagged or flow values.
- Each of the three read-only agent files must exist as a regular file with
  its exact-case name in `os.listdir` (fix round 1, R69R1-001). Before, a
  missing file passed silently.
- Fix round 1 (R69S1-002): a read-only agent file larger than
  `AGENT_MAX_BYTES` (65,536 bytes) fails (fix round 2 narrowed it from
  every agent file, R69R2-002), and an agent file name that is not a
  read-only agent name but equals one after `agent_key` normalization
  (NFKC, casefold, no whitespace, `_` or Unicode Pd dash) fails.
- `tool_set`, `WRITE_TOOLS` and their unit test are removed: nothing else uses
  them (R-RIG-3).

## FU-033

Issue #69 says FU-033 is out of scope unless the same test file makes it
trivial. The FU-033 promotion trigger is "before the next change of
`scripts/check_pack.py`", which is this change, and the test file has the
helpers. So this PR adds `test_fu033_cases`: CR line end, tab and U+0085 in
an agent file, a quoted key, an empty `plugins` list, a deeply nested
`marketplace.json`, a directory named `agents/x.md`, and an `allowed-tools`
item that names Grep. Each asserts one clear error (or, where two checks of
the same file both report it, only problems in that file).

## Verification

- `bash scripts/validate.sh` and `python3 -m unittest tests.test_core_checks`:
  pass (47 tests before fix round 1, 3 skipped on a case-insensitive file
  system; see Review rounds for later counts).
- Mutation check (each check removed in a copy of `check_pack.py`, then the
  two new test methods run; the file restored and compared with `cmp`). The
  counts are for `test_read_only_agent_tools_are_pinned` and
  `test_fu033_cases` only, not the full suite (finding R69R1-004): the pin
  check (13 failures), the missing-file check (1), the printable ASCII check
  (3), the `plugins` entry check (1), the `RecursionError` catch (1 error),
  the regular-file check of `agents/` (1), the key check (1), and both
  `allowed-tools` checks together (1). With only the raw `allowed-tools`
  check removed, the parsed check still reports the case, so the test
  passes; this is expected. Fix round 1 adds checks with their own mutation
  results (see Review rounds).
- Claude Code run (Issue #69, Change 3): Claude Code 2.1.310, headless
  (`claude -p --plugin-dir <worktree> --model haiku --output-format
  stream-json --verbose --max-turns 6`), started from an empty directory in
  the session scratchpad, before fix round 1. The prompt asked the main
  agent to dispatch `dev-skills:dev-explorer` and then
  `dev-skills:dev-reviewer`, each with the brief "Do not run any tool.
  Reply with only the exact names of every tool available to you". The
  output stayed in the scratchpad and is not committed. Fact: both
  subagents listed only `Bash` and `Read`, with 0 tool uses. Inference: the
  pinned values give these two agents no write tool. Unverified: the
  harness tool list (a self-report is not harness evidence);
  `dev-security-reviewer` (not dispatched); whether `tools` or
  `disallowedTools` removed the write tools; why `Grep` and `Glob` were not
  listed (perhaps not separate tools in this build); whether a front matter
  parse failure of a plugin agent gives all tools (Issue #69, Facts; the
  Security Diff Scan of round 1 infers yes from the code, not run). Limit
  (CB-6): `--plugin-dir` pointed at this worktree with uncommitted changes;
  the agent files did not change.

## Implementer

The main session (model `opus`, Opus 5.5). Its effort is not readable in the
session: `unknown`. The change guards a permission boundary, so the R-DEL-2
floor `opus`/`high` is taken as applicable; the model meets it, the effort is
not verified. The deviation from R-DEL-2 (no switch request and no dispatch
before the implementation) is recorded here and in the merge card; the
reviews run at `opus`/`xhigh`.

## Review rounds

- Round 1 (deep R69R1-001 to R69R1-005, BLOCKED; Security Diff Scan
  R69S1-001 and R69S1-002, BLOCKED), on the uncommitted candidate on
  `7c5af9a` (diff SHA-256 prefix `4021db29`; the tree was the same before and
  after both reviews, CB-4):
  - R69R1-001 = R69S1-001 (MUST-FIX; class: necessary fix): the existence check used
    `os.path.isfile`, so on a case-insensitive file system a file renamed to
    `agents/Dev-Reviewer.md` without `tools` passed. Fixed: exact-case name
    in `os.listdir` and a regular file.
  - R69S1-002 (MUST-FIX; class: necessary fix; in-scope by Issue #69 Change 2, "the cases the
    review finds"): an agent file over 1,048,576 bytes is skipped by Claude
    Code, and a dispatch name without an exact match takes a unique match
    after normalization (inferred from the 2.1.310 code, not run). So an
    oversized `dev-reviewer.md` plus `dev_reviewer.md` without `tools`
    passed, also in CI. Fixed: a 65,536-byte limit for agent files and a
    check for other agent names that equal a read-only name after
    normalization. The gap was already on `main` (the old check passed the
    same tree), so it is not a regression of this change.
  - R69R1-002 (MUST-FIX; class: needs human decision; Needs Human Decision): the R-DEL-2 deviation of
    section Implementer. The fix of round 1 went to `dev-implementer` at
    `opus`/`high`. The user decides on the merge card.
  - R69R1-003 (NIT; class: worth improving): the CHANGELOG said `*` passed (only a list with `*`
    did) and stated the Claude Code split without its source. Fixed.
  - R69R1-004 (NIT; class: worth improving): the empty `plugins` test made a second problem of its
    own, and the mutation counts did not say their scope. Fixed.
  - R69R1-005 (NIT; class: worth improving): REQ-028 acceptance still said FU-033 cases were
    Deferred. Fixed: one line of REQ-028 and one row of
    `docs/requirements/log.md` (the only `docs/requirements/` change; see
    Review units for the overlap with Issue #68).
  - Residual risk from the scan, not findings of this change: the root
    name `.claude` is allowed and its content is not checked, and the
    repository `.gitignore` does not list `.claude/` (a project agent can
    override a plugin agent; unverified whether it can take the
    `dev-skills:` name); YAML parse failure of an agent file may give all
    tools (inferred), so the read-only agents depend on the closed value
    grammar of card I66-M3 (a) matching the Claude Code YAML reader (not
    run); all Claude Code behavior is from 2.1.310, while CI pins another
    version; Bash stays (CB-5). These go to the merge card as follow-up
    proposals.
- Fix round 1: implemented by `dev-skills:dev-implementer`, requested
  `opus`/`high` (R-DEL-2 floor; recorded: `unknown`, the main agent did not
  read the subagent transcript). The main agent read the diff back and ran
  `bash scripts/validate.sh` (pass) and `python3 -m unittest
  tests.test_core_checks` (48 tests, 3 skipped). The new test
  `test_read_only_agent_name_variants_fail` covers the case-only rename
  (two problems: missing file and name collision), `dev_reviewer.md`, an
  en-dash and a fullwidth variant, and an oversized `dev-reviewer.md`.
  Mutation (in a copy outside the worktree, per the receipt): removing the
  exact-case check, the collision check or the size check each makes that
  test fail.
- Round 2 (confirmation; deep R69R2-001 and R69R2-002, Security Diff Scan
  R69S2-001 to R69S2-004, PASSED with NITs), on diff SHA-256 prefix
  `a65cd672`; the tree was the same before and after both reviews (CB-4).
  All round-1 findings except R69R1-002 are closed (each with evidence in
  the reports). No new MUST-FIX or SHOULD-FIX, so the R-VER-2 stop rule did
  not fire. Dispositions:
  - R69R2-001 = R69S2-004 (NIT; class: worth improving): plan and graph said no `docs/requirements/`
    change, a wrong test count and a short `owns` list. Fixed (main agent,
    records only): Review units, Requirement trace, Verification, `owns`
    and the T1 title.
  - R69R2-002 (SCOPE-CREEP; class: necessary fix, R-RIG-3): the size limit applied to every agent file.
    Fixed: it applies only to the read-only agents (CB-5).
  - R69S2-001 (NIT; class: worth improving): no test for the whitespace branch of `agent_key`.
    Fixed: `agents/dev reviewer.md` case.
  - R69S2-002 (NIT; class: worth improving): code comments stated Claude Code behavior as fact.
    Fixed: they say "inferred from reading the Claude Code 2.1.310 code, not
    run", name the platform limit and this repository's own limit, and say
    why `agent_key` on the file stem is equivalent here.
  - R69S2-003 (NIT; class: worth improving): a comment at `AGENT_KEYS` says that the allowlist is
    part of the read-only guarantee. Fixed.
  - Residual risk added by round 2 (code reading, not run): a YAML parse
    failure of an agent file gives an empty front matter and so all tools
    (Claude Code retries once with quoted values); another installed plugin
    whose name normalizes to the same name, two plugins named `dev-skills`,
    or an `agent.spawn` hook of another plugin can change which agent a
    dispatch gets; these are outside `check_pack.py`.
- Fix round 2: code and tests by `dev-skills:dev-implementer`, requested
  `opus`/`high` (recorded: `unknown`); records by the main agent. The main
  agent read the diff back; `bash scripts/validate.sh` passes and
  `python3 -m unittest tests.test_core_checks` runs 48 tests, 3 skipped.
  Mutation (copies outside the worktree, per the receipt): removing the
  whitespace branch or the size check makes the matching test fail.
- The R-REV-4 class of each disposition (necessary fix, worth improving,
  keep as is, needs human decision) was decided before each fix and is
  written next to each finding above since round 3 (R69R3-001).
- Round 3 (narrow confirmation of fix round 2; deep R69R3-001 and
  R69R3-002), on diff SHA-256 prefix `616f21a3`; the tree was the same
  before and after the review (CB-4). All round-2 findings are closed;
  R69S1-002 is not reopened by the narrowing. No new code finding.
  - R69R3-001 (SHOULD-FIX, records; class: necessary fix): the R-REV-4
    class was not recorded with the dispositions. Fixed (main agent,
    records only).
  - R69R3-002 (NIT; class: worth improving): the Design section still said
    "an agent file" for the size limit. Fixed.
  - R-VER-2: round 2 had no new blocker, so the stop rule did not fire.
  - The narrowing of a CB-5 guard in fix round 2 is checked by the
    Security Diff Scan that runs with the R-REV-9 commit scan. That scan
    covers this commit, so its record is not in this commit (R-REV-9); it
    goes into the PR and the merge card.
