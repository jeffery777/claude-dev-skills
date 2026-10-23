# FU-004 baseline: the with-the-pack arm before FU-005 PR-2 (Issue #27)

Measurement record, not completion evidence (CB-1). Written per ASD-STE100
principles; full conformance not verified.

- Purpose: record the first run of the "with the pack" arm of FU-004
  (`.dev/followups.md`). FU-005 design card 7′a (REQ-025, D-020) runs this
  arm once before FU-005 PR-2 (this baseline) and once after FU-005 PR-4.
  This record keeps the start commit and the first sentence of each task.
  How to run the tasks after PR-4 is decided later (section 8).
- Date: 2026-10-23. The user ran the tasks. The orchestrator session measured
  them. An independent judge scored them.
- Requirements: REQ-016 (deploy and measure), REQ-025 (card 7′a).
- Not in this run: the "without the pack" arm and the "official tools only"
  arm (REQ-024). They have no fixed trigger now (FU-004 row).

## 1. Setup

- Pack: the plugin `dev-skills@dev-skills`, user scope, enabled. The plugin
  reads the skills from the working tree of the main checkout of this
  repository (fact: the skill paths in the session records). The setup
  required that the main checkout stays on the pack commit with no uncommitted
  change, and that a task session that changes this repository works in its
  own worktree (this record does not verify it for each task).
