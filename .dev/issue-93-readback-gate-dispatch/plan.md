# Issue #93 plan: fail-closed read-back gate for dispatches of work under the floor (Issue #79 slice C1)

- Objective: GitHub Issue #93, slice C1 of the tracking Issue #79: the main
  agent reads the recorded model and effort of every subagent with the
  read-back script of Issue #89, and a dispatch of work under the R-DEL-2
  floor whose read-back does not pass stops the node and goes to the user.
- Rigor `strict`. Reason (R-RIG-1, re-assessed at Discover as R-RIG-2
  says): a change to a security rule (R-DEL-2) and to pack rule text.
- Base: `main` 51f9fd3, branch `issue-93-readback-gate-dispatch` (created
  from Issue #93 on GitHub).
- Method (lesson of slice C0): no word of an existing sentence changes; the
  slice adds sentences, and a deterministic word diff checks it.

## Source trace (dev-plan step 2)

Sources: the Issue #93 body; the Issue #79 body (Change 1 to 5, the spec
input and the tracking section); the slice B dependency table in REQ-009;
FU-021, FU-048 and FU-052; and these user answers (Claude Code session
2026-10-30, the user's words in the orchestrator session, relayed):

- 「I79C-C1 a，C2 b，C3 c，C4 a，這些我同意你的建議」: slice C1 is the core
  rules and the dispatches of work under the floor; transcript rewriting is
  a residual risk with a tamper-evidence follow-up (FU-051).
- 「I93-C1 a，C2 a」: the redo definition, the headless result and the note
  without a record before the dispatch are sentences; the pre-dispatch
  snapshot, the `.meta.json` cross-check and session confinement are
  FU-053, FU-054 and FU-055; only the user's own message in this session
  approves the use of a result that did not pass, and a `BELOW` or
  `unknown` result never counts as work at the floor.
- 「I93-R2-C1 a」: after the R-VER-2 stop of design round 2, rev 3 adds one
  sentence for each round 2 finding; no design round 3.

From the design reviews, not from the user's words: the sources of the
agent ID, the projects directory and the expected values; the finish of a
dispatch; the bootstrap copy of the base and its record; the validity of
an output; the meaning of a known ability to set a value; the tamper
statement.

## Design reviews

| Round | Target | Result | Outcome |
| --- | --- | --- | --- |
| 1 | Design rev 1 | deep: 5 MUST-FIX, 4 SHOULD-FIX, 3 NIT; security: BLOCKED, 2 MUST-FIX, 5 SHOULD-FIX, 1 REQ-GAP, 1 NIT | cards I93-C1 (a) and I93-C2 (a); rev 2 |
| 2 | Design rev 2 | deep: 2 NIT; security: PASS, 2 SHOULD-FIX, 5 NIT; no sentence wider than main | R-VER-2 (same mechanisms needed fixes again); card I93-R2-C1 (a); rev 3 |

All reviewers: requested `opus`/`xhigh`; recorded `claude-opus-5-5`/`xhigh`
from the transcript fields; effective `unknown`. The main agent ran the G1b
form on a synthetic fixture (PASS, exit 0); the security reviewer ran two
failing cases (both fail closed).

## Dispatches and floor check

The main session read its own transcript before it wrote this plan, and
again before it changed the R3-8 sentence and these records, and after
the pause before the round 1 fixes:
`claude-opus-5-5`/`high`; requested value `unknown` (set by the session
that started it).

| Node or step | Agent | Requested | Recorded | Effective |
| --- | --- | --- | --- | --- |
| Issue #93 and #79 text scan | `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |
| Design review rounds 1 and 2 | `dev-reviewer`, `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |
| T1 | `dev-implementer` | `opus`/`high` | `claude-opus-5-5`/`high` | `unknown` |
| Implementation review round 1 | `dev-reviewer`, `dev-security-reviewer` | `opus`/`xhigh` | `claude-opus-5-5`/`xhigh` | `unknown` |

## Word-diff check

Command (bash; base pinned; the six changed pack files as separate
arguments; `skills/dev-core/deltas.md` only gains the DL-042 row):

```
git --no-replace-objects diff --no-ext-diff --no-textconv --no-color --text --word-diff=porcelain --word-diff-regex='[^[:space:]]+' 51f9fd344e5a06c55748fe969cedc917a56ff7da -- skills/dev-core/SKILL.md skills/dev-core/references/model-effort-readback.md skills/dev-deliver/SKILL.md skills/dev-deliver/references/task-brief.md skills/dev-continue/SKILL.md skills/dev-core/deltas.md | LC_ALL=C grep -E '^-' | LC_ALL=C grep -Ev '^--- (a/|/dev/null)'; test $? -eq 1 && echo NO-WORD-REMOVED
```

Result on the working tree before the commit, after the round 1 fixes:
`NO-WORD-REMOVED`, with 27 added word lines over the six files. The result at the committed head goes into a PR comment
(R-EXH-3).

Two sentences of rev 3 name design labels that the pack does not have;
the implementer wrote "the copy at the bound base" for "G1b" and "The
user's approval below" for "G4". The main agent changed the added reference
sentence of R3-8 to "The second and the third sentence of this paragraph"
so that it names the sentences it means.

## Implementation review

Round 1 (T1 as implemented): deep, no MUST-FIX or SHOULD-FIX, NIT
I93-R1-01 to I93-R1-03; Security Diff Scan, PASS, NIT I93-S1-01 and
I93-S1-02. Both: no added sentence wider than main, every bypass of the
design rounds closed, and no finding in a mechanism that the design rounds
fixed. Both reviewers: requested `opus`/`xhigh`, recorded
`claude-opus-5-5`/`xhigh`. The work paused after this round by the user's
words in the orchestrator session, relayed: 「Issue #79當前的審查及安全掃瞄完成後就先暫停，等我通知繼續再接下去完成。」; it resumed on 「繼續」.

| ID | Severity | Disposition |
| --- | --- | --- |
| I93-R1-01 | NIT | Fixed: notes in the REQ-009 Limit paragraph and after the slice B dependency table |
| I93-R1-02, I93-S1-01 | NIT | Fixed: the word diff covers six files (`deltas.md` included) here, in REQ-009, in D-027 (both languages) and in the CHANGELOG |
| I93-R1-03 | NIT | Fixed: FU-048, REQ-009 and D-027 say that `dev-deliver` adds a shorter copy of the first clause |
| I93-S1-02 | NIT | Rejected: G6 before "It tells the user each requested value" leaves the reader of "It" in no doubt that the main agent tells the user, and moving G6 would change no rule |

## Residual risks

See D-027: without a record of the state before a dispatch there is no
basis for "what the result changed"; an agent ID can point to a transcript
of another session of the same user (FU-055); every agent that runs floor
work has Bash, so the gate does not resist an agent or a process that acts
against it (FU-051); headless runs are not tested; every case that cannot
be read back needs a redo or a user decision; the allowlist holds only the
Opus ID, so a newer Opus stops every dispatch until a strict change
(FU-049); the G1b form is checked by hand only.

## Non-goals

Reviews and scans (slice C2), `dev-retro` (slice C3), session read-back
(slice D), FU-049, FU-050, the other FU-052 items.
