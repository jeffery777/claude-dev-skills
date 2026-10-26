# claude-dev-skills 設計文件 v1

[繁體中文](#zh-tw) · [English](#english)

<a id="zh-tw"></a>

狀態：定稿（2026-10-20）。決策見第 7 節。英文版在文末，與中文版同義；兩者不一致時以中文版為準。

## 1. 參考來源讀到了什麼

| 來源 | 核心價值 | 不直接搬過來的部分 |
| --- | --- | --- |
| `engineering-workflow-core` | 四份純 Markdown 契約：工作流階段（Discover → Plan → Implement → Verify → Review&Fix → Docs Sync → Delivery Gate → Continue）、授權與停止條件、獨立審查與安全掃描、exact-head 與證據 | 長篇法條式寫法；codex 版的 Core snapshot 組裝器與 installer（pin 本身保留，見 D-001） |
| `codex-dev-skills` | 27 個技能；分成 primitive（plan / implement / review）與 formal gate；loop ledger（spec + manifest + 事件 + 物化狀態）；子代理 class/tier 路由；context continuity；確定性 evals | Codex 專屬 runtime 適配（Desktop sidebar、CLI session handoff、TOML profiles）、約 27k 行 Python、installer、memory M0/M1、GitNexus adapter |

Graph engineering 在原專案的定位（ADR OE-007）：
- 第一步只做「typed graph projection」。把 loop、task、evidence 投影成有型別的 node/edge 清單。
- 不做 graph DB，也不做執行引擎。投影只供參考，不能拿來授權或證明完成。
- 目前真正實作的圖邏輯只有一條：task manifest 的 `dependencies`。所有依賴都 done 之後，task 才能變成 `ready`。

## 2. 設計原則（Claude 版）

1. **Core 是唯一權威；dev-core 是精簡的執行版。**（「精簡的執行版」由 D-020 取代：`dev-core` 是 Core 與本專案加嚴規則的索引，各 skill 依階段讀 Core 原文。）Core 的義務全部保留：DoD、獨立 review、finding disposition、exact-head、授權與停止條件、證據生命週期。日常執行讀 dev-core，它是 Claude 一次讀得完的短規則加檢查清單。精簡的目的是減少重複載入，以及長文造成的注意力分散。實際的 context 成本還沒有量測；D-011 會量測，並和 codex-dev-skills 比較。兩者衝突時以 Core 原文為準（見第 7 節）。
2. **優先用 Claude Code 原生能力，不重造控制器。** 原生能力包括：subagent（Agent tool）、worktree isolation、plan mode、task list、hooks、`/code-review`、`/security-review`、Workflow 多代理編排、skills progressive disclosure。
3. **能用設定強制的，就不靠提示詞。** Codex 版只能宣告 reviewer 是唯讀；Claude Code 的 subagent 可以用 `tools` allowlist 拿掉 Edit/Write。reviewer 仍保留 Bash 以便跑測試，所以 Bash 的唯讀使用仍靠指示約束；這不等於技術隔離（Core `review-independent`）。
4. **狀態存在 repo 檔案和 Git。** 聊天摘要、子代理回報、hook 輸出都只是協調資訊，不能當完成證據。
5. **Graph 分階段做。** 先有可驗證的 task graph 檔案，再做投影與視覺化，最後才讓圖驅動並行執行。

## 3. 打包與執行環境

- 以 **Claude Code plugin** 發佈：`.claude-plugin/plugin.json` 加 marketplace。內容包括 `skills/`、`agents/`、`hooks/`（選用）。
- 同一份 skills 要能在 **Cowork** 使用。所以技能本體不能依賴 CLI 專屬工具；遇到 CLI 專屬能力時要標示，並提供 fallback。
- 腳本盡量只用 Python 標準庫（或 Node），避免 PyYAML 這類安裝依賴。graph 檔案用 JSON，或 YAML 子集。

## 4. Phase 1 技能組（MVP）

| 技能 | 對應 Codex 技能 | 用途 |
| --- | --- | --- |
| `dev-core` | engineering-workflow-core 契約 | （由 D-020 取代：現在是 Core 與本專案加嚴規則的索引。）Core 的精簡執行版，涵蓋階段、DoD、風險分級、授權與停止、finding 格式、證據規則。其他技能引用它，它不單獨觸發；它不是權威，權威是 vendor 的 Core |
| `dev-plan` | planning, closure-triage | 釐清目標與 scope、DoD、風險、切片，產出 task graph |
| `dev-implement` | implementation-slice | 單一有界修改：讀、改、驗證、自查 diff |
| `dev-review` | code-review(-deep), docs-review | 派**獨立的唯讀 reviewer subagent**，依風險選一般／深入／安全審查；finding 帶穩定 ID |
| `dev-gate` | *-gate, merge-review, merge-readiness-gate | 正式關卡：exact-head base/head 綁定、disposition 完整性。content、platform、授權三者分開判定 |
| `dev-docs` | docs-update | 依已驗證行為同步文件，檢查 code 和 docs 是否一致 |
| `dev-continue` | task-continuation, milestone-continuation | checkpoint、交接、接續（從 repo 狀態重建，不信聊天記憶） |
| `dev-deliver` | project-delivery, project-orchestrator | 外層編排：依 graph 選下一步、派工、整合、跑 gate，碰到人類關卡就停 |

Phase 1 之後新增的技能（不屬於 D-008 的 Phase 1 範圍）：

| 技能 | 對應 Codex 技能 | 用途 |
| --- | --- | --- |
| `dev-retro`（D-019 新增；PR-2 實作） | —（見 D-019） | 教訓：`capture` 分層級（L1–L4）並產出教訓草稿與卡片；`review` 審查有新證據的教訓及其指向的規則。只能由使用者呼叫，不寫檔（skill 規則；`disable-model-invocation` 只擋 Skill tool 呼叫，不是技術保證；見 D-019）；只支援 Claude Code |

### Subagents（`agents/`）

| Agent | 預設模型 | 預設思考深度 | 工具 | 角色 |
| --- | --- | --- | --- | --- |
| `dev-explorer` | haiku | low | 只有讀取工具與 Bash（唯讀靠指示） | 大範圍查讀，只回結論 |
| `dev-implementer` | sonnet | medium | 可寫，建議 worktree | 有界實作。不 commit、不 push，回傳一份結構化 receipt |
| `dev-reviewer` | opus | high | 沒有 Edit/Write；保留 Bash（唯讀靠指示） | 一般與深入 review |
| `dev-security-reviewer` | opus | xhigh | 沒有 Edit/Write；保留 Bash（唯讀靠指示） | 涉及信任邊界、權限、資料、依賴的變更；以及每次 commit、push 與貼出 PR 或 Issue 文字前的掃描（D-015） |

共用 brief 契約：目標、ownership（路徑）、DoD、驗證、升級條件，加上一份最終 receipt。子代理沒有外部寫入權；主代理負責整合與驗收。

#### 模型與思考深度的選擇（見 D-007）

設定分兩層：

1. **預設值**：寫在 `agents/*.md` 的 frontmatter（`model`、`effort`、`tools`），也就是上表的預設欄位。
2. **逐次覆寫**：`dev-deliver` 和 `dev-review` 派工前，依下表選定 `model` 和 `effort`，兩者都要傳；只傳 model 時，effort 會沿用 agent 檔的預設值。brief 寫明選擇的理由（R-DEL-2，FU-018）。

| 任務類型 | 模型 | 思考深度 |
| --- | --- | --- |
| 機械查讀、找檔案 | haiku | low |
| 一般探索、摘要 | sonnet | medium |
| 實作（`light`） | sonnet；跨模組或不明確的 slice 用 opus | medium；opus 時 high |
| 實作（`standard`） | opus；單一模組內機械、範圍明確的 slice 用 sonnet | high；sonnet 時 medium |
| 實作（`strict`，或適用 R-DEL-2 下限時） | opus | high |
| 一般 review | opus | high |
| 深入 review、高風險設計、commit／push 掃描 | opus | xhigh |
| 安全 review | opus | xhigh；使用者要求時才用 max |

主 session 自己實作時，plan 記錄它 transcript 上的 model 與 effort，讀不到時寫 `unknown` 和原因。主代理不改自己的 model 與 effort，由使用者在 app 設定。屬於下限範圍的工作，主 session 的 model 不是 opus、effort 低於 high，或其中之一是 `unknown` 時，主代理在實作前請使用者切換到 opus/high，或用 opus/high 把實作派給 `dev-implementer`；其他工作低於上表時，plan 要寫明。一輪 review 與修正沒有解決問題時，先分類失敗原因。spec、驗收條件或設計造成的失敗不算 quality：它走 R-VER-2 的停止規則和重新評估，不升級。只有 quality 類失敗才升級，而且只升修正的一方（implementer 或主 session），reviewer 照上表：先升 effort（low → medium → high），到 high 以上改升 model（haiku → sonnet → opus），到 opus 再升 effort（xhigh，然後 max）。升級後的設定在該節點剩下的工作中不降回。任何設定都不低於下限。升級不重設 review 輪數，也不清除 findings。證據互相矛盾時（例如兩份 review 對同一變更的結論相反），也重新評估 model 和 effort；重新評估本身不會升級。Fable 評估前不列入升級順序（D-007 規則 4；FU-018 卡 2 選 c，評估延後，由 FU-020 追蹤）。

## 5. Graph Engineering

### 5.1 這個詞指什麼

「Graph engineering」目前是社群用語，不是 Anthropic 或 Karpathy 的官方術語。這個詞主要來自一份獨立整理，內容串起三個官方來源：Karpathy 的 autoresearch loop 與 AgentHub 構想、Anthropic 的 Claude Code Dynamic Workflows，以及 Knowledge Graph Construction Cookbook。

整理後可以歸納成三層圖：

| 層 | 意思 | 在本專案的對應 |
| --- | --- | --- |
| **執行圖** | 一次工作拆成 node（有輸入／輸出契約的有界工作）和 edge（真的有資料流過的依賴）。沒有依賴的 node 就並行；典型形狀是 fan-out → reduce → verify → synthesize | Task graph（G0），交給 Claude Code 原生的 Agent／Workflow 執行。**不自己寫執行引擎** |
| **記憶／知識圖** | 跨 session 保存、有出處的 typed 紀錄。之後的 agent 只查相關的子圖，不必整包重讀 | 兩張圖：**程式圖用 GitNexus**（已安裝 1.6.12），**需求圖用 LLM Wiki 格式**（見 D-003） |
| **治理圖** | 由 loop 監督 loop：verifier node 在乾淨的 context 裡嘗試推翻結論；每個回圈都有輪數上限 | 獨立 reviewer node、gate node、human gate node |

### 5.2 階段

| 階段 | 交付物 | 「完成」的判準 |
| --- | --- | --- |
| **G0 Task graph + 需求錨點** | `.dev/<objective>/graph.json`：task node 帶 `requirements: [REQ-…]`、ownership paths、DoD、verification、review mode、risk；edge 用 `depends_on` 表示。另有 append-only 的 `events.jsonl`。`graph.py`（只用標準庫）負責驗證 schema、偵測循環、計算 ready set、檢查 ownership 是否重疊、執行 fake-edge 檢查，並追溯需求（找出沒對應到任何 REQ 的 task）。Phase 1 也已提供：GitNexus 唯讀查詢（`impact`／`detect-changes`，結果只供參考）與 `SCOPE-CREEP` finding（REQ-003、REQ-004） | `dev-plan` 能產出 graph；`dev-deliver` 依 ready set 逐一推進（單一 writer）；validator 有正反兩面的 fixtures |
| **G1 程式圖與需求圖整合** | 把需求圖、task graph 與 GitNexus 符號接起來：`graph.py render` 輸出 Mermaid 追溯圖（來源 → REQ → task，之後再接 GitNexus 符號）；review 依追溯圖系統化地檢查 scope 是否偏移 | review 能指出「這段改動對應哪條需求」和「影響了哪些符號」 |
| **G2 圖驅動並行** | 把 ready set 中 ownership 互不重疊的 task 編成 Workflow 腳本或並行的 Agent 呼叫，搭配 worktree 隔離；reducer 用程式碼做；每個 fan-out 後接 verifier node | 有界並行能跑通；不會有兩個 writer 改同一個檔案；派出與收回的數量對得上 |
| **G3 Evidence projection 與自我改進** | 驗證、review、finding、commit 也成為 typed node；互動式 HTML 視圖（可發佈為 Artifact），包含 finding 與 commit 節點；evals 與改善提案（只產出提案） | 暫定（G3 開工前依 G0–G2 的實際使用結果修正）：驗證、review、finding、commit 的 typed node 能從 Git 與 review 紀錄重新產生；HTML 視圖能從這些資料重新產生，而且不回寫成來源；evals 產出的改善提案只交給使用者決定，不自動套用 |

以下規則來自 D-009：

- G1、G2、G3 各自是一輪獨立交付：Issue → 分支 → review 與掃描 → PR → Merge Review。前一階段合併後，下一階段才開始。
- 每個階段開工前，先依前一階段的實際使用結果，修正上表該階段的交付物與完成判準。
- 每個階段的產出分屬兩層：
  - **runtime 中立層**：graph 與 REQ 的 schema、`graph.py`、fixtures。這一層不得依賴 Claude 專用工具，讓 Codex 和 Grok 也能使用。
  - **Claude 專用層**：用 Agent 與 Workflow 執行的方式。這一層供日後 Codex、Grok 參考，或提回 Core。
- 依目前的設計，各階段的分層如下；每個階段開工前一併修正：
  - G1：`graph.py render` 與追溯資料屬中立層；review 如何使用追溯圖屬 Claude 專用層。
  - G2：ready set 與 ownership 檢查屬中立層；Workflow 腳本、並行的 Agent 呼叫與 worktree 隔離屬 Claude 專用層。
  - G3：evidence node 的 schema 屬中立層；HTML 視圖與 Artifact 屬 Claude 專用層。

每個 graph 檔案都只是協調資料，不能當完成證據。完成仍以 Git、驗證結果、獨立 review 為準（Core `exact-head-and-evidence.md`）。

**所有圖形呈現都只是投影，不是權威**（同 codex-dev-skills OE-003）。包括 Mermaid 追溯圖、HTML 視圖、Artifact 與 Obsidian graph view。這些投影都從 REQ 檔、`graph.json` 與 Git 重新產生，不能拿來授權、證明完成，或回寫成來源。

## 6. 刻意不做（Phase 1）

- 不做 installer：改用 plugin marketplace。
- 不做 model/effort 路由引擎或完整矩陣：只用第 4 節那張對照表，由主代理依任務挑選（D-007）。
- 不做 memory backend，也不做記憶契約：專案狀態以 repo 為準；原生 memory 只當參考（D-010）。
- 不做事件 hash chain 和 fencing token：先靠 Git 歷史加單一 writer；G2 需要並行時再評估。`graph.py transition` 以檔案鎖序列化寫入。
- 不做並行 writer：`dev-deliver` 依序執行 ready 的 task；只有唯讀的 task（探索、review）可以並行。並行 writer 與 worktree 整合屬 G2。
- 不做 Desktop／CLI session 控制適配：直接使用原生 session 和 worktree 能力。
- D-019（`dev-retro`，Phase 1 之後的新範圍）不做：教訓 ledger 或教訓檔、使用者層級的教訓檔、hooks、排程、模型自動呼叫 `dev-retro`、檢查教訓的 validator。

## 7. 決策紀錄

### D-001 與 engineering-workflow-core 的關係：vendor 原文並 pin，另加精簡執行版（已決定，2026-10-20）

**背景**

- Core 寫成嚴格的法條式，是為了防止 Codex 跑偏。
- 使用者希望三個接口（Codex、Grok、Claude）都遵循同一份權威。
- 如果 Claude 版的精簡寫法效果好，希望能回饋給 Core。

**決定：三層結構**

| 層 | 內容 | 地位 |
| --- | --- | --- |
| Core（vendor + pin） | `vendor/engineering-workflow-core/` 放原文，並鎖定 immutable revision 與 digest | **唯一權威**；有衝突時以它為準 |
| `dev-core` | Claude 執行用的精簡規則；每條規則都對應到 Core 的錨點，例如 `workflow.md#wf-stages` | 執行用的摘要。只能改寫、壓縮或加嚴，不能放寬、刪除義務，也不能自行建立新的權限 |
| source-map 與覆蓋檢查 | `skills/dev-core/source-map.md`，加一支腳本 | 腳本檢查每個 Core 錨點都有對應規則，或有寫明理由的「不適用」；有漏掉就驗證失敗 |

- 日常執行只載入 `dev-core`，以節省 context。（由 D-020 取代，PR-2 起生效：各 skill 依階段讀 vendored Core 原檔；`dev-core` 保留比 Core 嚴格或 Claude 專屬的規則並作為索引。）
- 遇到邊界情況、有疑義或規則衝突時，回頭讀 vendor 的 Core 原文。

**為什麼 Codex 不會因此受影響**

- Codex 不追 Core 的 `main`，用的是它 pin 住的 revision。
- Core 合併任何修改，都要等 codex-dev-skills 自己重新 pin、跑過它的 evals 之後才會生效。
- 換句話說，防止跑偏靠的是各接口的採用流程，不需要凍結 Core。

**回饋給 Core 的流程**

1. `dev-core` 跟 Core 原文不同的地方，逐條記成 delta。每條 delta 註明類型（改寫、壓縮或加嚴）和理由。
2. 在 Claude 實際使用中累積證據，例如漏掉步驟、誤判完成、context 成本的變化。
3. 效果確認後，到 Core 開 issue。提案分兩種：
   - **增量型（優先）**：在 Core 新增一份非權威的精簡伴讀文件，權威原文不動。Codex 和 Grok 可以不採用。
   - **修改型**：改動權威原文。必須先讓 codex-dev-skills 和 grok-build-dev-skills 各自 pin 候選版本並跑過 evals，確認沒有退化才合併。
4. Core 合併不代表 Codex 或 Grok 已採用。各接口什麼時候重新 pin，由各接口自己決定、自己驗證。
5. 回饋項目與證據記錄在 `docs/core-feedback.md`（REQ-019）。

**本專案這次的範圍**

- 不修改 engineering-workflow-core。
- 不修改 codex-dev-skills 或 grok-build-dev-skills。

### D-002 語言（已決定，2026-10-20）

- SKILL.md 與 agents 用英文寫。
- README 與設計文件用中英雙語，因為技能主要由 agent 依需求調用，但也保留讓人手動調用。
- 英文版附在本文件末尾。

### D-003 需求圖：LLM Wiki 格式為來源，Graphify 列為選用的索引（已決定，2026-10-20）

**問題**：Codex 開發時有時會過度工程化，把原始專案需求改寫成通用需求。

**決定**

- 需求的唯一來源，是 repo 內的 `docs/requirements/` Markdown wiki，遵循 Karpathy LLM Wiki 的原則：
  - 每條需求有穩定 ID（`REQ-001`），寫在 frontmatter 裡：`status`、`sources`、`non_goals`。
  - 本文可以用 `[[wiki link]]` 方便閱讀；需求之間的正式關係寫在 typed 關係欄位（見本節最後一項）。
  - 附一份 `index.md`，以及一份 `log.md` 記錄需求的變更。
  - Agent 的操作只有三種：ingest（把新需求寫進來）、query（查需求）、lint（找出矛盾、孤兒需求、過期需求）。
- **出處要精確到能定位**：
  - frontmatter 的 `sources` 是一個清單。每筆都有 `type`、`locator`、`quote` 三欄。
  - `type` 是 `doc`、`chat`、`issue`、`commit` 其中之一；連回 Jira、Confluence、PRD 等正式需求系統時用 `external`。
  - `locator` 寫到能找回原處的程度：檔名加頁碼或章節錨點、日期、URL、commit SHA。
  - `quote` 是逐字原文。
  - 模型自己整理的敘述放在本文的 `Need` 段，和原文分開存放，不混寫。
- **來源衝突時兩邊並列**：
  - 來源互相矛盾時，雙方說法連同出處都保留，`status` 設為 `conflict`，交給使用者決定。
  - Agent 不得自行挑選一方，也不得覆寫。
  - 引用 `conflict` 需求、且尚未完成的寫入 task，`graph.py` 會判定失敗。
- **被取代的結論不刪除**：
  - `status` 改為 `superseded`，並填寫 `superseded_by` 與 `superseded_reason`。
  - 每次變更都記入 `log.md`。
- **wiki 建在哪裡、何時建**：
  - wiki 由 `dev-plan` 建在各目標專案內。第一次建立前，先徵求使用者同意。
  - 預設路徑是 `docs/requirements/`。可以在專案的 `.dev/config.json` 用 `requirements_dir` 改成別的路徑。
- **專案已有正式需求系統時**（例如 Jira、Confluence、PRD）：
  - wiki 只當索引，每筆連回原處。
  - 機密原文不得離開該專案：不複製到其他 repo、記憶或對外服務。
  - 不確定是否機密時，只記 `locator`，不抄錄原文。
- 選這個做法的原因：
  - 純 Markdown 加 Git，Codex、Grok Build、Claude 都能直接讀，不需要安裝任何工具。
  - Obsidian 只當閱讀器，可裝可不裝。
  - 結果是確定的，不需要 LLM 抽取，也不會產生額外費用。
- Graphify（Python，tree-sitter 加 LLM 語意抽取）列為**選用的索引層**，不當權威：
  - 它的程式 AST 圖跟 GitNexus 重疊。
  - 它抽取文件時需要 LLM，結果不是確定的。
  - 等需求數量多到純 wiki 查詢不夠用時，再接進來索引 `docs/requirements/`。
- **防止過度工程化的機制**：
  - 每個 task node 都要寫 `requirements: [REQ-…]`。
  - `graph.py` 會標出沒有對應需求的 task。
  - `dev-review` 有一類 finding 叫 `SCOPE-CREEP`：對應不到需求的新增抽象、設定、fallback、validator 都歸這類。處置方式沿用 Core 的 disposition。
  - 這呼應 Core `wf-assumptions-and-options` 的要求：新增實質複雜度前，要說明它的獨特作用。
- **REQ 之間的 typed 關係**（Phase 1）：
  - frontmatter 有四個關係欄位：`depends_on`、`refines`、`conflicts_with`、`superseded_by`。值都是 REQ ID 清單。
  - `graph.py validate` 檢查這些 ID 確實存在，並檢查 `depends_on` 沒有循環。
  - Obsidian 的 graph view 可以選用來瀏覽，但它的連結沒有型別，只能當輔助閱讀，不能取代這些欄位。

### D-004 適度嚴謹：依風險分級（已決定，2026-10-20）

| 等級 | 何時用 | 要做的事 |
| --- | --- | --- |
| `light` | 低風險、局部修改 | 簡短計畫、針對性測試、自查 diff，不建 graph 檔。若要 commit、push 或開 PR，仍須先經獨立 review 與 commit gate |
| `standard` | 一般功能 | 建 graph、派一個獨立 reviewer、finding disposition、同步文件 |
| `strict` | 涉及安全、資料、migration、對外契約、release | 初期就做深入／安全審查、exact-head gate，加上 human gate |

- 分級只決定流程要多重，不能降低 Core 的義務。例如判斷不出風險時，不能歸成低風險；review 一律要獨立進行。
- 判定分級的理由要寫在計畫裡。
- `light` 的工作若要 commit、push 或開 PR，必須先經過獨立 review 與 `dev-gate` commit gate；兩者缺一就停在該動作之前。沒有 commit 的 light 修改，在剩餘風險中註明「未經獨立審查」（`dev-core` R-RIG-2）。

### D-005 原生能力優先（已決定，2026-10-20）

下列工作直接使用 Claude Code 的原生能力，技能只補上 Core 要求、原生能力沒提供的部分（finding ID、disposition、需求追溯、gate 判定），並在文件中記錄這個對應關係：

- Review 與安全審查：`/code-review`、`/security-review`
- 程式簡化：`/simplify`
- 規劃：plan mode
- 隔離與多代理：worktree、Agent subagent、Workflow 多代理編排
- 交接：session handoff

### D-006 GitNexus 整合方式（已決定，2026-10-20）

- 只透過它的 CLI 或 MCP（`impact`、`detect-changes`、`context`）**查詢**。
- 結果只供參考：index 有過期或 dirty 狀態時，在報告中標明。
- 不由本專案安裝、設定或更新 GitNexus，也不修改它的 hooks。

### D-007 Subagent 的模型與思考深度依任務挑選（已決定，2026-10-20）

**決定**

- Subagent 一律使用 Claude Code 官方模型。
- 每個角色在 `agents/*.md` 設定預設的 `model` 與 `effort`；派工時由主代理依第 4 節的對照表逐次覆寫。

**挑選依據**（對齊 Core `workflow.md#wf-delegation`）

- 依推理需求、風險、context 量與驗證負擔挑選。
- 預設值足夠時就沿用，不固定使用最高思考深度。
- 不用「深入思考」之類的提示詞取代實際的 `effort` 設定。

**規則**

1. **用別名，不寫死模型 ID。** 寫 `haiku`、`sonnet`、`opus`、`fable`，不寫 `claude-opus-5-5` 這類完整 ID。新模型推出時不必改技能；這也符合 Core「不固定永久模型 ID」的要求。
2. **高風險不降級。** 涉及安全、資料、migration、對外契約的任務，最低使用 opus／high。不能為了成本或速度降低這個下限（沿用 codex 版 routing 的「風險觸發不可抵銷」）。
3. **重評時機。** 一輪修正沒有解決問題，或證據互相矛盾時，主代理重新評估模型與深度。環境或權限造成的失敗，不能靠提高深度解決（Core `wf-verification`）。
4. **Fable 暫不列入預設。** 它的定位與成本尚未實測，目前只列為可選；評估後再決定是否納入對照表。

**限制**

- 主代理只能確定自己「要求」的模型與深度。subagent 實際有沒有照這個設定執行，在對話中無法完全讀回。
- 因此 receipt 記錄要求的設定，以及 transcript 記錄的 model 與 effort（FU-018；只抄這兩個值），不宣稱已驗證生效；讀不回來的部分和實際生效的設定都標為 `unknown`。

### D-008 Phase 1 範圍（已決定，2026-10-20）

| 項目 | 內容 | 驗收 |
| --- | --- | --- |
| Core vendor | `vendor/engineering-workflow-core/`（v0.1.1，14 檔）加 `vendor/engineering-workflow-core.lock.json` | `scripts/verify_core.py` 比對每個檔案和集合的 digest；13 份 Markdown 的集合 digest 與 codex-dev-skills 的 lock 相同 |
| 8 個技能 | 第 4 節表中的 `dev-core`、`dev-plan`、`dev-implement`、`dev-review`、`dev-gate`、`dev-docs`、`dev-continue`、`dev-deliver` | 符合 frontmatter 規則；`dev-core` 的每條規則都對應到 Core 錨點 |
| source-map、delta、覆蓋檢查 | `skills/dev-core/source-map.md`、`skills/dev-core/deltas.md`、`scripts/check_core_coverage.py` | 21 個 Core 錨點全部是「已覆蓋」或「不適用（附理由）」，漏一個就失敗 |
| 4 個 agents | 第 4 節表中的 `dev-explorer`、`dev-implementer`、`dev-reviewer`、`dev-security-reviewer` | reviewer 類的 agent 沒有寫入工具 |
| G0 task graph | `skills/dev-plan/scripts/graph.py`（只用標準庫），以及 `tests/fixtures/graph/` 下的 `valid/` 和 `invalid/` | 正面 fixture 全部通過；每個負面 fixture 都回報預期的錯誤代碼 |
| 需求 wiki 範本與 ingest | `skills/dev-plan/templates/` 放 `REQ-template.md`、`index.md`、`log.md`；`dev-plan` 負責 ingest，把使用者原話寫成 REQ 檔，原話逐字存進 `sources`（type／locator／quote） | `graph.py validate` 預設在目標專案的 `docs/requirements/`（或 `.dev/config.json` 的 `requirements_dir`）找 REQ 檔；task 引用的每個 REQ 都要有實際存在、且 `id` 相符的檔案，否則失敗 |
| 本專案的需求實例 | `docs/requirements/`：把使用者最初的需求整理成 REQ，`sources` 逐字引用原話並標明出處 | 這是格式的第一個實例；`index.md` 與 `log.md` 齊全 |
| 打包 | `.claude-plugin/plugin.json`、`.claude-plugin/marketplace.json`、`scripts/validate.sh` | 本機一個指令跑完所有檢查 |

- 需求 wiki 放在各目標專案自己的 `docs/requirements/`，不另外建一個專案。
- `.dev/<objective-id>/` 是否 commit 由專案設定：`.dev/config.json` 的 `commit_state`，預設 `true`，也就是隨工作一起 commit，讓其他 session 可以接續。例外：PR 建立後，該 PR head 的審查與 gate 紀錄不 commit 到 PR 分支（D-013 第 6 項）。只有設成 JSON 的 `false` 才關閉；關閉後不 stage `.dev/<objective-id>/` 下的檔案，專案應把 `.dev/*/` 列入 gitignore，`.dev/config.json` 仍保留在版本控制中。裡面不得寫入 secrets、憑證、私有路徑或原始 log。本 repo 的 `.gitignore` 已列入 lock 與暫存檔；目標專案要自己把 `.dev/**/.graph.lock` 與 `.dev/**/.graph-*.tmp` 加進 `.gitignore`。（2026-10-20 使用者決定，PR #2 交接第 6 項）
- `scripts/check_pack.py` 只檢查本 repo REQ 檔的格式（欄位與關係 ID），不是需求 lint；矛盾、孤兒與過期需求的 lint 仍在 Phase 2。
- Plugin 名稱是 `dev-skills`。`claude plugin validate` 不接受以 `claude-` 開頭的第三方 plugin 名稱，所以 repo 名稱維持 `claude-dev-skills`，plugin 改名。安裝指令為 `claude plugin install dev-skills@dev-skills`。
- 不在 Phase 1：G1–G3、hooks、需求 wiki 的 lint 腳本（留到 Phase 2；Phase 1 只定格式並做 ingest）、CI workflow。CI 之後由 D-017 加入。

### D-009 Graph engineering 分階段完成（已決定，2026-10-20）

- 來源：使用者 2026-10-20 的決定。需求見 REQ-002（補上 D-009 的原話）。
- 規則寫在第 5.2 節：
  1. G1、G2、G3 各自是一輪獨立交付；前一階段合併後，下一階段才開始。
  2. 每個階段開工前，先依前一階段的實際使用結果修正設計。
  3. 第 5.2 節列出各階段的交付物與完成判準。
  4. graph 與 REQ 的 schema、`graph.py`、fixtures 屬 runtime 中立層，不得依賴 Claude 專用工具；用 Agent 與 Workflow 執行的方式屬 Claude 專用層。
- Core 回饋：目前否。理由：graph engineering 不在 Core 的契約內。中立層在 G1 之後才成形；之後若要提回 Core，依 D-001 的流程另外記錄在 `docs/core-feedback.md`。

### D-010 不做 agent memory（已決定，2026-10-20）

- 來源：使用者 2026-10-20 的決定。需求見 REQ-015。
- 不建立任何 memory backend 或記憶契約。
- 專案狀態以 repo 為準：REQ wiki、`graph.json`、`events.jsonl`、Git 與 review 紀錄。
- 原生記憶只當參考資料。原生記憶與 repo 衝突時，以 repo 為準。原生記憶不得作為需求來源、授權或完成證據。
- `dev-core` R-AUTH-1 與 R-AUTH-7 已經把記憶當成參考資料，所以技能規則不需要修改。第 6 節已同步改寫。
- Core 回饋：否。理由：Core 已涵蓋這些規則：`auth-scope` 規定記憶不得覆蓋指示順序，`wf-stages` 規定 session 記憶只供參考，`auth-data` 規定 native recall 不是合格的管理 backend，而且 Core 沒有資料 backend。D-010 只是本專案選擇不建 backend。

### D-011 部署與量測（已決定，2026-10-20）

- 來源：使用者 2026-10-20 的決定，以及同一天對原則 1 那句 context 成本說法的提問。需求見 REQ-016。
- 部署：下列步驟在 repo 之外，由使用者執行。本 PR 只記錄，不執行。
  1. 以 user scope 安裝到 Claude Code，只在個人專案使用。Cowork 要等 FU-001（GitHub Issue #3）驗證之後再說。
  2. 在 `~/.claude/CLAUDE.md` 加一段簡短指引：開發任務先用 `dev-deliver` 判斷等級。
- 量測計畫：
  1. 挑 3 到 5 個真實任務。每個任務在有裝技能包與沒裝技能包的情況下各跑一次。
  2. 每次執行記錄四項：漏掉的錯誤、不在需求內的改動、token 用量與耗時。
  3. Token 比較：同一個任務在 claude-dev-skills 與 codex-dev-skills 各跑一次，比較 token 用量，並記錄 `dev-core`（Codex 版是 Core 的參考文件）被讀取的次數。原則 1 的 context 成本以這項結果為準。
  4. 同時確認 plugin agent 的 `tools` 與 `disallowedTools` 在實際執行時有生效（2026-10-20 約定的後續項目）。
  5. Token 用量與耗時以平台提供的用量紀錄為準。agent 不自行估算，也不宣稱能精確讀取 context 用量。
  6. 依結果決定加強或刪減技能。修改走新的 Issue 與 PR。
- 追蹤項目是 `.dev/followups.md` 的 FU-004。
- 拆分 `dev-core` 的評估記錄在 `docs/core-feedback.md`。拆分的意思是：一份每次都讀的短核心，加上依階段需要時才讀的參考文件，類似 Codex 版的做法。要不要實作，等量測結果出來後，由使用者用決策卡片決定（FU-005）。
- Core 回饋：否。理由：部署與量測是 Claude 端的工作。量測結果會成為 D-001 回饋流程第 2 步的證據（`docs/core-feedback.md`）。

### D-012 自動交接（已決定，2026-10-20）

- 來源：使用者 2026-10-20 的決定。需求見 REQ-017。
- 規則（`dev-continue`）：
  1. 每個工作項目完成時，評估要不要換到新的對話（session）。工作項目例如一個 graph node、一輪 review 與修正，或一個階段。
  2. 評估依據是 review 與修正的輪數、階段邊界與工作量。context 用量只當參考。agent 不宣稱能精確讀取 context 用量。
  3. 決定要換時，自動寫好 checkpoint。PR 建立前，自動 commit，不先詢問使用者。D-012 是使用者的決定，涵蓋這個 checkpoint commit，不涵蓋其他 commit。這個 commit 仍遵守所有 commit 規則：先做 R-REV-9 掃描；`commit_state` 為 `false` 時不 stage 狀態檔。
  4. PR 建立後，checkpoint 不 commit，因為 commit 到 PR 分支會產生新的 head，新的 head 需要新的完整審查（R-EXH-3）。checkpoint 留在工作目錄，重點改貼成 PR comment，讓其他 clone 也能接手。貼出前由 `dev-security-reviewer` 掃描要貼出的原文（R-REV-9）。沒有這項掃描就不貼出。checkpoint 只指向審查與 gate 紀錄，不重複這些紀錄。這一項是使用者對 PR-C1 決策卡片 1 的回答，只涵蓋這則 comment，不涵蓋其他 comment。
  5. 接著提出新 session 的卡片，附上完整交接說明。使用者按下確認後，新 session 才開始。
  6. 使用者確認後就完成交接，原 session 停止寫入。使用者確認之前，或使用者拒絕時，沒有發生交接，原 session 繼續工作。
- 與 Core 的差異：Core `wf-stages` 已規定暫停前存 checkpoint，以及接續時重新讀取來源；接續工作時，Core 也規定優先使用原本的 session。D-012 只加上評估時機與交接步驟，沒有改 `dev-core` 的規則。D-012 的切換要等使用者確認才發生；沒有確認時，原本的 session 繼續工作。
- Core 回饋：否。理由：換對話的方式取決於各接口的 session 能力；Core `wf-stages` 已涵蓋 checkpoint 與接續。

### D-013 Review 收斂規則（已決定，2026-10-20）

- 來源：PR #2 的 Merge Review 1 到 5 一直出現新的 finding，沒有收斂；Merge Review 6 與 7 沒有 finding。PR-A（Issue #4）在第 2 輪之後先套用這些規則重新評估，移除了沒有需求對應的檢查（`.dev/issue-4-commit-security/reviews/round-2.md`）。需求見 REQ-012。
- 規則（`dev-core` R-REV-3、R-REV-4、R-VER-2、R-EXH-3）：
  1. 嚴重度門檻：MUST-FIX 只限 Core 的阻擋項；判斷不出是不是阻擋項時，算 MUST-FIX。SHOULD-FIX 必須有可重現的失敗，並影響需求、DoD 或文件寫明的行為。NIT 只限這次變更造成的回歸，或不實的文件內容。其餘列為剩餘風險（residual risk），不列為 finding。
  2. 修補前先分類：每個 finding 判讀為必要修正、值得改善、維持現狀或需要人類決策。修補要在需求範圍內；需求沒考量到的缺陷，先交給使用者決定（見 D-016）。Core 的阻擋項例外：先修正。管理措施（流程、文件、人工檢查）是有效的修補方式，但要寫明責任人、可驗證的前提與失效時的處理。
  3. 新增機制前，要說明它的獨特作用，以及對應哪一條需求；說不出來就列為 SCOPE-CREEP。`dev-core` R-RIG-3 已經有這條規則，所以本次不改。
  4. 修正後、push 前，由獨立 reviewer 做窄範圍的確認。完整 Merge Review 仍涵蓋整個 base..head 範圍；可證未受之後任何變更影響的部分，可以重用先前的證據，但要寫明理由與覆蓋範圍。
  5. 連續兩輪 review 仍出現新的阻擋項，或同一個機制連續兩輪修了又出新問題時，停止修正循環，不進入下一輪修正。先重新評估規格、驗收標準與做法；範圍問題用決策卡片（D-014）交給使用者。第二個條件由使用者在 PR-B 的決策卡片 1 加入。
  6. PR 建立後，這個 head 的審查與 gate 紀錄不 commit 到 PR 分支。commit 會產生新的 head，新的 head 又需要一次完整審查，這就是結構性的循環。使用者授權貼 comment 時，紀錄寫成 PR comment（貼出前先做 R-REV-9 掃描）；沒有授權時，紀錄不 commit，放進給使用者的報告。
- 與 Core 的差異：Core 沒有定義嚴重度門檻；Core 把連續兩輪未完成的 review 視為重新評估的時機，而不是停止。這些都是收緊，記錄在 `skills/dev-core/deltas.md` 的 DL-011、DL-012、DL-013。Core 的阻擋項一律保留為 MUST-FIX。
- Core 回饋：是。理由：Codex 版與 Grok 版用同一份 Core，同樣可能遇到 review 不收斂，以及紀錄 commit 造成的循環；嚴重度門檻與停止規則都不依賴特定接口。

### D-014 需要人類決策的描述格式（已決定，2026-10-20）

- 來源：PR #2 與 PR-A 交給使用者的決策，每次的格式都不同。需求見 REQ-013。
- 規則（`dev-core` R-AUTH-6、R-WRT-1）：
  1. 每個 Needs Human Decision 的 finding，以及每個交給使用者的決策，都使用固定的決策卡片。欄位：問題（一句）、為什麼需要你決定、選項（每個選項分別寫做什麼、結果、風險、成本）、建議與理由、不決定的後果（會擋住什麼、什麼可以繼續）、證據（檔案和行號、指令輸出；事實與推論分開）。
  2. 英文依 ASD-STE100 原則撰寫。繁體中文依 Core 的簡明寫作原則調適：一句只講一件事、寫明主詞、術語保持一致、技術詞第一次出現時用白話解釋、不用模糊詞、不套用英文字數規則。
  3. 審查報告與 gate 報告註明「依 ASD-STE100 原則編寫，未完成完整符合性驗證」，不得宣稱符合 STE。
  4. 範本與一個正例放在 `skills/dev-review/references/decision-card.md`。正例改寫自 PR-A 的決策卡片 1（貼出 PR 文字前要不要掃描）。
- `dev-review`、`dev-gate`、`dev-deliver` 的輸出規則都使用這張卡片。
- 與 Core 的差異：Core 列出提出決策時要寫的內容，但沒有固定格式。這是收緊，記錄在 DL-014。
- Core 回饋：是。理由：這是 Core `wf-writing` 與 `auth-stops` 的格式問題；三個接口都要把決策交給使用者。

### D-015 每次 commit 與 push 前做安全審查（已決定，2026-10-20）

D-009 到 D-016 是同一天的決定。D-015 由 PR #5（Issue #4）記錄；D-013、D-014、D-016 由 PR #7（Issue #6）記錄；D-009 到 D-012 由 PR-C1（Issue #8）記錄。

- 來源：PR #2 的 SEC-01。分支上 10 個 commit 的作者與 committer 是由本機帳號與主機名稱推導出來的，push 後已經公開。內容審查沒有檢查 commit 的中繼資料，到合併前的安全掃描才發現。需求見 REQ-011。
- 規則（`dev-core` R-REV-9）：每次 commit 與每次 push 之前，由獨立的 `dev-security-reviewer` 掃描「實際要公開的內容」。小改動或只改文件也不例外，這項掃描永遠不能標為「不適用」。
  - commit 前：已 stage 的 diff，以及這個 commit 會帶的作者、committer（用 `git var GIT_AUTHOR_IDENT` 與 `git var GIT_COMMITTER_IDENT` 讀出）、訊息與 trailer。掃描後不得再覆寫身分；commit 後立刻用 `git log -1 --format=fuller` 讀回。
  - push 前：這次 push 要送出的全部內容。主代理用和實際 push 完全相同的參數執行 `git push --dry-run --porcelain`，之後也用完全相同的參數 push。掃描它列出的每個 ref 上遠端還沒有的每一個 commit，包含身分、訊息、解決 merge 衝突時加入的內容，以及 annotated tag 的 tagger 與訊息。並確認實際記錄的身分與訊息和掃描時相同。
  - 掃描要看到內容，而不是編碼後的資料：每個掃描指令加上 `--text --no-textconv --no-ext-diff`。
  - 貼出 PR 或 MR 的標題、內文、留言或審查紀錄之前：掃描要貼出的原文。（Issue #12 把 Issue 的標題、內文與留言也加進來，見 FU-007 與 REQ-011。）
  - 合併前：base..head 範圍內的每一個 commit，不只看最後的 diff；以及平台合併時會建立的 merge 或 squash commit：合併方式、作者、訊息與 trailer（例如由分支 commit 產生的 `Co-authored-by:`）。
  - 要找的東西：金鑰、密碼、token、私人檔案、私人路徑、主機名稱、私人 email，以及作者沒有選擇公開的真實姓名。有發現就擋下 commit 或 push，修正後重新掃描。
  - 掃描後只要 stage 的內容、身分、訊息或要貼出的文字有變，就是新的候選，要重新掃描。掃描與 gate 的紀錄不放進它們所涵蓋的那個 commit，而是放進之後的 commit（由那個 commit 自己的掃描涵蓋）或 PR。PR 建立後，這些紀錄不 commit 到 PR 分支（D-013 第 6 項細化了這一點）。
  - 找不到 `dev-security-reviewer` 時，在 commit 或 push 之前停下。
- R-REV-1 補充：必要的安全審查或 Security Diff Scan 一律使用 `dev-security-reviewer`，不能用 `dev-reviewer`。
- 建議（不在本 PR 實作）：用 gitleaks 之類的 secret scanner，掛在 pre-commit 或 pre-push hook，作為確定性的補充檢查；並設定 `git config user.useConfigOnly true`，讓 Git 不會用主機名稱猜身分。安裝工具或 hook、改 Git 設定都需要使用者同意；它們都不能取代獨立審查。
- 審查報告也會 commit 或貼到 PR，所以兩個 reviewer agent 回報時一律遮蔽金鑰與私人識別資訊：只寫種類、位置與長度或類別；email 只說是不是 noreply 與提供者；路徑與主機名稱中的帳號或主機部分換成代稱。
- 與 Core 的差異：Core 只在變更碰到信任邊界時要求 Security Diff Scan；這裡改成每次 commit 與 push 都要掃。這是收緊，記錄在 `skills/dev-core/deltas.md` 的 DL-010。
- Core 回饋：是。理由：在公開 repo 中，每次 commit 與 push 都會公開內容與中繼資料，這和接口無關。證據是 PR #2 的 SEC-01（見 `docs/core-feedback.md`）。
- 同一個 PR 修正 `graph.py transition --evidence-file`：原本會把任何可讀檔案的內容複製進預設會被 commit 的 `events.jsonl`。現在只接受專案根目錄內的一般檔案（路徑的最後一段不得是 symlink，也不接受 FIFO 之類的非一般檔案），而且只記錄相對路徑與 SHA-256，不記錄內容（使用者選擇的選項，2026-10-20）。剩下的風險：專案內短而好猜的秘密檔（例如被 gitignore 的 `.env`）的雜湊會被 commit，可以離線猜測。專案內任何一般檔案（包括 `.git/` 底下的檔案或 hardlink）都只會記下路徑與雜湊，不會記下內容；這些情況沒有對應的需求，所以不另外擋（2026-10-20 使用者決定）。追蹤項目是 `.dev/followups.md` 的 FU-003。

### D-016 Review 範圍與需求的關係（已決定，2026-10-20）

- 來源：PR-A 第 2 輪之後的重新評估。每個 finding 先標明和需求的關係，再決定怎麼處理；沒有需求對應的檢查被移除，需求的缺口變成決策卡片 1。需求見 REQ-014。
- 規則（`dev-core` R-REV-3；`dev-review` 的 brief 規則與 finding 格式）：
  1. Review 找問題的範圍不限於需求，但每個 finding 都標明 `requirement_relation`，值為 `in-scope`、`gap`、`no-requirement` 或 `unrelated` 之一。
  2. 新增 finding 類別 `REQ-GAP`：需求沒有涵蓋、但看起來應該涵蓋的問題。`REQ-GAP` 不在當次修正，而是做成決策卡片（D-014），由使用者選擇：新增需求、延後處理或不採納。
  3. 只有使用者能新增需求。使用者同意後，`dev-plan` 把它 ingest 成新的 REQ（ingest 指把使用者的原話寫成需求 wiki 裡的 REQ 檔），sources 記下 finding ID 與使用者的決定。agent 不能自己把 `REQ-GAP` 寫成需求。
  4. `no-requirement` 歸為 `SCOPE-CREEP`；`unrelated` 列為剩餘風險或後續項目，不阻擋當次交付。
  5. 例外：Core 規定的阻擋項（安全、資料遺失、授權、完整性）不論 `requirement_relation` 為何都照樣阻擋；需求沒寫到不構成豁免。
- 與 Core 的差異：Core 沒有把 finding 和需求連起來。這是收緊，記錄在 DL-011。
- Core 回饋：是。理由：Codex 曾把專案需求改寫成通用需求（D-003）；這個欄位讓三個接口都能分辨需求範圍內的修正與範圍擴張。

### D-017 最小 CI（已決定，2026-10-21）

- 來源：PR #11 合併後，使用者同意加入最小 CI：「CI的部份也同意你的建議」。需求見 REQ-020。Phase 1 不含 CI（D-008），所以這是新範圍。
- 目的：先前每次 review 的 `platform_enforcement` 都是 `NOT_CONFIGURED`，因為 repo 沒有 CI，也沒有 branch protection。CI 讓 `validate.sh` 與 secret 掃描在 GitHub 平台上執行；Auto-fix 也需要 CI 的結果才有東西可修。
- 做法（`.github/workflows/ci.yml`）：
  1. 觸發：送往 `main` 的每個 pull request，以及每次 push 到 `main`。不用 `pull_request_target`。
  2. Job `validate`：用固定的 npm 版本安裝 Claude CLI（不登入），再執行 `scripts/validate.sh`。`claude plugin validate` 不需要登入，所以 CI 也執行它。
  3. Job `gitleaks`：下載固定版本的 gitleaks release，先用 workflow 裡寫死的 SHA-256 核對，再掃描從 checkout 的 commit 可到達的每個 commit。PR 時 checkout 的是 merge commit，所以涵蓋 PR 的每個 commit。輸出遮蔽（redact）secret，因為公開 repo 的 log 是公開的。限制：merge commit 本身的 patch 不掃；PR 可以修改 workflow、`.gitleaks.toml` 與 `.gitleaksignore` 而改變掃描內容；CI 找到的值已經公開，必須更換。
  4. 每個 action 都用完整 commit SHA 固定，註解寫 release tag。Workflow 層級只給 `permissions: contents: read`；checkout 不保留 token；不用任何 secret。
- `dev-gate` 的平台結果（R-EXH-4）：專案只能用明確的專案設定選定 provider profile（使用者決定 Q3 (b)）。這個 PR 不定義那個設定，所以結果仍是 `NOT_CONFIGURED`。`dev-gate` 用一次讀取取得 PR 的 head 與 check，並列出每個 check 的結果；讀取失敗或 head 不是受審的 head 時，結果是 `UNVERIFIED`。
- 第二輪 review 在 profile 讀回機制又找到新的阻擋問題（ES2-001 到 003），觸發停止規則。使用者決定把 profile 設定移到 FU-009，並和 FU-008（PR 可以削弱自己的 check，ES-004）一起設計（Q5 (a)）。
- 合併後由使用者把 `validate` 與 `gitleaks` 設成必要檢查；步驟見 README 的「CI」一節。
- CI 不取代 R-REV-9 的獨立掃描：gitleaks 只看 commit 內容，不看 commit 身分、訊息與 PR 文字。
- Core 回饋：否。理由：CI 與 provider profile 是各專案自選的 overlay（Core auth-scope 與 exact-dimensions）。`dev-core` R-EXH-4 只補上 Core 原文已有的規則：「已選或有相關狀態卻無當前成功讀回為 UNVERIFIED」。也就是說，有相關的平台狀態，卻沒有當前成功的讀回時，結果是 UNVERIFIED。

### D-018 平台設定（provider profile）的讀回（已決定，2026-10-21）

- 來源：FU-009 與 FU-008（使用者決定 Q5 (a)：兩者一起設計）。設計先寫成規格與威脅模型，經一輪獨立設計審查（DR-001 到 DR-008、ES0-001 到 ES0-008）後由使用者核准：「Q1 a。但 script 只實作規格列出的性質；review 若找到規格以外的新邊界情況，一律做成需求缺口卡片交給我決定，不可直接加程式。Q2 a。」需求見 REQ-021。
- 設定：`.dev/config.json` 的 `platform_profile`（provider `github`、repository、base branch、必要 check 名稱與 GitHub App id）。只從 bound base commit 讀，不讀 PR head，也不讀工作樹。選了設定就是 required profile。格式錯誤、未知 key、重複 key 等一律 fail closed，並顯示原因。
- 讀回：唯讀 checker `skills/dev-gate/scripts/platform_profile.py`。每個 `gh` 呼叫都用 `--hostname github.com` 與 bound repository；只有 `success` 算通過；必要 check 是 profile 與平台規則（ruleset 全部分頁、classic protection）的聯集；check 綁定 app id；同一 head 的重複 run 依 check suite 分組，每組最新的都要成功；讀完再確認 head 沒變；結果依 BLOCKED、UNVERIFIED、VERIFIED 的順序決定。理由：前兩輪的純文字規則沒有收斂；分頁、分組與優先順序是機器能檢查的事實（R-REV-8），負向案例寫成 `tests/test_platform_profile.py`，由 CI 執行。
- PR 修改 `.dev/config.json`：屬於平台政策變更（R-AUTH-2），gate 給使用者決策卡，答覆綁定 head 上該檔的 blob。
- FU-008（只回報，不阻擋；Q2 (a)）：GitHub 用 PR 自己的 workflow 跑 check，所以有 profile 時 `VERIFIED` 一律寫成「checks ran this PR's own definitions」，gate 也列出 PR 在固定路徑清單內改到的檔案。清單只是提示，任何被 check 讀到的檔案都可能削弱 check。
- 不保護的範圍：PR 削弱自己的 check、同一 GitHub App 的同名 check、admin 或 bypass 合併、`strict` 關閉時的 base 漂移、其他 ruleset 規則、GitHub API 回答的真實性、其他 forge。
- MR-001：`dev-core` R-EXH-4 寫明何時是 `NOT_CONFIGURED`、何時是 `UNVERIFIED`。
- 實作審查第 1 輪後觸發停止規則（設計審查與實作審查連續兩輪都有新的 blocker）。三個 blocker 都是「誤報 `NOT_CONFIGURED`」。使用者決定（「Q4 a；Q5 a；Q6 a」）：再修一輪；沒有 profile 時也比對 PR 的 base；checker 失敗或沒有結果行時一律是 `UNVERIFIED`。
- 這個 repo 的設定：`validate` 與 `gitleaks`，來源 GitHub Actions（app 15368），base `main`，與 2026-10-21 讀回的 ruleset 一致。這個 PR 本身的 base 還沒有設定，所以它的 merge gate 結果是 `NOT_CONFIGURED`，並因新增 `.dev/config.json` 給使用者一張政策變更卡；第一次 `VERIFIED` 要等下一個 PR。
- Core 回饋：否。理由：profile 是各專案自選的 overlay（Core exact-dimensions）；`dev-core` 的差異記在 DL-015。

### D-019 教訓技能 `dev-retro`（已決定，2026-10-26）

- 來源：使用者 2026-10-22 在 Claude Code session（PR #2 Merge Review 5 協調 session）的訊息。01:52 UTC（U1、U2）：「是不是能變成一個主動的技能，日後發現問題時，可以主動學起來，自我改進。」「並且，隨著往後模型龻得更聰明、能力更強，新模型會自動Review這些記下來的規則或者技能，並建議適度的修改？」01:59 UTC（U3）：「教訓只寫在這repo裡…只有該專案本身才知道…後續新加的b專案可能會再犯相同的錯。所以也要有個機制來識別教訓的層級。」（「龻得」是原文（sic；變得）；「…」是省略的原文；原文見 REQ-026 sources）。設計經兩輪 deep review（停止規則觸發）後，使用者回答設計卡片 D19-C1 到 D19-C7：「C7 選 a；C1a C2a C3a C4a C5a；C6 先做 R-REV-9 backlog PR」；其中 C3 (a) 回答 REQ-GAP D1-013。規格經三輪安全設計審查與 deep review（停止規則觸發兩次，卡片 D19-S1、D19-S2）後，使用者核准規格 v4（卡片 D19-A1 (a)）。需求見 REQ-026。Phase 1 不含這個技能（D-008），所以這是新範圍。
- 問題：session 發現的教訓只留在那次報告，或只留在一個專案。本 pack 沒有辦法把教訓變成經過審查的修改；有新證據時（例如更新的模型），沒有辦法重看已記錄的教訓與它們指向的規則；也沒有辦法判斷教訓屬於哪個層級，所以只在一個專案記下的教訓，可能在之後加入的專案再發生。
- 決定：
  1. 新技能 `dev-retro`，兩個模式：`/dev-skills:dev-retro capture` 與 `/dev-skills:dev-retro review`（卡片 D19-C1 (a)）。只能由使用者呼叫：frontmatter 寫 `disable-model-invocation: true`，它只擋模型用 Skill tool 呼叫；其他 skill 都不呼叫 `dev-retro`。它不寫任何檔案、不改紀錄、不做 Git 寫入或對外發布，也不呼叫其他 skill、MCP 或網路工具；例外只有：review 派唯讀的 `dev-skills:dev-reviewer`，以及讀回指令 `git diff HEAD` 可能更新 `.git/index`（finding MS2-001）。frontmatter 的 `disallowed-tools` 移除 Write、Edit、NotebookEdit；這是一層防護，不是保證（Bash 等工具仍在，使用者送出下一則訊息後限制失效）。輸出只有報告、草稿文字與卡片。每次執行前後記錄 `git rev-parse HEAD`，以及 `git --no-optional-locks status --porcelain=v1 --untracked-files=all`（讓 `git status` 不更新 `.git/index`；finding MS2-001）與 `git diff HEAD --binary --no-ext-diff --no-textconv` 輸出的 SHA-256，有差異就回報並作廢那次結果；限制：看不到未追蹤檔案內容的變化、ignored 檔案、`.git` 與 repo 外的任何東西（例如使用者的指示檔），`git diff HEAD` 可能更新 `.git/index`，前後值相同不證明沒有寫入。只支援 Claude Code，README 與 `SKILL.md` 寫明（卡片 D19-A3 (a)）。
  2. `dev-deliver` 的最後報告與 `dev-review` 的審查報告加「教訓候選」小節（英文標題 "Lesson candidates"）：新規則 R-VER-5 與 DL-035，是 Core `workflow.md:74` 在這兩種報告的加嚴，不是新的報告制度。小節只是報告內容，不寫檔、不改規則、不呼叫 skill；候選是提案，不是授權或完成證據。直接用 `dev-implement`、`dev-gate`、`dev-plan` 時沒有這個小節（殘餘風險）。
  3. 層級：L1 專案、L2 本 pack、L3 Core、L4 使用者個人的指示。層級不清楚時，capture 出卡問使用者；決定前草稿只留在報告（卡片 D19-C5 (a)）。L1 的教訓與理由留在該專案，不進本 repo 的 `deltas.md`；L2 寫成給本 repo 的 dev-plan 需求草稿，屬 `dev-core` 規則的理由寫成 `deltas.md` Reason／Evidence 的草稿句；L3 寫成 `docs/core-feedback.md` 的草稿，要不要上報由使用者決定；L4 只輸出一行建議文字，附來源類別與日期，由使用者決定要不要加到自己的指示檔，`dev-retro` 不寫這個檔（卡片 D19-C2 (a)、D19-A4 (a)）。L4 文字不含授權、權限、略過確認、略過審查或掃描、自動執行；這類教訓只在卡片中說明「這是授權變更」，由使用者自己撰寫。
  4. 出處與抽象化：locator 只能指向草稿將被 commit 或貼出的那個 repo；離開來源 repo 的文字只寫類別與日期，不寫來源 repo 的名稱、路徑、PR／Issue 編號或 finding ID。抽象化檢查表（專案名、客戶名、內部系統名、主機、帳號、真名、email、版本與弱點細節）的結果是模型自評，不是審查。不把 repo 外的檔案、原生 memory 或自動載入的指示檔內容當出處或放進草稿；這些內容可能已經在 context 中，skill 無法阻止它們被載入。R-REV-9 不檢查業務機密，所以控制只有兩項：檢查表，以及使用者逐字審。任何將被 commit 或貼出的教訓文字都在卡片中逐字列出，實際文字要和核准的相同，有改動就再給使用者看一次；貼出是另一項外部寫入（R-AUTH-2），先做 R-REV-9 貼文掃描。從未修補的安全問題得出的教訓，等修補發布後才升級或公開，沒有例外（卡片 D19-S1 (a)）。
  5. review：只在使用者呼叫時執行，沒有排程。範圍是有新證據、尚未審過的教訓，以及它們指向的規則與這些規則的 REQ 來源，只讀目前 repo 的檔案（卡片 D19-C3 (a)）。新證據是新的教訓候選、已記錄的失敗或使用者指定的疑慮；單純換了模型不算新證據（Core `workflow.md:72`、`:99`），這時 review 請使用者確認範圍。審查者是唯讀的 `dev-skills:dev-reviewer`（`opus`／`xhigh`），每次綁定 exact revision。每項建議標 Core 四種判讀之一；任何會改規則、skill、REQ 或紀錄的建議都出卡，「必要修正」也出卡。capture、review 與教訓候選都不建議放寬 Core 義務或刪除必要檢查；對 Core 的意見寫成 core-feedback 草稿（REQ-019）。審查結果不是核准，也不是完成證據。
  6. 教訓變規則只有一條路：卡片 → 使用者回答 → 使用者另下指令 → dev-plan（REQ sources 記卡片 ID 與使用者原話；另一專案的卡片只記類別與日期；抽象化的原話標「抽象化轉述」）→ 實作 → 獨立 review → R-REV-9 → PR → 使用者決定 merge。每張草稿卡片的選項是核准、延後、拒絕；只有延後的教訓才寫成 FU 列，並附 Deferred 的必填欄位。不建 ledger、教訓檔、使用者層級的教訓檔、hooks、排程或 validator（卡片 D19-C4 (a)、Core `workflow.md:74`）；D-010 不變。本決策不做任何從教訓得出的規則變更。
- 實作：四個循序 PR，每個在前一個合併之後開始；每次 merge 由使用者決定。Rigor 等級 `strict`：每個 PR 都有 deep review、R-REV-7 安全審查、R-REV-9 掃描與 exact-head gate。PR-1 紀錄（REQ-026、本決策、第 4 節與第 6 節、需求索引與 log、CHANGELOG）；PR-1 的 deep 與安全審查另外檢查規格 v4 沒經過獨立審查的新增內容，包括：R-VER-5 的三項新義務（抽象化檢查表的逐項結果、每句標事實、推論或未驗證、最小補強先縮小宣稱或加管理措施）、PR-4 DoD 的「未出現」選項，以及 PR-2 的使用者貼上的 Issue 內容作為 capture 輸入、定位規則的範圍（REQ sources 與內文、CHANGELOG、`deltas.md`、commit 訊息）、卡片說明答案是否也同意 commit 或貼到它指名的目的地、不寫入規則的 `.git/index` 例外（PR-2 縮小，finding MS2-001）、review 結果不是完成證據，和 PR-4 的 PR 說明中的第一次 review 報告與 DoD 的定位項目（卡片 D19-S2 (a) 的條件 2）。PR-2 `skills/dev-retro/SKILL.md`、`dev-core` 階段對照表一列、README（中英）；實作者重讀官方文件確認兩個呼叫控制欄位的名稱、語法與效果，讀不回或不同就是 PR-2 的 blocker。PR-3 R-VER-5、DL-035、`skills/dev-core/source-map.md` 一列、`dev-deliver` 的輸出與 reviewer 報告格式。PR-4 第一次使用：使用者對本 repo 五個已記錄的案例呼叫 capture，再呼叫 review；延後的教訓寫成 FU 列；案例 (b) 到 (e) 的判讀與第一次 review 的報告，遮蔽並抽象化後記在 PR 說明（卡片 D19-A2 (a)）。
- 未驗證：呼叫控制欄位的名稱、語法與效果；claude.ai、Skills API 與 Cowork 是否認得這兩個欄位（在不認的環境，「只能由使用者呼叫」只靠 skill 文字）；原生 auto-memory 是否會被「記下來」觸發或自行保存教訓文字。
- 與 REQ-005 的關係：REQ-005 的原話說技能主要由 agent 視需求呼叫；`dev-retro` 只能由使用者呼叫，是使用者自己選的例外（卡片 D19-C1 (a)）。
- 與 REQ-001 及第 3 節（`docs/design-proposal.md:32`，Cowork）的關係：`dev-retro` 只支援 Claude Code，是使用者選的例外（卡片 D19-A3 (a)）；其他技能維持 Cowork 的目標。
- Core 回饋：否（推論，由審查確認）。理由：Core `workflow.md:74` 已規定改善記在既有報告，不新增反思 executor、memory、hooks 或 scheduler。`dev-retro` 不套用任何變更，也不執行候選或比較，只在使用者呼叫時產出報告、草稿與卡片，所以它不是反思 executor；Core `docs/provenance/source-map.md:181` 也說自動化由接口另包驗證及取得授權。層級分類只決定本 pack 的紀錄去處。與 Core 引用的 codex-dev-skills 改善契約有一處分歧：本 pack 公開抽象化後的教訓文字，那些契約要求真實提案與評估保持私有，公開 Git 只用合成資料。這點寫進本理由，不另提 CF。

### D-020 按需載入 Core 原文（已決定，2026-10-22）

- 來源：FU-005（REQ-025）。FU-010 的盤點（Issue #18，REQ-023）顯示，壓縮的 `dev-core` 在審查中不收斂：三輪審查每一輪都找到摘要漏掉的 Core 條件（R-VER-2 停止規則兩次）。使用者：「壓縮的原因是因為任務一開始的時候以為技能包是一次全部載入。但其實可以像codex一樣設計成漸進式的按需載入。若是這樣，是否乾脆把原始的條文寫進來？」設計規格經三輪獨立審查（含一次安全設計審查；停止規則觸發兩次）後，使用者回答設計卡片（「那先照你的建議。我想先完成移植和功能完善。後續再來針對這部份優化」、「9b」）並核准（「核准 FU-005 規格」）。D-019 保留給 lessons skill。
- 決定：
  1. 各 skill 依階段直接讀 vendored Core 原檔，不把 Core 改寫成摘要（卡片 1a）。讀整份檔案（卡片 2a）。每個 skill 都讀 `authorization-and-stops.md`（卡片 3a）：移除「手上沒有原文」這條失敗路徑；這是一層防護，不是保證。
  2. `dev-core` 逐字保留 33 項：內文帶有 DL 列加嚴、比 Core 嚴格（含字面上）或 Claude 專屬的規則與 CB-1 到 CB-5。其餘 13 條之後改成「規則 ID 加 Core anchor」的索引行，規則 ID 與引用仍然有效。R-AUTH-5 與 R-VER-3 在這 13 條之中：它們成為索引行，並保留各自的專案讀法（第 3 點）。
  3. Core 兩處可以兩種讀法的句子，專案寫明讀法（卡片 5a、5b、9b）：`authorization-and-stops.md:35` 與 `workflow.md:76`（R-AUTH-5、R-VER-3；DL-028、DL-029）。
  4. 只有兩個 reviewer 拿 Core 檔，而且當作審查準則（資料），不當指令；政策只來自 brief；implementer 與 explorer 不拿（卡片 8a）。
  5. FU-011 只處理轉述「保留規則」的文字（卡片 6a）。FU-012 不新建 `rationale.md`；理由放在 `deltas.md` 的 Reason、Evidence 欄與 CB 出處行（卡片 6b，取代 FU-010 card 2a）。
  6. 現在決定並實作；FU-004 的「使用本 pack」組在 PR-2 之前與 PR-4 之後各跑一次（卡片 7′a，取代「Before FU-005 is decided」的等待）。
- 實作：四個循序 PR，每個在前一個合併之後開始（PR-2 另等 FU-004 基準量測）；每次 merge 由使用者決定。PR-1 紀錄（REQ-025、本決策、DL-018 到 DL-029、兩處讀法、CB 出處行、Core 回饋狀態、FU 列）；PR-2 在 `dev-core` 加階段對照表，各 skill 加讀 Core；PR-3 讓 reviewer 用 Core 當審查準則；PR-4 把 13 條規則改成索引行；R-STG-4、R-AUTH-4、R-VER-1 原列在規格的 16 條之中，因為有字面上比 Core 嚴格的句子而逐字保留（PR-4 決策卡 PR4-C1 (a)，DL-031 到 DL-033）。
- 已知代價：每個 skill 讀進的 bytes 估計約為現在的 1.5 到 1.85 倍；token 沒有量測。context 的優化（例如依 anchor 讀段落）之後依 FU-004 的量測決定。
- 與 D-001 的關係：D-001「日常執行只載入 `dev-core`」由本決策取代（PR-2 起生效）；Core 仍是唯一權威，`dev-core` 仍不放寬 Core。
- Core 回饋：是。CF-007（接口按階段讀取 Core 原文，不改寫成摘要）；兩處讀法作為 engineering-workflow-core#27 第 4、5 點的補充（由協調 session 起草，本專案不張貼）。

---

<a id="english"></a>

<details>
<summary>English</summary>

# claude-dev-skills design v1

Status: final (2026-10-20). See section 7 for the decisions. This English
version means the same as the Traditional Chinese version. If the two differ,
the Chinese version wins. This English text is written per ASD-STE100
principles; full conformance is not verified.

## 1. What the references contain

| Source | Core value | Not carried over directly |
| --- | --- | --- |
| `engineering-workflow-core` | Four Markdown contracts: the workflow stages (Discover → Plan → Implement → Verify → Review and Fix → Docs Sync → Delivery Gate → Continue), authority and stop conditions, independent review and security scans, and exact-head evidence | The long legal-style prose; the Codex Core snapshot assembler and installer (pinning itself is kept, see D-001) |
| `codex-dev-skills` | 27 skills, split into primitives (plan, implement, review) and formal gates; a loop ledger (spec, manifest, events, materialized state); class and tier routing for subagents; context continuity; deterministic evals | The Codex-specific runtime adapters (Desktop sidebar, CLI session handoff, TOML profiles), about 27k lines of Python, the installer, memory M0/M1, and the GitNexus adapter |

How the original project positions graph engineering (ADR OE-007):

- The first step is a typed graph projection only. It projects loops, tasks
  and evidence into a typed list of nodes and edges.
- It has no graph database and no execution engine. The projection is
  advisory. It cannot authorize anything or prove completion.
- The only graph logic actually implemented is the task manifest
  `dependencies` list: a task can become `ready` only after all of its
  dependencies are done.

## 2. Design principles (Claude version)

1. **Core is the only authority; dev-core is the compact execution version.**
   (Superseded by D-020: `dev-core` is the index of the vendored Core and
   the project's tightenings; each skill reads the original Core text for its
   stage.)
   Every Core obligation stays: DoD, independent review, finding
   dispositions, exact-head, authority and stop conditions, and the evidence
   lifecycle. Day-to-day work reads `dev-core`, a set of short rules and
   checklists that Claude can read in one pass. The compact form aims to cut
   repeated loading and the loss of attention in long text. The real context
   cost is not measured yet; D-011 measures it and compares it with
   codex-dev-skills. When the two conflict, the Core text wins (section 7).
2. **Use native Claude Code capabilities first; do not rebuild controllers.**
   Native capabilities include subagents (the Agent tool), worktree
   isolation, plan mode, the task list, hooks, `/code-review`,
   `/security-review`, Workflow multi-agent orchestration, and progressive
   disclosure of skills.
3. **When configuration can enforce a rule, do not rely on a prompt.** The
   Codex version can only declare a reviewer read-only. A Claude Code subagent
   can have Edit and Write removed by its `tools` allowlist. Reviewers keep
   Bash so they can run tests, so read-only Bash use still depends on
   instructions. This is not technical isolation (Core `review-independent`).
4. **State lives in repository files and Git.** Chat summaries, subagent
   reports and hook output are coordination data, not completion evidence.
5. **Build the graph in phases.** First a task graph file that can be
   validated, then projections and views, and only then graph-driven parallel
   execution.

## 3. Packaging and runtime

- Ship as a **Claude Code plugin**: `.claude-plugin/plugin.json` plus a
  marketplace. It contains `skills/`, `agents/`, and optionally `hooks/`.
- The same skills must work in **Cowork**. Skill bodies therefore must not
  depend on CLI-only tools. Mark any CLI-only capability and give a fallback.
- Scripts use the Python standard library (or Node) where possible, to avoid
  installed dependencies such as PyYAML. Graph files are JSON or a YAML
  subset.

## 4. Phase 1 skill set (MVP)

| Skill | Codex counterpart | Purpose |
| --- | --- | --- |
| `dev-core` | engineering-workflow-core contracts | (Superseded by D-020: now the index of the vendored Core and the project's tightenings.) The compact execution version of Core: stages, DoD, rigor tiers, authority and stops, finding format, evidence rules. Other skills cite it; it does not trigger on its own. It is not the authority; the vendored Core is |
| `dev-plan` | planning, closure-triage | Clarify the objective, scope, DoD, risk and slices; produce the task graph |
| `dev-implement` | implementation-slice | One bounded change: read, edit, verify, check the diff |
| `dev-review` | code-review(-deep), docs-review | Dispatch an **independent read-only reviewer subagent**; choose routine, deep or security review by risk; findings get stable IDs |
| `dev-gate` | *-gate, merge-review, merge-readiness-gate | Formal gate: binds the exact base and head, checks disposition completeness, and decides content, platform and authority separately |
| `dev-docs` | docs-update | Sync the docs with verified behavior and check that code and docs agree |
| `dev-continue` | task-continuation, milestone-continuation | Checkpoint, handoff and resume (rebuild from repository state; do not trust chat memory) |
| `dev-deliver` | project-delivery, project-orchestrator | Outer loop: pick the next step from the graph, dispatch, integrate, run the gates, stop at human gates |

Skills added after Phase 1 (not in the Phase 1 scope of D-008):

| Skill | Codex counterpart | Purpose |
| --- | --- | --- |
| `dev-retro` (added by D-019; implemented in PR-2) | — (see D-019) | Lessons: `capture` gives a level (L1 to L4) and outputs lesson drafts and cards; `review` reviews the lessons with new evidence and the rules that they point to. Only the user invokes it; it writes no file (skill rule; `disable-model-invocation` blocks only the Skill tool call; not a technical guarantee; see D-019); it supports only Claude Code |

### Subagents (`agents/`)

| Agent | Default model | Default effort | Tools | Role |
| --- | --- | --- | --- | --- |
| `dev-explorer` | haiku | low | Read tools and Bash (read-only by instruction) | Broad searches; returns conclusions only |
| `dev-implementer` | sonnet | medium | Can write; worktree recommended | Bounded implementation. Never commits or pushes; returns one structured receipt |
| `dev-reviewer` | opus | high | No Edit/Write; keeps Bash (read-only by instruction) | Routine and deep review |
| `dev-security-reviewer` | opus | xhigh | No Edit/Write; keeps Bash (read-only by instruction) | Changes to trust boundaries, permissions, data or dependencies; and the scan before every commit, push, PR post and Issue post (D-015) |

Shared brief contract: objective, ownership (paths), DoD, verification and
escalation conditions, plus one final receipt. Subagents have no
external-write authority. The main agent integrates and accepts the work.

#### Choosing the model and effort (see D-007)

There are two layers:

1. **Defaults** in the `agents/*.md` front matter (`model`, `effort`,
   `tools`), as in the table above.
2. **Per-dispatch overrides**: before each dispatch, `dev-deliver` and
   `dev-review` choose `model` and `effort` from this table and pass both. A
   dispatch that names only the model keeps the effort of the agent file. The
   brief states the reason (R-DEL-2, FU-018).

| Task type | Model | Effort |
| --- | --- | --- |
| Mechanical reads, finding files | haiku | low |
| General exploration, summaries | sonnet | medium |
| Implementation (`light`) | sonnet; opus for a cross-module or unclear slice | medium; high with opus |
| Implementation (`standard`) | opus; sonnet for a mechanical, clearly bounded slice in one module | high; medium with sonnet |
| Implementation (`strict`, or when the R-DEL-2 floor applies) | opus | high |
| Routine review | opus | high |
| Deep review, high-risk design, commit or push scan | opus | xhigh |
| Security review | opus | xhigh; max only when the user asks |

When the main session implements, the plan records the model and effort that
its transcript records, or `unknown` with the reason. The main agent does not
change its own model or effort; the user sets them in the app. For work under
the floor, when the main session's model is not opus, its effort is below
high, or either is `unknown`, the main agent asks the user to switch to
opus/high before it implements, or dispatches the
implementation to `dev-implementer` at opus/high; for other work, the plan
says when the effort is below this table. After one review and fix round that
did not solve the problem, the main agent classifies the failure. A failure
that the spec, the acceptance criteria or the design caused is not a quality
failure: it goes to the R-VER-2 stop rule and re-evaluation, and does not
escalate. Only a quality failure escalates, and only the side that fixes (the
implementer or the main session); reviewers keep this table. The steps are: effort first (low → medium → high), at high or more the model
(haiku → sonnet → opus), at opus the effort (xhigh, then max). An escalated
setting is not lowered for the rest of the node, no setting goes below the
floor, the round count is not reset and findings are not cleared. When the
evidence conflicts, for example two reviews of the same change disagree, the
main agent also re-assesses the model and effort; the re-assessment alone does
not escalate. Fable is not in the escalation order before an evaluation
(D-007 rule 4; FU-018 card 2 (c): evaluation deferred, tracked in FU-020).

## 5. Graph engineering

### 5.1 What the term means

"Graph engineering" is a community term, not an official Anthropic or
Karpathy term. It comes mainly from an independent synthesis that connects
three official sources: Karpathy's autoresearch loop and AgentHub idea,
Anthropic's Claude Code Dynamic Workflows, and Anthropic's Knowledge Graph
Construction Cookbook.

It comes down to three graph layers:

| Layer | Meaning | In this project |
| --- | --- | --- |
| **Execution graph** | Work is split into nodes (bounded jobs with an input and output contract) and edges (dependencies that real data crosses). Nodes without dependencies run in parallel. The typical shape is fan-out → reduce → verify → synthesize | The task graph (G0), run by Claude Code's native Agent and Workflow tools. **No self-written execution engine** |
| **Memory / knowledge graph** | Typed records with sources that persist across sessions. Later agents query only the relevant subgraph instead of rereading everything | Two graphs: **GitNexus for code** (1.6.12 is installed) and **an LLM Wiki format for requirements** (D-003) |
| **Governance graph** | Loops supervising loops: a verifier node in a clean context tries to disprove a result; every loop has a round limit | Independent reviewer nodes, gate nodes, human gate nodes |

### 5.2 Phases

| Phase | Deliverables | Done when |
| --- | --- | --- |
| **G0 Task graph + requirement anchors** | `.dev/<objective>/graph.json`: task nodes with `requirements: [REQ-…]`, owned paths, DoD, verification, review mode and risk; edges as `depends_on`. An append-only `events.jsonl`. `graph.py` (standard library only) validates the schema, detects cycles, computes the ready set, checks for overlapping ownership, runs the fake-edge test, and traces requirements (finds tasks that map to no REQ). Phase 1 also ships read-only GitNexus queries (`impact`, `detect-changes`; advisory results) and the `SCOPE-CREEP` finding (REQ-003, REQ-004) | `dev-plan` can produce a graph; `dev-deliver` advances through the ready set one node at a time (single writer); the validator has positive and negative fixtures |
| **G1 Code graph and requirement graph** | Connect the requirement graph, the task graph and GitNexus symbols: `graph.py render` outputs a Mermaid traceability graph (source → REQ → task, later extended to GitNexus symbols); review uses the trace to check scope drift systematically | A review can say which requirement a change serves and which symbols it affects |
| **G2 Graph-driven parallelism** | Tasks in the ready set with disjoint ownership become a Workflow script or parallel Agent calls with worktree isolation; the reducer is code; each fan-out is followed by a verifier node | Bounded parallel runs work; no two writers change the same file; dispatched and returned counts match |
| **G3 Evidence projection and self-improvement** | Verification, reviews, findings and commits also become typed nodes; an interactive HTML view (publishable as an Artifact) that includes finding and commit nodes; evals and improvement proposals (proposals only) | Provisional (revised from the real use of G0–G2 before G3 starts): the typed nodes for verification, reviews, findings and commits can be regenerated from Git and the review records; the HTML view can be regenerated from them and is never written back as a source; the improvement proposals from evals go to the user for a decision and are never applied automatically |

These rules come from D-009:

- G1, G2 and G3 are each one independent delivery: Issue → branch → review
  and scan → PR → Merge Review. The next stage starts only after the previous
  stage is merged.
- Before a stage starts, revise that stage's deliverables and done criteria
  in the table above from the real use of the previous stage.
- The output of each stage belongs to one of two layers:
  - **Runtime-neutral layer**: the graph and REQ schemas, `graph.py` and the
    fixtures. This layer must not depend on Claude-only tools, so that Codex
    and Grok can use it too.
  - **Claude-specific layer**: execution with Agent and Workflow. Codex and
    Grok can use it later as a reference, or it can go back to Core.
- In the current design, the stages split into these layers; revise this
  before each stage starts:
  - G1: `graph.py render` and the trace data are runtime-neutral; how a
    review uses the trace is Claude-specific.
  - G2: the ready set and the ownership checks are runtime-neutral; Workflow
    scripts, parallel Agent calls and worktree isolation are Claude-specific.
  - G3: the schema of the evidence nodes is runtime-neutral; the HTML view
    and the Artifact are Claude-specific.

Every graph file is coordination data only. It is not completion evidence.
Completion still rests on Git, verification results and independent review
(Core `exact-head-and-evidence.md`).

**Every graph rendering is a projection, not authority** (as in
codex-dev-skills OE-003). This includes the Mermaid traceability graph, the
HTML view, Artifacts and the Obsidian graph view. They are all regenerated
from the REQ files, `graph.json` and Git. They cannot authorize anything,
prove completion, or be written back as a source.

## 6. Deliberately not in Phase 1

- No installer; use the plugin marketplace.
- No model/effort routing engine or full matrix; only the table in section
  4, chosen per task by the main agent (D-007).
- No memory backend and no memory contract: project state lives in the
  repository; native memory is reference only (D-010).
- No event hash chain or fencing tokens; rely on Git history and a single
  writer for now, and re-evaluate when G2 needs parallelism. `graph.py
  transition` serializes writes with a file lock.
- No parallel writers: `dev-deliver` runs ready tasks one at a time; only
  read-only tasks (explore, review) may run in parallel. Parallel writers and
  worktree integration are G2.
- No Desktop or CLI session-control adapters; use the native session and
  worktree capabilities.
- D-019 (`dev-retro`, new scope after Phase 1) does not build: a lessons
  ledger or lessons file, a user-level lessons file, hooks, a schedule,
  model invocation of `dev-retro`, or a validator that checks lessons.

## 7. Decision record

### D-001 Relation to engineering-workflow-core: vendor and pin the original, add a compact execution version (decided, 2026-10-20)

**Background**

- Core is written as strict legal-style text to keep Codex from drifting.
- The user wants all three interfaces (Codex, Grok, Claude) to follow one
  authority.
- If Claude's compact version works well, the user wants to feed it back into
  Core.

**Decision: three layers**

| Layer | Content | Standing |
| --- | --- | --- |
| Core (vendored and pinned) | The original text in `vendor/engineering-workflow-core/`, locked to an immutable revision and digests | **The only authority**; it wins any conflict |
| `dev-core` | Compact rules for Claude; each rule cites a Core anchor, for example `workflow.md#wf-stages` | An execution summary. It may only rephrase, compress or tighten. It must not relax or remove obligations, and it must not create authority |
| Source map and coverage check | `skills/dev-core/source-map.md` plus a script | The script checks that every Core anchor has a matching rule, or a `not-applicable` entry with a reason; any gap fails validation |

- Day-to-day work loads only `dev-core`, to save context. (Superseded by D-020, in effect from PR-2: each skill reads the original vendored Core files for its stage; `dev-core` keeps the rules that are stricter than Core or Claude-specific and serves as an index.)
- At edge cases, in doubt, or when rules conflict, read the vendored Core text.

**Why Codex is not affected**

- Codex does not follow Core `main`; it uses the revision it pinned.
- A change merged into Core takes effect only after codex-dev-skills re-pins
  it and passes its own evals.
- Drift protection comes from each interface's adoption process. Core does
  not need to be frozen.

**Feeding back into Core**

1. Record every place where `dev-core` differs from Core as a delta, with its
   type (rephrase, compress or tighten) and the reason.
2. Collect evidence from real Claude use: missed steps, false completion,
   changes in context cost.
3. Once the effect is confirmed, open an issue in Core. There are two kinds
   of proposal:
   - **Additive (preferred)**: add a non-authoritative compact companion
     document to Core and leave the authoritative text unchanged. Codex and
     Grok may ignore it.
   - **Modifying**: change the authoritative text. codex-dev-skills and
     grok-build-dev-skills must each pin the candidate and pass their evals
     with no regression before it merges.
4. A merge into Core does not mean Codex or Grok adopted it. Each interface
   decides and verifies its own re-pin.
5. The feedback items and their evidence are in `docs/core-feedback.md`
   (REQ-019).

**Scope of this project for now**

- Do not modify engineering-workflow-core.
- Do not modify codex-dev-skills or grok-build-dev-skills.

### D-002 Language (decided, 2026-10-20)

- SKILL.md files and agents are written in English.
- The README and design documents are bilingual (Chinese and English). Agents
  select the skills as needed, but people can also invoke them by hand.
- The English version is at the end of this document.

### D-003 Requirement graph: the LLM Wiki format is the source; Graphify is an optional index (decided, 2026-10-20)

**Problem**: during development, Codex sometimes over-engineers and turns the
project's original requirements into generic ones.

**Decision**

- The single source of requirements is a Markdown wiki in the repository at
  `docs/requirements/`. It follows Karpathy's LLM Wiki principles:
  - Each requirement has a stable ID (`REQ-001`) in its front matter, along
    with `status`, `sources` and `non_goals`.
  - The body may use `[[wiki links]]` for reading. The formal relations
    between requirements are the typed relation fields (see the last item in
    this section).
  - An `index.md`, plus a `log.md` that records changes to the requirements.
  - Agents have three operations only: ingest (add a requirement), query
    (look one up) and lint (find contradictions, orphans and stale
    requirements).
- **Sources must be precise enough to locate**:
  - `sources` in the front matter is a list. Every entry has three fields:
    `type`, `locator` and `quote`.
  - `type` is one of `doc`, `chat`, `issue` or `commit`. Use `external` when
    the entry links back to a formal requirements system such as Jira,
    Confluence or a PRD.
  - `locator` is precise enough to find the original again: a file name plus
    a page or section anchor, a date, a URL, or a commit SHA.
  - `quote` is the verbatim original.
  - The model's own summary goes in the `Need` section of the body, stored
    apart from the originals and never mixed with them.
- **When sources conflict, keep both side by side**:
  - When sources contradict each other, keep both statements with their
    sources, set `status` to `conflict`, and let the user decide.
  - The agent must not pick a side or overwrite either one.
  - `graph.py` fails an unfinished write task that cites a requirement in
    `conflict`.
- **Superseded conclusions are not deleted**:
  - Set `status` to `superseded` and fill in `superseded_by` and
    `superseded_reason`.
  - Record every change in `log.md`.
- **Where and when the wiki is created**:
  - `dev-plan` creates the wiki inside each target project. It asks the user
    before creating it the first time.
  - The default path is `docs/requirements/`. A project can set another path
    with `requirements_dir` in `.dev/config.json`.
- **When the project already has a formal requirements system** (for
  example Jira, Confluence or a PRD):
  - The wiki is only an index; each entry links back to the original.
  - Confidential text must not leave the project. Do not copy it into other
    repositories, memory or external services.
  - When unsure whether text is confidential, record only the `locator` and
    do not copy the text.
- Why this approach:
  - Plain Markdown in Git can be read directly by Codex, Grok Build and
    Claude, with nothing to install.
  - Obsidian is only an optional viewer.
  - The results are deterministic, need no LLM extraction, and cost nothing
    extra.
- Graphify (Python, tree-sitter plus LLM semantic extraction) is an
  **optional index layer**, never the authority:
  - Its code AST graph overlaps with GitNexus.
  - Its document extraction needs an LLM, so its results are not
    deterministic.
  - Connect it to index `docs/requirements/` only when there are too many
    requirements for plain wiki lookups.
- **Mechanisms against over-engineering**:
  - Every task node must list `requirements: [REQ-…]`.
  - `graph.py` flags tasks that map to no requirement.
  - `dev-review` has a finding type called `SCOPE-CREEP`: any added
    abstraction, option, fallback or validator that maps to no requirement.
    It uses the Core dispositions.
  - This follows Core `wf-assumptions-and-options`: before you add
    substantial complexity, state the protection it alone provides.
- **Typed relations between REQs** (Phase 1):
  - The front matter has four relation fields: `depends_on`, `refines`,
    `conflicts_with` and `superseded_by`. Each value is a list of REQ IDs.
  - `graph.py validate` checks that these IDs exist and that `depends_on` has
    no cycle.
  - Obsidian's graph view may be used for browsing, but its links have no
    types. It is a reading aid only and cannot replace these fields.

### D-004 Proportionate rigor: tiers by risk (decided, 2026-10-20)

| Tier | When | What to do |
| --- | --- | --- |
| `light` | Low-risk, local change | Short plan, targeted tests, diff self-check, no graph file. Before a commit, push or PR it still needs an independent review and the commit gate |
| `standard` | A normal feature | Graph, one independent reviewer, finding dispositions, docs sync |
| `strict` | Security, data, migration, public contract, release | Early deep or security review, the exact-head gate, plus a human gate |

- The tier only sets how heavy the process is. It cannot lower Core
  obligations. For example, a risk that cannot be determined is never
  classified as low, and review is always independent.
- Write the reason for the tier in the plan.
- If `light` work is going to be committed, pushed or opened as a PR, it first
  needs an independent review and the `dev-gate` commit gate. Without both,
  stop before that action. A light change left uncommitted records "not
  independently reviewed" as residual risk (`dev-core` R-RIG-2).

### D-005 Native capabilities first (decided, 2026-10-20)

These jobs use Claude Code's native capabilities directly. The skills add
only what Core requires and the native capability lacks: finding IDs,
dispositions, requirement tracing and gate decisions. The documentation
records the mapping.

- Review and security review: `/code-review`, `/security-review`
- Code simplification: `/simplify`
- Planning: plan mode
- Isolation and multiple agents: worktrees, Agent subagents, Workflow
  orchestration
- Handoff: session handoff

### D-006 GitNexus integration (decided, 2026-10-20)

- **Query only**, through its CLI or MCP (`impact`, `detect-changes`,
  `context`).
- Results are advisory. When the index is stale or the tree is dirty, say so
  in the report.
- This project does not install, configure or update GitNexus, and does not
  change its hooks.

### D-007 Subagent model and effort chosen per task (decided, 2026-10-20)

**Decision**

- Subagents always use official Claude Code models.
- Each role sets a default `model` and `effort` in `agents/*.md`. The main
  agent overrides them per dispatch from the table in section 4.

**Basis for the choice** (aligned with Core `workflow.md#wf-delegation`)

- Choose by reasoning need, risk, context size and verification burden.
- Keep the default when it is enough. Do not always use the highest effort.
- Do not replace the real `effort` setting with prompts such as "think
  deeply".

**Rules**

1. **Use aliases, not hard-coded model IDs.** Write `haiku`, `sonnet`,
   `opus` or `fable`, not full IDs such as `claude-opus-5-5`. New models then
   need no skill changes, which also meets the Core rule against fixed
   permanent model IDs.
2. **No downgrade for high risk.** Security, data, migration and
   public-contract work uses at least opus with effort high. Cost or speed
   cannot lower this floor (carried over from the Codex routing rule that
   risk triggers cannot be offset).
3. **When to re-assess.** When one round of fixes does not solve the problem,
   or the evidence conflicts, the main agent re-assesses the model and
   effort. Raising effort does not fix environment or permission failures
   (Core `wf-verification`).
4. **Fable is not a default yet.** Its role and cost are untested, so it is
   optional only. Decide after evaluation whether to add it to the table.

**Limits**

- The main agent can only be sure of the model and effort it requested. It
  cannot fully read back from the conversation whether a subagent actually
  ran with those settings.
- Receipts therefore record the requested settings and the model and effort
  that the transcript records (FU-018; only these two values are copied), and
  do not claim they took effect. Anything that cannot be read back, and the
  effective setting, is marked `unknown`.

### D-008 Phase 1 scope (decided, 2026-10-20)

| Item | Content | Acceptance |
| --- | --- | --- |
| Core vendor | `vendor/engineering-workflow-core/` (v0.1.1, 14 files) plus `vendor/engineering-workflow-core.lock.json` | `scripts/verify_core.py` checks every file digest and the set digests; the 13-Markdown set digest equals the one in the codex-dev-skills lock |
| 8 skills | `dev-core`, `dev-plan`, `dev-implement`, `dev-review`, `dev-gate`, `dev-docs`, `dev-continue` and `dev-deliver` from the table in section 4 | Front matter rules hold; every `dev-core` rule cites a Core anchor |
| Source map, deltas, coverage check | `skills/dev-core/source-map.md`, `skills/dev-core/deltas.md`, `scripts/check_core_coverage.py` | All 21 Core anchors are `covered` or `not-applicable` with a reason; one gap fails |
| 4 agents | `dev-explorer`, `dev-implementer`, `dev-reviewer` and `dev-security-reviewer` from the table in section 4 | Reviewer agents have no write tools |
| G0 task graph | `skills/dev-plan/scripts/graph.py` (standard library only), plus `valid/` and `invalid/` under `tests/fixtures/graph/` | All positive fixtures pass; each negative fixture reports its expected error code |
| Requirements wiki templates and ingest | `REQ-template.md`, `index.md` and `log.md` in `skills/dev-plan/templates/`; `dev-plan` performs the ingest and writes the user's words verbatim into `sources` (type, locator, quote) | By default, `graph.py validate` looks for REQ files in the target project's `docs/requirements/` (or the `requirements_dir` in `.dev/config.json`); every REQ a task cites must exist as a file with a matching `id`, or validation fails |
| This project's requirements | `docs/requirements/`: the user's original requirements as REQ files, with verbatim `sources` and their locations | The first instance of the format; `index.md` and `log.md` are complete |
| Packaging | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `scripts/validate.sh` | One local command runs every check |

- The requirements wiki lives in each target project's own
  `docs/requirements/`. There is no separate requirements project.
- Whether `.dev/<objective-id>/` is committed is a project setting:
  `commit_state` in `.dev/config.json`. The default is `true`: the folder is
  committed with the work so another session can resume. Exception: once a
  PR exists, the review and gate records of its head never go into a commit
  on the PR branch (D-013 item 6). Only the JSON value
  `false` turns it off. Then the files under `.dev/<objective-id>/` are never
  staged, and the project should gitignore `.dev/*/` and keep
  `.dev/config.json` tracked. The folder must not contain secrets,
  credentials, private paths or raw logs. This repository's `.gitignore` lists the
  lock and temporary files; a target project adds `.dev/**/.graph.lock` and
  `.dev/**/.graph-*.tmp` to its own `.gitignore`. (User decision, 2026-10-20, PR #2 handoff item 6.)
- `scripts/check_pack.py` checks only the format of this repository's REQ files
  (fields and relation IDs). It is not the requirements lint; the lint for
  contradictions, orphans and stale requirements stays in Phase 2.
- The plugin name is `dev-skills`. `claude plugin validate` rejects
  third-party plugin names that start with `claude-`, so the repository keeps
  the name `claude-dev-skills` and the plugin has a different name. Install
  with `claude plugin install dev-skills@dev-skills`.
- Not in Phase 1: G1–G3, hooks, the requirements wiki lint script (moved to
  Phase 2; Phase 1 only defines the format and does the ingest), and a CI
  workflow. D-017 added CI later.

### D-009 Graph engineering in stages (decided, 2026-10-20)

- Origin: the user's decision of 2026-10-20. The requirement is REQ-002 (with
  the D-009 words added).
- The rules are in section 5.2:
  1. G1, G2 and G3 are each one independent delivery. The next stage starts
     only after the previous stage is merged.
  2. Before a stage starts, revise the design from the real use of the
     previous stage.
  3. Section 5.2 gives the deliverables and done criteria of each stage.
  4. The graph and REQ schemas, `graph.py` and the fixtures are the
     runtime-neutral layer and must not depend on Claude-only tools.
     Execution with Agent and Workflow is the Claude-specific layer.
- Core feedback: no for now. Reason: graph engineering is not in the Core
  contracts. The runtime-neutral layer takes shape only after G1. If it goes
  back to Core later, record it in `docs/core-feedback.md` through the D-001
  process.

### D-010 No agent memory (decided, 2026-10-20)

- Origin: the user's decision of 2026-10-20. The requirement is REQ-015.
- Build no memory backend and no memory contract.
- Project state lives in the repository: the REQ wiki, `graph.json`,
  `events.jsonl`, Git and the review records.
- Native memory is reference material only. When native memory conflicts with
  the repository, the repository wins. Native memory is never a requirement
  source, authority or completion evidence.
- `dev-core` R-AUTH-1 and R-AUTH-7 already treat memory as reference data, so
  no skill rule changes. Section 6 now says the same.
- Core feedback: no. Reason: Core already covers these rules: `auth-scope`
  keeps memory from overriding the instruction order, `wf-stages` makes
  session memory advisory, and `auth-data` says that native recall is not a
  qualified managed backend and that Core has no data backend. D-010 only
  records that this project builds no backend.

### D-011 Deploy and measure (decided, 2026-10-20)

- Origin: the user's decision of 2026-10-20, and the user's question on the
  same day about the context-cost sentence in principle 1. The requirement is
  REQ-016.
- Deployment: these steps are outside the repository, and the user does them.
  This PR records them and does not do them.
  1. Install the pack at user scope in Claude Code, for personal projects
     only. Cowork waits until FU-001 (GitHub Issue #3) is verified.
  2. Add a short note to `~/.claude/CLAUDE.md`: development tasks start with
     `dev-deliver` to choose the tier.
- Measurement plan:
  1. Pick 3 to 5 real tasks. Run each task once with the pack and once
     without it.
  2. Record four measures for each run: missed errors, changes outside the
     requirements, token use and time.
  3. Token comparison: run the same task once in claude-dev-skills and once
     in codex-dev-skills. Compare the token use, and count the reads of
     `dev-core` (in the Codex version, the Core reference files). The
     context cost in principle 1 is set from this result.
  4. Also check that the `tools` and `disallowedTools` of the plugin agents
     take effect at run time (a follow-up agreed on 2026-10-20).
  5. Token use and time come from the usage records of the platform. The
     agent does not estimate them, and it does not claim that it can read
     its exact context usage.
  6. The results decide what to strengthen or trim in the skills. Changes go
     through a new Issue and PR.
- The tracking entry is FU-004 in `.dev/followups.md`.
- `docs/core-feedback.md` records an evaluation of a split of `dev-core`: a
  short core that is always read, plus references for each stage that are
  read only when needed, as in the Codex version. Whether to implement it
  waits for the measurements; the user decides with a decision card (FU-005).
- Core feedback: no. Reason: deployment and measurement are work on the
  Claude side. The results become evidence for step 2 of the D-001 feedback
  process (`docs/core-feedback.md`).

### D-012 Automatic handoff (decided, 2026-10-20)

- Origin: the user's decision of 2026-10-20. The requirement is REQ-017.
- Rules (`dev-continue`):
  1. When a work item is complete, evaluate whether to switch to a new
     session. A work item is, for example, one graph node, one review and
     fix round, or one stage.
  2. The basis is the number of review and fix rounds, stage boundaries and
     the workload. Context usage is a reference only. The agent does not
     claim that it can read its exact context usage.
  3. When it decides to switch, it writes the checkpoint. Before a PR
     exists, it commits the checkpoint without asking first. D-012 is the
     user's decision; it covers this checkpoint commit and no other commit.
     The commit keeps every commit rule: the R-REV-9 scan first; with
     `commit_state` set to `false`, do not stage state files.
  4. Once a PR exists, the checkpoint is not committed, because a commit on
     the PR branch makes a new head, and the new head needs a new complete
     review (R-EXH-3). The checkpoint stays in the working tree, and its key
     points are posted as a PR comment so that another clone can take over.
     `dev-security-reviewer` scans the exact text before it is posted
     (R-REV-9); without that scan, it is not posted. The checkpoint points
     to the review and gate records and does not repeat them. This item is
     the user's answer to PR-C1 decision card 1; it covers this comment and
     no other comment.
  5. Then it offers a new-session card with a full handoff brief. The new
     session starts only after the user confirms.
  6. The handoff is complete when the user confirms; then the old session
     stops writing. Before the user confirms, or when the user declines, no
     handoff has happened and the old session continues.
- Difference from Core: Core `wf-stages` already requires a checkpoint before
  a pause and a re-read of the sources on resume, and prefers the original
  session when work resumes. D-012 adds only when to evaluate and the
  handoff steps; no `dev-core` rule changes. A D-012 switch happens only
  after the user confirms it; otherwise the original session continues.
- Core feedback: no. Reason: how to switch sessions depends on the session
  capabilities of each interface; Core `wf-stages` already covers the
  checkpoint and the resume.

### D-013 Review convergence (decided, 2026-10-20)

- Origin: PR #2 Merge Reviews 1 to 5 kept producing new findings and did not
  converge; Merge Reviews 6 and 7 had none. After round 2, PR-A (Issue #4) applied these rules early,
  re-evaluated its findings and removed the checks that no requirement
  covered (`.dev/issue-4-commit-security/reviews/round-2.md`). The
  requirement is REQ-012.
- Rules (`dev-core` R-REV-3, R-REV-4, R-VER-2, R-EXH-3):
  1. Severity thresholds: `MUST-FIX` only for Core blockers. When it is
     unclear whether an item is a Core blocker, it is `MUST-FIX`.
     `SHOULD-FIX` needs a reproducible failure that affects a requirement,
     the DoD or documented behavior. `NIT` is only a regression that this
     change causes, or false documentation. Everything else is residual
     risk, not a finding.
  2. Classify before fixing: each finding is a necessary fix, worth
     improving, keep as is, or needs human decision. A fix stays inside the
     requirements. A defect that the requirements did not foresee goes to
     the user first (see D-016). Exception: a Core blocker is fixed first.
     A management measure (a process,
     documentation or a manual check) is a valid fix when it names an owner,
     a verifiable premise and what happens when it fails.
  3. A new mechanism states its unique role and the requirement it serves;
     otherwise it is `SCOPE-CREEP`. `dev-core` R-RIG-3 already has this
     rule, so this PR does not change it.
  4. After the fixes and before a push, an independent reviewer confirms
     them in a narrow review. The complete Merge Review still covers the
     whole base..head range. Parts that are provably unaffected by every later
     change may reuse earlier evidence when the review records the reason and the coverage.
  5. When two consecutive review rounds still report new blockers, or the
     same mechanism needed fixes and produced new problems in two
     consecutive rounds, stop the fix loop and do not start the next fix
     round. The user added the second trigger in PR-B decision card 1. First re-evaluate the spec, the acceptance criteria and the
     approach, and take scope questions to the user as decision cards
     (D-014).
  6. Once a PR exists, the review and gate records of its head never go into
     a commit on the PR branch. A commit makes a new head, and a new head
     needs a new complete review: a structural loop. When the user has
     authorized the comment, the records go into a PR comment (scanned by
     R-REV-9 before posting); otherwise they stay uncommitted and go into
     the report to the user.
- Difference from Core: Core defines no severity thresholds, and Core treats
  two unfinished review rounds as a time to re-assess, not to stop. These
  are tightenings, recorded as DL-011, DL-012 and DL-013 in
  `skills/dev-core/deltas.md`. Every Core blocker stays `MUST-FIX`.
- Core feedback: yes. Reason: the Codex and Grok versions use the same Core
  and can meet the same non-converging reviews and the same loop from
  committed records; the thresholds and the stop rule do not depend on one
  interface.

### D-014 Format for human decisions (decided, 2026-10-20)

- Origin: the decisions that PR #2 and PR-A handed to the user had a
  different format each time. The requirement is REQ-013.
- Rules (`dev-core` R-AUTH-6, R-WRT-1):
  1. Every Needs Human Decision finding, and every decision handed to the
     user, uses a fixed decision card. Fields: the question (one sentence),
     why you must decide, the options (for each: what it does, the result,
     the risk, the cost), the recommendation and its reason, the consequence
     of no decision (what is blocked, what can continue), and the evidence
     (file and line, command output; facts apart from inferences).
  2. English follows the ASD-STE100 principles. Traditional Chinese uses the
     plain-writing adaptation of Core: one idea per sentence, an explicit
     subject, consistent terms, a plain explanation of each technical term at
     first use, no vague words, and no English word-count rules.
  3. Review and gate reports state "written per ASD-STE100 principles; full
     conformance not verified" and never claim STE conformance.
  4. The template and one positive example are in
     `skills/dev-review/references/decision-card.md`. The example is adapted
     from PR-A decision card 1 (scan PR text before posting or not).
- The output rules of `dev-review`, `dev-gate` and `dev-deliver` use the
  card.
- Difference from Core: Core lists what a decision request contains, but no
  fixed format. This is a tightening, recorded as DL-014.
- Core feedback: yes. Reason: this is a format question for Core
  `wf-writing` and `auth-stops`, and all three interfaces hand decisions to
  the user.

### D-015 Security review before every commit and push (decided, 2026-10-20)

D-009 to D-016 were decided on the same day. PR #5 (Issue #4) records
D-015; PR #7 (Issue #6) records D-013, D-014 and D-016; PR-C1 (Issue #8)
records D-009 to D-012.

- Origin: PR #2 SEC-01. The author and committer of all 10 branch commits were
  derived from the local account and the machine hostname, and the push
  published them. No content review checked commit metadata; the security
  scan before the merge found it. The requirement is REQ-011.
- Rule (`dev-core` R-REV-9): before every commit and every push, an
  independent `dev-security-reviewer` scans exactly what will be published.
  There is no exception for small or docs-only changes, and this scan is never
  `not applicable`.
  - Before a commit: the staged diff, and the author, committer (read with
    `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT`), message
    and trailers the commit will carry. Do not override the identity after
    the scan; read it back with `git log -1 --format=fuller` right after the
    commit.
  - Before a push: everything the push sends. The main agent runs
    `git push --dry-run --porcelain` with exactly the arguments of the real
    push, and then pushes with exactly those arguments. The scan covers every
    commit the remote does not have yet on each listed ref, with identities,
    messages and merge-resolution content, and the tagger and message of each
    listed annotated tag. Confirm that the recorded identity and message match
    what was scanned.
  - The scan shows content, not encoded data: every scan command uses
    `--text --no-textconv --no-ext-diff`.
  - Before posting a PR or MR title, body or comment, or a review record: the
    exact text. (Issue #12 adds Issue titles, bodies and comments; see FU-007
    and REQ-011.)
  - At merge readiness: every commit in base..head, not only the final diff,
    and the merge or squash commit that the platform will create: the merge
    method, author, message and trailers (for example `Co-authored-by:` lines
    built from the branch commits).
  - What to look for: keys, passwords, tokens, private files, private paths,
    machine hostnames, private email addresses, and real names the author has
    not chosen to publish. A finding blocks the commit or push until it is
    fixed and scanned again.
  - Any change to the staged content, identity, message or text after the
    scan is a new candidate and needs a new scan. The records of a scan and
    its gate never go into the commit they cover. They go into a later commit,
    whose own scan covers them, or into the PR. Once a PR exists, they never
    go into a commit on the PR branch (D-013 item 6 refines this).
  - Without `dev-security-reviewer`, stop before the commit or push.
- R-REV-1 clarification: a required security review or Security Diff Scan
  uses `dev-security-reviewer`, never `dev-reviewer`.
- Recommendation (not implemented in this PR): a secret scanner such as
  gitleaks in a pre-commit or pre-push hook, as an additional deterministic
  check, and `git config user.useConfigOnly true`, so that Git never guesses
  an identity from the hostname. Installing a tool or a hook, or changing Git
  config, needs the user's approval, and none of them replaces the
  independent review.
- Review reports are committed or posted to the PR too, so both reviewer
  agents mask secrets and private identifiers: they give only the kind,
  location and length or class; for an email, only whether it is a noreply
  address and its provider; for a path or hostname, a placeholder for the
  account or host part.
- Difference from Core: Core requires a Security Diff Scan only when a change
  touches a trust boundary. Here every commit and push needs the scan. This
  is a tightening, recorded as DL-010 in `skills/dev-core/deltas.md`.
- Core feedback: yes. Reason: in a public repository, every commit and push
  publishes content and metadata, whatever the interface. The evidence is
  PR #2 SEC-01 (see `docs/core-feedback.md`).
- The same PR fixes `graph.py transition --evidence-file`. It copied the
  content of any readable file into `events.jsonl`, which is committed by
  default. Now it accepts only a regular file inside the project root (the last
  component of the path must not be a symlink, and no FIFO or other
  non-regular file), and it records only the
  relative path and the SHA-256, never the content (the option the user
  chose, 2026-10-20). Remaining risk: the hash of a short, guessable secret
  file inside the project (for example a gitignored `.env`) is committed and
  can be guessed offline. For any regular file inside the project (including
  a file under `.git/` or a hardlink), only the path and hash are recorded,
  never the content. No requirement covers these cases, so they are not
  blocked separately (user decision, 2026-10-20). The tracking entry is
  FU-003 in `.dev/followups.md`.

### D-016 Review scope and requirements (decided, 2026-10-20)

- Origin: the PR-A re-evaluation after round 2. Each finding was first
  related to the requirements and then handled. Checks with no requirement
  behind them were removed, and the requirement gap became decision card 1.
  The requirement is REQ-014.
- Rules (`dev-core` R-REV-3; the brief rules and finding format of
  `dev-review`):
  1. A review looks for problems beyond the requirements, but every finding
     states its `requirement_relation`: `in-scope`, `gap`, `no-requirement`
     or `unrelated`.
  2. New finding category `REQ-GAP`: a problem that no requirement covers
     but one seemingly should. A `REQ-GAP` is not fixed in the same round. It
     becomes a decision card (D-014), and the user chooses: add a
     requirement, defer, or reject.
  3. Only the user adds requirements. After the user agrees, `dev-plan`
     ingests it as a new REQ, and its sources record the finding ID and the
     user's decision. An agent never turns a `REQ-GAP` into a requirement
     itself.
  4. `no-requirement` is `SCOPE-CREEP`. `unrelated` is residual risk or a
     follow-up and does not block the delivery.
  5. Exception: Core blockers (security, data loss, authorization,
     integrity) block for every `requirement_relation`. A missing
     requirement is no exemption.
- Difference from Core: Core does not relate findings to requirements. This
  is a tightening, recorded as DL-011.
- Core feedback: yes. Reason: Codex rewrote project requirements into
  generic ones (D-003); this field lets all three interfaces tell a fix
  inside the requirements from a scope expansion.


### D-017 Minimal CI (decided, 2026-10-21)

- Origin: after PR #11 merged, the user agreed to add minimal CI
  ("CI的部份也同意你的建議"). The requirement is REQ-020. Phase 1 excluded
  CI (D-008), so this is new scope.
- Purpose: every earlier review reported `platform_enforcement` as
  `NOT_CONFIGURED`, because the repository had no CI and no branch
  protection. CI runs `validate.sh` and a secret scan on the GitHub platform.
  Auto-fix also needs a CI result to act on.
- Design (`.github/workflows/ci.yml`):
  1. Triggers: every pull request to `main` and every push to `main`. No
     `pull_request_target`.
  2. Job `validate`: install the Claude CLI at an exact npm version (no
     login), then run `scripts/validate.sh`. `claude plugin validate` needs
     no login, so CI runs it too.
  3. Job `gitleaks`: download an exact gitleaks release, check it against a
     SHA-256 written in the workflow, then scan every commit reachable from
     the checked-out commit. On a pull request that commit is the merge
     commit, so the scan covers every commit of the PR. The output redacts
     secrets, because the log of a public repository is public. Limits: the
     patch of a merge commit is not scanned; a PR can change the workflow,
     `.gitleaks.toml` and `.gitleaksignore` and so change the scan; a value
     that CI finds is already public and must be rotated.
  4. Every action is pinned by full commit SHA, with the release tag in a
     comment. The workflow has only `permissions: contents: read`; checkout
     does not keep the token; no secrets are used.
- Platform result in `dev-gate` (R-EXH-4): a project selects a provider
  profile only through an explicit project setting (the user's decision
  Q3 (b)). This PR does not define that setting, so the result stays
  `NOT_CONFIGURED`. `dev-gate` reads the head and the checks of a PR in one
  call and lists each check; a failed read or another head gives
  `UNVERIFIED`.
- Review round 2 found new blockers in the profile read-back again
  (ES2-001 to ES2-003), and the stop rule applied. The user moved the
  profile setting to FU-009, designed together with FU-008 (a PR can weaken
  its own checks, ES-004) (Q5 (a)).
- After the merge, the user makes `validate` and `gitleaks` required checks;
  the steps are in the README section "CI".
- CI replaces no R-REV-9 independent scan: gitleaks reads commit content
  only, not the commit identity, the message or PR text.
- Core feedback: no. Reason: CI and provider profiles are overlays that each
  project selects (Core auth-scope and exact-dimensions). `dev-core` R-EXH-4
  only adds what the Core text already says: platform state without a
  current successful read-back is UNVERIFIED.

### D-018 Provider profile read-back (decided, 2026-10-21)

- Origin: FU-009 and FU-008 (the user's decision Q5 (a): design them
  together). The design was first written as a spec and threat model, had one
  independent design review (DR-001 to DR-008, ES0-001 to ES0-008), and the
  user approved it: "Q1 a。但 script 只實作規格列出的性質；review
  若找到規格以外的新邊界情況，一律做成需求缺口卡片交給我決定，不可直接加程式。Q2 a。"
  (the checker implements only the listed properties; a new edge case from a
  review becomes a REQ-GAP card for the user, never code). The requirement is
  REQ-021.
- Setting: `platform_profile` in `.dev/config.json` (provider `github`,
  repository, base branch, required check names with their GitHub App id).
  It is read only at the bound base commit, never at the PR head or in the
  working tree. A selected profile is a required profile. An invalid format,
  an unknown key or a duplicate key fails closed with a message.
- Read-back: the read-only checker `skills/dev-gate/scripts/platform_profile.py`.
  Every `gh` call uses `--hostname github.com` and the bound repository; only
  `success` passes; the required checks are the union of the profile and the
  platform rules (rulesets, all pages, and classic protection); each check is
  pinned to an app id; duplicate runs on one head are grouped by check suite
  and the newest of each must succeed; the head is read again at the end; the
  result is BLOCKED, then UNVERIFIED, then VERIFIED. Reason: the prose rules
  did not converge in two rounds; pagination, grouping and precedence are
  facts a machine can check (R-REV-8), and the negative cases are in
  `tests/test_platform_profile.py`, which CI runs.
- A PR that changes `.dev/config.json` makes a provider-policy change
  (R-AUTH-2): the gate gives the user a decision card, and the answer binds to
  the head blob of that file.
- FU-008 (report only, no block; Q2 (a)): GitHub runs the checks from the PR's
  own workflow, so with a profile `VERIFIED` always reads "checks ran this
  PR's own definitions", and the gate lists the files the PR changed under a
  fixed path list. The list is a hint: any file a check reads can weaken it.
- Not protected: a PR that weakens its own checks, a same-named check from the
  same GitHub App, admin or bypass merges, base drift with `strict` off, other
  ruleset rules, the truth of GitHub API answers, other forges.
- MR-001: `dev-core` R-EXH-4 states when the result is `NOT_CONFIGURED` and
  when it is `UNVERIFIED`.
- After implementation review round 1 the stop rule applied (the design
  review and implementation review round 1 both found new blockers). All
  three blockers were a false `NOT_CONFIGURED`. The user decided
  ("Q4 a；Q5 a；Q6 a"): one more fix round; without a profile, the PR's base
  is compared too; a checker failure or a missing result line is always
  `UNVERIFIED`.
- This repository's profile: `validate` and `gitleaks` from GitHub Actions
  (app 15368) on `main`, matching the ruleset read back on 2026-10-21. The
  base of this PR has no profile yet, so its merge gate reports
  `NOT_CONFIGURED` and gives the user a policy-change card for the new
  `.dev/config.json`; the first `VERIFIED` comes with the next PR.
- Core feedback: no. Reason: a profile is an overlay that each project
  selects (Core exact-dimensions); the `dev-core` difference is DL-015.

### D-019 Lessons skill `dev-retro` (decided, 2026-10-26)

- Origin: the user's messages of 2026-10-22 in a Claude Code session (PR #2
  Merge Review 5 orchestrator session). At 01:52 UTC (U1, U2):
  "是不是能變成一個主動的技能，日後發現問題時，可以主動學起來，自我改進。"
  "並且，隨著往後模型龻得更聰明、能力更強，新模型會自動Review這些記下來的規則或者技能，並建議適度的修改？"
  At 01:59 UTC (U3):
  "教訓只寫在這repo裡…只有該專案本身才知道…後續新加的b專案可能會再犯相同的錯。所以也要有個機制來識別教訓的層級。"
  (「龻得」 is in the original (sic; 變得); the ellipses mark original text
  that is left out; the original text is in the REQ-026 sources). After two deep review
  rounds of the design (the stop rule applied), the user answered the design
  cards D19-C1 to D19-C7: "C7 選 a；C1a C2a C3a C4a C5a；C6 先做 R-REV-9
  backlog PR"; C3 (a) answers REQ-GAP D1-013. After three rounds of security
  design review and deep review of the spec (the stop rule applied twice,
  cards D19-S1 and D19-S2), the user approved spec v4 (card D19-A1 (a)).
  The requirement is REQ-026. Phase 1 excluded this skill (D-008), so this
  is new scope.
- Problem: a lesson that a session finds stays in the report of that
  session, or in one project. The pack has no way to turn a lesson into a
  reviewed change. When there is new evidence (for example a newer model),
  it has no way to look again at the recorded lessons and the rules that
  they point to. It has no way to say which level a lesson belongs to, so a
  lesson that one project records can happen again in a project added later.
- Decision:
  1. A new skill `dev-retro` with two modes:
     `/dev-skills:dev-retro capture` and `/dev-skills:dev-retro review`
     (card D19-C1 (a)). Only the user invokes it: the front matter has
     `disable-model-invocation: true`, which blocks only the call through
     the Skill tool; no other skill invokes `dev-retro`. It writes no file,
     changes no record, does no Git write or publication, and invokes no
     other skill, MCP or network tool; the only exceptions are that review
     dispatches the read-only `dev-skills:dev-reviewer` and that the
     read-back command `git diff HEAD` can update `.git/index` (finding
     MS2-001). The front matter
     `disallowed-tools` removes Write, Edit and NotebookEdit; this is one
     defense layer, not a guarantee (Bash and other tools stay, and the
     restriction clears at the next user message). The output is only a
     report, draft text and cards. Before and after each run it records
     `git rev-parse HEAD` and the SHA-256 of
     `git --no-optional-locks status --porcelain=v1 --untracked-files=all`
     (so that `git status` does not update `.git/index`; finding MS2-001)
     and of `git diff HEAD --binary --no-ext-diff --no-textconv`; a
     difference is
     reported and voids that run. The limits: it does not see changes in the content of
     untracked files, ignored files, `.git`, or anything outside the repository, such as the user's
     instruction file; `git diff HEAD` can update `.git/index`; equal values do
     not prove that no write happened. Only Claude Code is supported, and README and
     `SKILL.md` say so (card D19-A3 (a)).
  2. The `dev-deliver` final report and the `dev-review` review report get
     a "Lesson candidates" section: new rule R-VER-5 and DL-035, a
     tightening of Core `workflow.md:74` for these two reports, not a new
     report system. The section is report content only: it writes no file,
     changes no rule and invokes no skill; a candidate is a proposal, never
     authority or completion evidence. When the user uses `dev-implement`,
     `dev-gate` or `dev-plan` directly, there is no such section (residual
     risk).
  3. Levels: L1 project, L2 this pack, L3 Core, L4 the user's own
     instructions. When the level is unclear, capture asks the user in a
     card; until the user decides, the draft stays in the report (card
     D19-C5 (a)). An L1 lesson and its reason stay in that project and
     never go into the `deltas.md` of this repository. L2 becomes a dev-plan
     requirement draft for this repository, and the reason of a `dev-core`
     rule a draft sentence for the `deltas.md` Reason and Evidence columns.
     L3 becomes a draft for `docs/core-feedback.md`; the user decides
     whether to report it. L4 is only one suggested line with the source
     category and the date; the user decides whether to add it to the
     user's own instruction file, and `dev-retro` does not write that file
     (cards D19-C2 (a), D19-A4 (a)). L4 text contains no authorization,
     permission, skipped confirmation, skipped review or scan, or automatic
     execution; for such a lesson the card says "this is an authorization
     change", and the user writes it.
  4. Sources and abstraction: a locator points only to the repository where
     the draft will be committed or posted. Text that leaves its source
     repository names only a category and a date, not the name, paths, PR
     or Issue numbers or finding IDs of the source repository. The result of
     the abstraction checklist (project names, customer names, internal
     system names, hosts, accounts, real names, email addresses, versions and
     vulnerability details) is a model self-assessment, not a review. No
     content of files outside the repository, of native memory or of
     automatically loaded instruction files is a source or goes into a
     draft; such content may already be in context, and the skill cannot
     stop it from loading. R-REV-9 does not check business secrets, so there are only two
     controls: the checklist and the user's word-for-word review. Every
     lesson text that will be committed or posted is shown word for word in
     a card; the real text is the same as the approved text, and any change
     is shown to the user again. Posting is a separate external write
     (R-AUTH-2) and comes after the R-REV-9 post scan. A lesson from a
     security problem that is not fixed is promoted or published only after
     the fix is released, with no exemption (card D19-S1 (a)).
  5. review runs only when the user invokes it; there is no schedule. Its
     scope is the lessons with new evidence that were not reviewed yet, the
     rules that they point to and the REQ sources of those rules; it reads
     only files of the current repository (card D19-C3 (a)). New evidence
     is a new lesson candidate, a recorded failure or a concern that the
     user names. A model change alone is not new evidence (Core
     `workflow.md:72`, `:99`); review then asks the user to confirm the
     scope. The reviewer is the read-only `dev-skills:dev-reviewer`
     (`opus`/`xhigh`), bound to the exact revision each time. Each
     suggestion has one of the four Core judgments; each suggestion that
     changes a rule, a skill, a REQ or a record is a card, also a "required
     fix". Neither capture, review nor a Lesson candidate suggests loosening a
     Core obligation or deleting a required check; a comment on Core becomes a core-feedback
     draft (REQ-019). A review result is not an approval and not completion
     evidence.
  6. A lesson becomes a rule only on one path: a card → the user's answer
     → the user's separate instruction → dev-plan (the REQ sources record
     the card ID and the user's words; for a card of another project, its
     category and date; abstracted words are marked "abstracted
     paraphrase") → implementation → independent
     review → R-REV-9 → PR → the user's merge decision. The options of each
     draft card are approve, defer and reject; only a deferred lesson
     becomes an FU row, with the required Deferred fields. No ledger, no
     lessons file, no user-level lessons file, no hooks, no schedule and no
     validator (card D19-C4 (a), Core `workflow.md:74`); D-010 does not
     change. This decision makes no rule change that comes from a lesson.
- Implementation: four sequential PRs; each starts after the previous one
  merges; the user decides each merge. Rigor tier `strict`: each PR has a
  deep review, an R-REV-7 security review, R-REV-9 scans and an exact-head
  gate. PR-1 records (REQ-026, this decision, sections 4 and 6, the
  requirements index and log, CHANGELOG); the PR-1 deep and security
  reviews also check the spec v4 additions that had no independent review,
  including:
  the three new R-VER-5 obligations (the item-by-item result of the
  abstraction checklist; each statement marked as fact, inference or
  unverified; the smallest fix narrows a claim or adds a management measure first), the
  PR-4 DoD value "not present", and in PR-2 Issue content that the user
  pastes as a capture input, the scope of the locator rule (REQ sources and body,
  CHANGELOG, `deltas.md`, commit messages), the card stating whether the
  answer also agrees to commit or post to the destination that it names,
  the `.git/index` exception of the no-write rule (narrowed in PR-2,
  finding MS2-001) and that a review result
  is not completion evidence, and in PR-4 the first review report in the
  PR description and the locator item of the DoD (card D19-S2 (a),
  condition 2). PR-2
  `skills/dev-retro/SKILL.md`, a `dev-core` stage map row and README (zh
  and EN); the implementer reads the official documentation again to
  confirm the names, syntax and effect of the two invocation control
  fields, and a failed read-back or a difference blocks PR-2. PR-3 R-VER-5,
  DL-035, a `skills/dev-core/source-map.md` row, the `dev-deliver` output
  and the reviewer report format. PR-4 first use: the user invokes capture
  for five recorded cases of this repository and then review; deferred
  lessons become FU rows; the judgments of cases (b) to (e) and the first
  review report, masked and abstracted, go into the PR description (card
  D19-A2 (a)).
- Not verified: the names, syntax and effect of the invocation control
  fields; whether claude.ai, the Skills API and Cowork support these two
  fields (where a platform does not, "invoked only by the user" rests on
  the skill text only); whether the native auto-memory reacts to "remember
  this" or saves lesson text by itself.
- Relation to REQ-005: the REQ-005 source says that the skills are mainly
  invoked by the agent as needed; `dev-retro` is invoked only by the user,
  an exception that the user chose (card D19-C1 (a)).
- Relation to REQ-001 and section 3 (`docs/design-proposal.md:32`,
  Cowork): `dev-retro` is a Claude Code-only exception chosen by the user
  (card D19-A3 (a)); the other skills keep the Cowork goal.
- Core feedback: no (inference, for the review to confirm). Reason: Core
  `workflow.md:74` already says that improvement is recorded in the
  existing report, with no new reflection executor, memory, hooks or
  scheduler. `dev-retro` applies no change and runs no candidate or
  comparison; it only outputs a report, drafts and cards when the user invokes it, so it is not a
  reflection executor. Core `docs/provenance/source-map.md:181` also says
  that an interface packages any automation with its own verification and
  authorization. The levels only decide where this pack records a lesson.
  There is one difference from the codex-dev-skills improvement contracts
  that Core cites: this pack publishes abstracted lesson text, and those
  contracts keep real proposals and evaluations private, with only
  synthetic fixtures in public Git. This reason records it; there is no
  separate CF item.

### D-020 On-demand loading of the original Core text (decided, 2026-10-22)

- Origin: FU-005 (REQ-025). The FU-010 audit (Issue #18, REQ-023) showed
  that the compressed `dev-core` does not converge in review: each of three
  rounds found Core conditions that the digest left out (R-VER-2 stop rule
  twice). The user: "壓縮的原因是因為任務一開始的時候以為技能包是一次全部載入。但其實可以像codex一樣設計成漸進式的按需載入。若是這樣，是否乾脆把原始的條文寫進來？"
  After three independent review rounds of the design spec (one of them a
  security design review; the stop rule applied twice), the user answered
  the design cards ("那先照你的建議。我想先完成移植和功能完善。後續再來針對這部份優化",
  "9b") and approved the spec ("核准 FU-005 規格"). D-019 is reserved for
  the lessons skill.
- Decision:
  1. Each skill reads the original vendored Core files for its stage; Core
     is not rewritten into a digest (card 1a). Whole files are read
     (card 2a). Every skill reads `authorization-and-stops.md` (card 3a):
     this removes the failure path "the text was not at hand"; it is one
     defense layer, not a guarantee.
  2. `dev-core` keeps 33 items word for word: the rules whose text carries
     a DL-row tightening, the rules with a sentence stricter than Core (also
     literally), the Claude-specific rules, and CB-1 to CB-5. The other 13
     rules later become index lines (rule ID plus Core anchor), so rule IDs
     and citations stay valid.
     R-AUTH-5 and R-VER-3 are among the 13: they become index lines that keep their
     project readings (item 3).
  3. Two Core sentences that can be read two ways get a written project
     reading (cards 5a, 5b, 9b): `authorization-and-stops.md:35` and
     `workflow.md:76` (R-AUTH-5, R-VER-3; DL-028, DL-029).
  4. Only the two reviewers get Core files, as review criteria (data), never
     as instructions; policy comes only from the brief; the implementer and
     the explorer get none (card 8a).
  5. FU-011 handles only restated text of the kept rules (card 6a). FU-012
     adds no `rationale.md`; the reasons stay in the Reason and Evidence
     columns of `deltas.md` and in the CB origin lines (card 6b, replaces
     FU-010 card 2a).
  6. Decided and implemented now; the FU-004 with-the-pack arm runs before
     PR-2 and after PR-4 (card 7′a, replaces the wait "Before FU-005 is
     decided").
- Implementation: four sequential PRs; each starts after the previous one
  merges (PR-2 also waits for the FU-004 baseline run); the user decides
  each merge. PR-1 records (REQ-025, this
  decision, DL-018 to DL-029, the two readings, CB origin lines, Core
  feedback statuses, FU rows); PR-2 adds a stage map to `dev-core` and the
  Core reads to each skill; PR-3
  lets the reviewers use Core as review criteria; PR-4 turns 13 rules into
  index lines. R-STG-4, R-AUTH-4 and R-VER-1 were among the 16 rules of the
  spec, but each has a sentence literally stricter than Core, so they stay
  word for word (PR-4 decision card PR4-C1 (a); DL-031 to DL-033).
- Known cost: the bytes each skill reads grow to an estimated 1.5 to 1.85
  times; tokens are not measured. Context optimization (for example reading
  by anchor section) follows the FU-004 measurements.
- Relation to D-001: D-001 "Day-to-day work loads only `dev-core`" is
  superseded by this decision (in effect from PR-2); Core stays the only authority, and `dev-core`
  still never relaxes Core.
- Core feedback: yes. CF-007 (interfaces read the original Core text by
  stage instead of rewriting it into a digest); the two readings as input
  for engineering-workflow-core#27 items 4 and 5 (drafted by the
  orchestrator session; this project posts nothing).

</details>
