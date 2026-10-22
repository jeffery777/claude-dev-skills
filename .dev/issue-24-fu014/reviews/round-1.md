# Review round 1 (deep, fresh reviewer), Issue #24

- Target: working tree against HEAD `c821a97`, `git diff HEAD --binary` (with the intent-to-add
  `.dev/issue-24-fu014/` files) sha256 `278ddaed…8c5fef`. Reviewer: `dev-skills:dev-reviewer` (opus, deep).
  Index and tree unchanged by the reviewer.
- Design: the FU-014 design spec and decision cards were reviewed before this round (deep and security
  reviewers, three rounds; the R-VER-2 stop rule fired after round 2 and the user chose card 4a, a smaller
  scope). User decision: 「同意你的建議，4a、1a、2a、3a」.
- Commands (reviewer): `git diff HEAD`, word-diff and a `diff` of the R-REV-9 bullet against the approved
  draft (identical); `git grep` for `prune`, `--remotes=`, `ls-remote`; temporary-repository tests with local
  bare repositories only (stale ref of a deleted branch, `receive.hideRefs`, empty remote, failing
  `ls-remote`, `--tags`, `--follow-tags`, tags that point to trees or blobs, SHA-256 repository);
  `PYTHONDONTWRITEBYTECODE=1 bash scripts/validate.sh` exit 0; `graph.py validate` ok. Skipped: GitNexus.
- Result: no MUST-FIX; one SHOULD-FIX, one REQ-GAP, two NITs. DoD items 1, 3, 4 and 6 pass; item 2 fails
  only on R1-001; item 5 passes after R1-002 and R1-004.

## Dispositions

| ID | Relation | Severity | Finding | Class | Disposition |
| --- | --- | --- | --- | --- | --- |
| R1-001 | in-scope | SHOULD-FIX | A head that the remote hides from pushes (`receive.hideRefs`) but still lists to `ls-remote` counts as present; a push that sends its commits again does not scan them. The FU-014 row and CHANGELOG said hidden refs no longer let a commit pass unscanned | necessary fix | Fixed: the claims are removed; FU-015 item 5 records the gap (the base text has the same gap for heads). The rule text does not change |
| R1-002 | in-scope | NIT | With the default refspec the old `git fetch --prune` removes the stale ref, so the old scan did not miss the commit; the records said it did | necessary fix | Fixed: the CHANGELOG, REQ-011 and FU-014 texts no longer claim it. The benefit is the removed prune without a return of the stale-ref miss |
| R1-003 | gap | REQ-GAP | `dev-gate` binds "the remote object IDs given to the scan", but the scan record format (`skills/dev-review/references/review-report.md:9`) has no field for them | needs human decision | Decision card 5 to the user (via the orchestrator session): (a) add the phrase, (b) defer to FU-015, (c) leave it |
| R1-004 | in-scope | NIT | The FU-015 row named "deep finding T11"; T11 is a spec test | necessary fix | Fixed: "spec test T11; deep review finding R1-001" |

## Residual risk

- The reviewer agent text says "every commit in the given range"; the new procedure gives an ID list plus
  a ref (wording gap, not a behavior change; the design keeps the agent file unchanged).
- `--heads` is the older name of `--branches`; Git 2.54 gives no warning; older Git and Windows untested.
- A failing `ls-remote` gives an empty list and a full-history scan (more, not less); a remote change
  between `ls-remote` and the push is not handled (same as before).

## Round 2 (narrow confirmation)

`dev-skills:dev-reviewer` (opus), diff sha256 `0f2f2623…7365c1d`, index and tree unchanged, `validate.sh`
exit 0. R1-001, R1-002 and R1-004 confirmed fixed; R1-003 waits for card 5. R2-001 (NIT, in-scope): the T1
DoD in `graph.json` says the test shows that the new scan finds commits that "a stale or hidden ref hid".
Disposition: kept as written; that DoD is met only for refs that `ls-remote --heads --tags` does not list
(for example `refs/pull/*`); heads or tags hidden by `receive.hideRefs` are FU-015 item 5.
