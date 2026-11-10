# Issue #106 PR-2 review, round 1

Written per ASD-STE100 principles; full conformance not verified.

Target: the index on base `9d17e9c30e5339e7877e46b22567e367d1a0d7d1` (54
files). `reviewer_acceptance.py check` printed `PASS` before and after; CB-4
before and after both reviews: HEAD `9d17e9c`, status SHA-256 `6f0f11f4…`,
diff SHA-256 `ce39808f…`; equal. Not a setup change (plan "PR-2
implementation").

| Review | Agent | Requested | Recorded | Verdict |
| --- | --- | --- | --- | --- |
| P2-deep | `dev-reviewer` | opus/xhigh | `unknown`, case `not read back` | PASS, 3 NIT |
| P2-sec | `dev-security-reviewer` | opus/xhigh | `unknown`, case `not read back` | PASS, 3 NIT |

| ID | Severity | Class (R-REV-4) | Disposition |
| --- | --- | --- | --- |
| P2R-01 | NIT | necessary fix: two bare `:NN` cites in REQ-026 did not move (the search found only `workflow.md:NN`) | Fixed: `:74` → `:77`, `:99` → `:104` |
| P2R-02 | NIT | necessary fix: DL-051 named a wider loosening (items 1, 2, 3, 5, 6) than was done | Fixed: DL-051 names the restated items 1 and 2 and what was deleted |
| P2R-03 | NIT | necessary fix: the brief line could give a reviewer `writing.md` from the tree under review; the review-criteria line already covers reviewers | Fixed by deletion: "or the review target" removed |
| S2R-01 | NIT | worth improving: the changed-pointer sample also changed `sha256` | Fixed: the new line is `oid sha256:` and 64 `b` |
| S2R-02 | NIT | worth improving: the `dev-implement` push summary missed the two new stops | Fixed: two clauses |
| S2R-03 | NIT | worth improving: the `push_precheck.py` docstring names the old dry-run form; Issue Out: the script is not changed | Deferred: FU-065 |

Residual notes of the reviews, handled without a finding: the fact sentences
of push step 3 and step 6a now give their source (a test with git 2.54.0 for
the hook in the dry-run, now also `tests/test_publication_data.py`; the Git
LFS specification, not tested); DL-004 gets the type `rephrase, tighten`
with the part that stays stricter (Issue #106 Scope 5). Kept as is (the
reviewers' own judgment): the R-REV-9 summary "exactly the arguments of the
dry-run", the R-DEL-2 mixed class, the "21 anchors" rows of the design
history, D-031 text (the re-check is in DL-049), the Core `:43` source note
(DL-011: Core governs), the published device numbers in the merged history.
For the user: `push.gpgSign` (push certificates) stays in "Not covered"
(accepted residual risk); no card unless the user asks.

The security reviewer saw an older reviewer definition in its instructions
(the session loaded the plugin before PR #108 merged); it read the current
agent file at HEAD instead. The commit scan brief points to that file.

## Round 2 (narrow confirmation, P2-R2)

Dispatch: `dev-security-reviewer`, requested opus/xhigh, recorded `unknown`,
case `not read back`. CB-4 before and after: status `3a17adba…`, diff
`89cb0fee…`; equal; `check` printed `PASS` before it. Result: the six round-1
fixes are applied; three new NITs.

| ID | Severity | Class (R-REV-4) | Disposition |
| --- | --- | --- | --- |
| P2R2-01 | NIT | necessary fix: `REQ-026:587` cites `source-map.md:177-179` of the vendored Core; at v0.5.0 the rows are at `:181-183` | Fixed (and the `log.md` row of this change) |
| P2R2-02 | NIT | necessary fix: FU-065 Owner; new rows write `maintainer` (FU-061 note) | Fixed |
| P2R2-03 | NIT | necessary fix: DL-004 called the check and detection before each review stricter, but Core `:31`, `:33` ask for them | Fixed: the review part is `rephrase`; the scans and the fixed commands stay `tighten` |

Residual notes, handled without a finding: "no hook runs in the dry-run" is
narrowed to the pre-push hook (the tested case); the LFS source names the
specification file and says it was not verified or tested.

The R-REV-9 commit scan of the previous candidate (diff `89cb0fee…`) was CLEAN;
the fixes make a new candidate, so it is scanned again.

## Round 3 (narrow confirmation, P2-R3)

Dispatch: `dev-security-reviewer`, requested opus/xhigh, recorded `unknown`,
case `not read back`. CB-4 before and after: status `3a17adba…`, diff
`81b7d32a…`; equal; `check` printed `PASS` before it. The commit scan of the
same candidate (diff `81b7d32a…`) was CLEAN. Result: the round-2 fixes are
applied; one new NIT.

| ID | Severity | Class (R-REV-4) | Disposition |
| --- | --- | --- | --- |
| P2R3-01 | NIT | necessary fix: four restatements still said "no hook" where `push-scan.md` now says "no pre-push hook" | Fixed: the `dev-implement` parenthesis is deleted; REQ-011, DL-050 and CHANGELOG say "no pre-push hook" |

Also deleted after the commit scan: a FU-065 sentence that had no source in
the repository. These changes make a new candidate, which gets a
new commit scan and a narrow confirmation.

## Round 4 (narrow confirmation, P2-R4) and commit scans

Round 4: `dev-security-reviewer`, requested opus/xhigh, recorded `unknown`,
case `not read back`; diff `272db379…`; PASS, no finding.

The commit scan of the same candidate gave BLOCKED with one finding: F-001,
this record still named the identifier of the deleted sentence, which has no
source in the repository. Fixed by deletion. The scan reviewer reported that
it ran `git write-tree` once, which wrote the tree object of the index into
`.git/objects` (no ref, index, file or HEAD changed; the commit writes the
same object). CB-4 does not detect such a write; it is recorded here as a
deviation from read-only use (CB-5). The fix makes a new candidate, which
gets a new commit scan.
