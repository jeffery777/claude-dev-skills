---
name: dev-gate
description: Formal readiness gate before commit, PR or merge - checks finding dispositions, verification, requirement trace and, once a PR/MR or base..head range exists, a complete exact-head Merge Review; reports content, platform and authority separately. Use when a workflow needs a blocking PASS/BLOCKED decision, not for ordinary review.
---

# dev-gate

Read `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` first. For merge readiness,
also read
`${CLAUDE_SKILL_DIR}/../../vendor/engineering-workflow-core/contracts/exact-head-and-evidence.md`
in full. It is short, and its rules are strict.

A gate summarizes evidence. It is not another review, and it authorizes no
commit, push, PR, merge or other external write (R-REV-5, R-AUTH-1).

## Which gate

| Gate | When | Requires |
| --- | --- | --- |
| commit / PR readiness | before a commit or PR the user asked for | current review for the exact diff, all dispositions complete, verification recorded, docs sync done or reasoned |
| merge readiness | a PR/MR or explicit base..head range exists | all of the above plus a complete base-to-head Merge Review at the current head (R-EXH-1 to R-EXH-3) |

## Workflow

1. Bind the identity: the repository, the branch, and the exact base, head
   and merge-base SHAs (`git rev-parse`, `git merge-base`). Bind the diff
   identity (`git diff --stat base...head` plus a hash of the diff), and the
   PR number when one exists. Before a commit, bind the working tree instead:
   HEAD, `git status --porcelain` (which lists untracked files) and a hash of
   `git diff HEAD` with untracked files included (`git add -N` first).
2. Collect the evidence: the review reports, verification output, the graph
   state, and the requirement trace. Reuse an earlier review only when its
   content (including the uncommitted diff), revision, scope, assumptions,
   policy, stage, environment and freshness still match (R-CAP-3). For merge readiness, a pre-commit
   or previous-head review never satisfies the gate.
3. For merge readiness, run or dispatch the complete base-to-head review:
   - `dev-review` in deep mode over `base...head`;
   - the deterministic repo checks;
   - the code ↔ docs coherence checks (R-EXH-2).
4. Check the blockers (R-REV-5, R-REV-7, R-AUTH-5). Any one blocks the gate:
   - an unresolved MUST-FIX, a missing or incomplete disposition, or an open
     Needs Human Decision;
   - a required independent review, verification or scan that is missing,
     incomplete, failed, has insufficient coverage, or is `NOT_RUN`;
   - an unresolved substantive security risk, with or without a finding ID;
   - a write change without a requirement, or a `SCOPE-CREEP` finding without
     a disposition.
5. Decide `content_review`.
6. Decide `platform_enforcement`. It is `NOT_CONFIGURED` unless the project
   selects a provider profile. Read GitHub checks (`gh pr checks`) only when
   one is selected, and never infer the platform result from the content
   result.
7. State the authority boundary. Name the exact next action, such as
   "merge PR 12", and whether the user has authorized it. If the head changes,
   the gate is void: rerun it from step 1 (R-EXH-3).

## Output

```text
Gate: commit | pr | merge
Gate result: PASS | BLOCKED | NEEDS HUMAN DECISION        (R-REV-5)
Content Review: PASSED | BLOCKED | NEEDS_HUMAN_DECISION   (merge gate, R-EXH-4)
Platform Enforcement: VERIFIED | UNVERIFIED | BLOCKED | NOT_CONFIGURED (merge gate)
Identity: repo, base, head, merge-base, diff hash, PR
Findings and dispositions: (table or link)
Verification evidence: (commands and results)
Requirement trace: complete | gaps
Residual risk:
Authority: <exact action> — authorized by <user message> | not authorized
```
