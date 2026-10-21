# claude-dev-skills

[繁體中文](#zh-tw) · [English](#english)

<a id="zh-tw"></a>

## 這是什麼

給 Claude Code 與 Cowork 使用的軟體開發技能包。它把一項有明確範圍的工作帶過這些步驟：釐清需求、規劃、實作、驗證、獨立審查、文件同步、交付關卡與接續。

它參考了 [codex-dev-skills](https://github.com/jeffery777/codex-dev-skills) 與 [engineering-workflow-core](https://github.com/jeffery777/engineering-workflow-core)，但不操作 Codex。工程義務以 vendor 進來的 Core v0.1.1 原文為唯一權威；`dev-core` 是 Claude 執行用的精簡版。

技能主要由 agent 依需求自動選用；人也可以手動指定，例如 `/dev-skills:dev-review`。

設計與決策紀錄：[docs/design-proposal.md](docs/design-proposal.md)。本專案自己的需求：[docs/requirements/](docs/requirements/index.md)。

## 安裝

Plugin 名稱是 `dev-skills`。Claude 保留 `claude-` 開頭的 plugin 名稱，所以 plugin 名稱和 repo 名稱不同。

Claude Code：

```bash
claude plugin marketplace add jeffery777/claude-dev-skills
```

```bash
claude plugin install dev-skills@dev-skills
```

在本機的 checkout 測試時，改用 `claude plugin marketplace add ./`。

Cowork：到 Customize > Plugins > Add marketplace，輸入 `jeffery777/claude-dev-skills`，再安裝 `dev-skills`。

Cowork 有兩項尚未實測：技能能否執行 `graph.py`（需要 shell），以及 `${CLAUDE_SKILL_DIR}` 的相對路徑能否解析。不能執行時，技能仍可依文件手動操作。

## 技能

| 技能 | 用途 |
| --- | --- |
| `dev-core` | 共用規則。每條規則都對應到 Core 的錨點 |
| `dev-plan` | 釐清需求並 ingest 成 REQ 檔，決定風險等級，產出 task graph |
| `dev-implement` | 實作一個有界修改，驗證後自查 diff |
| `dev-review` | 派獨立的唯讀 reviewer。finding 有 ID、與需求的關係、嚴重度（含 `SCOPE-CREEP`、`REQ-GAP`）與處置；需要使用者決定的事項用決策卡片 |
| `dev-gate` | commit／push／PR／merge 前的正式關卡。content、platform、授權三項分開判定 |
| `dev-docs` | 依已驗證的行為同步文件，並檢查 code 與文件是否一致 |
| `dev-continue` | 存 checkpoint；工作項目完成時評估是否換對話（D-012）；接續時從 repo 狀態重建 |
| `dev-deliver` | 外層編排：依 task graph 派工、整合、審查，再跑關卡 |

Subagents：`dev-explorer`（haiku）、`dev-implementer`（sonnet）、`dev-reviewer`（opus），以及 `dev-security-reviewer`（opus）。兩個 reviewer 沒有 Edit 和 Write 工具，但保留 Bash 以便跑測試；Bash 的唯讀使用靠指示約束，不是技術隔離。

## 適度嚴謹

- `light`：低風險的局部修改，不建 graph 檔。若要 commit、push 或開 PR，仍須先經獨立 review 與 commit gate。
- `standard`：一般功能。要有 task graph 和獨立 reviewer。
- `strict`：涉及安全、資料、migration、對外契約或 release。要初期就做深入或安全審查，並通過 exact-head 關卡與 human gate。
- 所有等級：每次 commit 與 push 之前，由 `dev-security-reviewer` 掃描已 stage 的 diff 與 commit 的身分和訊息，或 push 要送出的全部內容（D-015）。

每個寫入任務都要對應到需求（`REQ-…`）。對應不到需求的新增，會成為 `SCOPE-CREEP` finding。

## 原生能力對照（D-005）

| 需求 | 使用的原生能力 | 本技能包補上的部分 |
| --- | --- | --- |
| 程式審查 | `/code-review`、`/security-review` | finding ID、處置、需求追溯、`SCOPE-CREEP`、正式關卡 |
| 規劃 | plan mode | REQ 錨點、風險等級、task graph |
| 隔離與並行 | worktree、Agent subagent、Workflow | ownership 不重疊檢查、brief 與 receipt 契約 |
| 程式簡化 | `/simplify` | 不另做 |
| 交接 | 原生 session 交接 | checkpoint 格式、偏移檢查 |
| 程式影響範圍 | GitNexus（`impact`、`detect-changes`） | 只查詢，結果只供參考 |

## 驗證

```bash
./scripts/validate.sh
```

這支腳本依序執行：

1. Core 檔案與集合 digest 比對。
2. Core 錨點覆蓋檢查。
3. 技能、agent 與 REQ 的結構檢查。
4. 單元測試，包含 graph 的正反 fixtures。
5. `claude plugin validate`。

需要 Python 3（只用標準庫）與 `claude` CLI。找不到 `claude` CLI 時，第 5 項不會執行，腳本會顯示 INCOMPLETE 並以代碼 2 結束，不會判定為通過。

## 授權

MIT。`vendor/engineering-workflow-core/` 保留原 LICENSE 與上游 notices。

<a id="english"></a>

<details>
<summary>English</summary>

This English text is written per ASD-STE100 principles; full conformance is not verified.

## What it is

A software development skill pack for Claude Code and Cowork. It takes a bounded objective through these steps: requirements, planning, implementation, verification, independent review, docs sync, delivery gates and continuation.

It is modeled on [codex-dev-skills](https://github.com/jeffery777/codex-dev-skills) and [engineering-workflow-core](https://github.com/jeffery777/engineering-workflow-core). It does not operate Codex. The vendored Core v0.1.1 text is the only authority for engineering obligations. `dev-core` is a compact execution digest of it for Claude.

Agents select the skills as needed. People can also invoke one by name, for example `/dev-skills:dev-review`.

Design and decisions: [docs/design-proposal.md](docs/design-proposal.md). This project's own requirements: [docs/requirements/](docs/requirements/index.md).

## Install

The plugin name is `dev-skills`. Claude reserves plugin names that start with `claude-`, so the plugin name differs from the repository name.

Claude Code:

```bash
claude plugin marketplace add jeffery777/claude-dev-skills
```

```bash
claude plugin install dev-skills@dev-skills
```

To test from a local checkout, use `claude plugin marketplace add ./` instead.

Cowork: open Customize > Plugins > Add marketplace, enter `jeffery777/claude-dev-skills`, then install `dev-skills`.

Two things are not yet tested in Cowork: whether skills can run `graph.py` (a shell is required), and whether relative paths from `${CLAUDE_SKILL_DIR}` resolve. If they do not, the skills still work as written procedures.

## Skills

| Skill | Purpose |
| --- | --- |
| `dev-core` | Shared rules. Each rule cites a Core anchor |
| `dev-plan` | Clarify needs and ingest them as REQ files, choose the rigor tier, produce the task graph |
| `dev-implement` | Implement one bounded change, verify it, and check the diff |
| `dev-review` | Dispatch an independent read-only reviewer. Findings have IDs, a requirement relation, severities (including `SCOPE-CREEP` and `REQ-GAP`) and dispositions; decisions for the user use a decision card |
| `dev-gate` | Formal gate before a commit, push, PR or merge. Content, platform and authority are decided separately |
| `dev-docs` | Sync the docs with verified behavior and check that code and docs agree |
| `dev-continue` | Save a checkpoint, evaluate a session handoff when a work item is complete (D-012), and rebuild from repository state when resuming |
| `dev-deliver` | Outer loop: dispatch work from the task graph, integrate it, review it, then run the gates |

Subagents: `dev-explorer` (haiku), `dev-implementer` (sonnet), `dev-reviewer` (opus) and `dev-security-reviewer` (opus). Neither reviewer has the Edit or Write tool. They keep Bash to run tests, so read-only Bash use depends on their instructions; it is not technical isolation.

## Proportionate rigor

- `light`: a low-risk local change, with no graph file. Before a commit, push or PR, it still needs an independent review and the commit gate.
- `standard`: a normal feature. It needs a task graph and an independent reviewer.
- `strict`: security, data, migration, public contract or release work. It needs early deep or security review, the exact-head gate and a human gate.
- Every tier: before every commit and push, `dev-security-reviewer` scans the staged diff and the commit identity and message, or everything the push sends (D-015).

Every write task must trace to a requirement (`REQ-…`). An addition that no requirement covers becomes a `SCOPE-CREEP` finding.

## Native capability map (D-005)

| Need | Native capability used | What this pack adds |
| --- | --- | --- |
| Code review | `/code-review`, `/security-review` | Finding IDs, dispositions, requirement trace, `SCOPE-CREEP`, formal gate |
| Planning | Plan mode | REQ anchors, rigor tier, task graph |
| Isolation and parallel work | Worktrees, Agent subagents, Workflow | Disjoint ownership checks, brief and receipt contracts |
| Code simplification | `/simplify` | Nothing |
| Handoff | Native session handoff | Checkpoint format, drift checks |
| Code impact | GitNexus (`impact`, `detect-changes`) | Queries only; results are advisory |

## Verification

```bash
./scripts/validate.sh
```

The script runs these checks in order:

1. Core file and set digests.
2. Core anchor coverage.
3. Structure of skills, agents and REQ files.
4. Unit tests, including the positive and negative graph fixtures.
5. `claude plugin validate`.

It needs Python 3 (standard library only) and the `claude` CLI. If the `claude` CLI is missing, check 5 does not run: the script prints INCOMPLETE and exits with code 2. It never reports that as a pass.

## License

MIT. `vendor/engineering-workflow-core/` keeps its original LICENSE and upstream notices.

</details>
