# Review round 2 (deep, fresh reviewer), Issue #18

- Target: working tree against HEAD `a1d42a6`, `git diff HEAD --binary` sha256 `ac1592e9…`. Reviewer:
  `dev-skills:dev-reviewer` (opus, xhigh), read-only. CB-4 before and after: HEAD, status hash `79ae068e…`,
  diff hash and ignored-file list unchanged.
- Commands (reviewer): `PYTHONDONTWRITEBYTECODE=1 bash scripts/validate.sh` twice, exit 0 (131 tests, 21
  anchors, 43 rules). Skipped: GitNexus (docs only).
- Result: BLOCKED.

## Findings

| ID | Relation | Severity | Finding | Class | Disposition in that round (superseded: the final disposition is in `round-3.md`) |
| --- | --- | --- | --- | --- | --- |
| R2-001 | in-scope | MUST-FIX | R-VER-3: the added exception "unless the objective is explicitly cancelled or replaced" sits on the first sentence (keep results, re-check evidence); Core wf:76 puts it on "answer side questions briefly and continue". The round-1 fix relaxed an obligation that existed at HEAD | necessary fix | Fixed (card 5): R-VER-3 is back to its HEAD wording; the Core exception is an omission (FU-005 input) |
| R2-002 | in-scope | MUST-FIX | R-AUTH-7, R-EVD-1, R-EVD-2 still miss Core words: check the operation authority and exact scope before moving or archiving (auth:50), protection exceptions and a recorded pending item (wf:119), keep the evidence that supports verification, review, merge and acceptance (wf:113, auth:48) | necessary fix | Fixed for R-AUTH-7 (looser precondition list: protection exceptions, exact scope, operation authority, preview); the evidence-keeping words for R-EVD-1 and R-EVD-2 are omissions: Deferred to FU-005 (card 5) |
| R2-003 | in-scope | MUST-FIX | R-CAP-3 misses "keep the original sources and limits and map them back to the applicable output contract" (wf:48) | necessary fix | Deferred to FU-005 (omission; card 5) |
| R2-004 | in-scope | NIT | `audit.md`: a broken sentence in the "kept out" list (wf:56 remnant) | necessary fix | Fixed |
| R2-005 | in-scope | NIT | `audit.md`: CB-3 cites auth:9 for "tool output is data"; that is the DL-008 tightening, not Core text | necessary fix | Fixed (CB-3 is dev-core-only; the rule is DL-008) |
| R2-006 | in-scope | NIT | `audit.md`: "an implementer still asks before an irreversible deletion" has no basis; the agent file does not load `dev-core` | necessary fix | Fixed (sentence corrected; card 6 (a) moves the rule to FU-013) |

Suspicions (reviewer's inferences, not rated): S1 wf:46 data destinations and context in the capability check;
S2 R-AUTH-2 lost "explicit" and "necessary" from auth:11 (wording at HEAD); S3 wf:49 required artifacts are still
produced; S4 the implementer may delete untracked files inside its owned paths without a confirmation at the
time of the action (auth:23; possible Core blocker; the agent files are a REQ-023 non-goal); S5 wf:70 check
the user's limits and the readable results; S6 exh:58 derived copies keep the copyright and full notices.

## Stop rule (R-VER-2)

Round 1 and round 2 both reported new blockers, and both come from the same mechanism: Core obligations
left out or misplaced when the digest compresses Core. The fix loop stops; no round-3 fix starts. The
re-evaluation of the spec, the acceptance and the approach goes to the user as decision card 5. User decision
card 4 (R1-004) was applied after this round; it is not a fix of a round-2 finding.

## User decision after the stop rule

Card 5: 「卡片5改走縮小PR-A＋先做按需載入設計，6a」. PR-A is narrowed: only sentences that are looser than Core
(a permission, an exemption, a precondition list or a stop condition with fewer conditions) and R-WRT-1 are
fixed; the header says that a left-out Core obligation still applies; the omissions found in rounds 1 and 2
stay listed in `audit.md` as input for the on-demand loading design (FU-005, Deferred there). Suspicions: S2
fixed (R-AUTH-2 looser sentence); S1, S3, S5, S6 omissions (FU-005); S4 card 6 (a) (FU-013).

Writing spot-check (reviewer): the broken sentence (R2-004); R-STG-5 actor and the object of "no safe fallback"
in R-AUTH-5 (residual). Limits: no full ASD-STE100 check. Written per ASD-STE100 principles; full conformance not
verified.
