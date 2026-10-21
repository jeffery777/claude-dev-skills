---
name: dev-continue
description: Save a checkpoint before pausing, or resume saved development work from repository state - re-grounds from files and Git, not chat memory, then selects the next safe task or handoff. Use for "continue", "resume", "where were we", handoffs, when context is getting long, and when a work item is complete, to evaluate a session handoff.
---

# dev-continue

Read `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` first. The rules for resuming
are R-STG-5 and R-EVD-2. The handoff evaluation below is the user's decision
D-012 (REQ-017).

## Save a checkpoint

Write `.dev/<objective-id>/checkpoint.md`:

```markdown
# Checkpoint <ISO time>
- Objective / requirements: …
- Git: branch, HEAD, upstream, dirty files (git status --short)
- Done (with evidence refs): …
- In progress (owner, owned paths, last known state): …
- Unknown-outcome operations or delegated work: …
- Open findings and dispositions: …
- Next step and its verification: …
- Human gates pending: …
```

The checkpoint is a summary, not evidence. Point to the commits, the reports
and the command output instead of restating them.

## Evaluate a handoff

When a work item is complete (for example a graph node, a review and fix
round, or a stage), evaluate whether the work continues in a new session.

1. Base the decision on the number of review and fix rounds, stage
   boundaries and the remaining workload. Context usage is a reference only.
   You cannot read your exact context usage, so never claim a figure for it.
2. To switch:
   - Save the checkpoint (above). Before a PR exists, commit it without
     asking first. D-012 covers this checkpoint commit and no other commit.
     Every commit rule still applies: the R-REV-9 scan before the commit,
     and the `commit_state` setting (`dev-core` section 8; with `false`, do
     not commit the checkpoint).
   - Once a PR exists, never commit the checkpoint: a commit on the PR
     branch makes a new head that needs a new complete review (R-EXH-3).
     Keep it uncommitted, and post its key points as a PR comment so that
     another clone can take over. The user's answer to PR-C1 decision card 1
     covers this comment and no other comment. `dev-security-reviewer` scans
     the exact comment text before it is posted (R-REV-9); without that
     scan, do not post. The checkpoint points to the review and gate records
     and does not repeat them.
   - Offer a new session through the app's native session handoff (for
     example a new-session card), with the checkpoint as its full handoff
     brief. The new session starts only after the user confirms it. Without
     a native handoff, give the brief in your report and tell the user how
     to start the new session.
   - The handoff is complete when the user confirms it (or, without a native
     handoff, says that the new session has started). From then on, this
     session stops writing: no file edits, commits, pushes or posts. Before
     that, or when the user declines, no handoff has happened: continue in
     this session, and save the checkpoint again before the next offer.
3. Otherwise, continue in this session.

## Resume

1. Prefer the original session. If you are in a new session, re-ground from
   files: the project instructions, `docs/requirements/index.md`, and
   `.dev/<objective-id>/` (checkpoint, graph, events, reviews), plus the
   current Git state.
2. Compare the checkpoint with reality. Has HEAD moved? Are there unexpected
   changes or new commits? Did delegated work leave branches or worktrees
   (`git worktree list`)? Treat any mismatch as drift: re-read the affected
   sources before you trust the checkpoint.
3. Resolve each unknown outcome by reading the state back, never by replaying
   the operation (R-AUTH-4).
4. Pick the next step. For a graph, run `graph.py ready` (see `dev-plan`).
   Prefer the smallest ready node that advances the objective.
5. Choose how to execute it:
   - continue in this session;
   - a subagent, for a bounded independent node;
   - a new session, through the app's native session handoff, with the
     checkpoint as its brief;
   - stop at a human gate.

   Never present a prepared handoff as already started or as done.

## Output

- Current facts (with sources) and the drift found
- Recommended next step, the execution mode, and the human gate if any
- The handoff decision and its basis (rounds, stage boundary, workload)
- The updated checkpoint path
