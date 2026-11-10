# Issue #106 PR-2 design review round 1 (card I106-C12 (a), MR108-02, MR108-03)

Written per ASD-STE100 principles; full conformance not verified.

- Reviewer: `dev-security-reviewer`, requested opus/xhigh; effort recorded
  `unknown`, not read back (only merge-time dispatches are read back).
- Bound state: HEAD `9d17e9c`, status SHA-256 `a27e7f03…`, diff SHA-256
  `e3b0c442…` before and after (equal); `reviewer_acceptance.py check` gave
  `PASS` before and after.
- Target: `.dev/issue-106/pr2-c12-design.md` (first version), `cards-8.md`.
- Verdict: BLOCKED (LFS part). The push-option part passes.

| ID | Severity | Class (R-REV-4) | Disposition |
| --- | --- | --- | --- |
| P2D-01 | MUST-FIX | necessary fix: in the threat model (a host setting), card C12 (a) and Core `:81`, `:91`, `:99` cover it. The pre-push hook runs in the dry-run (push-scan "Not covered" says so), so an LFS hook can send objects before step 6a. Premise "git-lfs uploads in a dry-run" not tested here (no git-lfs) | Fixed in design: the dry-run gets `--no-verify` (no hook runs in it); the real push in step 9 drops `--dry-run --porcelain --no-verify`, so its hooks still run. Fix A of the reviewer: a change of means under card (a); told to the user (card I106-C13) |
| P2D-02 | MUST-FIX | necessary fix: a changed LFS file keeps the `version` line as context, so `^[+]version` misses the most common case | Fixed in design: pattern `oid sha256:[0-9a-f]{64}`, not anchored; the `hawser` form is deleted. A deleted pointer or a document that has this text also stops (fail closed). Told to the user (card I106-C13) |
| P2D-03 | SHOULD-FIX | necessary fix: forced color output hides an anchored `+` | Fixed by P2D-02 (no anchor); step 8 unchanged |
| P2D-04 | SHOULD-FIX | necessary fix: "the same text file" conflicts with "post the scanned file itself" | Fixed in design: a separate text file for the metadata and ref names, the same `awk`, then the reviewer |
| P2D-05 | SHOULD-FIX | needs human decision: the narrower LFS residual risk needs the user's acceptance (R-REV-8) | Card I106-C13 |
| P2D-06 | SHOULD-FIX | necessary fix: success is "prints `0` and exits 1" | Fixed in design |
| P2D-07 | NIT | worth improving: a committed pointer sample would stop the PR-2 push | Fixed in design: tests build the sample at run time |
| P2D-08 | NIT | necessary fix: incomplete change list | Fixed in design: `tests/test_publication_data.py:49` changes; REQ-011 note; the push-option test uses an isolated Git environment |

Keep as is (reviewer's list): an empty `push.pushOption` value stops (fail
closed); `GIT_CONFIG` (already in "Not covered"); "four" options; "both sides"
of a ref line; "the command of step 8" becomes "the `log` command of step 8";
"this push" wording of step 5 for a commit-time signature.
