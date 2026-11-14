# Implementation review round 1, Issue #115 (node U1)

- Target: the staged index at HEAD = base `e37a990391241a04c01df1a1aec333bcf9934364`; diff identity SHA-256 `bf4351d4ed89091256edc05f6f194d6ac342348785be9281e37f81d2d3abe903` of `git --no-replace-objects diff --cached --no-relative --binary --no-textconv --no-ext-diff --ignore-submodules=none --submodule=short`; index tree `42464984d1af5915d8b9d96c2f5815fc0fd0b05d` (`git write-tree` after the review).
- Reviewer check (R-REV-1): `reviewer_acceptance.py check` printed `PASS` (exit 0), in the same command as the CB-4 commands before the review.
- Tree check (CB-4): HEAD, the status hash and the diff hash were the same before and after the review (exit 0 each time).
- Deep: `dev-reviewer`, role `review-deep`, requested opus/xhigh; recorded: `unknown` (not read back); effective: `unknown`.
- Reviewer verification: `python3 -I -B -m unittest discover -s tests -q`: 424 tests, OK (skipped=3), exit 0.
- Completeness checks: run by the reviewer on the index; the same counts as the main agent's run in `plan.md` (Completeness checks, Results).
- Security Diff Scan: not applicable; the four conditions of the security design review hold for this diff (the reviewer checked each; condition 1 counts the records in `.dev/issue-115/` as records, as the plan says).
- Writing spot-check (R-WRT-2): fit for the reader and the type of document; no important information lost; observations below the thresholds: "key" and "field" for one concept, and a long first sentence in the CHANGELOG entry.
- Writing: written per ASD-STE100 principles; full conformance not verified.

## Findings and dispositions

| ID | Severity | Finding | Class | Disposition |
| --- | --- | --- | --- | --- |
| IR-01 | NIT | False fact in the FU-068 row: "Issue #115 changes only the schema text" (the change also adds a test) | necessary fix | `Fixed` by deletion: the column now says "Existed before Issue #115; `graph.py` is outside the scope of Issue #115."; narrow confirmation in round 2 |

Open question 2 of the reviewer (is the FU-068 request the user's own
words?): no. The relay of 2026-11-14 gives the user's words 「繼續」 for the
dispositions and gives no user words for FU-068; the FU-068 row is the
orchestrator session's request in that message, so the From column stays.

## Residual risk and not handled

