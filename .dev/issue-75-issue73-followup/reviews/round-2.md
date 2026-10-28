# Issue #75 review round 2

Target: uncommitted candidate on `9628c99` after fix rounds 1 and 1b
(tracked diff `--binary` SHA-256 prefix `dc534d9f7f75b4e6`, plus the
untracked folder `.dev/issue-75-issue73-followup/`). Round 2 is a narrow
re-review of the fixes by the same two roles as round 1.

- Deep review R2: `dev-reviewer`, requested `opus`/`xhigh`; recorded
  `unknown` (the main agent did not read the transcript field);
  self-reported: model `opus`, effort `unknown` (a claim, not a recorded
  value). All round 1 dispositions are resolved.
- Security Diff Scan S2: `dev-security-reviewer`, requested `opus`/`xhigh`;
  recorded `unknown` (the main agent did not read the transcript field);
  self-reported: model `opus`, effort `unknown` (a claim, not a recorded
  value). Result PASS: S1-001 to S1-004 resolved; no new finding; no
  private value found. gitleaks 8.30.1: no findings.

## Findings and dispositions

| ID | Severity | Relation | Location | Summary | Disposition |
| --- | --- | --- | --- | --- | --- |
| R2-001 | SHOULD-FIX | in-scope | `.dev/issue-75-issue73-followup/plan.md` ("Main session setting and dispatch"; "Design reviews"); `reviews/round-1.md` (reviewer lines) | A `recorded` value comes only from the transcript field (`skills/dev-deliver/references/task-brief.md`). The main agent did not read any transcript field, but the records give model `opus` as recorded from the reviewers' self-report | Fixed (T1-F3): every dispatch (design reviews, R1, S1, R2, S2; T1, T1-F1, T1-F2, T1-F3) records `unknown` (the main agent did not read the transcript field); the reviewers' self-report is kept apart as "self-reported: model `opus`, effort `unknown`" (a claim) |
| R2-002 | NIT | in-scope | `plan.md` Task graph; `docs/design-proposal.md` D-023 residual risk 7 (zh and en) | "Every review round checked the whole diff" is not true: only round 1 did | Fixed (T1-F3): round 1 deep and security reviews checked the whole diff; later rounds were narrow re-reviews of the fixes by the same two roles |
| R2-003 | NIT | in-scope | `plan.md` source trace (relay sentence row); D-023 "What the user decided" item 5 (zh and en) | The trace row gives the relay sentence without its limit and names only D5 (a); D-023 item 5 shows the limit as part of the card answer | Fixed (T1-F3): the row gives the limit (model and effort choices only; R-AUTH-1 to R-AUTH-6 unchanged for other decisions) and names D5 (a) and review finding R1-001 = S1-001; D-023 item 5 says that the limit came from R1-001/S1-001 (fix round 1), not from the card answer |
| R2-004 | NIT | in-scope | `reviews/round-1.md` (R1-003 row) | The relation of R1-003 is `gap`; the reviewer reported `in-scope` | Fixed (T1-F3): relation `in-scope` |

Residual risk noted by S2 (no finding):

- Inside the D5 (a) scope, a relayed answer that quotes the user can lower
  a table value that is above the floor (for example an R-REV-9 scan from
  `xhigh` to `high`) without the user's confirmation in this session.
  Resolved by card I75-R2-C1 (a) (user answer 「那依你的建議選a」): a
  relayed decision that sets a model or effort below its value in the
  `dev-deliver` or `dev-review` table also counts only after the user
  confirms it in the session that acts on it. Fix T2 (see below);
  reviewed in round 4 (`reviews/round-4.md`).
- Pre-existing: a tier set at Discover can be lowered at a later
  re-assessment without a user decision.

## Fix round 2 (T1-F3)

- `dev-implementer` T1-F3, requested `opus`/`high`; recorded `unknown`
  (the main agent did not read the transcript field).
- Fixed R2-001 in the plan ("Main session setting and dispatch", "Design
  reviews") and in `reviews/round-1.md` (R1, S1, T1-F2 lines).
- Fixed R2-002 in the plan (Task graph) and in D-023 residual risk 7 (zh
  and en) of `docs/design-proposal.md`.
- Fixed R2-003 in the plan source trace and in D-023 "What the user
  decided" item 5 (zh and en).
- Fixed R2-004 in `reviews/round-1.md`.
- No rule text changes.
- Reviewed in round 3 (R3 PASS).

## Round 3 (narrow check of fix round 2)

Target: uncommitted candidate on `9628c99` after fix round 2 (tracked diff
`--binary` SHA-256 prefix `7bdb9bb565276e0d`, plus the untracked folder
`.dev/issue-75-issue73-followup/`).

- Deep review R3: `dev-reviewer`, requested `opus`/`xhigh`; recorded
  `unknown` (the main agent did not read the transcript field);
  self-reported: model `opus`, effort `unknown` (a claim, not a recorded
  value). Result PASS: R2-001 to R2-004 resolved; no findings.
- Rule text: unchanged since `dc534d9f` except the D-023 records. R3
  checked this by numstat and by reading, not by byte comparison.
- No security re-review ran on round 3 alone. The commit scan by
  `dev-security-reviewer` covers the full staged diff.

## Fix T2 (card I75-R2-C1 (a); commit scan C1 NITs)

- `dev-implementer` T2, requested `opus`/`high`; recorded `unknown` (the
  main agent did not read the transcript field).
- Card I75-R2-C1 (a): R-DEL-2 in `skills/dev-core/SKILL.md` extends the
  relay exception sentence (still one sentence): a relayed loosening of a
  floor, or a relayed decision that sets a model or effort below its value
  in the `dev-deliver` or `dev-review` table, counts only after the user
  confirms it in this session. Copies with the same meaning: section 4 and
  D-023 (origin 5, rule 1, residual risk 6; both languages) of
  `docs/design-proposal.md`, REQ-009 (acceptance and a new source entry),
  DL-034, CHANGELOG, one new row in `docs/requirements/log.md`, and the
  plan (source trace, dispatch record, user answer).
- C1-002: the `T1` title in `graph.json` now names FU-037.
- Reviewed in round 4 (`reviews/round-4.md`).

## Correction note (commit scan C1, finding C1-001)

The evidence of `events.jsonl` seq 4 says "7bdb9bb5 R3 PASS; S2 PASS".
The bindings are: R3 at the tracked diff prefix `7bdb9bb565276e0d`; S2 at
the tracked diff prefix `dc534d9f7f75b4e6` (round 2 target), not at
`7bdb9bb5`. No security re-review ran on round 3 alone. The event line
stays as written: the event log is append-only, and `graph.py` has no
correction command.
