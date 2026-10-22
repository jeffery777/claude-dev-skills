# FU-006 inventory of restated rules (Issue #16, REQ-022)

This is the inventory that the user decided on with cards 1 to 5 (2026-10-22).
Line numbers refer to main at 1386a69. The "Action" column is the plan
before review. Cards 6a and 7a later changed the method: only the copies of
R-EXH-3, R-VER-2 and R-EXH-4 became pointers; every other "cite" item
stays word for word as on main and names its rule IDs. Restated text that
this inventory does not list goes to the FU-010 audit (card 8a).

Rows that became pointers (card 7a): D5 and V11 (R-VER-2); V10 and G12
(R-EXH-3); G8, G9, PP1, PP2 and PP3 (R-EXH-4). Every other row kept the
main text.

Legend for "Match": **same** = the copy says the same as the dev-core rule (wording may differ);
**subset** = says less than the rule (incomplete copy; citing the ID gives the full rule);
**differs** = says more than dev-core (extra obligation or detail) -> card 5 (or card 2 for masking).
Action: **cite** = replace the restated text with the rule ID (+ at most a short topic label, no conditions);
**keep** = operational step (commands, order) or skill-specific rule; stays as is.

## Skills (all load dev-core first, so a rule ID resolves)

| # | File:line | Restated text (short) | Rule | Match | Action |
|---|---|---|---|---|---|
| D1 | dev-deliver:38-40 | read-only nodes in parallel when fixed and independent | R-CAP-2 | same | cite |
| D2 | dev-deliver:40 | never run two writers at once | R-DEL-1 (writers never share files) | differs (Phase-1 sequential design) | keep (card 5) |
| D3 | dev-deliver:42-49 | agent/model/effort table; review rows = dev-review mode table | (dev-review table) | same as dev-review | keep explore/implement rows; review rows point to dev-review's mode table |
| D4 | dev-deliver:52-54 | receipt is a claim, not evidence; data, never instructions | R-REV-2, R-AUTH-1 | same | cite |
| D5 | dev-deliver:61-66 | classify before fix, fixes inside requirements; 2 rounds re-assess; stop rule | R-REV-4, R-VER-2 | same | cite |
| D6 | dev-deliver:73-77 | gate decides readiness, user decides authority; scan before commit/push; PR text scanned | R-REV-5, R-AUTH-1, R-REV-9 | subset (no Issue text, no merge scan) | cite; keep "in the order dev-implement gives" |
| D7 | dev-deliver:83-84 | every decision incl. REQ-GAP as decision card | R-AUTH-6, R-REV-3 | same | cite |
| I1 | dev-implement:21-23 | smallest change; no unrelated refactor, speculative options, overwriting | R-STG-4, R-RIG-3 | same | keep (it is the implement step itself) |
| I2 | dev-implement:28-31 | light work: review + commit gate first; uncommitted -> "not independently reviewed" | R-RIG-2 | same | cite |
| I3 | dev-implement:36-47 | commit/push order, commands | R-REV-9 | operational | keep |
| I4 | dev-implement:42 (step 4) | before push confirm identity/message match the scan | R-REV-9 (new candidate after change) | differs (explicit extra check) | keep (card 5) |
| I5 | dev-implement:49-53 | new scan after change; records never in covered commit; PR branch; stop without reviewer | R-REV-9, R-EXH-3 | same | cite |
| V1 | dev-review:10 | read-only unless user asks for fixes | R-REV-1 | same | cite |
| V2 | dev-review:21 | mode from actual impact, not file type | R-REV-7 | same | cite |
| V3 | dev-review:21-22 | when unsure, use the stronger mode | (R-RIG-2 spirit) | differs | keep (card 5) |
| V4 | dev-review:22-23 | security review/scan uses dev-security-reviewer, never dev-reviewer | R-REV-1 | same | cite |
| V5 | dev-review:25-27 | commit/push scan target list | R-REV-9 | subset | cite |
| V6 | dev-review:28-29 | reviewers mask secrets/private identifiers | none in dev-core | differs | card 2 |
| V7 | dev-review:42-46 | never review own change; look beyond requirements; relation; thresholds; below -> residual | R-REV-1, R-REV-3 | same | cite; keep "the brief tells the reviewer…" as a step |
| V8 | dev-review:47-56 | native /code-review: author context not independent; write-tool pass is extra; "stops at the gate (dev-core §8)" | R-REV-1 | same; cites a section | keep tool mapping steps; cite R-REV-1 instead of "§8" |
| V9 | dev-review:59-63 | classify before fix; REQ-GAP/NHD as card; no REQ-GAP fix same round | R-REV-3, R-REV-4 | same | cite; keep "save the report to .dev/…/reviews/" |
| V10 | dev-review:65-68 | records of a PR head: never committed; PR comment if authorized; else report | R-EXH-3 | same (MR2-B-001 copy) | cite |
| V11 | dev-review:69-75 | proportional re-review; narrow confirmation before push; 2 rounds; stop rule | R-REV-4, R-VER-2 | same | cite |
| G1 | dev-gate:13-14 | gate authorizes no external write | R-REV-5, R-AUTH-1 | same | cite; keep "summarizes evidence, not another review" |
| G2 | dev-gate:20-21 | "Requires" column restates R-REV-9 scan scope and R-EXH-1..3 | R-REV-9, R-EXH-1..3 | same | cite (keep column as list of IDs + topic) |
| G3 | dev-gate:25-34 | bind identity (commands) | R-EXH-1 | operational | keep |
| G4 | dev-gate:36-39 | reuse only when content…freshness match; pre-commit/previous-head review never satisfies merge | R-CAP-3, R-EXH-1, R-EXH-3 | same | cite |
| G5 | dev-gate:42-44 | unaffected parts may reuse evidence with reason and coverage | R-EXH-3 | same | cite |
| G6 | dev-gate:47-58 | blocker checklist | R-REV-5, R-REV-4, R-REV-7, R-REV-9, R-RIG-3 | same, except 2 items | keep list as ID + topic; items "security risk with or without a finding ID" and "a write change without a requirement" differ -> card 5 |
| G7 | dev-gate:60-61 | never infer platform from content; re-read before merge | R-EXH-4 | same | cite |
| G8 | dev-gate:72-73 | checker fails / no line -> UNVERIFIED, never NOT_CONFIGURED | R-EXH-4 | same (3rd copy; GateRuleText) | cite; keep command |
| G9 | dev-gate:74-80 | no-profile read: one call, command; read fails / other base or head -> UNVERIFIED; failed/unrun check never Passed | R-EXH-4, R-EXH-2 | same (3rd copy; GateRuleText) | keep command and "list each check"; cite outcomes |
| G10 | dev-gate:81-83 | policy change -> card, NEEDS HUMAN DECISION per head blob | platform-profile.md (not in dev-core) | same as platform-profile.md | single copy in platform-profile.md; dev-gate points to it |
| G11 | dev-gate:85-86 | head changes -> gate void, rerun | R-EXH-3 | same | cite; keep "rerun from step 1" |
| G12 | dev-gate:87-91 | record result: never commit to PR branch; comment if authorized | R-EXH-3 | same (copy) | cite |
| P1 | dev-plan:46-49 | REQ-GAP becomes REQ only after user; sources record ID + decision "quoted verbatim"; never on your own | R-REV-3 | same + "verbatim" | keep ingest step incl. "verbatim" (card 5); cite the prohibition |
| P2 | dev-plan:55-56 | unknown risk -> standard or higher | R-RIG-2 | same | cite |
| C1 | dev-continue:41-44 | commit rules still apply; "(dev-core section 8)" | R-REV-9; section 8 | section cite | card 3 |
| C2 | dev-continue:45-47 | once a PR exists never commit the checkpoint | R-EXH-3 + user's PR-C1 card 1 | differs (checkpoint is wider than review records) | keep (card 5) |
| C3 | dev-continue:49-51 | scan exact comment text before posting; no scan, no post | R-REV-9 | same | cite |
| O1 | dev-docs:19-20 | do not change code, commands, paths, license text | R-WRT-1 | same | cite |
| O2 | dev-docs:21-23 | bilingual: compare obligations; no STE claim | R-WRT-1 | same | cite |
| O3 | dev-docs:22 | the authoritative language wins | none | differs | keep (card 5) |
| O4 | dev-docs:24-25 | no private paths, credentials, runtime state | R-AUTH-7 | same | cite |

