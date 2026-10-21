# Review round 1 — issue-10-cleanups (PR-C2)

- Target: working tree at ea80fa496fe2322732b1aebe88750749d7130372 (+ uncommitted changes and the untracked `.dev/issue-10-cleanups/`)
- Diff identity: sha256 of `git diff HEAD --binary` = d8263644dbb7bcb832f17e47a485580bd32c5c2095fcdd29f316d49b66797687 (the reviewer matched it before and after; HEAD and the status hash were also unchanged)
- Reviewer: `dev-skills:dev-reviewer` deep (R1-*); requested model opus; effective: unknown
- Scope: all changed paths. Items A1 to A13, B1 to B11 and FU-007 (Issue #10, user-approved list). Requirements: REQ-007, REQ-008, REQ-009, REQ-011, REQ-012, REQ-013, REQ-016, REQ-017, REQ-018, REQ-019. DoD: graph nodes T1 to T3
- Thresholds: `dev-core` R-REV-3 (strict)
- Commands: `bash scripts/validate.sh` (all checks passed, 82 tests); `graph.py validate` on both graphs (ok); the new block-scalar test run against `git show HEAD:scripts/check_pack.py` (fails, as intended); a mutation run without the string-type guards (tests still passed: R1-001)
- Result: 1 SHOULD-FIX; no MUST-FIX, NIT, SCOPE-CREEP or REQ-GAP. Per-item verdicts: every item PASS except A3 (partial, R1-001)
- Writing: written per ASD-STE100 principles; full conformance not verified. Spot-check of the new zh and EN text: short active sentences, explicit subjects, consistent terms; limits: no dictionary check, sample only

## Findings and dispositions

Each finding was classified before any fix (R-REV-4).

| ID | Relation | Severity | Finding | Class | New mechanism | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| R1-001 | in-scope (A3; REQ-009, REQ-007) | SHOULD-FIX | The new guard tests used only non-empty values outside the allowed sets, so they did not cover the MR4-02 string-type guards: with `not isinstance(..., str)` removed, the tests still passed and an empty `model:` crashed `check_pack.py` with TypeError | necessary fix | no | Fixed: `test_empty_values_fail_without_crash` covers an empty `model`, `effort` and REQ `status`; with the type guards removed, all three cases fail (error), and with them, the tests pass |

## Residual risk (below the thresholds)

Changed after the review (own text, no new obligation):
- The REQ-016 locator now says the runtime tools check is item 4 of the D-011 measurement plan.
- Node T3 also cites REQ-007.
- The FU-007 verification plan lists add, defer and reject, as `decision-card.md` asks for a REQ-GAP card.

Kept:
- D-015 (zh, EN) and `dev-core` section 8 still say records go "into the PR" or "in the PR or the final report"; the D-013 item 6 pointer and R-EXH-3 cover the PR case.
- `--evidence-file` accepts `link/` with a trailing slash when the target is a file inside the project; the agreed MR-A-001 wording is true in the POSIX sense; a target outside the root is still refused.
- Other PR #2 records (merge-review-1, -2, -5, other round-2 rows, round-3, round-4) mention `tree_fingerprint.py` without a note; A1 named only SR-006, R2S-01, MR3-02, MR4-04 and the checkpoint.
- Git history keeps the old masked fragments (the HEAD version of `security-review-merge.md`) and the PR #2 branch commits keep the old identity (SEC-01; user decision pending on the branch `1-phase1-skills`).
- Block-scalar indentation indicators (`|2`) are not parsed by `check_pack.py` or `graph.py` (unchanged).
- D-012 item 3 names the R-REV-9 scan and `commit_state` but not the `dev-gate` commit gate; "every commit rule" covers it.
- The REQ-016 quote could not be checked by the reviewer; the main agent read it from the session transcript.
- GitNexus not run (advisory).

## Narrow confirmation C1

- Target: diff sha256 fd2cc2e328671d42fffeb77ccf1f177d447cc6104a3c0971379f48b781b84a73, status sha256 b81648d8ff5bedcb4b8b86338d59415c8ab739c88c3a286d1ef919cf3430a05b, HEAD ea80fa4 (same at start and end); reviewer `dev-skills:dev-reviewer`, requested model opus, effective unknown
- Scope: R1-001 fix and the post-review edits (REQ-016 locator, FU-007 plan, T3 requirements, this record)
- Result: CONFIRMED, no findings. Each of the three type guards, removed alone in a temporary copy, makes its own subtest fail; `validate.sh` passed (83 tests); both graphs validate
- Limit: the round-1 diff was not stored, so "nothing else changed" was checked by modification times and content, not byte for byte. The main agent ran its own guard mutation in the working tree and restored `scripts/check_pack.py` from a saved copy; the reviewer confirmed that its diff is only the A4 change and that the guards match HEAD
