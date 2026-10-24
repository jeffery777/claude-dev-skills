---
name: dev-gate
description: Formal readiness gate before commit, push, PR or merge - checks finding dispositions, verification, requirement trace and, once a PR/MR or base..head range exists, a complete exact-head Merge Review; reports content, platform and authority separately. Use when a workflow needs a blocking PASS/BLOCKED decision, not for ordinary review.
---

# dev-gate

Read `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` first, then the Core files that its stage map lists for `dev-gate`. For merge readiness,
also read
`${CLAUDE_SKILL_DIR}/../../vendor/engineering-workflow-core/contracts/exact-head-and-evidence.md`
in full. It is short, and its rules are strict.

A gate summarizes evidence. It is not another review, and it authorizes no
commit, push, PR, merge or other external write (R-REV-5, R-AUTH-1).

## Which gate

| Gate | When | Requires |
| --- | --- | --- |
| commit / push / PR readiness | before a commit, push or PR the user asked for | current review for the exact diff, all dispositions complete, verification recorded, docs sync done or reasoned, and a passed R-REV-9 scan of exactly the staged diff and the commit identity and message (before a push: of everything the push sends; before a PR: of its title and body) |
| merge readiness | a PR/MR or explicit base..head range exists | all of the above plus a complete base-to-head Merge Review at the current head (R-EXH-1 to R-EXH-3) and an R-REV-9 scan of every commit in base..head, including identities and messages, and of the merge or squash commit the platform will create (method, author, message, trailers) |

## Workflow

1. Bind the identity: the repository, the branch, and the exact base, head
   and merge-base SHAs (`git rev-parse`, `git merge-base`). Bind the diff
   identity (`git diff --stat base...head` plus a hash of the diff), and the
   PR number when one exists. Before a commit, bind the working tree instead:
   HEAD, `git status --porcelain` (which lists untracked files) and a hash of
   `git diff HEAD` with untracked files included (`git add -N` first). Also
   bind what the R-REV-9 scan covered: for a commit, the hash of
   `git --no-replace-objects diff --cached --no-relative --binary --no-textconv --no-ext-diff` and the author, committer and message; for a
   push, the exact push command, the refs and commit range its dry-run lists, and the remote object IDs given to the scan. The scan record must show the
   same values.
2. Collect the evidence: the review reports, verification output, the graph
   state, and the requirement trace. Reuse an earlier review only when its
   content (including the uncommitted diff), revision, scope, assumptions,
   policy, stage, environment and freshness still match (R-CAP-3). For merge readiness, a pre-commit
   or previous-head review never satisfies the gate (R-EXH-1, R-EXH-3).
3. For merge readiness, run or dispatch the complete base-to-head review:
   - `dev-review` in deep mode over `base...head`. The review covers the
     whole range; parts that are provably unaffected by every change since an
     earlier review may reuse its evidence when the review records the reason and the coverage
     (R-EXH-3);
   - the deterministic repo checks;
   - the code ↔ docs coherence checks (R-EXH-2).
4. Check the blockers (R-REV-5, R-REV-7, R-AUTH-5). Any one blocks the gate:
   - an unresolved MUST-FIX, a missing or incomplete disposition, or an open
     Needs Human Decision (including an undecided `REQ-GAP`) (R-REV-3,
     R-REV-5);
   - before a push: fixes without the narrow independent confirmation
     (R-REV-4);
   - a required independent review, verification or scan that is missing,
     incomplete, failed, has insufficient coverage, or is `NOT_RUN`
     (R-AUTH-5, R-REV-7);
   - a missing R-REV-9 scan, or one that does not match the current staged
     content, commit identity and message, or commit range (R-REV-9);
   - an unresolved substantive security risk, with or without a finding ID
     (R-REV-7);
   - a write change without a requirement, or a `SCOPE-CREEP` finding without
     a disposition (R-RIG-3, R-REV-5).
5. Decide `content_review`.
6. Decide `platform_enforcement` (R-EXH-4). Never infer it from the content
   result, and re-read it right before a merge.
   - A project selects a provider profile only with `platform_profile` in
     `.dev/config.json`, read at the bound base commit, never at the PR head
     or in the working tree. The format, the read-back and its limits are in
     `${CLAUDE_SKILL_DIR}/references/platform-profile.md`; read it in full.
   - Run the checker with the bound values:
     `python3 -I <checker> --repo-dir . --repo <owner/name> --pr <n> --base <base> --head <head> --pack-dir ${CLAUDE_SKILL_DIR}/../..`.
     `<checker>` is `${CLAUDE_SKILL_DIR}/scripts/platform_profile.py`, or
     its copy from the bound base when the pack lies inside the repository
     under review (see the reference). Report its result line, every item,
     the policy-change line and the list of changed check files. A checker
     failure or a missing result line gives the result of R-EXH-4.
   - No profile (`NOT_CONFIGURED`): when a PR exists, read its base, head and
     checks in one call:
     `gh pr view <pr> --repo github.com/<owner/name> --json baseRefOid,headRefOid,statusCheckRollup`.
     List each check with its result; an empty list means the PR has no
     checks. Compare `baseRefOid` with the bound base and `headRefOid` with
     the reviewed head; R-EXH-4 gives the result when the read fails or
     either differs: a stale base may lack a profile that the PR's real base
     has. A failed or unrun check is never Passed (R-EXH-2).
   - A policy change (`.dev/config.json` differs between base and head) needs
     the user's decision (R-AUTH-2): give a decision card; the gate result is
     `NEEDS HUMAN DECISION` until the user answers for that head blob.
7. State the authority boundary. Name the exact next action, such as
   "merge PR 12", and whether the user has authorized it. If the head changes,
   the gate is void: rerun it from step 1 (R-EXH-3).
8. Record the result. Once a PR exists, store it by R-EXH-3. Give each open
   decision as a decision card
   (`${CLAUDE_SKILL_DIR}/../dev-review/references/decision-card.md`) (R-AUTH-6).

## Output

```text
Gate: commit | push | pr | merge
Gate result: PASS | BLOCKED | NEEDS HUMAN DECISION        (R-REV-5)
Content Review: PASSED | BLOCKED | NEEDS_HUMAN_DECISION   (merge gate, R-EXH-4)
Platform Enforcement: VERIFIED (checks ran this PR's own definitions) | UNVERIFIED | BLOCKED | NOT_CONFIGURED (merge gate; items, policy change, changed check files)
Identity: repo, base, head, merge-base, diff hash, PR
Findings and dispositions: (table or link)
Verification evidence: (commands and results)
Commit / push security scan (R-REV-9): PASSED | FINDINGS | NOT_RUN — scope (staged diff, identity, message, commit range)
Requirement trace: complete | gaps
Open decisions: one decision card each | none
Residual risk:
Authority: <exact action> — authorized by <user message> | not authorized
Writing: written per ASD-STE100 principles; full conformance not verified
```
