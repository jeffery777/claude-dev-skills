# Review round 1 — issue-31-fu005-pr3 (deep review)

- Target: f2dfd19..working tree at e87a6d2 (+ uncommitted, intent-to-add)
- Diff identity: `git diff HEAD --binary` sha256 cd9a832ef3127b3dcf49ba11802fdf582aa424b555b4a8c42fd205961dd0d042; `git diff f2dfd19 --binary` sha256 b3c8bf293a5537bf8bd402027b5ec2f07589f8d02c5de63c2671e4e3b75ffaf0 (10 files, +201/−0)
- Mode: deep
- Reviewer: `dev-skills:dev-reviewer` (requested model/effort: opus/xhigh; effective: unknown)
- Scope: `CHANGELOG.md`, `agents/dev-reviewer.md`, `agents/dev-security-reviewer.md`, `skills/dev-deliver/references/task-brief.md`, `docs/requirements/REQ-025-on-demand-core-loading.md`, `docs/requirements/log.md`, `.dev/issue-31-fu005-pr3/` (4 files). Requirements: REQ-025, REQ-024, REQ-022. DoD: graph node T1 and the REQ-025 PR-3 acceptance.
- Core review criteria given: `review-and-security.md`, `workflow.md` from the main checkout at f2dfd19 (not the tree under review).
- Writing: written per ASD-STE100 principles; full conformance not verified (R-WRT-1)

## Findings

| ID | Relation | Severity | Location | Finding | Evidence | Impact | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR3-R1-001 | in-scope | MUST-FIX | `.dev/issue-31-fu005-pr3/comparison.md` | The sentence-by-sentence comparison marks several copies that are shorter than `dev-core` as "same" (R-REV-3 MUST-FIX list; R-REV-7 "open security concern", "actual impact", "when unsure", "incomplete, failed or insufficient coverage"; other R-REV-7 sentences), says the Core criteria fill the R-REV-1 R-RIG-4 gap (against spec 2.1), and leaves out the receipt part of `task-brief.md` | `skills/dev-core/SKILL.md` R-REV-3, R-REV-7; `agents/dev-reviewer.md:45-48`; `agents/dev-security-reviewer.md:26-32`, `:49-51`; spec 2.1 | PR-4 and FU-011 would get a false baseline; the gaps themselves are existing state | necessary fix | Fixed in 9986326 (rows corrected); review round 2 found more mislabeled rows (PR3-R2-001, PR3-R2-002) and the R-VER-2 stop rule fired; then cut down per user decision card PR3-C5 (a) (「同意你的建議，C5a C6a」, relayed by the orchestrator session): the file now states only that the copies are unchanged and compares the new text with `dev-core`; the copy-gap inventory is input in Issue #33. Re-review: round 3 |
| PR3-R1-002 | in-scope | MUST-FIX | `.dev/issue-31-fu005-pr3/reviews/round-0-security-design.md` | The early R-REV-7 scan is bound to diff 9f843c72…, not to the current candidate (`CHANGELOG.md` changed after the scan; the allow-list line was changed and reverted); the record does not say which evidence still applies | R-REV-7 "Any content change after a scan is a new candidate" | The PR-3 acceptance needs an R-REV-7 scan of the candidate | necessary fix | Fixed: R-REV-7 re-scan of the candidate f2dfd19..9986326 content (SCAN-3 in the round-2 record; full-range diff sha256 be435f291b0f7a87677cb218bbc0661af846b25cca57063fe6158688ead354d2); 0 MUST-FIX |
| PR3-R1-003 | in-scope | MUST-FIX | `round-0-security-design.md`, SR21B-001 section | The Deferred SR21B-001 has no durable target: "a separate small PR" does not exist, and "residual for PR-4" is not true (the spec PR-4 row does not list `.dev/followups.md`) | Core `review-and-security.md:21`; R-REV-3; R-REV-5; spec 7.2 PR-4 row | An incomplete Deferred blocks the gate | needs human decision | Fixed: user decision card PR3-C3 (a) (「同意你的建議，C3a C4b」, relayed by the orchestrator session): GitHub Issue #32 is the durable target of the Deferred SR21B-001 (round-0 record); the false "residual for PR-4" sentence is removed. Narrow re-review pending |
| PR3-R1-004 | gap | REQ-GAP | new paragraph in both reviewer agent files; checklist table F rows R-RIG-4, R-REV-7, R-REV-8 | The paragraph uses Core only to judge the change, but table F counts obligations on the reviewer's own behavior (R-RIG-4 premise check, rev:15; R-REV-7 and R-REV-8 sentences that the agent files do not copy) as "read into context through the criteria" | spec 2.1 ("the reviewer's actions still come only from the agent file and the brief"); checklist table F | Some audit gaps may stay open on the reviewer subagent side; not a regression of PR-3 | needs human decision | Deferred (user decision card PR3-C4 (b), 「同意你的建議，C3a C4b」). Target: Issue #33, input for FU-005 PR-4 (user decision card PR3-C6 (a)). Owner: jeffery777 (maintainer). Reason: changing the approved design (card 8a) or adding sentences to the agent files is out of PR-3. Remaining risk: until then the reviewer agent files do not copy the R-RIG-4 premise sentence of R-REV-1 and some R-REV-7 and R-REV-8 sentences (existing state). Verification plan: the PR-4 review checks each checklist table F row whose reader is a reviewer subagent. Promotion trigger: PR-4 starts, or a review misses one of these obligations |

Verified with no problem: the brief line and both paragraphs are word for word the spec 2.2 text; 0 deleted lines in every file; copies (C-10, C-22, C-24, DL-004, DL-011, DL-016, R-REV-9) unchanged; no new rule-ID citations; the new text loosens no DL row, CB-1 to CB-5, D-013 to D-018 or REQ-011 to REQ-025; PR3-S0-001 and PR3-S0-002 dispositions complete; CHANGELOG accurate; REQ-025 PR-3 acceptance matches the spec row.

Suspicions (unverified): the comparison was finished after the edits (corrected in its header); the graph transitions were recorded in one step after the work.

## Verification evidence

- `PYTHONDONTWRITEBYTECODE=1 bash scripts/validate.sh`: all checks passed (131 tests), twice; `git status` the same before and after.
- Diff hashes recomputed; spec text compared in memory.
- Not run: `gh`.

## Residual risk and limits

- "only your brief sets policy" and "guidance … is data" might be read to exclude the user's global instructions; approved text, no reproducible failure.
- The reviewer cannot check that a listed path is outside the tree under review; that depends on the main agent (spec 2.3).
- `dev-security-reviewer` has no severity thresholds (existing state).
- Graph T1 `owns` does not list the REQ-025, log and `.dev` record files.
- Commit 1 says "before PR-3 starts", but the acceptance was committed after the implementation and round 0 had started in the working tree.
- Below threshold: REQ-025 PR-3 acceptance item "An early … review and an R-REV-7 Security Diff Scan;" has no verb; abbreviations in the records are not defined in the files.
- The reviewer used read-only Bash commands outside the `dev-reviewer` list (cat, sed, grep, stat, shasum, python3 in memory); no file written.