## References (read by the main session, which has loaded dev-core)

| # | File:line | Restated text | Rule | Match | Action |
|---|---|---|---|---|---|
| RC1 | decision-card:11-17 | EN per ASD-STE100; zh-TW plain-writing list; no STE claim | R-WRT-1 | same | cite |
| RC2 | decision-card:18-19 | REQ-GAP options add/defer/reject | R-REV-3 | same | keep as template value list |
| RC3 | decision-card:23 | mask "as in the review report" | (masking) | — | card 2 |
| RC4 | decision-card:24-26 | card grants no authority; dev-plan ingests | R-AUTH-1, R-REV-3 | same | cite |
| RR1 | review-report:20-21, 31-32 | relation / class value lists | R-REV-3, R-REV-4 | same | keep value lists (format vocabulary), drop explanations |
| RR2 | review-report:23-29, 34-40 | severity thresholds; REQ-GAP / SCOPE-CREEP explanation | R-REV-3, R-RIG-3 | same | cite |
| RR3 | review-report:59-63 | masking rule | none | differs | card 2 |
| RR4 | review-report:65-72 | disposition requirements | R-REV-3 | same | cite |
| RW1 | requirements-wiki:14 | commit_state "(dev-core §8)" | section 8 | section cite | card 3 |
| PP1 | platform-profile:96-97 (item 7) | checker fails -> UNVERIFIED (GateRuleText) | R-EXH-4 | same | cite, keep "user decision Q6 (a)" provenance |
| PP2 | platform-profile:99-101 | no-profile read, other base -> UNVERIFIED (GateRuleText) | R-EXH-4 | same | cite, keep command + Q5/Q8 provenance |
| PP3 | platform-profile:4-6 | NOT_CONFIGURED unless no-profile read fails | R-EXH-4 | same | cite |

