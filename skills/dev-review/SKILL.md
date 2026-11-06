---
name: dev-review
description: Independent read-only review of code, docs or mixed changes - routine, deep, or security - with stable finding IDs, requirement relations, severities including SCOPE-CREEP and REQ-GAP, and dispositions. Use for review requests and for the Review-and-Fix stage of standard or strict work.
allowed-tools:
  - Read(/${CLAUDE_PLUGIN_ROOT}/skills/**)
  - Read(/${CLAUDE_PLUGIN_ROOT}/vendor/engineering-workflow-core/contracts/**)
---

# dev-review

Read `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` first, then the Core files that its stage map lists for `dev-review`.
Read, run or copy each file that this skill names with a `${CLAUDE_SKILL_DIR}`
path only with that full absolute path, never with a path relative to the
working directory; when such a path does not resolve or cannot be read, stop
and report it (CB-6).

Review stays read-only unless the user asks for fixes (R-REV-1).

## Choose the mode

| Mode | When | Reviewer |
| --- | --- | --- |
| routine | low or medium risk | `dev-reviewer`, role `review-routine`; at the `light` tier, role `review-routine-light` unless an escalation trigger below applies |
| deep | high or unknown risk, cross-module contracts, packaging, migrations, integrations (R-REV-6) | `dev-reviewer`, role `review-deep` |
| security | trust boundaries, auth, permissions, sensitive data, dependencies, installers (R-REV-7) | `dev-security-reviewer`, role `review-security` (a higher effort only when the user asks, R-DEL-2) |
| commit / push scan | before every commit and every push, and at merge readiness, at any tier (R-REV-9) | `dev-security-reviewer`, role `scan` |

Escalation triggers for `light` routine review (Issue #73, C4). Decide them
before the dispatch from the diff and the plan, and check them again after
the review. When any of them applies, the routine review uses the role
`review-routine`:

1. The R-DEL-2 floor applies: security, a trust boundary or another R-REV-7
   case, data, persistent state, migration, or a public contract.
2. The change touches packaging, installation, CI or dependencies.
3. The change touches more than one module.
4. A finding is disputed: the main agent or the author rejects a finding, or
   two reviews of the same change disagree.
5. The reviewer reports a part of the target that it could not check.

A trigger found after the review re-runs the review at the role
`review-routine` on the same target; the first report and its findings
stay. The brief of a `light` routine review at the role
`review-routine-light` lists triggers 1 to 3 and asks the reviewer to
report, for each of them, whether it holds (card I73-R2-C2 (a)). When the
reviewer reports one, the review re-runs at the role `review-routine`, as
for trigger 5, and the node keeps that role. A report that does not say,
for each of triggers 1 to 3, whether it holds counts as trigger 5: the
review re-runs at the role `review-routine` (card I73-R3-C1 (a)). Once a
trigger applies to a node, every later review round of that node uses the
role `review-routine`, never the role `review-routine-light` again (R-DEL-2:
an escalated setting is never lowered for the rest of the node). The
`standard` and `strict` tiers always use the role `review-routine` for
routine review.

Decide the mode from the actual impact, not the file type (R-REV-7). When unsure, use
the stronger mode. A required security review or scan always uses
`dev-security-reviewer`, never `dev-reviewer` (R-REV-1).

The Merge Review, a security review of the head at the merge and the merge
readiness scan are read back by R-DEL-2 (`dev-core`); no other review or scan is.

For a commit / push scan, the target is exactly what will be published: the
staged diff plus the author, committer, message and trailers the commit will
carry, or everything the push sends, or the range and the merge or squash
commit at merge readiness, or the PR or Issue text to be posted (R-REV-9).
Review records are committed or posted too, so both reviewer agents mask any
secret or private identifier they report (R-REV-8).

## Workflow

1. Fix the review target. Record the base and head revisions, or the
   working-tree diff including untracked files (R-REV-6). Note the scope, DoD and
   requirement IDs.
2. Gather the context the reviewer needs: requirement files, the plan or graph
   node, and the verification output. When `dev-plan` step 2 requires a
   source trace (a spec or REQ from a user decision), the brief tells the
   reviewer to check it: a missing trace, or a condition of the user's
   words dropped without a reason, is a finding.
   The brief of an implementation review and of a fix round review (not
   of an R-REV-9 scan) gives the completeness checks of the plan: the
   search list and the co-change rules with their commands in the forms of
   `dev-plan` step 6, and only the values come from the plan (Issue #101).
   The reviewer checks each value by the value rule; when its target is staged, it runs the
   commands on the index and compares them with the outputs in the plan, if
   the plan has any; it always checks co-change rule 1 by reading the diff
   that it reviews (for a fix round, the fix diff), and on a cumulative
   diff its report says that it cannot tell the rounds apart and that
   this item does not count as passed.
   The Merge Review lists the commits with
   `git --no-replace-objects rev-list --reverse '<base ID>..<head ID>'` and
   runs co-change rule 1 on each commit, with
   `'<commit ID>^1' '<commit ID>'` in place of `--cached`; it reads a merge
   commit by hand, and the report says so. The search list runs on the head
   with
   `git --no-replace-objects --literal-pathspecs -c core.quotePath=false grep -c -F -i -e '<string>' '<head ID>' --`.
   When GitNexus is available, add
   `gitnexus detect-changes` to map the hunks to affected symbols and flows,
   and label it advisory (CB-3).
3. Dispatch the reviewer subagent with a brief (R-DEL-1). Pass the model
   and the effort of the mode table in the dispatch call (R-DEL-2). Give the target, the
   context paths, the mode, and the output format in
   `${CLAUDE_SKILL_DIR}/references/review-report.md`. Never review your own
   change as the required reviewer (R-REV-1). The brief tells the reviewer to look for
   problems beyond the requirements, to give every finding a
   `requirement_relation`, and to rate severity by the R-REV-3 thresholds;
   items below the thresholds go to residual risk.
   - Native option (D-005): `/code-review` and `/security-review` can be the
     primary review pass. Run it in a context that did not write the change,
     for example a fresh subagent; when the author's own session runs it, it
     is not the independent review. Map its findings into the report format
     below, run the requirement-trace and SCOPE-CREEP pass through
     `dev-reviewer` (never yourself as the author), and record which tool ran
     and in which context. A native pass that
     does not run in a subagent of this session never counts (`dev-core`). A native pass that runs in a context with write
     tools is an extra pass only; the required review still needs
     `dev-reviewer` (`dev-security-reviewer` for a security review or scan), and without them the work
     stops at the gate (R-REV-1, CB-4).
4. Read the report back. For a review that R-DEL-2 reads back, read back the
   reviewer's model and effort after the review has finished (`dev-core`) and
   fill in `recorded` and the Read-back line from its result. Check that each finding has a file and line and
   evidence (R-REV-2). Mark claims you could not reproduce as unverified.
5. Assign IDs (`F-001`, …). Before any fix, classify each finding and
   propose a disposition (R-REV-3, R-REV-4). Raise each `REQ-GAP` and each
   Needs Human Decision as a decision card
   (`${CLAUDE_SKILL_DIR}/references/decision-card.md`); do not fix a
   `REQ-GAP` in the same round (R-REV-3, R-AUTH-6). Save the report to
   `.dev/<objective-id>/reviews/<round>.md` for standard and strict work.
   When the main session does this itself for work under the R-DEL-2 floor,
   the floor check of R-DEL-2 applies (`dev-core`).
   Once a PR exists, store the records of a review of its head by
   R-EXH-3.
6. When fixes follow, apply them with `dev-implement` or `dev-docs`, then
   re-review proportionally (R-REV-4). Before the main session fixes a node
   under the R-DEL-2 floor itself, the floor check of `dev-deliver` step 2
   runs first. Before a push, an independent
   reviewer confirms the fixes in a narrow review. Apply the re-assessment
   and the re-evaluation of R-VER-2.

## Output

The report format in `${CLAUDE_SKILL_DIR}/references/review-report.md`. Findings come first (R-REV-2).