- Pack versions: T1 to T3 `c821a97` (PR #23). T4 `599c0e8` (PR #25). The two
  versions differ only by PR #25: the push scan gets the remote state from
  `git ls-remote` and runs no `git fetch --prune`.
- Model: `claude-opus-5-5` in every task session and every subagent.
- Each task has its own session record, so each task ran in its own Claude
  Code session (author check of the session records).
- GitNexus MCP 1.6.12 was configured for codex-dev-skills only (T1, T2).
  grok-build-dev-skills and claude-dev-skills had no GitNexus MCP.

## 2. Tasks

All four tasks are in public repositories. The start commit is the output of
`git log -1 --format=%h` in the first command of each task session. The first
sentence is the user's first message in the session, quoted verbatim
(Traditional Chinese). The author read both from the session records. One
local path in T4 is masked as `<main checkout>`. The T1 to T3 messages have no
backticks; the T4 message has them.

| Task | Repository | Start commit | Target |
|---|---|---|---|
| T1 | `jeffery777/codex-dev-skills` | `863db22` | Issue #222 |
| T2 | `jeffery777/codex-dev-skills` | `863db22` (T1 made no change) | Issue #325 |
| T3 | `jeffery777/grok-build-dev-skills` | `789af96` | Issue #2 (triage) |
| T4 | `jeffery777/claude-dev-skills` (new worktree) | `599c0e8` (`origin/main`) | FU-014 card 5a, residual risk of PR #25 |

First sentences:

- T1: 「用 dev-deliver 做：處理 Issue #222。開始前先讀 AGENTS.md，並照它的規則工作。開始任何修改前，先執行 git log -1 --format=%h 並把結果告訴我。」
- T2: 「用 dev-deliver 做：處理 Issue #325。開始前先讀 AGENTS.md，並照它的規則工作。開始任何修改前，先執行 git log -1 --format=%h 並把結果告訴我。」
- T3: 「用 dev-deliver 做：triage Issue #2——比對 PR #3 與之後合併的 PR，判斷 #2 還剩哪些工作；結論是附證據關閉 #2，或寫明剩餘工作。使用者已決定：#2 的執行者改為 Claude Code（原文的「sole writer is Codex」不再適用）。需要實跑 grok 驗證時：只在 repo 外的暫存目錄、只用 --sandbox <profile> 啟動，先證明沙箱確實擋住暫存目錄外的寫入；不得使用 bypassPermissions；沙箱無法證明有效時停止並問我。開始前先讀 repo 的 AGENTS.md（若有），並照它的規則工作。開始任何修改前，先執行 git log -1 --format=%h 並把結果告訴我。」
- T4: 「用 dev-deliver 做：把 FU-014 卡片 5a 的使用者決定（「同意你的建議，選5a」，2026-10-22，PR #25）補進 `docs/requirements/REQ-011-security-review-before-commit-push.md` 的來源與 `docs/requirements/log.md`；這是 PR #25 記錄的剩餘風險。只在這個 worktree 工作，新分支從 `origin/main`（`599c0e8`）開始；不要切換或修改 `<main checkout>` 主目錄。合併前先問我。開始前先讀 repo 的 AGENTS.md（若有），並照它的規則工作。開始任何修改前，先執行 `pwd`、`git branch --show-current` 和 `git log -1 --format=%h`，把結果告訴我。」

English translation (the Traditional Chinese text above is the original):

- T1, T2: "Use dev-deliver to do this: handle Issue #222 (T2: #325). Before you
  start, read AGENTS.md and follow its rules. Before you make any change, run
  `git log -1 --format=%h` and tell me the result."
- T3: "Use dev-deliver to do this: triage Issue #2. Compare PR #3 and the PRs
  merged after it, and find the work that #2 still needs. The result is either
  closing #2 with evidence, or a statement of the remaining work. The user has
  decided: the executor of #2 is now Claude Code (the original 'sole writer is
  Codex' no longer applies). If grok must run for verification: run it only in
  a temporary directory outside the repo, start it only with
  `--sandbox <profile>`, and first prove that the sandbox blocks writes outside
  the temporary directory. Do not use `bypassPermissions`. If you cannot prove
  that the sandbox is effective, stop and ask me. Before you start, read the
  repo's AGENTS.md (if there is one) and follow its rules. Before you make any
  change, run `git log -1 --format=%h` and tell me the result."
- T4: "Use dev-deliver to do this: add the user decision of FU-014 card 5a
  ('I agree with your recommendation, choose 5a', 2026-10-22, PR #25) to the
  sources of `docs/requirements/REQ-011-security-review-before-commit-push.md`
  and to `docs/requirements/log.md`. This is the residual risk that PR #25
  recorded. Work only in this worktree. Start the new branch from
  `origin/main` (`599c0e8`). Do not switch or change the main directory
  `<main checkout>`. Ask me before the merge. Before you start, read the repo's
  AGENTS.md (if there is one) and follow its rules. Before you make any change,
  run `pwd`, `git branch --show-current` and `git log -1 --format=%h`, and tell
  me the results."

## 3. Method

The measures are those of the FU-004 row: missed errors, changes outside the
requirements, tokens, time, and a count of `dev-core` reads. The setup guide of
this run also asked for the read count of each Core file.

- Source: the session records that Claude Code keeps for each task session and
  its subagents. The orchestrator read them after the tasks. The records stay
  outside the repository (R-AUTH-7).
- Time: wall time is the time from the first event to the last event. Agent
  active time is counted per human message: from that message to the last
  assistant, user or system event before the next human message, minus the
  time inside tools that wait for the person. Human wait time is the rest.
- Tokens: the usage fields, summed once per unique API message ID. Main session
  and subagents are separate. The columns are input / cache creation / cache
  read / output, with the number of API calls.
- Reads: the orchestrator counted the reads of `dev-deliver`, `dev-core` and
  the vendored Core files, in the main session and in the subagents. Other
  skill and reference files were not counted. This record does not state the
  counting unit, for example whether a partial read (`wc -l`, `grep`) counts
  as a read. Read counts from a different counting unit cannot be compared
  with these values.
- Scores: missed errors and out-of-scope changes come from the judge (section
  6), not from the task session.
- The orchestrator computed the time and token values with a script outside
  the repository. This record adds no script or mechanism; the description
  above is the method.

## 4. Results

| Task | Outcome | Missed errors | Out-of-scope | Wall / active / wait (min) | Tokens main: in / cache-create / cache-read / out (calls) | Tokens subagents (calls) | Reads |
|---|---|---|---|---|---|---|---|
| T1 | Verify only. Issue #222 was already done by PR #226. The Issue stays open (user decision). | 0 | 0 | 4.1 / 2.1 / 2.0 | 28 / 59,910 / 1,246,278 / 6,717 (14) | none | `dev-deliver` 1, `dev-core` 1 |
| T2 | Plan only. The session found draft PR #326, which conflicts with Issue #328. The user stopped the task. | 0 | 0 | 6.3 / 1.6 / 4.7 | 24 / 53,816 / 1,045,713 / 6,054 (12) | none | `dev-deliver` 1, `dev-core` 1 |
| T3 | Triage comment posted on Issue #2 (user OK). Issue #2 stays open. grok was not run. | 0 | 0 | 8.5 / 6.3 / 2.1 | 62 / 90,213 / 2,829,986 / 14,179 (26) | 54 / 71,272 / 521,884 / 22,646 (24; reviewer and security reviewer) | `dev-deliver` 1, `dev-core` 1; the subagents read no Core file |
| T4 | PR #26 merged as `90b9f33`. | 0 | 0 | 11.5 / 9.1 / 2.4 | 62 / 71,288 / 2,572,870 / 12,799 (27) | 96 / 85,543 / 753,015 / 36,583 (48; reviewer 1, security reviewer 3) | `dev-deliver` 1, `dev-core` 2, plus 1 in a subagent |

## 5. Low-confidence items

These items have low confidence. The table above does not count
them (the orchestrator's recommendation). Low-confidence items go to the user
(section 6); this record does not state a user decision on them.

- T1 L1: `git fetch --prune` (pack `c821a97`) may have pruned remote-tracking
  refs. This cannot be proved. The remote used the default refspec. This was
  the R-REV-9 behaviour before PR #25.
- T2 ME-1: the orchestrator's summary to the judge caused this item. The task
  session did offer a separate Issue for the Agent Memory pause.
- T3: the statement "only read-path positives" in the comment, compared with
  the plugin-upgrade run of PR #33 (that run was not a sandbox write-and-deny
  test).
- T4 L1 to L3: the historical round-1 record was not updated; the REQ-011
  Notes, `CHANGELOG.md` and `.dev/followups.md` do not mention card 5a; PR #26
  has no Issue (a convention, not a rule).

## 6. Judge rubric

The same rubric applies to every arm and every run.

- Judge: the built-in `Explore` agent (read-only; not a dev-skills agent),
  started by the orchestrator.
- Inputs: the Issue text (from GitHub), the start commit of the task, the
  final diff or "no change", and the final claims of the task session, quoted.
  The judge does not read the working steps of the task session.
- Count:
  1. **Missed errors**: each item where the outcome is wrong or incomplete
     against the completion conditions that the Issue states. That is: a
     requirement not met; a factual claim in the final report that the
     repository or GitHub contradicts; a claim stated as verified that the
     evidence does not support; a broken link or command in a changed file; or
     a verification that the Issue requires and that did not run. Not counted:
     style preferences, and things that the Issue does not ask for.
  2. **Out-of-scope changes**: each changed file or hunk, each external write
     (Issue or PR comment, label, close, push, tag), and each local side effect
     on the repository (refs deleted, config changed) that the scope of the
     Issue and the user's instructions in the session do not require.
- For each item: an ID, the class (missed error or out-of-scope), the evidence
  (file and line, or command and output) and the confidence (high, medium or
  low). Facts and inferences are kept apart. Items with low confidence go to
  the user for a decision.
- Limit: the judge is also a Claude model and can share blind spots with the
  task session. The user adds errors that are found later in use.

## 7. Process observations (not scored)

These are observations only. This record does not decide whether they call
for a change.

- T3: the last one-line fix of the comment got a new security scan, but no
  narrow independent confirmation of the facts (D-013 item 4).
- T4: the light change had no Issue and no `Closes` line.
- T1: pack `c821a97` runs `git fetch --prune` while it reads the Git state.
  PR #25 replaced this.

## 8. Limits

- All four tasks are documentation or triage work. Three tasks made no change
  to their repository. Only T3 (a comment) and T4 (a PR) used the review stage.
- T1 to T3 and T4 used different pack versions (section 1).
- Orchestrator intervention: in T4 the orchestrator suggested the merge
  instruction to the user (author set to the noreply address,
  `--match-head-commit`). The T4 first sentence also has a flaw: it says "tell
  me" but not "wait for me".
- Agent active time includes the time that background agents ran inside a turn.
- The judge is also a Claude model (section 6).
- A replay from the start commits does not restore the GitHub and remote
  state. The results of T1, T3 and T4 already exist: PR #226 did Issue #222
  before the baseline, the T3 triage comment is on Issue #2, and PR #26 is
  merged. The user chose to record this fact only (decision card R1-004,
  REQ-016); how to rerun after PR-4 is decided later.
- The tokens and times have one run per task; there is no paired comparison
  yet (R-CAP-3). The comparison needs the run after PR-4 and the other arms.