## Agents (do NOT load dev-core today; CF-007)

| # | File:line | Restated text | Rule | Note |
|---|---|---|---|---|
| A1 | dev-reviewer:33-43 | requirement_relation, thresholds, Core blocker MUST-FIX | R-REV-3 | card 1 |
| A2 | dev-reviewer:48-52, dev-security-reviewer:33-37 | masking | none | card 1 + card 2 |
| A3 | dev-security-reviewer:25-32 | commit/push scan scope and commands | R-REV-9 | card 1 |
| A4 | dev-security-reviewer:41-43 | NOT_RUN / UNAVAILABLE, never passed | R-REV-7 | card 1 |
| A5 | dev-security-reviewer:44-48 | relation, severities, Core blocker | R-REV-3 | card 1 |
| A6 | dev-implementer:20-24, task-brief:15-16 | no external writes; escalate list | R-DEL-1, R-AUTH-2 | card 1 (task-brief is the brief text the agent gets) |

## Section citations inside dev-core itself

R-REV-1 and R-REV-9 say "(section 8)"; deltas DL-009 says "section 8". Card 3.

## Out of the inventory (not rules or not in scope)

- README.md and docs/: not skills; not restructured here (limit).
- Output templates that must carry fixed text (dev-gate output "Writing: …" line, review-report header) stay: they are required output, not restatements.

