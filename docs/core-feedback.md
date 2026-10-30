# Core 回饋紀錄

[繁體中文](#zh-tw) · [English](#english)

<a id="zh-tw"></a>

狀態：持續更新的紀錄（最後更新 2026-10-30，依 main `41f7256` 的內容）。英文版在文末，與中文版同義；兩者不一致時以中文版為準。

## 用途

`engineering-workflow-core`（以下簡稱 Core）是 codex-dev-skills、grok-build-dev-skills 與 claude-dev-skills 共用的核心流程。本專案的修改如果是 Core 層級的問題，就記在這裡，讓 Core 可以採用，另外兩個專案再自行重新 pin（REQ-019）。

- 流程依 `docs/design-proposal.md` 的 D-001：增量型提案優先，也就是在 Core 新增非權威的伴讀文件，權威原文不動。修改型提案要先讓 codex-dev-skills 與 grok-build-dev-skills 各自 pin 候選版本並跑過 evals。
- 本文件只是紀錄。本專案不修改 Core、codex-dev-skills 或 grok-build-dev-skills。到 Core 開 Issue 或留言，每一則都需要使用者另外授權。
- 依據的 Core 版本：v0.1.1（commit `7b66978a76597d09be1b55ad199a969b4ee59c0f`）。行號依 v0.1.1。
- 上游狀態（2026-10-30 讀取）：CF-001 到 CF-006 與 CF-009 對應的 `engineering-workflow-core#21` 到 `engineering-workflow-core#27`（2026-10-22 開立）都還是 open，沒有維護者回覆；唯一的留言是本專案在 `engineering-workflow-core#27` 補充第 4、5 點的讀法（2026-10-22）。Core 的 main 仍是 v0.1.1，之後沒有新的 tag 或 PR。所以上游沒有任何變化影響本文件的項目。
- 本文件中的「Issue #n」與「PR #n」指 claude-dev-skills 的 Issue 與 PR；上游 Issue 寫成 `engineering-workflow-core#n`。

## 總覽

| 項目 | 上游 | 狀態（2026-10-30） | 下一步 |
| --- | --- | --- | --- |
| CF-001 Review 收斂 | `engineering-workflow-core#21` | 已提出；新增證據，新增第 4、5 點（候選） | 留言草稿，等使用者核准 |
| CF-002 commit 與 push 前的掃描 | `engineering-workflow-core#22` | 已提出；新增範圍與遮蔽格式（候選） | 留言草稿，等使用者核准 |
| CF-003 有寫入工具的替代者 | `engineering-workflow-core#23` | 已提出；新增證據 | 無 |
| CF-004 `requirement_relation` | `engineering-workflow-core#24` | 已提出；沒有變化 | 無 |
| CF-005 決策卡片 | `engineering-workflow-core#25` | 已提出；沒有變化 | 無 |
| CF-006 機制對應需求 | `engineering-workflow-core#26` | 已提出；新增證據 | 無 |
| CF-007 Context 載入方式 | 未提出 | 歷史紀錄：本專案已用 D-020 實作 | 併入 `engineering-workflow-core#27` 第 7 點的留言 |
| CF-008 每條規則只寫一處 | 未提出 | 本專案已部分實作 | 併入 `engineering-workflow-core#27` 第 7 點的留言 |
| CF-009 Core 用語問題 | `engineering-workflow-core#27` | 已提出；第 4、5 點已留言；第 2、6 點有新結果；新增第 8 到 10 點（候選，第 10 點含三處） | 留言草稿，等使用者核准 |
| CF-010 確認與轉述 | 未提出 | 候選 | 等 FU-041 驗證 host 怎麼顯示加進 session 的文字 |
| CF-011 事先寫好的分級 | 未提出 | 候選 | 使用者決定是否提出 |
| CF-012 subagent 怎麼取得 Core | 未提出 | 候選 | 使用者決定是否提出 |

## 項目

### CF-001 Review 收斂：嚴重度門檻、停止規則、紀錄不產生新 head

- 來源決策：D-013（REQ-012）；delta DL-011、DL-012、DL-013。第 4 點：Issue #68、#73、#77、#78 的停止卡片。第 5 點：FU-018（PR #51，REQ-009 卡片 C2a）。
- 問題：Core 沒有定義嚴重度門檻。Core 把連續兩輪未完成的 review 當成重新評估的時機，不是停止。Core 也沒有規定 PR 建立後 review 紀錄要存在哪裡；紀錄 commit 到 PR 分支會產生新的 head，新的 head 又需要完整審查，形成循環。
- 證據：
  - PR #2 的 Merge Review 1 到 5 一直出現新的 finding；Merge Review 6 與 7 沒有 finding。`merge-review-1.md` 到 `merge-review-4.md` 隨修正一起 commit（c72c64d、c934a29、eb8e08a、2280228），每次都產生新的 head（`.dev/handoff/pr-2-checkpoint.md`）。
  - PR-A（PR #5）第 2 輪後的重新評估移除了沒有需求對應的檢查（`.dev/issue-4-commit-security/reviews/round-2.md`）。
  - PR-B（PR #7）的 Merge Review 連續兩次被擋（MR-B-001 與 MR-B-002，接著是 MR2-B-001）。停止規則因此觸發，使用者用決策卡片 2 決定修正（PR #7 的 comment）。
  - PR #19（Issue #18）：同一機制連續兩輪出現新的阻擋項，停止規則觸發兩次（`engineering-workflow-core#21` 已引用）。
  - 之後停止規則又觸發多次：D-019 的設計與規格審查、D-020 的規格審查、Issue #68 第 2 輪（D-021）、Issue #73 第 2 輪（`.dev/issue-73-model-routing/reviews/round-2.md` 的 Stop rule 段）、Issue #77 設計審查第 2、3 輪（D-024）、Issue #78 設計審查第 3 輪（D-025）。出處是 `docs/design-proposal.md` 各決策的來源與審查紀錄。
  - FU-023（未解）：PR 建立之前 commit 的 round 紀錄，也會成為 base 到 head diff 的一部分；Merge Review 找到只和紀錄有關的阻擋項（PR #30 的 MR30-002；PR #34 的 MR34-001、MR34-RC-001）。所以第 3 點的問題不只在 PR 建立之後。
- 提議的 Core 修改：
  1. 在 `review-and-security.md#review-findings` 加上嚴重度門檻。
  2. 在 `workflow.md#wf-verification` 加上停止規則。
  3. 在 `exact-head-and-evidence.md#exact-transition` 規定 PR 建立後的紀錄不 commit 到 PR 分支。
  4. 停止之後的做法（候選，2026-10-30）：Core `workflow.md:72` 只要求兩輪未完成的 review/fix 觸發重新評估，「並非自動停工」；停止規則是第 2 點的提議。本專案的 R-VER-2 規定停止修正、重新評估，並用決策卡片交使用者決定，但沒有說停止之後可以怎麼做。本專案的停止至少有七次用了同一個做法（依 `docs/design-proposal.md` 與 `.dev/` 的搜尋結果，可能還有更多）：把反覆出問題的機制移到 follow-up、另一個 Issue 或殘餘風險，其餘部分照常交付。早期的三次：D-017（Issue #12；profile 設定移到 FU-009）、Issue #18（`--prune` 規則移到 FU-014，卡片 8a）、FU-015 PR-2（Issue #48；卡片 PR2-R2-C1 (a)，`+`／`-` 檢查移到 FU-019）。近期的四個 Issue 中，有兩個（#68、#73）是使用者先同意再做一輪限定範圍的修正，並事先約定：同一個機制再出現新的阻擋項就移出。近期的實例：Issue #68（卡片 I68-R2-C1 事先約定；第 3 輪的 R3-001 之後改走回退 (c)，綁定機制移到 Issue #71）；Issue #73（卡片 I73-R2-C1 (a) 事先約定；第 3 輪的下限檢查時機 finding 移到 FU-035）；Issue #77（停止卡 I77-R2-C1 (a)、I77-R3-C1 (a)；讀回 gate 直接移到 Issue #79）；Issue #78（第 3 輪第一次停止，卡片 I78-R3-C1 (c)；D-025 第 3、8、9 項構成的從嚴機制移到 FU-044）。範圍的改變每次都是使用者的決定。Core `workflow.md:62` 是在缺能力時要求不降低 DoD；本專案的判斷是：使用者決定的範圍改變不是那種情形。建議：在 `workflow.md#wf-verification` 的停止規則加上這個做法，作為交給人決定的選項之一。本專案的 `dev-core` R-VER-2 還沒有這一句（推論：先在本專案寫成規則再提出，證據會更完整）。
  5. 規格或設計造成的失敗不是品質失敗（候選，2026-10-30）：Core `workflow.md:72` 把服務、認證、環境、資料、權限及 context 的失敗和品質返工分開，並說提高 effort 不能解決環境或權限缺失。它沒有說規格、驗收條件或設計造成的失敗屬於哪一類。本專案的 `dev-core` R-DEL-2 寫明：這種失敗不是品質失敗，要走停止規則與重新評估，不升級 model 或 effort（FU-018，REQ-009 卡片 C2a）。證據：FU-018 的評估（PR #2 到 #49 的彙總）中，116 個阻擋項有 52 個是品質問題，64 個是規格或機制問題（`.dev/followups.md` FU-018 列）。建議 Core 在同一段寫明這一類。
- 類型：第 1 到 3 點是修改型（停止規則與紀錄位置會改變義務），可以先用增量型伴讀文件試行。第 4 點是增量型（交給人決定的一個選項）。第 5 點是修改型（新增一個失敗分類）。
- 對其他專案的影響：codex-dev-skills 與 grok-build-dev-skills 採用後，review 輪數可能減少；兩者都要檢查自己的 gate 與紀錄流程。在它們重新 pin 之前沒有影響。
- 狀態：第 1 到 3 點已提出（`engineering-workflow-core#21`，2026-10-22）。第 4、5 點與新增的證據，已起草為 `engineering-workflow-core#21` 的留言，還沒有張貼；張貼需要使用者核准。

### CF-002 每次 commit 與 push 前的安全審查，包含 commit 中繼資料

- 來源決策：D-015（REQ-011）；delta DL-010。新增範圍：D-015（merge 時的範圍掃描）、FU-015、FU-017、D-021。遮蔽格式：DL-016（R-REV-8）。
- 問題：Core 只在變更碰到信任邊界時要求 Security Diff Scan。在公開 repo 中，每次 commit 與 push 都會公開內容，也會公開作者、committer 與訊息。
- 證據：
  - PR #2 的 SEC-01。分支上 10 個 commit 的作者與 committer 由本機帳號與主機名稱推導出來，push 後已經公開；內容審查沒有檢查中繼資料（`.dev/issue-1-phase1/reviews/security-review-merge.md`）。
  - merge 時的範圍掃描：D-015 從一開始（PR #5）就要求 merge 前掃描每個 commit，以及 merge 或 squash 產生的 commit（DL-010）；`engineering-workflow-core#22` 的本文沒有寫到這一項。
  - 之後的結果（CHANGELOG 的 Security 段）：簽章可能帶有標頭沒有顯示的名字或 email（x509 憑證、OpenPGP 簽署者 ID；FU-017，Issue #54）。`.mailmap`、replace refs、`log.showSignature` 等設定會改變掃描看到的內容（FU-015 PR-1，Issue #46）。fetch 與 push 的 URL 可能不同，所以掃描讀的 repo 不一定是 push 送往的 repo（FU-015 PR-2，Issue #48）。
  - D-021（Issue #68）：為了降低掃描成本而設計的證據綁定，讓任何人都能離線確認猜到的身分（R3-001：公開的 nonce 加上報告中的 binding 行，可以驗證猜測的 email）。使用者選回退 (c1)：push 一律做完整掃描，只加一道確定性預檢，綁定程式移除。
  - 公開紀錄的遮蔽：PR #5 的 SR-A-008 發現遮蔽規則只寫在一處、定義也不清楚，之後改成固定格式（DL-016）。FU-003：`graph.py transition --evidence-file` 會 commit 專案內一般檔案的路徑與 SHA-256；可以猜的短秘密，能從公開的 hash 離線猜出。使用者在 2026-10-20 決定不加額外的檢查，這是本專案接受的殘餘風險。
- 提議的 Core 修改：
  1. 在 `review-and-security.md#review-security` 規定公開 repo 的每次 commit、push，以及 PR 與 Issue 文字都要掃描，範圍包含身分、訊息與 trailer。
  2. 範圍補充（候選，2026-10-30）：merge 前掃描整個範圍的每個 commit，以及 merge 或 squash 產生的 commit；commit 與 tag 的簽章；用不受設定影響的檢視來掃描（例如不套用 `.mailmap` 與 replace refs）；push 前確認掃描讀的 remote 就是 push 送往的 remote。
  3. 公開紀錄的遮蔽格式（候選，2026-10-30）：Core `authorization-and-stops.md:52` 要求公開記錄只保留安全的來源、必要限制與可追溯資訊，但沒有遮蔽格式。建議在伴讀說明中給一個格式：只寫值的種類、位置與長度或類別；email 只寫是不是 noreply 與提供者；路徑或主機名稱的帳號或主機部分用代號取代；不貼含有這些值的原始輸出。另外，私人值的 hash 或 binding 可以靠猜測驗證（D-021 的 R3-001、FU-003）。本專案的 R-REV-8 與 DL-016 沒有「不公開私人值的 hash」這條規則，FU-003 的 hash 是接受的殘餘風險；所以這一句是給 Core 的觀察，不是本專案的做法。要不要在上游提出這一句，由使用者決定。
- 類型：第 1、2 點是修改型（新增義務）。第 3 點是增量型（格式放在伴讀文件）。
- 對其他專案的影響：Codex 與 Grok 的 commit 與 push 步驟要加上這項掃描。第 2 點的檢查依 Git 而定，不依接口而定；第 3 點只改紀錄格式。
- 狀態：第 1 點已提出（`engineering-workflow-core#22`，2026-10-22）。第 2、3 點與新增的證據，已起草為 `engineering-workflow-core#22` 的留言，還沒有張貼；張貼需要使用者核准。

### CF-003 有寫入工具的替代者不能當獨立 reviewer

- 來源決策：PR #2 交接的決定 3（D-008 的 Phase 1 範圍內）；delta DL-009、DL-004。
- 問題：brief 無法拿掉 subagent 的工具。有 Edit 或 Write 工具的替代 agent 不能證明它沒有改動受審內容。為了偵測改動而自製的機制（`tree_fingerprint.py`）一直擴大。
- 證據：
  - PR #2 第 1 輪的 SR-006（`.dev/issue-1-phase1/reviews/round-1.md`）；`tree_fingerprint.py` 在第 2 輪加入後累積了 15 項以上的 finding，之後依使用者決定移除（`.dev/handoff/pr-2-checkpoint.md` 決定 3）。PR #2 的 SEC-02：reviewer 的說明寫「不能編輯檔案」，但它們保留 Bash（`security-review-merge.md`）。
  - Issue #69（CHANGELOG 的 Fixed 段）：宣告的工具清單可能和 host 實際給的不同。Claude Code 2.1.310（由它的 binary 推論，用 probe 確認）也用空格切分 `tools`，並把 `*` 當成所有工具，所以只用逗號切分的檢查會放過寫入工具；本專案改成逐字比對原始字串。這是 Claude Code 的細節，只當證據，不建議寫進 Core。
  - D-019：skill 的 `disallowed-tools` 是一層防護，不是保證（Bash 等工具仍在）。
- 提議的 Core 修改：在 `review-and-security.md#review-independent` 寫明：必要的 review 不使用有寫入工具的替代者；找不到唯讀 reviewer 時停在 gate。
- 類型：修改型（收緊）。
- 對其他專案的影響：Codex 版的 reviewer 只靠宣告維持唯讀（`docs/design-proposal.md` 原則 3）；採用後，它要說明在沒有唯讀 reviewer 時怎麼停下。
- 狀態：已提出（`engineering-workflow-core#23`，2026-10-22）。新增的證據只記在本文件，沒有起草留言（推論：新證據不改變提案）。

### CF-004 每個 finding 標明和需求的關係（`requirement_relation`、`REQ-GAP`）

- 來源決策：D-016（REQ-014）；delta DL-011。
- 問題：Core 沒有把 finding 和需求連起來，所以需求範圍內的修正和範圍擴張分不開。
- 證據：PR-A 第 2 輪後的重新評估；需求缺口變成決策卡片 1（`round-2.md`）。PR-B 的 B1-004 先被歸為 `SCOPE-CREEP`，再由使用者用決策卡片 1 加成需求（`.dev/issue-6-review-convergence/reviews/round-1.md`）。D-003 記錄 Codex 曾把專案需求改寫成通用需求。
- 提議的 Core 修改：在 `review-and-security.md#review-findings` 加上 `requirement_relation` 欄位與 `REQ-GAP` 類別；Core 的阻擋項不論關係都照樣阻擋。
- 類型：修改型（finding 格式改變）。
- 對其他專案的影響：Codex 與 Grok 的 review 報告格式要多一個欄位；它們需要有需求來源才能填寫。
- 狀態：已提出（`engineering-workflow-core#24`，2026-10-22）。

### CF-005 決策卡片

- 來源決策：D-014（REQ-013）；delta DL-014。
- 問題：Core 列出提出決策時要寫的內容，但沒有固定格式；交給使用者的決策每次格式都不同。
- 證據：PR-A 的決策卡片 1，使用者用一行回答（「Card1，我選a」；REQ-011 的 sources）。PR-C 的三張卡片也用一行回答（「1a、2b、3a」）。
- 提議的 Core 修改：在 `workflow.md#wf-writing` 與 `authorization-and-stops.md#auth-stops` 附上卡片範本。
- 類型：增量型（範本放在伴讀文件，權威原文不動）。
- 對其他專案的影響：可以不採用；採用時只改輸出格式。
- 狀態：已提出（`engineering-workflow-core#25`，2026-10-22）。

### CF-006 新增機制要對應需求（防止機制擴張）

- 來源決策：D-003、D-013 第 3 項；delta DL-003。
- 問題：Core `wf-assumptions-and-options` 要求說明新增複雜度的獨特作用，但沒有要求對應到需求。
- 證據：
  - `tree_fingerprint.py`（CF-003）；PR-A 的 `--evidence-file` 檢查在第 1、2 輪連續需要修正並產生新問題，重新評估後移除（`round-2.md`）。
  - D-021（Issue #68）：綁定程式連續三輪出現新問題；使用者選 (c1)，依 R-RIG-3 移除沒有用到、而且已知有洩漏設計的程式碼。
- 提議的 Core 修改：在 `workflow.md#wf-assumptions-and-options` 規定新增的機制要對應一條需求，否則列為範圍擴張。
- 類型：修改型（收緊）。
- 對其他專案的影響：Codex 與 Grok 需要有需求來源（例如 REQ wiki）才能檢查。
- 狀態：已提出（`engineering-workflow-core#26`，2026-10-22）。新增的證據只記在本文件，沒有起草留言（推論：新證據不改變提案）。

### CF-007 Context 載入方式：短核心加按需讀取的參考文件（已實作；歷史紀錄）

- 來源：使用者 2026-10-20 對原則 1 的提問；D-011（REQ-016）。
- 狀態（2026-10-30）：本專案已用 D-020（REQ-025）實作，方式和原本的評估不同：各 skill 依階段讀完整的 Core 原檔，不讀 Core 的摘要；`dev-core` 變成 Core 的索引加上本專案的收緊規則。實作分四個 PR（PR #23、#29、#34、#36）。本項沒有向上游提出，也不另外提出：與接口無關的部分（接口按階段讀 Core 原文，不改寫成摘要）就是 CF-009 第 7 點，也就是 `engineering-workflow-core#27` 第 7 點。實作結果已起草為該 Issue 的留言。
- 目前的事實（2026-10-30）：
  - `skills/dev-core/SKILL.md` 現在是 68,933 bytes（索引行加上逐字保留的收緊規則與 CB-1 到 CB-7）；FU-005 PR-4 合併時（`33ba87c`）是 35,063 bytes，之後的規則（D-021 到 D-025 等）讓它變成約兩倍。每個 skill 讀 `dev-core` 的階段對照表列出的 Core 檔；只有兩個 reviewer 拿 Core 檔，而且當作審查準則（D-020 決定 4，卡片 8a）。
  - D-020 估計每個 skill 讀進的 bytes 約為之前的 1.5 到 1.85 倍；這個估計假設改完之後的 `dev-core` 約 34 KB（FU-005 規格第 6 節的推論；規格寫成時 `dev-core` 是 38,181 bytes）。`dev-core` 變大之後，目前的倍數沒有重新估計（推論：比估計高）。D-020 決定時沒有量測 token。
  - FU-004 的「使用本 pack」組跑了兩次（Issue #27 是基準，Issue #38 是 PR-4 之後），兩次都記錄了每個任務的 token。PR-2 之前與 PR-4 之後的成對比較（T1／T1′、T2／T2′，各一次）沒有結論（`.dev/issue-38-fu004-after-pr4/report.md` 第 5 節與第 9 節）。token 是每個任務的總數，所以也分不出讀 Core 的 token（推論，依同一份報告第 3 節）。另外兩組沒有跑，所以沒有跨組的比較。
- 2026-10-21 的評估（已由 D-020 取代，保留作為紀錄）：
  - 問題：原則 1 曾說法條式重複是 Codex 版最大的 context 成本，但沒有量測。
  - 事實（2026-10-21 量測檔案大小，不是 token 數）：claude-dev-skills 的 `skills/dev-core/SKILL.md` 當時是 35,425 bytes，每個 dev-* 技能都先讀完整份，subagent 的 agent 檔與 brief 不要求讀它；其他 7 個技能的 SKILL.md 是 1.5 到 5.5 KB；Core v0.1.1 的 4 份契約共 42,425 bytes；codex-dev-skills（commit 9935975）的 27 個技能的 SKILL.md 是 0.9 到 14 KB（中位數 3.3 KB），`references/` 共約 199 KB，依操作需要才讀取；grok-build-dev-skills（commit d68b7ad）當時沒有技能。
  - 推論：真正的成本可能是重複載入同一份長文，以及長文造成的注意力分散，而不是單次完整載入。
  - 評估的做法：一份每次都讀的短核心（停止條件、授權、阻擋規則），加上依階段讀取的參考文件（plan、review、gate、交付）。好處：每次讀取的內容變少；Claude 與 Codex 的載入方式一致。風險：技能可能漏讀需要的參考文件；規則分散後更容易出現副本不一致（CF-008）；拆分會動到所有技能，review 成本高。使用者沒有等量測就決定（FU-005 設計卡片 7′a）。
- 提議的 Core 修改（如果 Core 採用）：在 Core 新增一份非權威的接口載入說明，讓三個接口用同一種載入模型：接口按階段讀取或引用 Core 原文，不改寫成摘要；比 Core 嚴格的接口規則另外列出；附「階段 → anchor」的建議對照（FU-005 規格第 8 節第 1 項；本專案 `dev-core` 的階段對照表可以當起點）。這就是 CF-009 第 7 點的建議。
- 類型：增量型。
- 對其他專案的影響：Codex 版已經按需讀取；採用後主要是對齊名稱與分段。

### CF-008 每條規則只寫在一個地方（本專案已部分實作）

- 來源：PR-C 的決策卡片 2，使用者選 (b) 延後（REQ-019 的 sources；FU-006）。
- 問題：同一條規則在多個技能裡重寫，改規則時容易漏改副本。
- 證據：PR-B 連續三輪都出現同一類漏改：C1-001（`round-1.md`）、MR-B-002 與 MR2-B-001（PR #7 的 comment）。後來 PR #13（MR-001）和 PR #15（R2-001、MR15-001、F-001）也出現同一類漏改。
- 提議的 Core 修改：在給接口作者的伴讀說明中，建議每條規則只在摘要中寫一次，其他地方只引用規則 ID。
- 類型：增量型。
- 對其他專案的影響：只影響各接口自己的技能結構。
- 狀態（2026-10-30）：
  - 使用者在 2026-10-21 決定先做，不再等 D-011 量測（「FU-009 合併後 FU-006 優先處理」）。
  - Issue #16（REQ-022）：只有三條規則（R-EXH-3 紀錄存放、R-VER-2 停止規則、R-EXH-4 平台結果）的副本換成引用；盤點清單內的其他規則文字逐字保留並加上規則 ID（card 8a）。
  - FU-011 已修正（Issue #40）：清單外轉述保留規則的地方，在句尾或子句尾加上規則 ID（70 處，74 個 ID），文字不改。驗收只涵蓋搜尋與三輪審查找到的地方（卡片 MR41-C1 (a)）；`README.md` 不加 ID（17 處），也可能還有沒標到的地方。
  - agent 檔與 `task-brief.md` 保留自己的副本：DL-016 的卡片 1a，以及 D-020 決定 4（只有 reviewer 拿 Core 檔，當作審查準則）。FU-016 還在處理這些副本比 `dev-core` 短或寬的地方。
  - 本項沒有向上游提出。與接口無關的心得（下一點）已起草為 `engineering-workflow-core#27` 第 7 點的留言。
- 心得（使用者 2026-10-22，card 7a 原話）：「規則文字不改寫、只有單一規則的副本才換成引用、給 subagent 的文件保留全文」。理由（本專案的推論）：subagent 不讀 `dev-core`，例如 review-report.md、task-brief.md 與 agent 檔的讀者。證據：Issue #16 的前三輪審查都找到改寫造成的阻擋問題（FR1-001、FR1-002、FR1-005、FR2-001、FR3-001 到 FR3-004）：改寫掉了條件、執行者或讀者，或引用了錯的規則。

### CF-009 FU-010 盤點與 FU-005 清單發現的 Core 用語問題

- 來源：FU-010 的完整盤點與審查第 1 到 3 輪（Issue #18，REQ-023；`.dev/issue-18-core-audit/audit.md` 與 `reviews/`）。使用者要求：「原始的core並非沒缺陷，有些條文沒寫得很明確，…應該在上游的core中開Issue回饋給core」。第 8 到 10 點來自 FU-005 的不退步清單（REQ-025；DL-018、DL-023、DL-025、DL-026、DL-027）。
- 問題與證據（行號依 v0.1.1）：
  1. `authorization-and-stops.md:52`：「共用庫不收 … runtime state」。本專案推論「共用庫」指 Core 本身的 repo。Core 沒有寫清楚：使用端專案 commit 進自己 repo 的協調狀態（graph、event 檔；本專案 CB-1、D-010）算不算 runtime state。
  2. `review-and-security.md:9`：「Review request 保持唯讀，只有明確轉為修正／實作才修改受審內容」。Core 沒有寫清楚「唯讀」是只不改受審內容，還是完全不寫任何檔案（例如 repo 外的暫存檔、跑測試產生的 cache）。第 3 輪的 reviewer 在 repo 外寫了一個 log 檔。結果（FU-013，Issue #20，REQ-024）：reviewer 在任何地方都不寫檔，包含 session 的 scratchpad（卡片 9b）；跑 Python 測試時用 `PYTHONDONTWRITEBYTECODE=1` 與 pytest `-p no:cacheprovider`，不在 repo 產生檔案（卡片 3d）；例外是指定的測試在系統暫存目錄自己建立、自己刪除的暫存檔，不算 reviewer 寫檔（卡片 11b）。
  3. `workflow.md:35`：中文註記是「依 ASD-STE100 原則編寫，尚未完成完整符合性驗證」。本專案用使用者在 REQ-013 寫的「…，未完成完整符合性驗證」，意思相同、字面不同。Core 如果把註記定成固定字面，各接口就能逐字比對。
  4. `authorization-and-stops.md:35`：「必要能力、獨立 review、必要 scan、驗證或 gate 缺失／未完成／失敗／覆蓋不足；缺安全 fallback。」「缺安全 fallback」可以讀成獨立的停止條件，也可以讀成前半句的限定條件。兩位 reviewer 的讀法不同（Issue #18 第 1 輪 S1）。
  5. `workflow.md:76`：「狀態或旁支問題先簡答再續行，除非明確取消／替換目標」。例外是限制「續行」，還是也限制同段前面「保留仍適用成果並重查受影響證據」？第 2 輪（R2-001）與第 3 輪（R3-004）的 reviewer 讀法不同。
  6. `authorization-and-stops.md:21`：破壞性操作列出「刪除／purge／prune」。Core 沒有寫清楚：push 前為了正確判斷要掃描哪些 commit 而 prune 本機 remote-tracking refs（`git fetch --prune`）算不算。使用者在卡片 4 同意記為專案規則；之後的審查（R3-006、MR19-001、MR19-002）又找到 preview、設定讀回與當下確認的問題，所以使用者把它移到 FU-014 另外設計（卡片 8a）。結果（FU-014，Issue #24）：push 前改用 `git ls-remote --heads --tags <remote>` 取得 remote 的狀態，不執行 `git fetch`，所以本專案不再需要 prune。Core 的用語問題仍然存在。
  7. 摘要的做法（沒有單一 Core 行；相關的是 `exact-head-and-evidence.md:58`：衍生副本保留唯一來源，共享 Markdown 不能證明等價）：壓縮過的摘要無法保住 Core 每一句的條件。Issue #18 的三輪審查，每輪都找到新的漏寫義務或少了條件的句子（R-VER-2 停止規則兩次觸發）。建議 Core 在給接口作者的說明中寫明：接口應引用或按需載入權威原文，不要改寫；比 Core 嚴格的接口規則另外列出（與 CF-007、CF-008 相關）。本專案已用 D-020 實作這個做法（CF-007）。
  8. `authorization-and-stops.md:50`：Core 要求搬移或歸檔前查核必要的 preview，清理前先 dry-run。本專案在搬移、歸檔與清理前都要 dry-run（DL-018，不退步清單 C-1）。Core 的字面是清楚的：只有清理要 dry-run。問題是 Core 是否有意如此：搬移與歸檔只要 preview 就夠，還是也應該 dry-run？證據：Issue #18 第 3 輪的 R3-009（搬移與歸檔前的 dry-run 被誤刪，之後補回）。
  9. `workflow.md:115`：未解或間歇的失敗、安全或資料遺失事件，以及共享或仍被引用的證據，「須依專案有效要求及保護例外適當保留」。本專案無條件保留這些紀錄（DL-023，不退步清單 C-7；DL-023 沒有記錄實例）。Core 沒有寫清楚：專案的要求或例外能不能縮短這些紀錄的保留，還是只決定保留的位置與方式。本專案的無條件保留只在保留時間上比 Core 的字面嚴格；如果保護例外要求移除資料（例如 `authorization-and-stops.md:52` 不能公開的內容），兩者可能衝突，這也是本點要問的。
  10. `review-and-security.md:39`：每次 review 與 scan 綁定「含適用未提交修改」的內容。本專案綁定所有未提交的修改（DL-025，不退步清單 C-20）。Core 沒有寫清楚由誰判斷哪些未提交的修改「適用」。同一個限定詞「適用」也出現在 `exact-head-and-evidence.md:22`「專案提供且適用的 deterministic offline … checks」（本專案 R-EXH-2 寫成執行 repository 的 deterministic checks；DL-026，不退步清單 C-21），Core 同樣沒有說由誰判斷。類似的限定詞在 `review-and-security.md:47`「具有安全影響的 executable」（本專案 R-REV-7 寫成 executables；DL-027，不退步清單 C-22）；但 `:45` 到 `:47` 已規定適用性依權責與政策、依實際影響判斷，所以這一處不需要問誰判斷。三處本專案都省略了限定詞，所以字面上比 Core 嚴格。證據：FU-005 設計審查的 R2-004（FU-005 規格第 8 節第 6 項）。
- 提議的 Core 修改：在伴讀說明中補上第 1 到 6 點與第 8 到 10 點的明確讀法，以及第 7 點的建議；權威原文要改時，走修改型流程。
- 類型：第 1 到 6 點與第 8 到 10 點是增量型（說明）；如果 Core 決定改寫原文，則是修改型。第 7 點是增量型。
- 對其他專案的影響：codex-dev-skills 與 grok-build-dev-skills 可以照同樣的讀法核對自己的摘要；在它們重新 pin 之前沒有影響。
- 本專案的讀法（REQ-025，使用者核准的 FU-005 設計卡片 5a、5b、9b）：
  - 第 4 點（`dev-core` R-AUTH-5，DL-028）：必要的獨立 review、scan、驗證或 gate，以及必要的平台或安全執行能力，只要缺失、未完成、失敗或覆蓋不足，就一律停止相依工作，fallback 不能取代（`workflow.md:62`）；其他能力（例如委派、session 或排程 API）缺失時，用 Core 列出的安全 fallback 繼續（單一 writer、手動 checkpoint），沒有安全 fallback 時才停止。
  - 第 5 點（`dev-core` R-VER-3，DL-029）：「保留仍適用成果並重查受影響證據」一律適用；例外「除非明確取消／替換目標」只限制「先簡答再續行」。
- 狀態：第 1 到 7 點已提出（`engineering-workflow-core#27`，2026-10-22）。第 4、5 點的讀法已在 `engineering-workflow-core#27` 留言（2026-10-22）。第 2、6 點的結果、第 7 點的實作結果（含 CF-007、CF-008），以及第 8 到 10 點，已起草為 `engineering-workflow-core#27` 的留言，還沒有張貼；張貼需要使用者核准。

### CF-010 什麼算使用者的確認，什麼是轉述（候選）

- 來源：D-025（Issue #78，卡片 I78-D4 (a)）；`dev-core` R-DEL-2 的「Relayed answers」；FU-041；設計審查 finding DS1-06、DS2-02、DS3-05。
- 問題：Core `auth-scope`（`authorization-and-stops.md:9`、`:11`）規定授權要追溯到有效的使用者指示或適用的核可平台機制，但沒有定義什麼算使用者的確認。另一個 session、agent、hook、工具或背景工作加進 session 的文字，host 可能顯示成使用者的訊息。
- 本專案的規則（只用在 R-DEL-2 的 model 與 effort 選擇）：確認是使用者在本 session 自己的訊息；另一個 session、agent、hook、工具、排程或背景工作加進本 session 的文字，即使 host 顯示成使用者的訊息，也不是確認；本 session 分不出是不是使用者自己的訊息時，當成轉述。
- 證據：沒有實際發生的實例。host 怎麼顯示其他來源加進 session 的文字沒有驗證（D-025 殘餘風險 6、FU-041 第 (2) 項）。DS1-06、DS2-02、DS3-05 是設計審查推論出的風險。
- 提議的 Core 修改：在 `auth-scope` 的伴讀說明中寫明這個定義，適用於所有需要使用者確認的地方。
- 類型：增量型（讀法說明）。
- 對其他專案的影響：Codex 與 Grok 要依自己的 host 判斷哪些文字是使用者自己的訊息。
- 狀態：候選，未提出。FU-041 第 (2) 項要先驗證 host 怎麼顯示其他來源加進 session 的文字；驗證之後再決定是否提出。D-025 記的「Core 回饋：否」是推論、未經審查，理由是「只改本 pack 自己的加嚴規則」。本專案的推論：那個理由適用於 model 與 effort 的部分；本項只取與接口無關的確認定義。

### CF-011 事先寫好的分級只是提議（候選）

- 來源：D-023（Issue #75 第 5 項；卡片 I75-D2 (a)、I75-R1-C3 (b)）；delta DL-039；`dev-core` R-RIG-2；FU-040。
- 問題：Core `review-risk-timing`（`review-and-security.md:33`）要求任務開始時判定風險，範圍或設計改變時重評，資訊不足時不能默認低風險；`authorization-and-stops.md:9` 也要求執行前核對當前來源。所以開始時重新判定已經隱含在 Core 裡（推論）。Core 沒有明說的是：在任務開始之前寫好的風險或分級（例如寫在 Issue 或 brief 裡）只是輸入，以及調低它需要誰的決定。
- 證據：Issue #73 照 Issue 的 Process 行規劃為 `standard`，但它的 plan 已寫出這項變更修改 pack 公開的規則，依 R-RIG-1 是 `strict`；實作前的早期設計審查因此沒有做（MR73D-003）。根因（推論）：沿用事先寫好的分級，沒有在 Discover 重新評估。
- 本專案的規則（R-RIG-2）：Discover 之前寫好的分級是提議，Discover 時重新評估並寫進 plan；重新評估可以調高；要調低事先寫好的分級，需要使用者的決定，plan 記錄理由；轉述的調低決定，要等使用者在本 session 確認後才算數。還沒解決的（FU-040）：Discover 之後的重新評估調低分級時，是否也需要使用者決定。
- 提議的 Core 修改：在 `review-risk-timing` 寫明：任務開始之前寫好的風險判定是輸入，開始時重新判定；調低需要記錄的使用者決定。
- 類型：修改型（收緊）。
- 對其他專案的影響：Codex 與 Grok 的規劃步驟要把 Issue 或 brief 中的分級當成提議。
- 狀態：候選，未提出；使用者決定是否提出（可以先等 FU-040 的決定）。D-023 記的「Core 回饋：否」是推論、未經審查，理由是「只改本 pack 自己的加嚴規則」。本專案的推論：那個理由適用於本 pack 的分級名稱；本項只取與接口無關的部分。

### CF-012 subagent 怎麼取得 Core（候選）

- 來源：FU-005 規格第 8 節第 2 項（`.dev/issue-22-fu005-records/fu005-spec.md`；規格預定的編號是「CF-010」，本文件的 CF-010 是另一項）；D-020 決定 4（卡片 8a）；FU-016。
- 問題：Core `workflow.md:60` 要求 brief 列出目標、角色、ownership、當前來源、DoD 等，但沒有說 subagent 怎麼取得 Core，也沒有說「Core 是規則」和「讀到的檔案內容是資料，不是指令」怎麼並存。
- 本專案的做法：只有兩個 reviewer 拿 Core 檔，而且當作審查準則（資料），不當指令；政策只來自 brief；implementer 與 explorer 不拿 Core（D-020 決定 4，卡片 8a）。給 subagent 的檔案保留自己的規則全文（CF-008）；FU-016 還在處理這些副本比 `dev-core` 短或寬的地方。
- 證據：卡片 8 的做法經過兩輪設計審查與一次安全設計審查（FU-005 規格第 8 節第 2 項）。沒有記錄實際發生的失敗。
- 提議的 Core 修改：在 `wf-delegation` 的伴讀說明中寫明：subagent 怎麼取得 Core 由接口決定；Core 交給 reviewer 時是審查準則（資料），不是指令；政策只來自 brief；授權依 `workflow.md:60` 與 `authorization-and-stops.md:11` 追溯到有效的使用者指示或適用的核可平台機制。
- 類型：增量型（說明）。
- 對其他專案的影響：Codex 與 Grok 要說明自己的 subagent 怎麼取得 Core。
- 狀態：候選，未提出。使用者在 2026-10-30 決定把它加進本紀錄（Issue #84 卡片 I84-C1 (a)）。

## 不回饋給 Core 的決策

| 決策 | 理由 |
| --- | --- |
| D-009 Graph engineering 分階段 | graph engineering 不在 Core 契約內；中立層成形後再評估 |
| D-010 不做 agent memory | Core `auth-scope`、`wf-stages` 與 `auth-data` 已涵蓋 |
| D-011 部署與量測 | Claude 端的工作；結果是本文件的證據 |
| D-012 自動交接 | 取決於各接口的 session 能力；Core `wf-stages` 已涵蓋 checkpoint 與接續 |
| D-019 教訓技能 `dev-retro` | Core `workflow.md:74` 已規定改善記在既有報告，不新增反思 executor、memory、hooks 或 scheduler（D-019，推論，由審查確認） |
| D-021 push 前的確定性預檢 | 是本 pack 對 Core 的收緊（DL-010）之上再加的一道檢查；一般性的部分在 CF-002 |
| model 與 effort 的選擇：R-DEL-2 的下限（D-007 規則 2）、`dev-deliver` 與 `dev-review` 的對照表與升級順序（FU-018、DL-034、D-022、D-023）、參考值（D-025） | Core `wf-delegation`（`workflow.md:56`、`:64`）把 model、effort 與其控制交給各接口；與接口無關的部分在 CF-001 第 5 點、CF-010 與 CF-011 |
| D-024 model 與 effort 的讀回測試 | Claude Code host 的行為；Core `workflow.md:64` 要求各接口自己記錄版本、surface 與驗收範圍 |
| DL-037 `allowed-tools`（Issue #66） | Claude Code plugin 的權限設定，不是共用流程 |

D-021 到 D-025 自己記的「Core 回饋：否」都是推論、未經審查。D-022 到 D-025 的理由是「只改本 pack 自己的加嚴規則」（D-022 另加「與數值」，D-024 另加「與紀錄」）；D-021 的理由見上表該列。上表 D-021 之後各列的理由（含 `workflow.md:56`、`:64` 的引用）是本紀錄的推論。

---

<a id="english"></a>

<details>
<summary>English</summary>

# Core feedback record

Status: a record that is kept up to date (last update 2026-10-30, from the
content of main `41f7256`). This English version means the same as the
Traditional Chinese version. If the two differ, the Chinese version wins.
Written per ASD-STE100 principles; full conformance not verified.

## Purpose

`engineering-workflow-core` (Core) is the shared workflow of
codex-dev-skills, grok-build-dev-skills and claude-dev-skills. When a change
in this project is a Core-level issue, it is recorded here, so that Core can
adopt it and the other two projects can re-pin it themselves (REQ-019).

- The process is D-001 in `docs/design-proposal.md`. An additive proposal is
  preferred: a non-authoritative companion document in Core, with the
  authoritative text unchanged. A modifying proposal first needs a candidate
  pin and passing evals in codex-dev-skills and grok-build-dev-skills.
- This document is a record only. This project does not change Core,
  codex-dev-skills or grok-build-dev-skills. Each Issue or comment in Core
  needs separate approval from the user.
- Core version: v0.1.1 (commit `7b66978a76597d09be1b55ad199a969b4ee59c0f`).
  Line numbers are at v0.1.1.
- Upstream state (read on 2026-10-30): `engineering-workflow-core#21` to
  `engineering-workflow-core#27` (opened 2026-10-22) for CF-001 to CF-006 and
  CF-009 are all open, with no reply from a maintainer. The only comment is
  this project's note on the readings of points 4 and 5 in
  `engineering-workflow-core#27` (2026-10-22). Core main is still v0.1.1,
  with no later tag or PR. So nothing upstream changes the items of this
  document.
- In this document, "Issue #n" and "PR #n" are Issues and PRs of
  claude-dev-skills; an upstream Issue is written
  `engineering-workflow-core#n`.

## Overview

| Item | Upstream | Status (2026-10-30) | Next step |
| --- | --- | --- | --- |
| CF-001 Review convergence | `engineering-workflow-core#21` | Proposed; new evidence, new points 4 and 5 (candidates) | Comment drafted, waits for the user's approval |
| CF-002 Scan before commit and push | `engineering-workflow-core#22` | Proposed; new scope and a masking format (candidates) | Comment drafted, waits for the user's approval |
| CF-003 Substitute with write tools | `engineering-workflow-core#23` | Proposed; new evidence | None |
| CF-004 `requirement_relation` | `engineering-workflow-core#24` | Proposed; no change | None |
| CF-005 Decision card | `engineering-workflow-core#25` | Proposed; no change | None |
| CF-006 Mechanism traces to a requirement | `engineering-workflow-core#26` | Proposed; new evidence | None |
| CF-007 How context is loaded | Not proposed | History: implemented in this project by D-020 | Part of the comment on point 7 of `engineering-workflow-core#27` |
| CF-008 Each rule in one place | Not proposed | Partly implemented in this project | Part of the comment on point 7 of `engineering-workflow-core#27` |
| CF-009 Core wording questions | `engineering-workflow-core#27` | Proposed; comment on points 4 and 5 posted; new results for points 2 and 6; new points 8 to 10 (candidates; point 10 covers three places) | Comment drafted, waits for the user's approval |
| CF-010 Confirmation and relay | Not proposed | Candidate | Wait for FU-041 to verify how the host shows text that is added to a session |
| CF-011 A tier written in advance | Not proposed | Candidate | The user decides whether to propose it |
| CF-012 How a subagent gets Core | Not proposed | Candidate | The user decides whether to propose it |

## Items

### CF-001 Review convergence: severity thresholds, stop rule, records without a new head

- Decision: D-013 (REQ-012); deltas DL-011, DL-012, DL-013. Point 4: the
  stop cards of Issues #68, #73, #77 and #78. Point 5: FU-018 (PR #51,
  REQ-009 card C2a).
