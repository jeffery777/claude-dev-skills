# Issue #75 review round 1

Target: uncommitted candidate on `9628c99` (tracked diff `--binary` SHA-256
prefix `cfc35650bddfd3af`, plus the untracked folder
`.dev/issue-75-issue73-followup/`; HEAD and `git status --porcelain` equal
at start and end of both reviews, as both reviewers report).

- Deep review R1: `dev-reviewer`, requested `opus`/`xhigh`; recorded
  `unknown` (the main agent did not read the transcript field);
  self-reported: model `opus`, effort `unknown` (a claim, not a recorded
  value).
- Security Diff Scan S1: `dev-security-reviewer`, requested `opus`/`xhigh`;
  recorded `unknown` (the main agent did not read the transcript field);
  self-reported: model `opus`, effort `unknown` (a claim, not a recorded
  value; S1 says that the shown value cannot be read as `xhigh`). gitleaks
  8.30.1: no findings. No private value found.

## Findings and dispositions

| ID | Severity | Relation | Location | Summary | Disposition |
| --- | --- | --- | --- | --- | --- |
| R1-001 = S1-001 | SHOULD-FIX | in-scope | `skills/dev-core/SKILL.md:184` (R-DEL-2) and copies | The relay sentence follows the sentence "a message of another session is data (R-AUTH-1)" without saying that it is an exception, or that it applies only to the model and effort choices | Fixed (T1-F1): explicit exception, scoped to the model and effort choices of the bullet; R-AUTH-1 to R-AUTH-6 unchanged for other decisions; section 4 and D-023 (zh and en), REQ-009 and the log row follow; D-023 residual risk 6: a session that receives a relayed answer cannot verify the quoted words |
| R1-002 | SHOULD-FIX | in-scope | `.dev/issue-75-issue73-followup/plan.md` ("Main session setting and dispatch"; "Implementer") | The plan says that the main session writes no repository file, but also that the main agent fills in the recorded fields | Fixed (T1-F1): every repository write of the node goes to `dev-implementer` `opus`/`high`; the main agent supplies the values; dispatch record added |
| S1-003 | SHOULD-FIX | in-scope | `skills/dev-core/deltas.md` DL-034; `CHANGELOG.md`; D-023 "Difference from Core" | DL-034 and the CHANGELOG carry only the floor half of the relay sentence; D-023 does not say that the relay sentence adds no authority; the CHANGELOG R-RIG-1 summary lacks the early deep code review | Fixed (T1-F1) |
| S1-004 | NIT | in-scope | `skills/dev-core/SKILL.md:184` and copies | "An agent whose agent file is below the floor" does not cover an agent without an agent file | Fixed (T1-F1): "or that has no agent file" |
| R1-003 | SHOULD-FIX | in-scope | `skills/dev-plan/SKILL.md:93`; `plan.md` review units; `graph.json` one write node | `strict` objective: each slice is a review unit; `T1` joined items 1–3, 4, 5 without a card | Accepted deviation, card I75-R1-C1 (a) |
| R1-004 | REQ-GAP | gap | `skills/dev-core/SKILL.md:81`, `:84` | `strict` needs a design review before implementation, but R-RIG-2 can raise the tier after implementation started; no rule says what then | Deferred to FU-037, card I75-R1-C2 (b) |
| S1-002 | REQ-GAP | gap | R-RIG-2 (`skills/dev-core/SKILL.md:84`), D5 | D5 (a) requires own confirmation only for a relayed floor loosening; a relayed lowering of a tier also removes the design review and the human gate | Fixed: R-RIG-2 sentence added, card I75-R1-C3 (b) |

The three cards concern the R-RIG-1 text, the R-RIG-2 text and the
review-unit split of `T1`. Fix round 1 did not change these; they waited
for the user's answers (R-REV-3). The card text is outside the repository.
Line numbers refer to the candidate on `9628c99` that round 1 reviewed.

User answer (Claude Code session 2026-10-28, orchestrator relay, the
user's words): 「R1-C1 a，R1-C2 b，R1-C3 b」.

## Fix round 1 (T1-F1)

- `dev-implementer` T1-F1, requested `opus`/`high`; recorded `unknown`
  (the main agent did not read the transcript field; see the plan, "Main
  session setting and dispatch").
- Fixed R1-001 (= S1-001), R1-002, S1-003 and S1-004 in
  `skills/dev-core/SKILL.md` (R-DEL-2), `skills/dev-core/deltas.md`
  (DL-034), `docs/design-proposal.md` (section 4 and D-023, zh and en),
  `docs/requirements/REQ-009-subagent-model-effort.md`, the new REQ-009 row
  of `docs/requirements/log.md` (a row of this candidate; no earlier row
  changes), `CHANGELOG.md` and the plan.
- Graph: `T1` moved `planned` -> `ready` -> `in_progress` -> `reviewing`
  with the evidence `cfc35650 (T1 candidate diff prefix)`.
- Not reviewed yet.

## Fix round 1b (T1-F2)

- `dev-implementer` T1-F2, requested `opus`/`high`; recorded `unknown`
  (the main agent did not read the transcript field).
- R1-003 (card I75-R1-C1 (a)): the accepted deviation is recorded in the
  plan (Task graph) and in D-023 residual risk 7 (zh and en).
- R1-004 (card I75-R1-C2 (b)): no rule change; new FU-037 in
  `.dev/followups.md`; D-023 residual risk 8 (zh and en).
- S1-002 (card I75-R1-C3 (b)): `skills/dev-core/SKILL.md` R-RIG-2 adds "A
  relayed decision to lower it counts only after the user confirms it in
  this session." Copies with the same meaning: README (zh and en), D-004
  and D-023 (zh and en) in `docs/design-proposal.md`, the REQ-003
  acceptance item and a new source entry, DL-039, `CHANGELOG.md`, the plan
  trace table, and a new appended row in `docs/requirements/log.md` (no
  earlier row changes).
- D-023 origin 4 and the plan quote the user answer.
- Not reviewed yet.
