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

1. **Core 是唯一權威；dev-core 是精簡的執行版。** Core 的義務全部保留：DoD、獨立 review、finding disposition、exact-head、授權與停止條件、證據生命週期。日常執行讀 dev-core，它是 Claude 一次讀得完的短規則加檢查清單。法條式重複是 Codex 版最大的 context 成本。兩者衝突時以 Core 原文為準（見第 7 節）。
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
| `dev-core` | engineering-workflow-core 契約 | Core 的精簡執行版，涵蓋階段、DoD、風險分級、授權與停止、finding 格式、證據規則。其他技能引用它，它不單獨觸發；它不是權威，權威是 vendor 的 Core |
| `dev-plan` | planning, closure-triage | 釐清目標與 scope、DoD、風險、切片，產出 task graph |
| `dev-implement` | implementation-slice | 單一有界修改：讀、改、驗證、自查 diff |
| `dev-review` | code-review(-deep), docs-review | 派**獨立的唯讀 reviewer subagent**，依風險選一般／深入／安全審查；finding 帶穩定 ID |
| `dev-gate` | *-gate, merge-review, merge-readiness-gate | 正式關卡：exact-head base/head 綁定、disposition 完整性。content、platform、授權三者分開判定 |
| `dev-docs` | docs-update | 依已驗證行為同步文件，檢查 code 和 docs 是否一致 |
| `dev-continue` | task-continuation, milestone-continuation | checkpoint、交接、接續（從 repo 狀態重建，不信聊天記憶） |
| `dev-deliver` | project-delivery, project-orchestrator | 外層編排：依 graph 選下一步、派工、整合、跑 gate，碰到人類關卡就停 |

### Subagents（`agents/`）

| Agent | 預設模型 | 預設思考深度 | 工具 | 角色 |
| --- | --- | --- | --- | --- |
| `dev-explorer` | haiku | low | 唯讀 | 大範圍查讀，只回結論 |
| `dev-implementer` | sonnet | medium | 可寫，建議 worktree | 有界實作。不 commit、不 push，回傳一份結構化 receipt |
| `dev-reviewer` | opus | high | 沒有 Edit/Write；保留 Bash（唯讀靠指示） | 一般與深入 review |
| `dev-security-reviewer` | opus | xhigh | 沒有 Edit/Write；保留 Bash（唯讀靠指示） | 涉及信任邊界、權限、資料、依賴的變更 |

共用 brief 契約：目標、ownership（路徑）、DoD、驗證、升級條件，加上一份最終 receipt。子代理沒有外部寫入權；主代理負責整合與驗收。

#### 模型與思考深度的選擇（見 D-007）

設定分兩層：

1. **預設值**：寫在 `agents/*.md` 的 frontmatter（`model`、`effort`、`tools`），也就是上表的預設欄位。
2. **逐次覆寫**：`dev-deliver` 和 `dev-review` 派工時，依下表另外指定 `model` 和 `effort`。

| 任務類型 | 模型 | 思考深度 |
| --- | --- | --- |
| 機械查讀、找檔案 | haiku | low |
| 一般探索、摘要 | sonnet | medium |
| 有界實作 | sonnet；跨模組或需求模糊時用 opus | medium／high |
| 一般 review | opus | high |
| 深入 review、安全 review、高風險設計 | opus | xhigh 或 max |

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
| **G3 Evidence projection 與自我改進** | 驗證、review、finding、commit 也成為 typed node；互動式 HTML 視圖（可發佈為 Artifact），包含 finding 與 commit 節點；evals 與改善提案（只產出提案） | 待 G0–G2 實際使用後再定 |

每個 graph 檔案都只是協調資料，不能當完成證據。完成仍以 Git、驗證結果、獨立 review 為準（Core `exact-head-and-evidence.md`）。

**所有圖形呈現都只是投影，不是權威**（同 codex-dev-skills OE-003）。包括 Mermaid 追溯圖、HTML 視圖、Artifact 與 Obsidian graph view。這些投影都從 REQ 檔、`graph.json` 與 Git 重新產生，不能拿來授權、證明完成，或回寫成來源。

## 6. 刻意不做（Phase 1）

- 不做 installer：改用 plugin marketplace。
- 不做 model/effort 路由引擎或完整矩陣：只用第 4 節那張對照表，由主代理依任務挑選（D-007）。
- 不做 memory backend：使用 Claude Code 原生 memory 與 repo 檔案。
- 不做事件 hash chain 和 fencing token：先靠 Git 歷史加單一 writer；G2 需要並行時再評估。`graph.py transition` 以檔案鎖序列化寫入。
- 不做並行 writer：`dev-deliver` 依序執行 ready 的 task；只有唯讀的 task（探索、review）可以並行。並行 writer 與 worktree 整合屬 G2。
- 不做 Desktop／CLI session 控制適配：直接使用原生 session 和 worktree 能力。

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