- Problem: Core defines no severity thresholds. Core treats two unfinished
  review rounds as a time to re-assess, not to stop. Core does not say where
  review records go once a PR exists. A record committed to the PR branch
  makes a new head, and the new head needs a complete review: a loop.
- Evidence:
  - PR #2 Merge Reviews 1 to 5 kept producing new findings; Merge Reviews 6
    and 7 had none.
    `merge-review-1.md` to `merge-review-4.md` were committed with their
    fixes (c72c64d, c934a29, eb8e08a, 2280228), and each commit made a new
    head (`.dev/handoff/pr-2-checkpoint.md`).
  - The PR-A (PR #5) re-evaluation after round 2 removed checks that no
    requirement covered (`.dev/issue-4-commit-security/reviews/round-2.md`).
  - In PR-B (PR #7), two Merge Reviews in a row were blocked (MR-B-001 and
    MR-B-002, then MR2-B-001). The stop rule fired, and the user decided the
    fix with decision card 2 (PR #7 comments).
  - PR #19 (Issue #18): the same mechanism had new blockers in two
    consecutive rounds, and the stop rule fired twice
    (`engineering-workflow-core#21` already cites it).
  - Later, the stop rule fired again several times: the design and spec
    reviews of D-019, the spec reviews of D-020, Issue #68 round 2 (D-021),
    Issue #73 round 2 (the Stop rule section of
    `.dev/issue-73-model-routing/reviews/round-2.md`), Issue #77 design
    review rounds 2 and 3 (D-024) and Issue #78 design review round 3
    (D-025). The source is the origin and review
    record of each decision in `docs/design-proposal.md`.
  - FU-023 (open): a round record committed before the PR exists also
    becomes part of the base-to-head diff, and the Merge Review finds
    blockers that concern only the record (PR #30 MR30-002; PR #34
    MR34-001, MR34-RC-001). So the problem of point 3 is not only after the
    PR exists.
- Proposed Core change:
  1. Severity thresholds in `review-and-security.md#review-findings`.
  2. The stop rule in `workflow.md#wf-verification`.
  3. In `exact-head-and-evidence.md#exact-transition`, records are never
     committed to the PR branch once a PR exists.
  4. What to do after a stop (candidate, 2026-10-30): Core
     `workflow.md:72` only says that two unfinished review and fix rounds
     trigger a re-assessment, "not an automatic stop"; the stop rule is
     the proposal of point 2. R-VER-2 of this project stops the fixes,
     re-evaluates, and gives the decision to the user with a decision card,
     but does not say what can be done after the stop. At least seven
     stops of this project used the same method (from a search of
     `docs/design-proposal.md` and `.dev/`; there can be more): the
     mechanism that kept failing moved to a follow-up, another Issue or
     residual risk, and the rest was delivered. The three early ones: D-017
     (Issue #12; the profile settings moved to FU-009), Issue #18 (the
     `--prune` rule moved to FU-014, card 8a) and FU-015 PR-2 (Issue #48;
     card PR2-R2-C1 (a), the `+`/`-` check moved to FU-019). In two of the
     four recent Issues (#68, #73), the user first agreed to one more round
     of narrow fixes, with the agreement in advance that the mechanism
     moves out when it has a new blocker again. Recent examples: Issue
     #68 (card I68-R2-C1 agreed in advance; after R3-001 in round 3,
     fallback (c), and the binding mechanism moved to Issue #71); Issue #73
     (card I73-R2-C1 (a) agreed in advance; the floor-check timing findings
     of round 3 moved to FU-035); Issue #77 (stop cards I77-R2-C1 (a) and
     I77-R3-C1 (a); the read-back gate moved directly to Issue #79); Issue
     #78 (the first stop, in round 3, card I78-R3-C1 (c); the fail-closed
     mechanism of D-025 items 3, 8 and 9 moved to FU-044). Each change of
     scope was the user's decision. Core `workflow.md:62` asks for no
     lower DoD when a capability is missing; this project's judgment is
     that a change of scope that the user decides is not that case.
     Suggestion: add this method to the stop rule in
     `workflow.md#wf-verification` as one of the options for a person to
     decide. R-VER-2 in `dev-core` of this project does not have this
     sentence yet (inference: the evidence is more complete when this
     project writes it as a rule first).
  5. A failure that the spec or the design caused is not a quality failure
     (candidate, 2026-10-30): Core `workflow.md:72` keeps service, auth,
     environment, data, permission and context failures apart from quality
     rework, and says that more effort does not fix a missing environment
     or permission. It does not say which class a failure belongs to when
     the spec, the acceptance criteria or the design caused it. R-DEL-2 in
     `dev-core` of this project says that such a failure is not a quality
     failure: it goes to the stop rule and re-evaluation and does not
     escalate the model or the effort (FU-018, REQ-009 card C2a).
     Evidence: in the FU-018 evaluation (aggregate of PR #2 to #49), 52 of
     116 blocking findings were quality problems and 64 were spec or
     mechanism problems (the FU-018 row of `.dev/followups.md`).
     Suggestion: Core names this class in the same paragraph.
- Kind: points 1 to 3 are modifying (the stop rule and the record location
  change obligations); an additive companion document can try them first.
  Point 4 is additive (one option for a person to decide). Point 5 is
  modifying (a new failure class).
- Impact on the other projects: after adoption, codex-dev-skills and
  grok-build-dev-skills may need fewer review rounds; both must check their
  gates and record handling. No effect before they re-pin.
- Status: points 1 to 3 are proposed (`engineering-workflow-core#21`,
  2026-10-22). Points 4 and 5 and the new evidence are drafted as a comment
  on `engineering-workflow-core#21` and are not posted; a post needs the
  user's approval.

### CF-002 Security review before every commit and push, including commit metadata

- Decision: D-015 (REQ-011); delta DL-010. New scope: D-015 (the range scan
  at merge), FU-015, FU-017, D-021. Masking format: DL-016 (R-REV-8).
- Problem: Core requires a Security Diff Scan only when a change touches a
  trust boundary. In a public repository, every commit and push publishes the
  content and also the author, the committer and the message.
- Evidence:
  - PR #2 SEC-01. The author and committer of all 10 branch commits were
    derived from the local account and the machine hostname, and the push
    published them. No content review checked the metadata
    (`.dev/issue-1-phase1/reviews/security-review-merge.md`).
  - The range scan at merge: from the start (PR #5), D-015 asks for a scan
    of every commit and of the merge or squash commit before a merge
    (DL-010); the body of `engineering-workflow-core#22` does not name it.
  - Later results (the Security section of the CHANGELOG): a
    signature can carry a name or email that the headers do not show (an
    x509 certificate, an OpenPGP signer's user ID; FU-017, Issue #54).
    Settings such as `.mailmap`, replace refs and `log.showSignature` change
    what a scan sees (FU-015 PR-1, Issue #46). The fetch and push URLs can
    differ, so the repository that the scan reads is not always the one
    that the push goes to (FU-015 PR-2, Issue #48).
  - D-021 (Issue #68): an evidence binding designed to lower the scan cost
    let anyone confirm a guessed identity offline (R3-001: the public nonce
    and the binding line in the report verify a guessed email). The user
    chose fallback (c1): every push gets a full scan plus one deterministic
    pre-check, and the binding code was removed.
  - Masking in public records: PR #5 SR-A-008 found the masking rule in one
    place only and loosely defined; it now has a fixed format (DL-016).
    FU-003: `graph.py transition --evidence-file` commits the path and the
    SHA-256 of a regular file inside the project; a short secret that can
    be guessed can be found offline from its public hash. On 2026-10-20
    the user decided not to add more checks; this is a residual risk that
    this project accepts.
- Proposed Core change:
  1. In `review-and-security.md#review-security`, scan every commit, push,
     and PR and Issue text of a public repository, including identity,
     message and trailers.
  2. Scope additions (candidate, 2026-10-30): before a merge, scan every
     commit of the range and the merge or squash commit; commit and tag
     signatures; scan with a view that settings do not change (for example
     without `.mailmap` and replace refs); before a push, check that the
     remote that the scan reads is the remote that the push goes to.
  3. A masking format for public records (candidate, 2026-10-30): Core
     `authorization-and-stops.md:52` asks that public records keep only a
     safe source, the necessary limits and traceable information, but gives
     no masking format. Suggestion, in a companion note: give only the kind,
     the location and the length or class of a value; for an email, only
     whether it is a noreply address and its provider; replace the account
     or host part of a path or hostname with a placeholder; paste no raw
     output that contains such a value. Also, a guess can verify a hash or
     a binding of a private value (D-021 R3-001, FU-003). R-REV-8 and
     DL-016 of this project have no rule "publish no hash of a private
     value", and the FU-003 hash is an accepted residual risk; so this
     sentence is an observation for Core, not a practice of this project.
     The user decides whether to propose it upstream.
- Kind: points 1 and 2 are modifying (new obligations). Point 3 is additive
  (the format goes into a companion document).
- Impact on the other projects: the commit and push steps of Codex and Grok
  add this scan. The checks of point 2 depend on Git, not on the interface;
  point 3 changes only the record format.
- Status: point 1 is proposed (`engineering-workflow-core#22`, 2026-10-22).
  Points 2 and 3 and the new evidence are drafted as a comment on
  `engineering-workflow-core#22` and are not posted; a post needs the
  user's approval.

### CF-003 A substitute with write tools is not an independent reviewer

- Decision: PR #2 handoff decision 3 (Phase 1 scope, D-008); deltas DL-009,
  DL-004.
- Problem: a brief cannot remove a subagent's tools. A substitute agent with
  Edit or Write tools cannot prove that it did not change what it reviewed.
  The self-made mechanism to detect such changes (`tree_fingerprint.py`) kept
  growing.
- Evidence:
  - PR #2 round 1 SR-006 (`.dev/issue-1-phase1/reviews/round-1.md`);
    `tree_fingerprint.py` collected 15 or more findings after round 2 added
    it, and was then removed by user decision
    (`.dev/handoff/pr-2-checkpoint.md`, decision 3). PR #2 SEC-02: the
    reviewer descriptions said "Cannot edit files", but the reviewers keep
    Bash (`security-review-merge.md`).
  - Issue #69 (the Fixed section of the CHANGELOG): the
    declared tool list can differ from the tools that the host gives.
    Claude Code 2.1.310 (inferred from its binary, confirmed by a probe)
    also splits `tools` on spaces and reads `*` as all tools, so
    a check that splits on commas only let a write tool pass; this project
    now compares the raw strings exactly. This is a Claude Code detail: it
    is evidence only, not a suggestion for Core.
  - D-019: the `disallowed-tools` of a skill is one layer of protection,
    not a guarantee (Bash and other tools stay).
- Proposed Core change: in `review-and-security.md#review-independent`, a
  required review never uses a substitute with write tools; without a
  read-only reviewer, the work stops at the gate.
- Kind: modifying (a tightening).
- Impact on the other projects: the Codex reviewer is read-only by
  declaration only (`docs/design-proposal.md`, principle 3); after adoption,
  Codex must state how it stops when no read-only reviewer is available.
- Status: proposed (`engineering-workflow-core#23`, 2026-10-22). The new
  evidence is only in this document; no comment is drafted (inference: the
  new evidence does not change the proposal).

### CF-004 Every finding states its relation to the requirements (`requirement_relation`, `REQ-GAP`)

- Decision: D-016 (REQ-014); delta DL-011.
- Problem: Core does not relate findings to requirements, so a fix inside
  the requirements cannot be told apart from a scope expansion.
- Evidence: the PR-A re-evaluation after round 2; the requirement gap became
  decision card 1 (`round-2.md`). PR-B finding B1-004 was first rated
  `SCOPE-CREEP`, and the user then added it as a requirement with decision
  card 1 (`.dev/issue-6-review-convergence/reviews/round-1.md`). D-003 records
  that Codex rewrote project requirements into generic ones.
- Proposed Core change: a `requirement_relation` field and a `REQ-GAP`
  category in `review-and-security.md#review-findings`; a Core blocker blocks
  for every relation.
- Kind: modifying (the finding format changes).
- Impact on the other projects: the review reports of Codex and Grok get one
  more field; they need a requirement source to fill it.
- Status: proposed (`engineering-workflow-core#24`, 2026-10-22).

### CF-005 Decision card

- Decision: D-014 (REQ-013); delta DL-014.
- Problem: Core lists what a decision request contains, but gives no fixed
  format. The decisions handed to the user had a different format each time.
- Evidence: PR-A decision card 1; the user answered in one line ("Card1，我選a";
  REQ-011 sources). The three PR-C cards were also answered in one line
  ("1a、2b、3a").
- Proposed Core change: a card template for `workflow.md#wf-writing` and
  `authorization-and-stops.md#auth-stops`.
- Kind: additive (the template goes into a companion document; the
  authoritative text does not change).
- Impact on the other projects: optional; adoption changes only the output
  format.
- Status: proposed (`engineering-workflow-core#25`, 2026-10-22).

### CF-006 A new mechanism traces to a requirement (against mechanism creep)

- Decision: D-003, D-013 item 3; delta DL-003.
- Problem: Core `wf-assumptions-and-options` requires the unique role of added
  complexity, but not a link to a requirement.
- Evidence:
  - `tree_fingerprint.py` (CF-003); the PR-A `--evidence-file` checks needed
    fixes and produced new problems in rounds 1 and 2, and the
    re-evaluation removed them (`round-2.md`).
  - D-021 (Issue #68): the binding code had new problems in three rounds in
    a row; the user chose (c1), and under R-RIG-3 the code, unused and with
    a known leaking design, was removed.
- Proposed Core change: in `workflow.md#wf-assumptions-and-options`, a new
  mechanism traces to a requirement, otherwise it is a scope expansion.
- Kind: modifying (a tightening).
- Impact on the other projects: Codex and Grok need a requirement source (for
  example a REQ wiki) to check it.
- Status: proposed (`engineering-workflow-core#26`, 2026-10-22). The new
  evidence is only in this document; no comment is drafted (inference: the
  new evidence does not change the proposal).

### CF-007 How context is loaded: a short core plus references read on demand (implemented; history)

- Origin: the user's question on principle 1 (2026-10-20); D-011 (REQ-016).
- Status (2026-10-30): this project implemented it with D-020 (REQ-025), in
  a different way from the original evaluation: each skill reads the full
  original Core files for its stage, not a digest of Core; `dev-core` is now
  an index of Core plus this project's tightenings. The work was four PRs
  (PR #23, #29, #34, #36). This item was not proposed upstream and is not
  proposed on its own: its interface-neutral part (an interface reads the
  original Core text per stage and does not reword it) is CF-009 point 7,
  that is point 7 of `engineering-workflow-core#27`. The result of the
  implementation is drafted as a comment on that Issue.
- Current facts (2026-10-30):
  - `skills/dev-core/SKILL.md` is now 68,933 bytes (index lines, the
    tightenings kept word for word, and CB-1 to CB-7); when FU-005 PR-4
    merged (`33ba87c`) it was 35,063 bytes, and later rules (D-021 to
    D-025 and others) made it about twice as large. Each skill reads the
    Core files that the stage map of `dev-core` lists for it; only the two
    reviewers get Core files, as review criteria (D-020 decision 4,
    card 8a).
  - D-020 estimates that each skill reads about 1.5 to 1.85 times the bytes
    of before; the estimate assumes a `dev-core` of about 34 KB after the
    change (an inference in section 6 of the FU-005 spec; when the spec was
    written, `dev-core` was 38,181 bytes). After `dev-core` grew, the current factor was not estimated
    again (inference: it is higher than the estimate). Tokens were not
    measured when D-020 was decided.
  - The with-the-pack arm of FU-004 ran twice (Issue #27, the baseline;
    Issue #38, after PR-4), and both runs recorded the tokens of each task.
    The paired comparison before PR-2 and after PR-4 (T1/T1′, T2/T2′, one
    run each) has no conclusion (`.dev/issue-38-fu004-after-pr4/report.md`,
    sections 5 and 9). The tokens are one total per task, so they also
    cannot separate the tokens of the Core reads (inference, from section 3
    of the same report).
    The other two arms did not run, so there is no comparison between
    arms.
- The evaluation of 2026-10-21 (replaced by D-020, kept as a record):
  - Problem: principle 1 said that the repeated legal-style text was the
    largest context cost in the Codex version, but nothing measured it.
  - Facts (file sizes measured on 2026-10-21; these are not token counts):
    in claude-dev-skills, `skills/dev-core/SKILL.md` was then 35,425 bytes,
    and every dev-* skill read all of it first, while the agent files and
    briefs of the subagents did not require it; the SKILL.md files of the
    other 7 skills were 1.5 KB to 5.5 KB; the 4 contracts of Core
    v0.1.1 are 42,425 bytes in total; in codex-dev-skills (commit 9935975),
    the SKILL.md files of its 27 skills are 0.9 KB to 14 KB (median 3.3 KB),
    and its `references/` folders hold about 199 KB, read only when an
    operation needs them; grok-build-dev-skills (commit d68b7ad) then had no
    skills.
  - Inference: the real cost may be the repeated loading of the same long
    text and the loss of attention in long text, not one full load.
  - The evaluated method: a short core that is always read (stop
    conditions, authority, blocking rules), plus references read per stage
    (plan, review, gate, delivery). Benefit: less text per read; Claude and
    Codex load in the same way. Risk: a skill can miss a reference it
    needs; rules spread over more files can drift apart (CF-008); a split
    touches every skill, so the review cost is high. The user decided
    without waiting for the measurements (FU-005 design card 7′a).
- Proposed Core change (if Core adopts it): a non-authoritative loading
  note in Core, so that the three interfaces use one loading model: an
  interface reads or quotes the original Core text per stage and does not
  reword it into a digest; interface rules that are stricter than Core are
  listed separately; a suggested "stage → anchor" map is attached (FU-005
  spec section 8 item 1; the stage map of `dev-core` here can be a start).
  This is the advice of CF-009 point 7.
- Kind: additive.
- Impact on the other projects: Codex already reads on demand; adoption
  mainly aligns names and sections.

### CF-008 Each rule in one place (partly implemented in this project)

- Origin: PR-C decision card 2; the user chose (b) defer (REQ-019 sources;
  FU-006).
- Problem: the same rule is restated in several skills, so a rule change can
  miss a copy.
- Evidence: PR-B had the same kind of missed copy in three rounds in a row:
  C1-001 (`round-1.md`), MR-B-002 and MR2-B-001 (PR #7 comments). Later,
  PR #13 (MR-001) and PR #15 (R2-001, MR15-001, F-001) had the same kind of
  missed copy.
- Proposed Core change: a companion note for interface authors that writes
  each rule once in the digest and cites only its rule ID elsewhere.
- Kind: additive.
- Impact on the other projects: only their own skill structure.
- Status (2026-10-30):
  - On 2026-10-21 the user decided to do it now, without waiting for the
    D-011 measurements (「FU-009 合併後 FU-006 優先處理」: do FU-006 first
    after FU-009 merges).
  - Issue #16 (REQ-022): only the copies of three rules (R-EXH-3 record
    storage, R-VER-2 stop rule, R-EXH-4 platform result) became citations;
    other rule text that the inventory lists stays word for word and names
    its rule IDs (card 8a).
  - FU-011 is fixed (Issue #40): the places outside the inventory that
    restate a kept rule name the rule ID at the end of the sentence or
    clause (70 places, 74 IDs); no word changed. The acceptance covers
    only the places that the search and the three review rounds found
    (card MR41-C1 (a)); `README.md` gets no IDs (17 places), and places
    without an ID can remain.
  - The agent files and `task-brief.md` keep their own copies: card 1a of
    DL-016, and D-020 decision 4 (only the reviewers get Core files, as
    review criteria). FU-016 still works on the places where these copies
    are shorter or looser than `dev-core`.
  - This item was not proposed upstream. The interface-neutral lesson (next
    point) is drafted as a comment on point 7 of
    `engineering-workflow-core#27`.
- Lesson (user, 2026-10-22, card 7a): 「規則文字不改寫、只有單一規則的副本才換成引用、給 subagent 的文件保留全文」
  (translation: do not reword rule text; replace only a copy of a single
  rule with a citation; files given to a subagent keep the full text). Reason (this project's inference): a
  subagent does not read `dev-core`, for example the readers of
  review-report.md, task-brief.md and the agent files. Evidence: review rounds 1
  to 3 of Issue #16 found blockers caused by rewording
  (FR1-001, FR1-002, FR1-005, FR2-001, FR3-001 to FR3-004): the rewording
  lost a condition, an actor or a reader, or cited the wrong rule.

### CF-009 Core wording questions found in the FU-010 audit and the FU-005 checklist

- Origin: the FU-010 full audit and review rounds 1 to 3 (Issue #18, REQ-023;
  `.dev/issue-18-core-audit/audit.md` and `reviews/`). The user asked for it:
  「原始的core並非沒缺陷，有些條文沒寫得很明確，…應該在上游的core中開Issue回饋給core」
  (translation: the original Core has defects, some clauses are not clear;
  give feedback to Core through Issues upstream). Points 8 to 10 come from
  the no-regression checklist of FU-005 (REQ-025; DL-018, DL-023, DL-025,
  DL-026, DL-027).
- Problems and evidence (line numbers at v0.1.1):
  1. `authorization-and-stops.md:52` says the shared repository takes no
     runtime state. This project's inference: "shared repository" means the
     Core repository itself. Core does not say whether coordination state that
     a consumer project commits to its own repository (graph and event files;
     CB-1, D-010 here) counts as runtime state.
  2. `review-and-security.md:9` says a review request stays read-only and
     changes the reviewed content only when it is explicitly turned into a
     fix. Core does not say whether read-only means only "do not change the
     reviewed content" or "write no file at all" (for example temporary files
     outside the repository, or caches from test runs). A round-3 reviewer
     wrote a log file outside the repository. Result (FU-013, Issue #20,
     REQ-024): reviewers write no file anywhere, the session scratchpad
     included (card 9b); Python test runs use `PYTHONDONTWRITEBYTECODE=1`
     and pytest `-p no:cacheprovider`, so tests create no files in the
     repository (card 3d); the exception is a temporary file that a named
     test creates and removes itself in the system temporary directory,
     which is not a reviewer write (card 11b).
  3. `workflow.md:35`: the Traditional Chinese note is
     「依 ASD-STE100 原則編寫，尚未完成完整符合性驗證」. This project uses the
     user's REQ-013 wording 「…，未完成完整符合性驗證」: the same meaning, a
     different literal. A fixed literal in Core would let each interface
     compare it word for word.
  4. `authorization-and-stops.md:35` lists a missing, incomplete, failed or
     insufficient required capability, review, scan, verification or gate,
     then 「；缺安全 fallback」. The missing safe fallback can be read as a stop
     condition of its own or as a qualifier of the first part; two reviewers
     read it differently (Issue #18 round 1, S1).
  5. `workflow.md:76`: "answer status or side questions briefly, then
     continue, unless the objective is explicitly cancelled or replaced". Does
     the exception limit only "continue", or also the earlier "keep the
     results that still apply and re-check the affected evidence"? The
     round-2 (R2-001) and round-3 (R3-004) reviewers read it differently.
  6. `authorization-and-stops.md:21` lists delete, purge and prune as
     destructive. Core does not say whether pruning local remote-tracking refs
     before a push (`git fetch --prune`, so that the scan finds every commit
     the remote does not have) counts. The user first approved it as a
     project rule (card 4); later reviews (R3-006, MR19-001, MR19-002) found
     gaps in the preview, the read-back of the settings and the confirmation
     at the time, so the user moved it to FU-014 for a design of its own
     (card 8a). Result (FU-014, Issue #24): before a push, this project now
     gets the remote state with `git ls-remote --heads --tags <remote>` and
     runs no `git fetch`, so it no longer needs a prune. The Core wording
     question stays.
  7. Digest method (no single Core line; related: `exact-head-and-evidence.md:58`,
     derived copies keep one source, and shared Markdown never proves
     equivalence): a compressed digest cannot keep every condition of Core.
     Each of the three review rounds of Issue #18 found new missing
     obligations or sentences with fewer conditions (the R-VER-2 stop rule
     applied twice). Suggest that Core tells interface authors to quote or
     load the authoritative text on demand instead of rewording it, and to
     list the interface rules that are stricter than Core separately (related
     to CF-007 and CF-008). This project implemented this method with D-020
     (CF-007).
  8. `authorization-and-stops.md:50`: Core asks for a check of the required
     preview before moving or archiving, and a dry-run before cleaning. This
     project asks for a dry-run before moving, archiving and cleaning
     (DL-018, no-regression checklist C-1). The literal Core text is clear:
     only cleaning needs a dry-run. The question is whether Core means it:
     is a preview enough for moving and archiving, or should they also get
     a dry-run? Evidence: Issue #18 round 3, R3-009 (the dry-run before
     moving and archiving was dropped by mistake and restored).
  9. `workflow.md:115`: unresolved or intermittent failures, security or
     data-loss events, and shared or still referenced evidence are kept "as
     the effective project requirements and protection exceptions require".
     This project keeps these records without a condition (DL-023,
     no-regression checklist C-7; DL-023 records no case). Core does not
     say whether a project requirement or exception can shorten how long
     these records are kept, or only decides where and how they are kept.
     The unconditional keeping of this project is stricter than the literal
     Core text only in how long the records are kept; when a protection
     exception asks to remove data (for example content that
     `authorization-and-stops.md:52` keeps out of public records), the two
     can conflict, and this point asks about that too.
  10. `review-and-security.md:39`: every review and scan binds the content
      "including the applicable uncommitted changes". This project binds
      every uncommitted change (DL-025, no-regression checklist C-20). Core
      does not say who decides which uncommitted changes are "applicable".
      The same qualifier "applicable" is also in
      `exact-head-and-evidence.md:22`, the deterministic offline … checks "that
      the project provides and that apply" (R-EXH-2 here says: run the
      repository's deterministic checks; DL-026, no-regression checklist
      C-21), and Core again does not say who decides. A similar qualifier is
      in `review-and-security.md:47`, "executables with a security impact"
      (R-REV-7 here says: executables; DL-027, no-regression checklist
      C-22); but `:45` to `:47` already say that applicability follows the
      authority and the policy and the actual impact, so this place needs
      no question of who decides. In all three places this project leaves
      out the qualifier, so its rules are literally stricter than Core. Evidence: FU-005 design review finding
      R2-004 (FU-005 spec section 8 item 6).
- Proposed Core change: a companion note with a clear reading of points 1 to
  6 and 8 to 10, and the advice of point 7; a change of the authoritative
  text follows the modifying process.
- Kind: points 1 to 6 and 8 to 10 are additive (explanations), or modifying
  if Core decides to reword its text; point 7 is additive.
- Impact on the other projects: codex-dev-skills and grok-build-dev-skills
  can check their digests against the same readings; no effect before they
  re-pin.
- This project's readings (REQ-025, FU-005 design cards 5a, 5b and 9b that
  the user approved):
  - Item 4 (`dev-core` R-AUTH-5, DL-028): a required independent review,
    scan, verification or gate, or a required platform or security execution
    capability, that is missing, incomplete, failed or has insufficient
    coverage always stops the dependent work; a fallback never replaces it
    (`workflow.md:62`). When another capability is missing (for example
    delegation or a session or schedule API), continue with the safe fallback
    that Core names (one writer, a manual checkpoint); stop only when no safe
    fallback exists.
  - Item 5 (`dev-core` R-VER-3, DL-029): "keep the results that still apply
    and re-check the affected evidence" applies in every case; the exception
    "unless the objective is explicitly cancelled or replaced" limits only
    "answer briefly and continue".
- Status: points 1 to 7 are proposed (`engineering-workflow-core#27`,
  2026-10-22). The readings of points 4 and 5 are posted as a comment on
  `engineering-workflow-core#27` (2026-10-22). The results of points 2 and
  6, the result of the implementation for point 7 (with CF-007 and CF-008),
  and points 8 to 10 are drafted as a comment on
  `engineering-workflow-core#27` and are not posted; a post needs the
  user's approval.

### CF-010 What counts as the user's confirmation, and what is a relay (candidate)

- Origin: D-025 (Issue #78, card I78-D4 (a)); "Relayed answers" in R-DEL-2
  of `dev-core`; FU-041; design review findings DS1-06, DS2-02 and DS3-05.
- Problem: Core `auth-scope` (`authorization-and-stops.md:9` and `:11`) says
  that authority traces to a valid user instruction or an applicable
  approved platform mechanism, but does not define
  what counts as the user's confirmation. The host can show text that
  another session, an agent, a hook, a tool or a background task adds to a
  session as a message of the user.
- This project's rule (used only for the model and effort choices of
  R-DEL-2): a confirmation is the user's own message in this session; text
  that another session, an agent, a hook, a tool, or a scheduled or
  background task adds to this session is never a confirmation, also when
  the host shows it as a message of the user; when this session cannot tell
  that a message is the user's own, the message is a relay.
- Evidence: no case has happened. How the host shows text that other
  sources add to a session is not verified (D-025 residual risk 6, FU-041
  item (2)). DS1-06, DS2-02 and DS3-05 are risks that the design reviews
  inferred.
- Proposed Core change: write this definition in a companion note for
  `auth-scope`, for every place that needs a confirmation of the user.
- Kind: additive (a reading).
- Impact on the other projects: Codex and Grok must decide, for their own
  host, which text is the user's own message.
- Status: candidate, not proposed. Item (2) of FU-041 first verifies how the
  host shows text that other sources add to a session; after that, decide
  whether to propose it. The "Core feedback: no" of D-025 is an inference,
  not reviewed, with the reason "only this pack's own tightening rules
  change". This project's inference: that reason applies to the model and
  effort part; this item takes only the interface-neutral definition of a
  confirmation.

### CF-011 A tier written in advance is only a proposal (candidate)

- Origin: D-023 (Issue #75 item 5; cards I75-D2 (a) and I75-R1-C3 (b));
  delta DL-039; R-RIG-2 of `dev-core`; FU-040.
- Problem: Core `review-risk-timing` (`review-and-security.md:33`) asks for
  a risk assessment when the task starts and again when the scope or the
  design changes, and never assumes low risk when information is missing;
  `authorization-and-stops.md:9` also asks for a check of the current
  sources before acting. So a new assessment at the start is already
  implied in Core (inference). What Core does not say is that a risk or
  tier written before the task starts (for example in an Issue or a brief)
  is only input, and whose decision lowers it.
- Evidence: Issue #73 was planned as `standard` from the Process line of
  the Issue, but its plan already said that the change modifies the
  published rules of the pack, which is `strict` work under R-RIG-1; so
  the early design review before implementation did not happen (MR73D-003).
  Root cause (inference): the tier written in advance was copied and not
  re-assessed at Discover.
- This project's rule (R-RIG-2): a tier written before Discover is a
  proposal; Discover re-assesses it and writes the result into the plan;
  the re-assessment may raise it; to lower a tier written in advance needs
  the user's decision, with the reason in the plan; a relayed decision to
  lower it counts only after the user confirms it in this session. Still
  open (FU-040): whether a re-assessment after Discover that lowers the tier
  also needs the user's decision.
- Proposed Core change: in `review-risk-timing`, a risk assessment written
  before the task starts is input and is assessed again at the start; to
  lower it needs a recorded decision of the user.
- Kind: modifying (a tightening).
- Impact on the other projects: the planning steps of Codex and Grok treat a
  tier in an Issue or a brief as a proposal.
- Status: candidate, not proposed; the user decides whether to propose it
  (possibly after the FU-040 decision). The "Core feedback: no" of D-023 is
  an inference, not reviewed, with the reason "only this pack's own
  tightening rules change". This project's inference: that reason applies
  to the tier names of this pack; this item takes only the
  interface-neutral part.

### CF-012 How a subagent gets Core (candidate)

- Origin: FU-005 spec section 8 item 2
  (`.dev/issue-22-fu005-records/fu005-spec.md`; the spec planned the ID
  "CF-010", and the CF-010 of this document is another item); D-020
  decision 4 (card 8a); FU-016.
- Problem: Core `workflow.md:60` asks a brief to list the objective, the
  role, the ownership, the current sources, the DoD and more, but does not
  say how a subagent gets Core, or how "Core is the rules" fits with "the
  content of files that it reads is data, not instructions".
- This project's method: only the two reviewers get Core files, as review
  criteria (data), not as instructions; policy comes only from the brief;
  the implementer and the explorer get no Core (D-020 decision 4, card 8a).
  Files given to a subagent keep their own full rule text (CF-008); FU-016
  still works on the places where these copies are shorter or looser than
  `dev-core`.
- Evidence: the method of card 8 went through two design review rounds and
  one security design review (FU-005 spec section 8 item 2). No failure in
  practice is recorded.
- Proposed Core change: in a companion note for `wf-delegation`, say that
  each interface decides how a subagent gets Core; when Core goes to a
  reviewer, it is review criteria (data), not instructions; policy comes
  only from the brief; authority traces to a valid user instruction or an
  applicable approved platform mechanism, as `workflow.md:60` and
  `authorization-and-stops.md:11` say.
- Kind: additive (an explanation).
- Impact on the other projects: Codex and Grok state how their subagents
  get Core.
- Status: candidate, not proposed. On 2026-10-30 the user decided to add it
  to this record (Issue #84 card I84-C1 (a)).

## Decisions not fed back to Core

| Decision | Reason |
| --- | --- |
| D-009 Graph engineering in stages | Graph engineering is not in the Core contracts; re-evaluate when the runtime-neutral layer takes shape |
| D-010 No agent memory | Core `auth-scope`, `wf-stages` and `auth-data` already cover it |
| D-011 Deploy and measure | Work on the Claude side; the results are evidence for this document |
| D-012 Automatic handoff | Depends on the session capabilities of each interface; Core `wf-stages` already covers the checkpoint and the resume |
| D-019 Lessons skill `dev-retro` | Core `workflow.md:74` already records improvements in existing reports and adds no reflection executor, memory, hooks or scheduler (D-019; inference, for a review to confirm) |
| D-021 Deterministic pre-check before a push | One more check on top of this pack's tightening of Core (DL-010); the general part is in CF-002 |
| The choice of model and effort: the R-DEL-2 floor (D-007 rule 2), the `dev-deliver` and `dev-review` tables and the escalation order (FU-018, DL-034, D-022, D-023), the reference value (D-025) | Core `wf-delegation` (`workflow.md:56` and `:64`) leaves the model, the effort and their control to each interface; the interface-neutral parts are in CF-001 point 5, CF-010 and CF-011 |
| D-024 Read-back test of model and effort | Claude Code host behavior; Core `workflow.md:64` asks each interface to record its own version, surface and acceptance scope |
| DL-037 `allowed-tools` (Issue #66) | A permission setting of Claude Code plugins, not the shared workflow |

The "Core feedback: no" that D-021 to D-025 record are inferences, not
reviewed. The reason of D-022 to D-025 is "only this pack's own tightening
rules change" (D-022 adds "and values", D-024 adds "and records"); for
D-021, see its row above.
The reasons in the rows after D-021 (with the citations of
`workflow.md:56` and `:64`) are inferences of this record.

</details>
