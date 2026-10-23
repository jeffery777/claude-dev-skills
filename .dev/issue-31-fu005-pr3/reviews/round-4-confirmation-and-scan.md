# Review round 4 — issue-31-fu005-pr3 (narrow confirmation R4 and commit scan SCAN-6)

- Target: HEAD 9986326 + staged candidate, committed unchanged as 5173b2a (commit 3)
- Diff identity: staged `git diff --cached --binary` sha256 1d6f49e5bfafcd75d4724fbb143abe2097dc509146a40ed6449070284f16dcc7 (5 files in `.dev/issue-31-fu005-pr3/`, +103/−56)
- Mode: narrow confirmation after user decision card PR3-C7 (a) (R-REV-4); commit scan (R-REV-9) and R-REV-7 reuse check
- Reviewers: `dev-skills:dev-reviewer` (R4; requested opus/high; effective: unknown); `dev-skills:dev-security-reviewer` (SCAN-6; requested opus/high; effective: unknown); in parallel on the same staged state
- Scope: the changes after round 3 (the `comparison.md` title, the PR3-S3-001 wording, the round-3 record). Requirements: REQ-025, REQ-011.
- Core review criteria given: R4 `review-and-security.md`; SCAN-6 `review-and-security.md`, `authorization-and-stops.md` (main checkout at f2dfd19).
- Writing: written per ASD-STE100 principles; full conformance not verified (R-WRT-1)

## Findings

| ID | Relation | Severity | Location | Finding | Evidence | Impact | Class | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR3-R4-001 | in-scope | NIT | `reviews/round-3-narrow-and-scan.md`, PR3-R3-001 disposition and requirement trace | "review rounds 1 and 2 checked it" is not exact: round 1 checked the earlier working-tree version of `comparison.md` (its findings led to the version in 9986326); only round 2 checked the 9986326 version, and round 2 found more mislabeled rows in it (PR3-R2-001, PR3-R2-002) | `round-1-deep.md` Target; `round-2-narrow-and-scan.md` Target | A reader may think the 9986326 version passed two checks | necessary fix | Fixed by this record (the round-3 record is not edited again, so that commit 3 stays as scanned): the correct statement is the one in this row. Re-review: the push and merge-time reviews of this PR |
| SCAN5-001 | in-scope | NIT | `reviews/round-2-narrow-and-scan.md`, PR3-S3-001 disposition | The disposition gave no re-review pointer | `review-and-security.md` review-findings | Record completeness only | necessary fix | Fixed: the re-review of PR3-S3-001 is SCAN-5 (round-3 record) and SCAN-6 (this record): both confirmed that the allow-list lines 13-15 equal f2dfd19 and that the records state the event truly |
| SCAN6-001 | in-scope | NIT | `reviews/round-3-narrow-and-scan.md`, residual risk | SCAN5-001 was listed as residual risk without one of the four dispositions | `review-and-security.md` review-findings | A gate could count it as a missing disposition | necessary fix | Fixed: SCAN5-001 has the disposition Fixed in the row above |

SCAN-6 (R-REV-9 commit scan of commit 3): staged diff, identity (author and committer `jeffery777`, GitHub noreply; config from the global gitconfig with `user.useConfigOnly`), message (sha256 7e9a35e5b29ab8783ffeb6638de33a6931fb66096db055575adb9259df609706): PASSED. Commit 3 read back with `git log -1 --format=fuller`: identity as scanned. R-REV-7: no non-`.dev` file changed since 9986326; f2dfd19..9986326 equals the SCAN-3 range (be435f29…), so the SCAN-3 result (0 MUST-FIX) still applies.

## Requirement trace

| REQ | Covered by | Verified by |
| --- | --- | --- |
| REQ-025 PR-3 (copies unchanged) | `comparison.md` | R4: `git diff f2dfd19 --cached --numstat`, 0 deleted lines in the three files |
| REQ-025 PR-3 (sentence-by-sentence comparison) | round-3 PR3-R3-001 disposition, corrected by PR3-R4-001 | R4: the 9986326 version exists with the per-row tables |
| REQ-011 | SCAN-6 | PASSED |

## Security scan

Applicable: yes (commit scan; records of security decisions). Status: PASSED; R-REV-7 evidence reused (reason above).

## Verification evidence

- R4: read-only `git diff --cached`, `git show 9986326:<path>`, `git log`, `git merge-base --is-ancestor`, grep.
- SCAN-6: read-only git commands with `--text --no-textconv --no-ext-diff`; identity and environment; pattern scan.
- Not run: tests (records only); `gh` by R4 and SCAN-6 (Issue #33 content was read by R3).

## Residual risk and limits

- The repository merges with squash (main has single-parent commits). After a squash merge, commit 9986326 is reachable only through the PR's commits on GitHub, not from `main`; the pointer was chosen by the user (card PR3-C7 (a)). The Merge Review record names the PR number.
- The `comparison.md` title says "against dev-core" while its Copies section compares with f2dfd19; the Labels line still defines `[fact]`, which the cut file no longer uses.
- The date in the PR3-S3-001 wording comes from the orchestrator session's confirmation; the repository holds no other evidence of it.
- The full text of cards PR3-C5 to PR3-C7 is not in the repository (answers and labels only).
- The records of this round's own scan (the commit-4 scan) are not in commit 4; they go to the Merge Review record.
- Zero MUST-FIX does not prove there are no defects.
