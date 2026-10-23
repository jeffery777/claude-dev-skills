# Review round 1 (deep, fresh reviewer), Issue #27

Written per ASD-STE100 principles; full conformance not verified.

- Target: working tree against HEAD `90b9f33`, `git diff HEAD --binary` (with the intent-to-add
  `.dev/issue-27-fu004-baseline/` files) sha256 `a336264d…597276278`. Reviewer: `dev-skills:dev-reviewer`
  (opus, xhigh, deep, strict). HEAD, status and diff hash were the same before and after the review.
- DoD: the report gives the results, the judge rubric, the method in words, and each task's start commit
  and verbatim first sentence; the FU-004 row records the run and stays Open; no private path or session
  ID; no script or mechanism; no change to `skills/`, `agents/`, `skills/dev-core/deltas.md` or
  `CHANGELOG.md`; process observations are observations only; the report is faithful to the sources;
  `validate.sh` passes.
- Sources: the orchestrator's results note, judge rubric and setup guide (outside the repository).
- Commands (reviewer): `git diff HEAD` and `--check`, `git log`/`git show --stat`, `git grep`, `gh issue
  view 27`, read-only `python3 -I` comparisons of the prompts and numbers with the sources, `git log -1
  <sha>` in the local clones of the two other public repositories, `PYTHONDONTWRITEBYTECODE=1 bash
  scripts/validate.sh` exit 0 (131 tests OK). Skipped: session records (not in the brief), GitHub facts
  of the other repositories, gitleaks.
- Result: no MUST-FIX; three SHOULD-FIX; one REQ-GAP. All numbers in the results table match the source.
  No repository rule requires a CHANGELOG entry for this change.

## Dispositions

| ID | Relation | Severity | Finding | Class | Disposition |
| --- | --- | --- | --- | --- | --- |
| R1-001 | in-scope | SHOULD-FIX | The start commits, the "verbatim" first sentences and "each task ran in a new session" were stated as facts, but the only source was the setup guide written before the run | necessary fix | Fixed: the author read the first command output and the first user message of each task from the session records. The start commits match; the T1 to T3 messages have no backticks, so the quotes now use the actual text. The report states where the values come from |
| R1-002 | in-scope | SHOULD-FIX | The method said that every skill file was counted; the source counts only `dev-deliver`, `dev-core` and Core files. The FU-004 row asks only for `dev-core` reads | necessary fix | Fixed: the method names the counted files and says that the setup guide added the Core files |
| R1-003 | in-scope | SHOULD-FIX | The short English summary of the prompts left out the safety and authority conditions of T3 and T4 (R-WRT-1) | necessary fix | Fixed: full English translations, with every condition |
| R1-004 | gap | REQ-GAP | A replay after FU-005 PR-4 from the same start commits cannot restore the GitHub and remote state: T1 was already done by PR #226, the T3 comment is posted, PR #26 is merged. No requirement says how to handle this | needs human decision | Decision card R1-004 to the user (via the orchestrator session); the user chose (a). Fixed: one factual statement in section 8 of the report; REQ-016 sources and the requirements log record the answer |
| S-1 | — | suspicion | "The judge gave these items low confidence": the source does not say who gave the confidence | below threshold | Reworded: "These items have low confidence" |

Decision card R1-004, as sent (Traditional Chinese):

> 決策卡 R1-004
> - 問題：報告說 PR-4 之後要「從同一個開始 commit、用同一句第一句話」重跑四個任務。但外部狀態已改變：T4 的修改已在 PR #26 合併（main 現為 90b9f33）；T3 的 triage 留言已貼在 grok-build-dev-skills Issue #2；T1 的 Issue #222 在基準時就已完成。REQ-016、REQ-025（卡片 7′a）和 FU-004 列都沒規定重跑時怎麼處理這些已改變的 GitHub／remote 狀態。
> - 影響：重跑可能不是同條件比較（推論）。這項不影響本次基準數字的正確性。
> - 選項：
>   (a) 在報告 §8 Limits 加一句事實說明（「從開始 commit 重跑不會還原 GitHub 與 remote 狀態；T1、T3、T4 的結果已存在」），不訂規則。
>   (b) 延後：本 PR 不寫，等 PR-4 之後的重跑規劃時再決定（由協調者負責）。
>   (c) 接受此風險，不記錄。
> - 建議：(a)。理由：只記一句可驗證的事實，不新增機制或規則，讓重跑的人一定看得到；(b) 的風險是沒有持久位置記住這件事。

User answer (relayed by the orchestrator session, 2026-10-23): 「同意你的建議，選a」.

## Residual risk

- `events.jsonl` seq 3 records the SHA-256 of the report at the transition to `reviewing`; the report
  changed later (append-only coordination data, CB-1).
- Below the threshold: "orchestrator" is not explained at first use; some long sentences.
- Suspicions not counted: T2 ME-1 shows that the judge got the orchestrator's summary for that item;
  T4 ran in claude-dev-skills, which the setup guide first excluded.
