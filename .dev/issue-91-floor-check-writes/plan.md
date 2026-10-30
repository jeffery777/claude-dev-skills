# Issue #91 plan: the floor check of the main session covers every write, records included, from every entry point (Issue #79 slice C0)

- Objective: GitHub Issue #91 (body and its 2026-10-30 update), slice C0 of
  the tracking Issue #79: close FU-035 (the entry points and the record
  writes of the floor check of a main session) and FU-021 item (2), with
  added sentences only.
- Rigor `strict`. Reason (R-RIG-1, re-assessed at Discover as R-RIG-2
  says): a change to a security rule (R-DEL-2) and to pack rule text.
- Base: `main` 03cc3dd, branch `issue-91-floor-check-writes` (created from
  Issue #91 on GitHub).

## Source trace (dev-plan step 2)

Sources: the Issue #91 body and update; FU-035 and FU-021 in
`.dev/followups.md`; the findings MR85B-01 (PR #86) and MR89-01 (PR #90);
and these user answers (Claude Code session 2026-10-30, the user's words in
the orchestrator session, relayed by the orchestrator):

- 「I79C-C1 a，C2 b，C3 c，C4 a，這些我同意你的建議」: card I79C-C2 (b),
  FU-035 becomes slice C0 before C1.
- 「I79C0-C1 a，C2 a，C3 a」: every record counts as a write, and a failed
  check puts the values and the choice into the reply; the check runs
  before every write, also within one turn; FU-021 item (2) is part of C0.
- 「I91-R2-C1 c，加逐字比對，做窄範圍第 3 輪」: after the R-VER-2 stop
  rule of design review round 2, the slice only adds sentences, keeps every
  word of the R-DEL-2 text on main, checks this with a deterministic word
  diff, and moves the record-line mechanism to FU-052; a narrow round 3
  checks the added sentences.

## Design reviews

| Round | Target | Result | Outcome |
| --- | --- | --- | --- |
| 1 | Design rev 1 | deep: BLOCKED, 2 MUST-FIX; security: BLOCKED, 2 MUST-FIX | cards I79C0-C1 to C3; rev 2 |
| 2 | Design rev 2 | deep: BLOCKED, new MUST-FIX D2-01; security: BLOCKED, new MUST-FIX S2-01 (the rewritten definition of a write dropped "fixes" and "a re-applied change") | R-VER-2 stop card I91-R2-C1 (c); rev 3 adds sentences only |
| 3 | Design rev 3 (the added sentences only) | deep: no added sentence wider than main, no new blocker; security: PASS, same answer | the word-diff command and two record notes fixed (rev 3 section G) |

All reviewers: requested `opus`/`xhigh`; recorded `claude-opus-5-5`/`xhigh`
from the transcript fields; effective `unknown`.

## Implementation review

Round 1: deep, no MUST-FIX, SHOULD-FIX I91-R1-01 and I91-R1-02; Security
Diff Scan, PASS, SHOULD-FIX I91-S1-01 and I91-S1-05, NIT I91-S1-02 to
I91-S1-04. Both: no added sentence wider than main, no new blocker.

| ID | Severity | Disposition |
| --- | --- | --- |
| I91-R1-01, I91-S1-05 | SHOULD-FIX | Fixed: this plan records the word-diff command and its result, and the T1 dispatch; D-026 says that the plan records the result before the commit and a PR comment at the committed head |
| I91-R1-02 | SHOULD-FIX | Fixed: `--no-color --text` in the command here and in D-026 (both languages) |
| I91-S1-01 | SHOULD-FIX | Fixed: one added pointer sentence after "The plan records the values and the choice." in `dev-deliver` step 2 |
| I91-S1-02 | NIT | Deferred to FU-052: who writes the other records that a dispatch needs when the check does not pass |
| I91-S1-03 | NIT | Fixed: the FU-052 item no longer states that a decision card is never a write |
| I91-S1-04 | NIT | Rejected: every reading of "does this itself" at `dev-continue` Resume step 5 runs the check |

## Word-diff check (card I91-R2-C1 (c))

Command (base pinned; the eight skill files as separate arguments; run in
bash):

```
git --no-replace-objects diff --no-ext-diff --no-textconv --no-color --text --word-diff=porcelain --word-diff-regex='[^[:space:]]+' 03cc3dde743e0ebf8f089378ed334b6fbc0e46ab -- skills/dev-core/SKILL.md skills/dev-deliver/SKILL.md skills/dev-review/SKILL.md skills/dev-gate/SKILL.md skills/dev-implement/SKILL.md skills/dev-docs/SKILL.md skills/dev-plan/SKILL.md skills/dev-continue/SKILL.md | LC_ALL=C grep -E '^-' | LC_ALL=C grep -Ev '^--- (a/|/dev/null)'; test $? -eq 1 && echo NO-WORD-REMOVED
```

Result on the working tree before the commit, after the round 1 fixes:
`NO-WORD-REMOVED`, with 39 added word lines (not vacuous). The result at the
committed head goes into a PR comment (R-EXH-3). `--no-color` and `--text`
were added after implementation review round 1 (I91-R1-02): without them a
color setting or a `-diff` attribute could hide a removed word.

## Dispatches and floor check

The main session read its own transcript before it wrote this plan, and
again before it wrote the round 1 fixes and these records:
`claude-opus-5-5`/`high`; requested value `unknown` (set by the session
that started it).

| Node or step | Agent | Requested | Recorded | Effective |
| --- | --- | --- | --- | --- |
| Discover survey | `dev-explorer` | `opus`/`high` | `claude-opus-5-5`/`high` | `unknown` |
| Issue #91 and #79 text scan | `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |
| Design review rounds 1 to 3 | `dev-reviewer`, `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |
| T1 | `dev-implementer` | `opus`/`high` | `claude-opus-5-5`/`high` | `unknown` |
| Implementation review round 1 | `dev-reviewer`, `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |

## Residual risks

The check still reads the session's own setting by the manual read of
R-DEL-2, now before every write, so the risk of FU-021 item (4) grows with
the number of reads until slice D. The plan line of a check is a record that
the session writes itself, not evidence (FU-052). A setting changed within a
turn by another path shows only in a later transcript record. With
`unknown`, every record write needs a user question or a dispatch.
MR89-01 was a breach of the rule on main; C0 makes such a case easier to
see, not impossible. The main text of R-DEL-2 keeps "(FU-035 lists entry
points that the check does not cover yet)", which the added sentence after
it updates.

## Non-goals

The read-back gate of slices C1 to C3; session read-back (slice D); the
record-line format, placement and severity (FU-052); FU-044, FU-046 to
FU-050.
