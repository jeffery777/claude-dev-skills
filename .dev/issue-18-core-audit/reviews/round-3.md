# Review round 3 (deep, fresh reviewer), Issue #18

- Target: working tree against HEAD `a1d42a6`, `git diff HEAD --binary` sha256 `08631fb7…` (scope narrowed by
  user decision card 5). Reviewer: `dev-skills:dev-reviewer` (opus, xhigh). CB-4 before and after: HEAD, status
  hash `9f3f8def…`, diff hash and ignored-file list unchanged.
- Commands (reviewer): `PYTHONDONTWRITEBYTECODE=1 bash scripts/validate.sh` exit 0 (131 tests, 21 anchors, 41
  rules); `man git-fetch` (PRUNING); read-only `git config --get` of the prune settings. Skipped: GitNexus.
- Result: BLOCKED. Process deviation reported by the reviewer: it wrote the `validate.sh` output to a file in
  the session scratchpad outside the repository (`<scratchpad>/validate.log`), against the no-write brief.
  Evidence for FU-013 (card 3d: record the exact file names first).

## Findings

| ID | Relation | Severity | Finding |
| --- | --- | --- | --- |
| R3-001 | in-scope | MUST-FIX | R-EXH-4 merge preconditions miss the live base and the review identity and freshness (exh:48); audit rated it an omission |
| R3-002 | in-scope | MUST-FIX | R-CAP-1 substitute conditions miss prerequisites, target, operations and completion conditions (wf:47) |
| R3-003 | in-scope | MUST-FIX | R-RIG-4 outcome classes and "stop optimizing" miss Core's conditions (wf:95-97, wf:99) |
| R3-004 | in-scope | MUST-FIX | R-VER-3 "answer side questions briefly and continue" misses "unless the objective is explicitly cancelled or replaced" (wf:76) |
| R3-005 | in-scope | MUST-FIX | R-REV-4 management measure misses "real" owner and "stop or handoff" (rev:15); DL-017 claims it carries Core's conditions |
| R3-006 | in-scope | MUST-FIX | The R-REV-9 `--prune` policy states no preview, recovery or lower-risk check (auth:21); "local branches and commits do not change" holds only with the default refspec and no tag pruning; the policy names no project scope |
| R3-007 | in-scope | MUST-FIX | Missing qualifiers in permissions: R-AUTH-2 exact target (auth:13), R-REV-1 explicitly (rev:9), R-REV-8 independent authorized safe work (rev:69), R-CAP-2 bounded reads, available and compatible (wf:50) |
| R3-008 | in-scope | MUST-FIX | R-EVD-2 "summarize or archive only at a safe close" misses superseded, bounded material and the checks before the operation (wf:119) |
| R3-009 | in-scope | NIT | R-AUTH-7 no longer asks a dry-run before moving and archiving (HEAD did); equal to Core but a change against HEAD not recorded |
| R3-010 | in-scope | NIT | Record errors: audit cites R-VER-4 (removed); R-CAP-2 marked fixed but partly omitted; DL-017 lacks R-REV-9; R-WRT-1 copies in `review-report.md` and `decision-card.md` not listed; round-1/round-2 rows carry two dispositions; CHANGELOG claim not yet true |
| R3-011 | in-scope | MUST-FIX | FU-005, the target of the Deferred omissions, still has the FU-004 reason, plan and trigger, and no remaining risk or verification plan for the omissions |

Reviewer suspicions (not rated): R-EXH-1 reuse conditions (exh:9); R-AUTH-2 "do not re-ask" (exh:30); R-RIG-4
"and similar mechanisms" (wf:82); R-REV-7 policy basis (rev:45); R-AUTH-5 new reading vs CB-4 fallbacks; CB-1
runtime state (CF-009).

## Stop

Rounds 2 and 3 both reported new blockers from the same mechanism: a compressed sentence drops a Core
condition. The narrowed acceptance ("no sentence looser than Core") did not converge either. Under R-VER-2 and
the user's instruction for this round, no fix starts; decision card 7 goes to the user, and the work waits for
the user's 「繼續」.

## User decision and final dispositions (rounds 1 to 3)

User decision card 7: 「繼續，7a」. The header says that where a rule is shorter or looser than its cited Core
section, that Core section governs, and that a stricter rule (DL rows, CB-1 to CB-5, user decisions) still
applies; PR-A keeps only that header, R-WRT-1 and the card-4 `--prune` rule. The user also required
(2026-10-22) that no project tightening regresses: PR-A changes no DL row except the new DL-017, no CB binding,
no other skill and no agent file. R-AUTH-7 (dry-run before moving, archiving and cleaning, stricter than Core)
is back to its base wording.

Each finding has exactly one final disposition. "Deferred to FU-005" means: target `.dev/followups.md` FU-005,
owner jeffery777 (maintainer); reason, remaining risk, verification plan and promotion trigger are in that row.

| Finding | Final disposition |
| --- | --- |
| R1-001 | Deferred to FU-005 (omissions; the R-AUTH-3 conditions are a looser sentence that the header now hands to Core) |
| R1-002 | Deferred to FU-005 (R-EXH-5 omission) |
| R1-003 | Fixed: R-WRT-1 keeps machine literals unchanged for the writing rules; R-REV-8 masking still applies |
| R1-004 | Fixed: user card 4 (a); scope and preconditions per R3-006 |
| R1-005 | Fixed (audit text) |
| R1 S1 to S6 | Deferred to FU-005 |
| R1 S7 | Deferred to FU-013 (card 6 (a)) |
| R1 S8 | Fixed (audit lists the Core lines and their rules) |
| R2-001 | Fixed: R-VER-3 has its base wording again (the misplaced exception is gone; the Core exception itself is R3-004) |
| R2-002, R2-003 | Deferred to FU-005 |
| R2-004, R2-005, R2-006 | Fixed (audit text) |
| R2 S1, S2, S3, S5, S6 | Deferred to FU-005 |
| R2 S4 | Deferred to FU-013 (card 6 (a)) |
| R3-001 to R3-005, R3-007, R3-008 | Deferred to FU-005 (looser sentences; Core governs by the header) |
| R3-006 | Fixed: the rule names the default refspec, no tag pruning, a stop and ask otherwise, no recovery needed, and the fetch output as the read-back. A separate preview was option (b) of card 4, which the user did not choose |
| R3-009 | Fixed: R-AUTH-7 base wording restored (no regression of the dry-run tightening) |
| R3-010 | Fixed: audit (no R-VER-4, PR-A column, R-REV-9 row, R-WRT-1 copies), DL-017 lists R-REV-9, source-map note, one final disposition per finding (this table), CHANGELOG wording |
| R3-011 | Fixed: the FU-005 row has the Deferred fields for these findings |
| R3 suspicions | Deferred to FU-005 (CB-1 runtime state: CF-009 item 1) |

Writing spot-check (reviewer): R-AUTH-5 "a safe fallback is missing" has no object (as in Core); the R-REV-9 policy
sentence carries three facts and a citation; R-REV-4 and R-RIG-4 use different terms for one concept. Limits: no
full ASD-STE100 check. Written per ASD-STE100 principles; full conformance not verified.
