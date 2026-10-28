# Issue #75 review round 4

Target: `83084a7` plus the uncommitted fix T2 (tracked diff `--binary`
SHA-256 prefix `58272b6e269c8878`). Round 4 is a narrow re-review of fix
T2 (card I75-R2-C1 (a); commit scan C1 NITs) by the same two roles as
rounds 1 and 2.

- Deep review R4: `dev-reviewer`, requested `opus`/`xhigh`; recorded
  `unknown` (the main agent did not read the transcript field);
  self-reported: model `opus`, effort `unknown` (a claim, not a recorded
  value). Result: card I75-R2-C1 (a) is applied in all copies; C1-001 and
  C1-002 are resolved; the T1-R edits in `83084a7` are checked; no false
  record found. One finding, R4-001 (see below).
- Security re-review S4: `dev-security-reviewer`, requested
  `opus`/`xhigh`; recorded `unknown` (the main agent did not read the
  transcript field); self-reported: model `opus`, effort `unknown` (a
  claim, not a recorded value). Result PASS: the first residual risk that
  S2 noted (`reviews/round-2.md`) is closed; the copies agree; no private
  value found. gitleaks 8.30.1: no findings.

## Findings and dispositions

| ID | Severity | Relation | Location | Summary | Disposition |
| --- | --- | --- | --- | --- | --- |
| R4-001 | SHOULD-FIX | in-scope | `.dev/issue-75-issue73-followup/graph.json`, `events.jsonl` | `T1` is `done` with evidence at `7bdb9bb5`, but fix T2 changed rule text in files that `T1` owns | Fixed (T2-R): `graph.py transition` moved `T1` done -> ready -> in_progress (evidence "58272b6e T2 fix, card I75-R2-C1 (a)") -> reviewing (evidence "58272b6e R4 deep, S4 security narrow re-reviews") -> done (evidence "58272b6e R4 PASS except R4-001 graph state (fixed here); S4 PASS"); `events.jsonl` seq 5 to 8 |

Residual risk noted by R4 (no finding):

- "below its value in the `dev-deliver` or `dev-review` table" is unclear
  for a row with more than one value (for example, the standard
  implementer row allows `sonnet`/`medium` for a mechanical slice).

Residual risk noted by S4 (below the finding threshold; not a
regression):

- A relayed answer can still lower a setting without the user's
  confirmation in this session in two ways: (1) it undoes an R-DEL-2
  escalation back to the table value; (2) it relays a judgment that moves
  the work to a lower table row (for example "mechanical slice" or "no
  light trigger holds"). The floor stays protected.

Status of the R4 and S4 residual risks: to the merge card for the user
(proposed follow-up).

## Fix T2-R (R4-001 and this record)

- `dev-implementer` T2-R, requested `opus`/`high`; recorded `unknown`
  (the main agent did not read the transcript field).
- Fixed R4-001 (see the table).
- Wrote this record; added round 4 to the plan (Task graph, dispatch
  record) and to D-023 residual risk 7 (zh and en) of
  `docs/design-proposal.md`.
- No rule text changes.
- The T2-R record edits are covered only by the commit scan.
