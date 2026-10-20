# Follow-ups

Durable targets for Deferred findings. Each entry is the tracking object a
Deferred disposition points to. Close an entry by linking the change that
resolved it; never delete it.

| ID | From | Item | Owner | Reason deferred | Remaining risk | Verification plan | Promotion trigger | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FU-001 | DR-022b (Issue #1) | Cowork runtime test of the plugin | jeffery777 (maintainer) | No Cowork environment and no installed plugin session were available in the Phase 1 session; the test needs the maintainer's Cowork account | Skills may not load in Cowork, `${CLAUDE_SKILL_DIR}` relative paths may not resolve, or no shell may be available | Install `dev-skills` from the marketplace in Cowork, run `dev-plan` on a sample objective, try `graph.py validate`, record the result in this row | Blocking before any claim that REQ-001 "skills load in Cowork" is met, and before the first tagged release | Open (GitHub Issue #3) |
| FU-002 | MR-18 (PR #2) | Faster fingerprinting of large ignored trees | jeffery777 (maintainer) | A content hash of every ignored file is correct and fail-safe; a faster stat-based scheme weakens detection and needs a design decision | `tree_fingerprint.py` may take minutes in projects with large `node_modules` or `.venv` folders | Time the script on a large project; if slow, evaluate excluding named dependency folders with a recorded limit | Blocking when a real project reports a fingerprint run longer than one minute | Rejected (obsolete): `tree_fingerprint.py` was removed by user decision (PR #2 handoff, decision 3); required reviews now stop at the gate when the read-only plugin reviewer is unavailable |
