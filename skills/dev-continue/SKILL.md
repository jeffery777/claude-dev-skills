---
name: dev-continue
description: Save a checkpoint before pausing, or resume saved development work from repository state - re-grounds from files and Git, not chat memory, then selects the next safe task or handoff. Use for "continue", "resume", "where were we", handoffs, or when context is getting long.
---

# dev-continue

Read `${CLAUDE_SKILL_DIR}/../dev-core/SKILL.md` first. The rules for resuming
are R-STG-5 and R-EVD-2.

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
- The updated checkpoint path
