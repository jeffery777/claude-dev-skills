---
name: dev-review
description: Independent read-only review of code, docs or mixed changes - routine, deep, or security - with stable finding IDs, severities including SCOPE-CREEP, and dispositions. Use for review requests and for the Review-and-Fix stage of standard or strict work.
---

# dev-review

Read `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` first.

Review stays read-only unless the user asks for fixes (R-REV-1).

## Choose the mode

| Mode | When | Reviewer |
| --- | --- | --- |
| routine | low or medium risk | `dev-reviewer`, model `opus`, effort `high` |
| deep | high or unknown risk, cross-module contracts, packaging, migrations, integrations | `dev-reviewer`, model `opus`, effort `xhigh` |
| security | trust boundaries, auth, permissions, sensitive data, dependencies, installers (R-REV-7) | `dev-security-reviewer`, model `opus`, effort `xhigh` or `max` |

Decide the mode from the actual impact, not the file type. When unsure, use
the stronger mode.

## Workflow

1. Fix the review target. Record the base and head revisions, or the
   working-tree diff including untracked files. Note the scope, DoD and
   requirement IDs.
2. Gather the context the reviewer needs: requirement files, the plan or graph
   node, and the verification output. When GitNexus is available, add
   `gitnexus detect-changes` to map the hunks to affected symbols and flows,
   and label it advisory.
3. Dispatch the reviewer subagent with a brief (R-DEL-1). Give the target, the
   context paths, the mode, and the output format in
   `${CLAUDE_SKILL_DIR}/references/review-report.md`. Never review your own
   change as the required reviewer.
   - Native option (D-005): `/code-review` and `/security-review` can be the
     primary review pass. Run it in a context that did not write the change,
     for example a fresh subagent; when the author's own session runs it, it
     is not the independent review. Map its findings into the report format
     below, run the requirement-trace and SCOPE-CREEP pass through
     `dev-reviewer` (never yourself as the author), and record which tool ran
     and in which context. A native pass that runs in a context with write
     tools is an extra pass only; the required review still needs
     `dev-reviewer` or `dev-security-reviewer`, and without them the work
     stops at the gate (dev-core §8).
4. Read the report back. Check that each finding has a file and line and
   evidence. Mark claims you could not reproduce as unverified.
5. Assign IDs (`F-001`, …) and propose a disposition for each finding
   (R-REV-3). Save the report to `.dev/<objective-id>/reviews/<round>.md` for
   standard and strict work.
6. When fixes follow, apply them with `dev-implement` or `dev-docs`, then
   re-review proportionally (R-REV-4). After two unfinished rounds,
   re-assess the approach (R-VER-2).

## Output

The report format in `references/review-report.md`. Findings come first.
