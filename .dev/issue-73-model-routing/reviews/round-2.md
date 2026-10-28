# Issue #73 review round 2

Target: uncommitted candidate on `f7b2ea8` (diff `--binary` SHA-256 prefix
`cbdf8aa3`; HEAD, `git status --porcelain` and the diff equal at start and
end of both reviews). Complete review of the candidate after fix round 1
(parts A and B; card answers 「I73-R1-C1 選 c，I73-R1-C2 選 a」).

- Fix round 1 part B: `dev-implementer` T1-F2, requested `opus`/`high`;
  recorded `opus` (`claude-opus-5-5`)/`high`; effective `unknown`.
- Deep review R2: `dev-reviewer`, requested `opus`/`xhigh`; recorded `opus`
  (`claude-opus-5-5`)/`xhigh`; effective `unknown`. PASS with two NITs.
- Security Diff Scan S2: `dev-security-reviewer`, requested `opus`/`xhigh`;
  recorded `opus` (`claude-opus-5-5`)/`xhigh`; effective `unknown`. BLOCKED
  (no MUST-FIX).

## Findings and proposed dispositions

| ID | Severity | Relation | Location | Summary | Class / proposed disposition |
| --- | --- | --- | --- | --- | --- |
| S2-001 | SHOULD-FIX | in-scope | `reviews/round-1.md` part A; `docs/requirements/log.md:116` | The main session (`opus`/`medium`, below the floor) wrote one line of an owned file of T1 itself ("record sync"); R-DEL-2 has no such exception | necessary fix: `dev-implementer` at `opus`/`high` re-applies or confirms the line; the deviation goes to the user (card I73-R2-C1) |
| S2-002 | SHOULD-FIX | in-scope | `skills/dev-core/SKILL.md:183`; `skills/dev-deliver/SKILL.md` step 5; `skills/dev-review/SKILL.md` step 6; REQ-009 Notes | The floor check is bound to the Dispatch step; a fix round that the main session does itself does not point back to it | necessary fix: the same check before the main session fixes or writes any part of a node under the floor |
| S2-003 | NIT | in-scope | `skills/dev-deliver/SKILL.md:59-61` | "any node under the floor (explore, implement or docs)" leaves out `verify`, `gate`, `human_gate` without a reason | worth improving: say why they are outside the check |
| S2-004 = R2-001 | SHOULD-FIX (R2: NIT) | in-scope | `.dev/issue-73-model-routing/graph.json`; `plan.md` trace and FU-005 sections | The graph title, T1 title, DoD, requirements and owns still describe C3 and REQ-011 and omit `.dev/followups.md` | necessary fix: re-plan with `dev-plan` and `graph.py validate` |
| R2-002 | NIT | in-scope | `.dev/followups.md` FU-021 (2); REQ-009 Notes | "runs once" and "no rule re-reads before later nodes" are no longer true after C5 | necessary fix: note what C5 covers; only fix rounds remain (or close with S2-002) |
| S2-005 | REQ-GAP | gap | `skills/dev-review/SKILL.md:28-46` | C4 triggers 1 to 3 are judged only by the main agent, usually the author; no independent second judgment | Needs Human Decision: card I73-R2-C2 |

## Stop rule

R-VER-2: review rounds 1 and 2 both reported new blockers (round 1: S1-001,
S1-002, R1-001 and others; round 2: S2-001, S2-002, S2-004). The fix loop
stops; no fix round starts before the user decides (cards I73-R2-C1 and
I73-R2-C2 in the shared notes folder, `issue73-cards.md`).

## Deviation of the main session (recorded, S2-001)

Fact: in fix round 1 part A, the main session (transcript `opus`/`medium`)
changed one sentence of `docs/requirements/log.md` (REQ-009 row of Issue
#73) itself, and later wrote `plan.md`, the review records and the FU-034
Owner cell. Fix round 1 part B (`dev-implementer`, `opus`/`high`) rewrote
the REQ-009 log row afterwards (receipt T1-F2); whether the final text still
holds words of the main session is not verified.

User decision: the user accepted the deviation (card I73-R2-C1 (a); Claude
Code session 2026-10-28, orchestrator relay:
「I73-R2-C1 選 a，接受 S2-001；I73-R2-C2 選 a」). In fix round 2,
`dev-implementer` T1-F3 (requested `opus`/`high`) re-applied the REQ-009 row
of Issue #73 in `docs/requirements/log.md`: it rewrote the whole row for the
current change (C4 with the rule for the rest of the node and the reviewer's
report on triggers 1 to 3; C5 with the floor check before each node and each
fix or write under the floor; C3 deferred to FU-034; four source entries).
