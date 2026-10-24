---
name: dev-review
description: Independent read-only review of code, docs or mixed changes - routine, deep, or security - with stable finding IDs, requirement relations, severities including SCOPE-CREEP and REQ-GAP, and dispositions. Use for review requests and for the Review-and-Fix stage of standard or strict work.
---

# dev-review

Read `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` first, then the Core files that its stage map lists for `dev-review`.

Review stays read-only unless the user asks for fixes (R-REV-1).

## Choose the mode

| Mode | When | Reviewer |
| --- | --- | --- |
| routine | low or medium risk | `dev-reviewer`, model `opus`, effort `high` |
| deep | high or unknown risk, cross-module contracts, packaging, migrations, integrations (R-REV-6) | `dev-reviewer`, model `opus`, effort `xhigh` |
| security | trust boundaries, auth, permissions, sensitive data, dependencies, installers (R-REV-7) | `dev-security-reviewer`, model `opus`, effort `xhigh` or `max` |
| commit / push scan | before every commit and every push, at any tier (R-REV-9) | `dev-security-reviewer`, model `opus`, effort `high` or more |

Decide the mode from the actual impact, not the file type (R-REV-7). When unsure, use
the stronger mode. A required security review or scan always uses
`dev-security-reviewer`, never `dev-reviewer` (R-REV-1).

For a commit / push scan, the target is exactly what will be published: the
staged diff plus the author, committer, message and trailers the commit will
carry, or everything the push sends, or the PR or Issue text to be posted (R-REV-9).
Review records are committed or posted too, so both reviewer agents mask any
secret or private identifier they report (R-REV-8).

## Workflow

1. Fix the review target. Record the base and head revisions, or the
   working-tree diff including untracked files (R-REV-6). Note the scope, DoD and
   requirement IDs.
2. Gather the context the reviewer needs: requirement files, the plan or graph
   node, and the verification output. When GitNexus is available, add
   `gitnexus detect-changes` to map the hunks to affected symbols and flows,
   and label it advisory (CB-3).
3. Dispatch the reviewer subagent with a brief (R-DEL-1). Give the target, the
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
     and in which context. A native pass that runs in a context with write
     tools is an extra pass only; the required review still needs
     `dev-reviewer` (`dev-security-reviewer` for a security review or scan), and without them the work
     stops at the gate (R-REV-1, CB-4).
4. Read the report back. Check that each finding has a file and line and
   evidence (R-REV-2). Mark claims you could not reproduce as unverified.
5. Assign IDs (`F-001`, …). Before any fix, classify each finding and
   propose a disposition (R-REV-3, R-REV-4). Raise each `REQ-GAP` and each
   Needs Human Decision as a decision card
   (`${CLAUDE_SKILL_DIR}/references/decision-card.md`); do not fix a
   `REQ-GAP` in the same round (R-REV-3, R-AUTH-6). Save the report to
   `.dev/<objective-id>/reviews/<round>.md` for standard and strict work.
   Once a PR exists, store the records of a review of its head by
   R-EXH-3.
6. When fixes follow, apply them with `dev-implement` or `dev-docs`, then
   re-review proportionally (R-REV-4). Before a push, an independent
   reviewer confirms the fixes in a narrow review. Apply the re-assessment
   and the stop rule of R-VER-2.

## Output

The report format in `references/review-report.md`. Findings come first (R-REV-2).