- 日常執行只載入 `dev-core`，以節省 context。
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
- 因此 receipt 只記錄要求的設定，不宣稱已驗證生效；無法驗證的部分標為 `unknown`。

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
- `.dev/<objective-id>/` 預設隨工作一起 commit，讓其他 session 可以接續；裡面不得寫入 secrets、憑證、私有路徑或原始 log。lock 與暫存檔已列入 `.gitignore`。專案也可以選擇把整個 `.dev/` 列入 gitignore。
- `scripts/check_pack.py` 只檢查本 repo REQ 檔的格式（欄位與關係 ID），不是需求 lint；矛盾、孤兒與過期需求的 lint 仍在 Phase 2。
- Plugin 名稱是 `dev-skills`。`claude plugin validate` 不接受以 `claude-` 開頭的第三方 plugin 名稱，所以 repo 名稱維持 `claude-dev-skills`，plugin 改名。安裝指令為 `claude plugin install dev-skills@dev-skills`。
- 不在 Phase 1：G1–G3、hooks、需求 wiki 的 lint 腳本（留到 Phase 2；Phase 1 只定格式並做 ingest）、CI workflow。

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
   Every Core obligation stays: DoD, independent review, finding
   dispositions, exact-head, authority and stop conditions, and the evidence
   lifecycle. Day-to-day work reads `dev-core`, a set of short rules and
   checklists that Claude can read in one pass. The repeated legal-style text
   was the largest context cost in the Codex version. When the two conflict,
   the Core text wins (section 7).
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
| `dev-core` | engineering-workflow-core contracts | The compact execution version of Core: stages, DoD, rigor tiers, authority and stops, finding format, evidence rules. Other skills cite it; it does not trigger on its own. It is not the authority; the vendored Core is |
| `dev-plan` | planning, closure-triage | Clarify the objective, scope, DoD, risk and slices; produce the task graph |
| `dev-implement` | implementation-slice | One bounded change: read, edit, verify, check the diff |
| `dev-review` | code-review(-deep), docs-review | Dispatch an **independent read-only reviewer subagent**; choose routine, deep or security review by risk; findings get stable IDs |
| `dev-gate` | *-gate, merge-review, merge-readiness-gate | Formal gate: binds the exact base and head, checks disposition completeness, and decides content, platform and authority separately |
| `dev-docs` | docs-update | Sync the docs with verified behavior and check that code and docs agree |
| `dev-continue` | task-continuation, milestone-continuation | Checkpoint, handoff and resume (rebuild from repository state; do not trust chat memory) |
| `dev-deliver` | project-delivery, project-orchestrator | Outer loop: pick the next step from the graph, dispatch, integrate, run the gates, stop at human gates |

### Subagents (`agents/`)

| Agent | Default model | Default effort | Tools | Role |
| --- | --- | --- | --- | --- |
| `dev-explorer` | haiku | low | Read-only | Broad searches; returns conclusions only |
| `dev-implementer` | sonnet | medium | Can write; worktree recommended | Bounded implementation. Never commits or pushes; returns one structured receipt |
| `dev-reviewer` | opus | high | No Edit/Write; keeps Bash (read-only by instruction) | Routine and deep review |
| `dev-security-reviewer` | opus | xhigh | No Edit/Write; keeps Bash (read-only by instruction) | Changes to trust boundaries, permissions, data or dependencies |

Shared brief contract: objective, ownership (paths), DoD, verification and
escalation conditions, plus one final receipt. Subagents have no
external-write authority. The main agent integrates and accepts the work.

#### Choosing the model and effort (see D-007)

There are two layers:

1. **Defaults** in the `agents/*.md` front matter (`model`, `effort`,
   `tools`), as in the table above.
2. **Per-dispatch overrides**: `dev-deliver` and `dev-review` set `model`
   and `effort` for each dispatch from this table.

| Task type | Model | Effort |
| --- | --- | --- |
| Mechanical reads, finding files | haiku | low |
| General exploration, summaries | sonnet | medium |
| Bounded implementation | sonnet; opus when cross-module or the requirements are ambiguous | medium / high |
| Routine review | opus | high |
| Deep review, security review, high-risk design | opus | xhigh or max |

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
| **G3 Evidence projection and self-improvement** | Verification, reviews, findings and commits also become typed nodes; an interactive HTML view (publishable as an Artifact) that includes finding and commit nodes; evals and improvement proposals (proposals only) | To be defined after G0–G2 are in real use |

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
- No memory backend; use Claude Code's native memory and repository files.
- No event hash chain or fencing tokens; rely on Git history and a single
  writer for now, and re-evaluate when G2 needs parallelism. `graph.py
  transition` serializes writes with a file lock.
- No parallel writers: `dev-deliver` runs ready tasks one at a time; only
  read-only tasks (explore, review) may run in parallel. Parallel writers and
  worktree integration are G2.
- No Desktop or CLI session-control adapters; use the native session and
  worktree capabilities.

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

- Day-to-day work loads only `dev-core`, to save context.
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
- Receipts therefore record the requested settings and do not claim they took
  effect. Anything that cannot be verified is marked `unknown`.

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
- `.dev/<objective-id>/` is committed with the work by default so another
  session can resume. It must not contain secrets, credentials, private paths
  or raw logs. The lock and temporary files are in `.gitignore`. A project may
  choose to gitignore `.dev/` instead.
- `scripts/check_pack.py` checks only the format of this repository's REQ files
  (fields and relation IDs). It is not the requirements lint; the lint for
  contradictions, orphans and stale requirements stays in Phase 2.
- The plugin name is `dev-skills`. `claude plugin validate` rejects
  third-party plugin names that start with `claude-`, so the repository keeps
  the name `claude-dev-skills` and the plugin has a different name. Install
  with `claude plugin install dev-skills@dev-skills`.
- Not in Phase 1: G1–G3, hooks, the requirements wiki lint script (moved to
  Phase 2; Phase 1 only defines the format and does the ingest), and a CI
  workflow.

</details>
