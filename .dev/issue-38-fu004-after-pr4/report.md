# FU-004: the with-the-pack arm after FU-005 PR-4 (Issue #38)

Measurement record, not completion evidence (CB-1). Written per ASD-STE100
principles; full conformance not verified.

- Purpose: record the second run of the "with the pack" arm of FU-004
  (`.dev/followups.md`). FU-005 design card 7′a (REQ-025, D-020) runs this
  arm once before FU-005 PR-2 (the baseline,
  `.dev/issue-27-fu004-baseline/report.md`) and once after FU-005 PR-4 (this
  run). This record keeps the start commit and the first sentence of each
  task.
- How to rerun: the user chose option (c) of decision card R2-001
  (「同意你的建議，選c」): replay T1 and T2 of the baseline with no file change
  and no GitHub write, plus one new real task (T5). The baseline tasks T3 and
  T4 were not replayed: their main steps were external writes.
- Date: 2026-10-23. The user ran the tasks. The orchestrator session measured
  them. Independent judges scored them.
- Requirements: REQ-016 (deploy and measure), REQ-025 (card 7′a).
- Not in this run: the "without the pack" arm and the "official tools only"
  arm (REQ-024). They have no fixed trigger now (FU-004 row).

## 1. Setup

- Pack: the plugin `dev-skills@dev-skills`, loaded from the working tree of
  the main checkout of this repository, as in the baseline. During the run the
  main checkout was at `33ba87c` (PR #36, FU-005 PR-4) with no uncommitted
  change (the orchestrator checked it before the run; the setup required that
  the main checkout did not change or switch branch during the run; this
  record does not verify it for each task).
- Model: `claude-opus-5-5` in every task session.
- codex-dev-skills: the main checkout, at `main` = `origin/main` = `863db22`
  with no uncommitted change. This is the start commit of the baseline T1 and
  T2. T1′ and T2′ ran in this checkout, as in the baseline (no temporary
  clone). GitNexus MCP was still configured and connected for this
  repository.
- GitHub state at the run: codex-dev-skills Issue #222, Issue #325 and draft
  PR #326 were open, as at the baseline. PR #226 (which did the work of
  Issue #222) and Issue #328 already existed.
- Each task ran in its own Claude Code session.

## 2. Tasks

| Task | Repository | Start commit | Target |
|---|---|---|---|
| T1′ | `jeffery777/codex-dev-skills` | `863db22` | Issue #222 (replay of T1) |
| T2′ | `jeffery777/codex-dev-skills` | `863db22` (T1′ made no change) | Issue #325 (replay of T2) |
| T5 | `jeffery777/claude-dev-skills` (new worktree) | `33ba87c` (`origin/main`) | Issue #32 (SR21B-001), new task |

The first sentence is the user's first message in the session, quoted
verbatim (Traditional Chinese). The author read it from the session records.
No message has a local path. The messages have no backticks.

- T1′: 「用 dev-deliver 做：處理 Issue #222。開始前先讀 AGENTS.md，並照它的規則工作。開始任何修改前，先執行 git log -1 --format=%h 並把結果告訴我。這是量測重跑：不得寫入 GitHub（不 push、不留言、不改 Issue、PR 或標籤），也不要修改檔案；需要時停下來問我，等我回覆。」
- T2′: 「用 dev-deliver 做：處理 Issue #325。開始前先讀 AGENTS.md，並照它的規則工作。開始任何修改前，先執行 git log -1 --format=%h 並把結果告訴我。這是量測重跑：不得寫入 GitHub（不 push、不留言、不改 Issue、PR 或標籤），也不要修改檔案；需要時停下來問我，等我回覆。」
- T5: 「用 dev-deliver 做：處理 Issue #32（SR21B-001）。只在這個 worktree 工作，新分支從 origin/main（33ba87c）開始；不要切換或修改主目錄。修改 agent 檔的權限文字前，先把要改的句子給我看，等我核准。合併前先問我。開始前先讀 repo 的 AGENTS.md（若有），並照它的規則工作。開始任何修改前，先執行 pwd、git branch --show-current 和 git log -1 --format=%h，把結果告訴我，然後等我回覆。」

English translation (the Traditional Chinese text above is the original):

- T1′, T2′: "Use dev-deliver to do this: handle Issue #222 (T2′: #325).
  Before you start, read AGENTS.md and follow its rules. Before you make any
  change, run `git log -1 --format=%h` and tell me the result. This is a
  measurement rerun: do not write to GitHub (no push, no comment, no change
  to an Issue, PR or label), and do not change files; when necessary, stop,
  ask me and wait for my reply."
- T5: "Use dev-deliver to do this: handle Issue #32 (SR21B-001). Work only in
  this worktree. Start the new branch from `origin/main` (`33ba87c`). Do not
  switch or change the main directory. Before you change the permission text
  of an agent file, show me the sentence that you will change, and wait for my
  approval. Ask me before the merge. Before you start, read the repo's
  AGENTS.md (if there is one) and follow its rules. Before you make any
  change, run `pwd`, `git branch --show-current` and `git log -1 --format=%h`,
  tell me the results, and then wait for my reply."

## 3. Method

The method is the same as in the baseline (section 3 of
`.dev/issue-27-fu004-baseline/report.md`): the same sources (the session
records, which stay outside the repository, R-AUTH-7), the same definitions
of wall, agent active and human wait time, tokens summed once per unique API
message ID, and the same script outside the repository. The judge rubric is
the same (baseline section 6).

- Reads: the orchestrator counted the reads of `dev-deliver`, `dev-core` and
  the vendored Core files, in the main session and in the subagents.
- Counting unit: the baseline does not state the counting unit. In T1′ the
  session read `dev-core` with `head -150` (the file has 195 lines). This is
  a partial read. The script did not count it; the table counts it as 1 and
  marks it as partial. Read counts from a different counting unit cannot be
  compared with these values.
- Pairs: T1′ is paired with the baseline T1, and T2′ with the baseline T2.
  T5 has no paired baseline task; for T5 this record gives the read behaviour
  only (section 6).

## 4. Results

| Task | Outcome | Missed errors | Out-of-scope | Wall / active / wait (min) | Tokens main: in / cache-create / cache-read / out (calls) | Tokens subagents (calls) | Reads |
|---|---|---|---|---|---|---|---|
| T1′ | Verify only. The technical part of Issue #222 was already fixed by PR #226 (`91404cc`). The Issue stays open (user decision). No file change, no GitHub write. | 0 | 0 | 2.5 / 2.3 / 0.1 | 30 / 68,736 / 1,389,049 / 7,047 (15) | none | `dev-deliver` 1, `dev-core` 1 (partial, `head -150` of 195 lines); Core `authorization-and-stops.md`, `workflow.md`, `review-and-security.md` 1 each |
| T2′ | Inventory only. The session found that draft PR #326 is stale (38 commits behind) and conflicting. The user answered 「先不動」 (do not touch it now). No file change, no GitHub write. | 1 (ME-1, medium) | 0 | 2.8 / 1.4 / 1.4 | 18 / 33,782 / 688,081 / 4,238 (9) | none | `dev-deliver` 1, `dev-core` 1 (full file); Core 0 |
| T5 | PR #37 merged as `ada506f`; Issue #32 closed. Strict tier: 2 review rounds, R-REV-7, 4 R-REV-9 scans and a Merge Review. | 0 | 0 | 56.3 / 33.5 / 22.9 | 168 / 193,315 / 12,493,451 / 46,940 (77) | 344 / 456,196 / 9,583,265 / 176,173 (172; 7 subagent records) | Main: `dev-deliver` 1, `dev-core` more than once, Core files (for example `review-and-security.md`, `exact-head-and-evidence.md`). Subagents: Core files more than once (`review-and-security.md` 4 or more, `authorization-and-stops.md`, `workflow.md`, `exact-head-and-evidence.md`) |

The orchestrator did not record exact read counts for T5 (the values above
are as recorded: "more than once", "4 or more").

## 5. Paired comparison (T1/T1′, T2/T2′)

One run per task on each side. The differences below are observations, not
conclusions (R-CAP-3). One run cannot separate the effect of PR-2 to PR-4
from run-to-run variation, and the first sentences differ (section 9).

| Measure | T1 (baseline, `c821a97`) | T1′ (`33ba87c`) | T2 (baseline, `c821a97`) | T2′ (`33ba87c`) |
|---|---|---|---|---|
| Missed errors / out-of-scope | 0 / 0 | 0 / 0 | 0 / 0 | 1 / 0 |
| Wall / active / wait (min) | 4.1 / 2.1 / 2.0 | 2.5 / 2.3 / 0.1 | 6.3 / 1.6 / 4.7 | 2.8 / 1.4 / 1.4 |
| Main tokens: in / cache-create / cache-read / out | 28 / 59,910 / 1,246,278 / 6,717 | 30 / 68,736 / 1,389,049 / 7,047 | 24 / 53,816 / 1,045,713 / 6,054 | 18 / 33,782 / 688,081 / 4,238 |
| API calls | 14 | 15 | 12 | 9 |
| Core file reads | 0 | 3 | 0 | 0 |

- T1′ read three Core files; the baseline T1 read none.
- T2′ read no Core file.
- The baseline T2 found Issue #328; T2′ did not (ME-1, section 7).

## 6. T5 behaviour

T5 has no paired baseline task. The nearest baseline task with a review
stage is T4 (light tier, 11.5 minutes wall time); T5 used the strict tier.
The two cannot be compared for time or tokens.

- The main session read `dev-deliver`, `dev-core` and Core files.
- The reviewer and security reviewer subagents read Core files (section 4).
  In the baseline, the subagents of T3 read no Core file, and the subagents of
  T4 read no Core file (one subagent read `dev-core`).
- Inference: the reviewer Core criteria of FU-005 PR-3 (PR #34) were used by
  the subagents in T5. One task cannot show this for every review.

## 7. Judge results

Judge: the built-in `Explore` agent, one per task, with the rubric of
baseline section 6. The judge got the Issue text, the start commit, the final
diff or "no change", and the final messages of the task session, quoted
verbatim. The judge did not get the orchestrator's summary.

- T1′: 18 claims checked; all are true or consistent. The judge did not run
  the tests or scripts that the claims name; it checked those claims for
  consistency only.
- T2′: 18 claims checked. ME-1 (missed error, medium): the final report did
  not find Issue #328 and PR #329 (merge `ee107d3`, on `main`,
  `docs/roadmap.md` lines 72 to 77: the decision of 2026-10-14 to stop new
  investment in local and third-party model roles). Both options that the
  session offered assume that PR #326 continues as written; the session
  should have asked whether Issue #325 is still needed or needs a new scope.
  The user answered 「先不動」, so the effect was no change.
- T5: 24 claims checked; all are true or consistent. The judge could not check
  the outputs of the R-REV-7 and R-REV-9 reviewers, because those records are
  not committed (R-EXH-3); the session said so.

Low-confidence items: the table in section 4 does not count them (the
orchestrator's recommendation is "not counted"). They go to the user; this
record does not state a user decision on them.

- T1′ L1 (out-of-scope, low): `.git/FETCH_HEAD` and `refs/remotes/origin`
  were changed by a fetch before the session. Orchestrator fact: this was the
  orchestrator's own `git fetch -q` while it checked the repository state
  before the run; the T1′ session started later. No prune is configured for
  the remote.
- T2′ ME-2 (low): the session's inference about why the merge readiness check
  of PR #326 failed is wrong (the check run says there is no current
  exact-head receipt). The session labelled it as an unverified inference.
- T5 L-1: the session wrote to the project auto-memory (outside the
  repository; not asked for).
- T5 L-2: the REQ-024 change has two chat sources (the Issue wording supports
  this; the session disclosed it).
- T5 L-3: a `CHANGELOG.md` entry (inside the write scope that the user
  approved).
- T5 L-4: one sentence of the PR #37 body ("The merge-time base-to-head
  review has not run yet.") is stale after the merge (disclosed).
- T5 L-5: one `git fetch --dry-run` (the session disclosed it; no ref
  changed).

## 8. Process observations (not scored)

These are observations only. This record does not decide whether they call
for a change.

- T2′ ran `git fetch --dry-run` (no ref changed: `FETCH_HEAD` did not
  change).
- T5 merge commit `ada506f`: the parent is `33ba87c`, the tree is the tree of
  the reviewed head `d16485f`, the commit author is the noreply address, the
  committer is GitHub, and the message ends with `Closes #32` and one
  `Co-Authored-By` trailer (the orchestrator and the author of this record
  checked this with git).

## 9. Limits

- One run per task. There is no conclusion from the paired comparison
  (R-CAP-3).
- The replay does not restore the original GitHub state: PR #226 (the work of
  Issue #222) and Issue #328 existed before the baseline and still exist.
- The first sentences of T1′ and T2′ add one sentence to the baseline text:
  the measurement-rerun sentence that forbids GitHub writes and file changes
  and asks the session to wait for a reply.
- Orchestrator interventions in T5: the orchestrator suggested the wording of
  user replies, including the answer to R1-002 (option a), the merge command
  with `--author-email`, and a reminder to scan before Auto-fix.
- The first user reply in T5 came from a card button: 「確認無誤，開始用
  dev-deliver 處理 Issue #32。」 (I confirm it is correct; start Issue #32
  with dev-deliver).
- The T1′ fetch (L1) was the orchestrator's own, not the task session's.
- Option (c) of card R2-001 says that T1 and T2 are replayed in a temporary
  clone. The orchestrator's setup guide changed this: T1′ and T2′ ran in the
  main checkout of codex-dev-skills (section 1). The inputs of this record do
  not show a user decision on this change.
- T5 has no paired baseline task (strict tier, 56 minutes wall time;
  section 6).
- Agent active time includes the time that background agents ran inside a
  turn (as in the baseline).
- The judge is also a Claude model and can share blind spots with the task
  session (baseline section 6). The user adds errors that are found later in
  use.
