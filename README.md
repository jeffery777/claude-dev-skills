# claude-dev-skills

[繁體中文](#zh-tw) · [English](#english)

<a id="zh-tw"></a>

## 這是什麼

給 Claude Code 與 Cowork 使用的軟體開發技能包。它把一項有明確範圍的工作帶過這些步驟：釐清需求、規劃、實作、驗證、獨立審查、文件同步、交付關卡與接續。

它參考了 [codex-dev-skills](https://github.com/jeffery777/codex-dev-skills) 與 [engineering-workflow-core](https://github.com/jeffery777/engineering-workflow-core)，但不操作 Codex。工程義務以 vendor 進來的 Core v0.1.1 原文為唯一權威；`dev-core` 是 vendored Core 與本專案加嚴規則的索引：各 skill 依階段讀 Core 原文。

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

安裝到用戶層級時，pack 檔案在工作目錄之外。每個技能宣告兩條範圍很窄的 Read 規則（CB-7），所以在呼叫技能的那一回合，技能讀自己的 pack 檔案不會跳出權限詢問。之後的回合可能再次詢問：再呼叫一次技能（例如 `/dev-skills:dev-continue`），或同意該詢問。不需要改設定。不要改在設定裡加入範圍更大的 Read 規則。這些行為只在 headless 執行中測過；互動 session 與實際安裝的測試尚待進行（FU-031）。

Cowork：到 Customize > Plugins > Add marketplace，輸入 `jeffery777/claude-dev-skills`，再安裝 `dev-skills`。

Cowork 有三項尚未實測：技能能否執行 `graph.py`（需要 shell）、`${CLAUDE_SKILL_DIR}` 的相對路徑能否解析，以及使用 `${CLAUDE_PLUGIN_ROOT}` 的 `allowed-tools` 規則能否生效（FU-001）。沒有 shell 時，技能依文件手動操作。路徑無法解析時，技能會停下並回報，不會改讀工作目錄裡的同名檔案，也不會在沒有規則的情況下繼續（CB-6）。

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
| `dev-retro` | 教訓：`/dev-skills:dev-retro capture` 把使用者指定的問題寫成分層級（L1–L4）的教訓草稿與決策卡片；`/dev-skills:dev-retro review` 派唯讀 reviewer 審查有新證據的教訓及其指向的規則。只能由使用者呼叫，不寫檔（skill 規則；`disable-model-invocation` 只擋 Skill tool 呼叫，不是技術保證）；只支援 Claude Code |

Subagents：`dev-explorer`（haiku）、`dev-implementer`（sonnet）、`dev-reviewer`（opus），以及 `dev-security-reviewer`（opus）。兩個 reviewer 沒有 Edit 和 Write 工具，但保留 Bash 以便跑測試；Bash 的唯讀使用靠指示約束，不是技術隔離。

## 適度嚴謹

- `light`：低風險的局部修改，不建 graph 檔。若要 commit、push 或開 PR，仍須先經獨立 review 與 commit gate。
- `standard`：一般功能。要有 task graph 和獨立 reviewer。
- `strict`：涉及安全、資料、migration、對外契約或 release。要初期就做深入或安全審查，並通過 exact-head 關卡與 human gate。
- 所有等級：每次 commit 與 push 之前，由 `dev-security-reviewer` 掃描已 stage 的 diff 與 commit 的身分和訊息，或 push 要送出的全部內容（D-015；R-REV-9 列出掃描不涵蓋的情況）。

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
3. 技能、agent 與 REQ 的結構檢查，也檢查 plugin 的封閉清單（closed world）：根目錄與 `.claude-plugin/` 只能有清單上的名稱，所以根目錄的本機檔案（例如 `.DS_Store`）也會讓檢查失敗；`skills/` 只能放含 `SKILL.md` 的非隱藏技能目錄，`agents/` 只能放非隱藏的 `*.md` 檔案。錯誤訊息會說明兩種原因：新的 plugin 元件需要修改 `check_pack.py` 並經過審查；`.DS_Store` 這類本機檔案則應移除。
4. 單元測試，包含 graph 的正反 fixtures。
5. `claude plugin validate`。

需要 Python 3（只用標準庫）與 `claude` CLI。找不到 `claude` CLI 時，第 5 項不會執行，腳本會顯示 INCOMPLETE 並以代碼 2 結束，不會判定為通過。

### CI

`.github/workflows/ci.yml` 在送往 `main` 的每個 pull request 與每次 push 到 `main` 時執行兩個 job（D-017）：

- `validate`：安裝固定版本的 Claude CLI（不登入），執行 `scripts/validate.sh`。
- `gitleaks`：下載固定版本的 gitleaks，先核對 SHA-256，再掃描從 checkout 的 commit 可到達的每個 commit。輸出會遮蔽 secret。

限制：gitleaks 不掃 merge commit 本身的 patch，也不讀 commit 身分、訊息與 PR 文字。PR 可以修改 workflow、`.gitleaks.toml`、`.gitleaksignore`，進而改變掃描內容，所以 review 要檢查這類變更。CI 在 push 之後才執行：CI 找到的值已經公開，必須更換（rotate）。

Workflow 只有 `contents: read` 權限，不用任何 secret；每個 action 都用完整 commit SHA 固定。CI 不取代每次 commit 與 push 前的獨立安全審查（D-015）。

把兩個 check 設成必要檢查（由維護者在 GitHub 上設定）：

1. 先讓 CI 在 `main` 或某個 PR 上至少跑完一次，GitHub 才列得出 check 名稱。
2. 開啟 repo 的 Settings → Rules → Rulesets → New ruleset → New branch ruleset。
3. Ruleset name 填 `main`，Enforcement status 選 Active。Bypass list 保持空白，規則也適用於維護者自己。
4. Target branches → Add target → Include default branch。
5. 勾選 Require status checks to pass，按 Add checks，加入 `validate` 與 `gitleaks`（來源 GitHub Actions）。
6. 按 Create。之後 `main` 只接受通過這兩個 check 的變更，所以變更要經由 PR 合併。通過的 check 只證明它實際檢查到的內容（見上面的限制）。
7. 讀回確認：`gh api repos/<owner>/<repo>/rules/branches/main` 的輸出要有 `required_status_checks`，並列出這兩個 check。
8. 專案用 `.dev/config.json` 的 `platform_profile` 選定平台設定（provider profile，REQ-021）。`dev-gate` 只從 PR 的 base commit 讀這個設定，並在 merge gate 讀回 GitHub 上的必要檢查：只有 `success` 算通過；結果是 `VERIFIED`、`UNVERIFIED` 或 `BLOCKED`。沒有這個設定時結果是 `NOT_CONFIGURED`；但讀不到 PR，或 PR 的 base 或 head 不是受審的版本時，結果是 `UNVERIFIED`。格式與限制見 `skills/dev-gate/references/platform-profile.md`。這個 repo 的設定列出 `validate` 與 `gitleaks`（GitHub Actions，app 15368）。GitHub 用 PR 自己的 workflow 跑 check，所以 `VERIFIED` 一律標註「checks ran this PR's own definitions」，gate 也會列出 PR 改到的 check 相關檔案（FU-008，只回報、不阻擋）。

## 授權

MIT。`vendor/engineering-workflow-core/` 保留原 LICENSE 與上游 notices。

<a id="english"></a>

<details>
<summary>English</summary>

This English text is written per ASD-STE100 principles; full conformance is not verified.

## What it is

A software development skill pack for Claude Code and Cowork. It takes a bounded objective through these steps: requirements, planning, implementation, verification, independent review, docs sync, delivery gates and continuation.

It is modeled on [codex-dev-skills](https://github.com/jeffery777/codex-dev-skills) and [engineering-workflow-core](https://github.com/jeffery777/engineering-workflow-core). It does not operate Codex. The vendored Core v0.1.1 text is the only authority for engineering obligations. `dev-core` is the index of the vendored Core and the project's tightenings: each skill reads the original Core text for its stage.

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

In a user-level install, the pack files are outside the working directory. Each skill declares two narrow Read rules for them (CB-7), so in the turn that invokes a skill, the skills read their pack files without a permission prompt. A later turn can prompt again: invoke a skill again (for example `/dev-skills:dev-continue`) or approve the prompt. No settings change is needed. Do not add a broad Read rule to your settings instead. This was tested in headless runs only; tests in interactive sessions and with a real install are pending (FU-031).

Cowork: open Customize > Plugins > Add marketplace, enter `jeffery777/claude-dev-skills`, then install `dev-skills`.

Three things are not yet tested in Cowork: whether skills can run `graph.py` (a shell is required), whether relative paths from `${CLAUDE_SKILL_DIR}` resolve, and whether the `allowed-tools` rules with `${CLAUDE_PLUGIN_ROOT}` work (FU-001). Without a shell, the skills use the written procedures. When a path does not resolve, a skill stops and reports it; it does not read a file with the same name from the working directory and does not continue without the rules (CB-6).

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
| `dev-retro` | Lessons: `/dev-skills:dev-retro capture` turns a problem that the user names into a lesson draft with a level (L1 to L4) and a decision card; `/dev-skills:dev-retro review` dispatches the read-only reviewer to review the lessons with new evidence and the rules that they point to. Only the user invokes it; it writes no file (skill rule; `disable-model-invocation` blocks only the Skill tool call; not a technical guarantee); it supports only Claude Code |

Subagents: `dev-explorer` (haiku), `dev-implementer` (sonnet), `dev-reviewer` (opus) and `dev-security-reviewer` (opus). Neither reviewer has the Edit or Write tool. They keep Bash to run tests, so read-only Bash use depends on their instructions; it is not technical isolation.

## Proportionate rigor

- `light`: a low-risk local change, with no graph file. Before a commit, push or PR, it still needs an independent review and the commit gate.
- `standard`: a normal feature. It needs a task graph and an independent reviewer.
- `strict`: security, data, migration, public contract or release work. It needs early deep or security review, the exact-head gate and a human gate.
- Every tier: before every commit and push, `dev-security-reviewer` scans the staged diff and the commit identity and message, or everything the push sends (D-015; R-REV-9 lists what the scans do not cover).

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
3. Structure of skills, agents and REQ files, and the plugin's closed-world layout: the root and `.claude-plugin/` may hold only the listed names, so a local file at the root such as `.DS_Store` makes the check fail; `skills/` may hold only non-hidden skill directories with a `SKILL.md`, and `agents/` only non-hidden `*.md` files. The error names both causes: a new plugin component needs a change of `check_pack.py` with review; a local file such as `.DS_Store` must be removed.
4. Unit tests, including the positive and negative graph fixtures.
5. `claude plugin validate`.

It needs Python 3 (standard library only) and the `claude` CLI. If the `claude` CLI is missing, check 5 does not run: the script prints INCOMPLETE and exits with code 2. It never reports that as a pass.

### CI

`.github/workflows/ci.yml` runs two jobs on every pull request to `main` and every push to `main` (D-017):

- `validate`: installs the Claude CLI at an exact version (no login) and runs `scripts/validate.sh`.
- `gitleaks`: downloads an exact gitleaks version, checks its SHA-256, and scans every commit reachable from the checked-out commit. The output redacts secrets.

Limits: gitleaks does not scan the patch of a merge commit, and it does not read the commit identity, the message or PR text. A PR can change the workflow, `.gitleaks.toml` or `.gitleaksignore` and so change what is scanned, so the review must examine such changes. CI runs after the push: a value that CI finds is already public and must be rotated.

The workflow has only the `contents: read` permission and uses no secrets; every action is pinned by full commit SHA. CI does not replace the independent security review before every commit and push (D-015).

To make the two checks required (the maintainer does this on GitHub):

1. Let CI finish at least once on `main` or on a PR, so that GitHub can list the check names.
2. Open the repository's Settings → Rules → Rulesets → New ruleset → New branch ruleset.
3. Set Ruleset name to `main` and Enforcement status to Active. Keep the bypass list empty, so the rules also apply to the maintainer.
4. Target branches → Add target → Include default branch.
5. Select Require status checks to pass, click Add checks, and add `validate` and `gitleaks` (source GitHub Actions).
6. Click Create. From then on `main` accepts only changes that passed both checks, so changes go in through PRs. A passed check proves only what it actually examined (see the limits above).
7. Read it back: the output of `gh api repos/<owner>/<repo>/rules/branches/main` must contain `required_status_checks` with both checks.
8. A project selects a provider profile with `platform_profile` in `.dev/config.json` (REQ-021). `dev-gate` reads this setting only from the PR's base commit and, at the merge gate, reads the required checks back from GitHub: only `success` passes, and the result is `VERIFIED`, `UNVERIFIED` or `BLOCKED`. Without the setting the result is `NOT_CONFIGURED`, but `UNVERIFIED` when the PR read fails or shows another base or head than the reviewed one. The format and the limits are in `skills/dev-gate/references/platform-profile.md`. This repository's setting lists `validate` and `gitleaks` (GitHub Actions, app 15368). GitHub runs the checks from the PR's own workflow, so `VERIFIED` always says "checks ran this PR's own definitions", and the gate lists the check-related files that the PR changed (FU-008, report only, no block).

## License

MIT. `vendor/engineering-workflow-core/` keeps its original LICENSE and upstream notices.

</details>