- The `SCHEMA` row of the error-code table ("Missing field or a value
  outside the enum") stays narrower than `## Fields`; it existed before and
  is outside the scope (security design review condition 3).
- "key" and "field" name one concept; "a value of the wrong type" means the
  values of the five keys (a wrong `consumes` type is `FAKE_EDGE`,
  `graph.py:496-497` at the base).
- The write-node DoD rule has no test (no case in `tests/test_graph.py` or
  `tests/fixtures/graph/invalid/`); the new test uses only the `review` kind
  (`check_schema` splits by kind only at `graph.py:161` at the base).
- FU-068: `dev-deliver` step 1 and `dev-continue` also run `ready` directly
  (`skills/dev-deliver/SKILL.md:40`, `skills/dev-continue/SKILL.md:95` at the
  base). The row's "not a release blocker" stays an inference.
- The Issue title still says "the four list keys"; the body names five.
- FU-068 is unique on the index only; other branches and open PRs were not
  checked by the reviewer (the main agent checks `origin/main` before the
  push).

## Lesson candidates

- Trigger: the same kind of finding in two rounds of this work (DR-D-01 and
  IR-01: a record sentence wider than its source). Observation (fact): two
  record sentences stated more than their sources. Lesson (inference): a
  summary of scope ("only X") is easy to write too wide; check each record
  sentence against its source before review. Events: 2, same work and
  author, not independent. Covered by R-EVD-3 and the reviews, which found
  both. Judgment: keep as is. Level: L2 or unclear. Abstraction checklist:
  each item not present.

## Round 2: narrow confirmation of the round-1 fix

- Target: the staged index, diff identity SHA-256 `edb940c87df7838f5f0cf1c8017e2eb864b9898c0ac51b0ff426efaacefad1ac`; fix diff against the round-1 tree `42464984d1af5915d8b9d96c2f5815fc0fd0b05d` (three paths: `.dev/followups.md`, `.dev/issue-115/plan.md`, this file); index tree after the review `ca87f0f258265a53eb471d7fbe18628128ee2b0d`.
- Reviewer check and tree check: `PASS` (exit 0) and CB-4 equal before and after (exit 0 each time).
- Deep: `dev-reviewer`, role `review-deep`, requested opus/xhigh; recorded: `unknown` (not read back); effective: `unknown`.
- IR-01: confirmed fixed (word diff: only the clause is gone).

| ID | Severity | Finding | Class | Disposition |
| --- | --- | --- | --- | --- |
| IR2-01 | NIT | False fact in this record: `validate` does not report a missing requirements folder before `SCHEMA` (the reviewer ran it in memory) | necessary fix | `Fixed` by deletion of the clause; re-review: round 3 (tree `abb02e2c46d114d5453173c266cf7670c0a9eb84`) |
| IR2-02 | NIT | False fact in this record: `ready` gives no traceback for an empty `nodes` value that is not a list | necessary fix | `Fixed` by deletion of the sentence about `nodes`; re-review: round 3 (same tree) |

Also fixed (below the thresholds): the K4 reason in the plan no longer
quotes hit text; sources added to the true fact sentences of the residual
risk list; the condition-1 note; the open-question answer no longer says
"only".

Re-evaluation (R-VER-2): record sentences needed fixes in two consecutive
rounds (IR-01, then IR2-01 and IR2-02), with no blocker. The approach for
records changes: a sentence about program behavior that this session did
not read in the code is deleted or marked unverified, not rewritten. No
`MUST-FIX`, requirement change or loosening, so the work continues.

## Round 3: narrow confirmation of the round-2 fixes

- Target: the staged index, diff identity SHA-256 `085f30edddf318b91201aa42f503a1b87256486c3070240646f8c0dc46436268`; fix diff against the round-2 tree `ca87f0f258265a53eb471d7fbe18628128ee2b0d`; index tree `abb02e2c46d114d5453173c266cf7670c0a9eb84`.
- Reviewer check and tree check: `PASS` (exit 0) and CB-4 equal before and after (exit 0 each time).
- Deep: `dev-reviewer`, role `review-deep`, requested opus/xhigh; recorded: `unknown` (not read back); effective: `unknown`.
- IR2-01 and IR2-02: confirmed fixed.
- The reviewer reports that one of its commands ran `git write-tree --missing-ok`, which writes a tree object (git-write-tree(1)) and can write the cache-tree of the index (unverified). The diff identity, HEAD and status were the same after it (CB-4 after-check), so the detection found no change of the content under review; equal values do not prove that nothing changed.

| ID | Severity | Finding | Class | Disposition |
| --- | --- | --- | --- | --- |
| IR3-01 | NIT | The round-2 lesson candidate counted three events for a lesson that only IR2-01 and IR2-02 fit | necessary fix | `Fixed` by deletion of that candidate; re-review: round 4 (tree `abb02e2c46d114d5453173c266cf7670c0a9eb84` to `82089e00a182cb2f38a02f5864166813fd7d70ff`) |

## Round 4: narrow confirmation of the round-3 fix

- Target: diff identity SHA-256 `3a397d3f9197ba390c5f3024d9a09ba6c78fe2cfe661ec79351786c775ce4b60`; fix diff against `abb02e2c46d114d5453173c266cf7670c0a9eb84`; index tree `82089e00a182cb2f38a02f5864166813fd7d70ff`. `PASS` and CB-4 equal before and after. Deep, requested opus/xhigh; recorded `unknown` (not read back). The brief forbade commands that write objects, the index or refs; the reviewer reports none.
- IR3-01: confirmed fixed.

| ID | Severity | Finding | Class | Disposition |
| --- | --- | --- | --- | --- |
| IR4-01 | NIT | With the round-2 candidate deleted, the Lesson candidates section has no candidate whose trigger is the R-VER-2 re-evaluation | keep as is | `Rejected`: R-VER-5 asks that the section give a candidate when a trigger holds, and it gives one (round 1); the final `dev-deliver` report gives the candidate for the R-VER-2 trigger. The finding touches only this record, not a delivered file (triage note of the orchestrator session, 2026-11-14, applied as R-REV-4 allows) |

R-VER-2: the record text of a fix round needed a fix in the next round
again (rounds 2 and 3). Re-evaluation: the spec, the acceptance criteria
and the approach of the delivered files stay; for records, no fix round
starts for a NIT that touches only a review record. No `MUST-FIX`,
requirement change or loosening.
