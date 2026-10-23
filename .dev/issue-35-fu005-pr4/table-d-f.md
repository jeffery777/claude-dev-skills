# FU-005 PR-4: table D decisions and table F reviewer rows (Issue #35, REQ-025)

Coordination data, not completion evidence (CB-1). Written per ASD-STE100
principles; full conformance not verified.

Base: `041a6be` (main). Checklist: `.dev/issue-22-fu005-records/fu005-checklist.md`.
Core line numbers are those of the pinned v0.1.1: wf = `workflow.md`, auth =
`authorization-and-stops.md`, rev = `review-and-security.md`, exh =
`exact-head-and-evidence.md`.

## Criterion

A rule keeps its text word for word when one of its sentences is stricter
than Core, also only literally, in the protective direction: the sentence
requires more checks, records or stops than Core, for example because it
leaves out a Core qualifier such as 「適用」 (checklist items C-20 to C-22) or
a Core condition (item C-7). A sentence whose broader prohibition makes the
agent do less (fewer questions, less improvement work) is looser, and Core
governs it (user decision card PR4-C2 (a)). A stricter sentence that a kept
rule or a file that stays carries for the same reader is not lost.

## Table D decisions

| Rule | Decision | Reason |
| --- | --- | --- |
| R-STG-1 | index line | Same as wf:9 and wf:11-20 |
| R-STG-3 | index line | "A plan authorizes nothing" is wider than wf:14 (modification, delegation, external writes); R-AUTH-1 (kept) gives authority only to the user's instructions or an approved platform mechanism, and `skills/dev-plan/SKILL.md` step 8 keeps the sentence |
| R-STG-4 | **kept word for word** (DL-031) | "cheap security checks" leaves out 「適用」 of wf:16 and rev:37; no other file carries it |
| R-STG-5 | index line | Same as wf:20 and wf:22, or shorter; `skills/dev-continue/SKILL.md` keeps its resume steps |
| R-RIG-4 | index line | Same as wf:82-99 or shorter; "do not delay delivery" and "stop optimizing" make the agent do less (card PR4-C2 (a)); "does not prove a fact" is carried by R-AUTH-1 (facts are checked against the repository, Git or platform evidence) |
| R-AUTH-2 | index line | Same as auth:11-15 or shorter; "Do not re-ask" makes the agent ask less (card PR4-C2 (a)) |
| R-AUTH-3 | index line | Shorter than auth:21-23; the copies in `agents/dev-implementer.md` and `task-brief.md` stay and are stricter (checklist item C-23) |
| R-AUTH-4 | **kept word for word** (DL-032) | Leaves out 「外部」 of auth:25, and does not name the compliant substitute that auth:25 allows |
| R-AUTH-5 | index line with the project reading | Same as auth:31-38; the looser "and no safe fallback exists" is replaced by the reading (DL-028) |
| R-REV-5 | index line | Same as rev:25-27 or shorter; "No review or gate authorizes an external write" is carried by R-AUTH-1 ("a PASS, a review, a gate … grants nothing") |
| R-EXH-1 | index line | Same as exh:9-14 or shorter; "SHAs" and the DoD are carried by `skills/dev-gate/SKILL.md` and R-REV-8 |
| R-CAP-2 | index line | Shorter than wf:50 |
| R-CAP-3 | index line | Same as wf:48-49 |
| R-DEL-1 | index line | Shorter than wf:60; "owned paths", "report blockers" and "one final receipt" are carried by `task-brief.md` and the agent files |
| R-VER-1 | **kept word for word** (DL-033) | "Keep failures, skips and negative cases" has no condition; wf:70 keeps them as the evidence lifecycle requires (like item C-7) |
| R-VER-3 | index line with the project reading | Same as wf:76; the reading limits the exception (DL-029) |

Before the edit, an independent design review (dev-reviewer) made the same
judgment. Its tree check (CB-4) found a change during the review (the main
agent edited `README.md` and `skills/dev-plan/SKILL.md`), so its result is
not evidence; the PR-4 review checks table D again.

## Table F rows whose reader is a reviewer subagent (Issue #33 item 1)

Result of the PR-4 deep review (round 1, dev-reviewer, at the diff with
SHA-256 `4652b2ef…c6c98` of `git diff HEAD --binary`). How the Core
obligation reaches the reviewer subagent:

- (a) the agent file or the brief template states it as an instruction;
- (b) only through the Core review criteria, which design 2.1 and card 8a
  use only to judge the change, not to direct the reviewer's own actions;
- (c) not at all.

| Table F row | Core | Result | What only (b) or (c) covers |
| --- | --- | --- | --- |
| R-RIG-4 (reviewer through rev:15) | rev:15; trigger in wf:82 | (b); the trigger is (c) when the review covers no documents | The premise and counter-evidence check is in no agent file, `task-brief.md` or `review-report.md`; `dev-reviewer` gets `workflow.md` only for document reviews |
| R-AUTH-1 (security reviewer, criteria) | auth:9, 11, 15 | mostly (a), the rest (b) | The other checks of auth:9, and auth:15. `dev-reviewer` gets no auth file and has only its own copy |
| R-REV-1 (reviewer) | rev:9-15 | (a) and (b) | The document-review focus of rev:9 (missing prerequisites, unsafe guidance, private data) and the premise check of rev:15 |
| R-REV-7 (security reviewer, criteria) | rev:45-57 | (a) and (b) | Actual impact, an open security concern, examine the boundary first when unsure, an unresolved risk blocks readiness (rev:49), an incomplete or failed scan is never Passed (rev:53) |
| R-REV-8 (both reviewers) | rev:63-69 | (a) and (b) | Deterministic checks for machine-checkable facts (rev:63), records for outside evidence (rev:67), a missing tool blocks only the dependent readiness (rev:69) |
| R-EXH-1 (Merge Review reviewer) | exh:9-16 | mostly (a), the rest with the main agent | The merge-base and the change-request identity are bound by the main agent (`dev-gate` step 1) |
| R-EXH-2 (Merge Review reviewer, criteria) | exh:22-24 | (a) and (b) | Feature states, compatibility claims, release scope, superseded descriptions, "changed behavior needs a docs change or a reason", a missing CI run or an empty inventory is not Passed |

The table F answer "yes, read into context" overstates what reaches the
reviewer's own actions for these rows. The gaps existed before PR-4
(subagents never loaded `dev-core`); PR-4 does not cause them. They are
input for FU-011, as Issue #33 item 2 is; the agent files do not change in
PR-4.
