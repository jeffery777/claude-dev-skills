# Issue #106 卡片（設計審查第 1 輪之後）

請在本 session 直接打字回答，例如「C1 a，C2 a」。轉述的答案不算：C1 是 Core 規定要由你本人做的接受，C2 的 (b) 有一部分是放寬。

回答（使用者在本 session 的訊息，2026-11-09）：「C1 a，C2 b」。

## I106-C1：reviewer 寫入通道的一次性接受，「環境」綁到哪裡？

- 問題：要不要接受 reviewer 有 Bash 這個殘餘風險？如果接受，綁定的環境範圍要多大？
- 為什麼要你決定：Core v0.5.0 `review-and-security.md:29` 寫明「Agent 不自行接受或推定接受」。
- 事實：
  - Core 要求必要 reviewer 沒有有效寫入通道（`review-and-security.md:21`）。pack 的 `dev-reviewer` 和 `dev-security-reviewer` 有 Bash，所以不算技術唯讀（`agents/dev-reviewer.md:6-7`）。
  - Core 允許你對「特定執行環境」一次性接受這個風險（`:29`）。每次 review 都要核對接受紀錄適用於「當前路徑與資源」；工具、權限、受保護資源或偵測方法改變時，要重新接受（`:31`）。
  - 替代偵測是 CB-4：review 前後比對 HEAD、status 和 diff hash。worktree 和 index 以外的一切它都看不到，包括 `.git` 裡的 refs 和 objects（push 和 merge 掃描的對象）、未追蹤的文字檔（文字掃描的對象）、網路寫入（例如用你的 `gh` token 做 merge 或關 Issue），以及改了又改回的修改。
  - 接受紀錄會放進公開 repo（`docs/design-proposal.md` 的 D-032），別人 clone 後也讀得到。所以每次 review 前，主代理會跑一行檢查，只印 PASS 或 STOP。檢查失敗時，review 不算完成，相依的 gate 停下。
  - 變更本身如果改到 reviewer 的 agent 檔、`check_pack.py` 的釘選或 D-032，這次變更的 review 不適用 D-032，要你重新接受。
- 推論：換一個 repo，受保護資源也就換了。所以「任何 repo」是否還算 Core 說的「特定執行環境」並不清楚；選 (c) 可能變成放寬 Core。
- 選項：
  - **(a) 只限你的帳號、只限 `jeffery777/claude-dev-skills`。**（建議）
    - 檢查：`gh api user` 的登入名是 `jeffery777`，而且目前 repo 是 `jeffery777/claude-dev-skills`。
    - 代價：你在其他 repo 用這個 pack 時，必要 review 會停下，要另外接受，例如把那個 repo 加進 D-032。
  - **(b) 你的帳號，加上 `jeffery777` 擁有的所有 repo。**
    - 檢查：登入名是 `jeffery777`，而且目前 repo 的 owner 是 `jeffery777`。組織或客戶的 repo 不在內。
    - 代價：每個 repo 的受保護資源不同。這樣的範圍是否仍算「特定環境」，屬於推論。
  - **(c) 你的帳號，任何 repo。**
    - 檢查：只看登入名。
    - 代價：可能放寬 Core（見推論）；依 `skills/dev-core/deltas.md:4`，放寬 Core 一律是缺陷。
  - **(d) 不接受。**
    - 結果：PR-1 合併之後，每個必要 review 和掃描都會停在 gate（這句在你回答之後更正：原文寫「PR-2 的 vendor bump 合併之後」，DR2-03），直到另有唯讀 reviewer 或你另做接受。
- 未驗證：無法在不公開主機名稱的情況下檢查是哪一台機器，所以所有選項都不綁機器。主機權限設定的改變無法每次檢查，責任人是你。

## I106-C2：R-WRT-1 的詳細寫作規則，一般摘要還要全部適用嗎？

- 問題：Core v0.5.0 把寫作分兩層。一般摘要和紀錄只要短的最低要求。文件本身是交付物或審查對象時，才讀完整的 `writing.md`。pack 現在的 R-WRT-1 對所有摘要都適用較長的一組規則。要保留這組規則嗎？
- 為什麼要你決定：其中有一部分是專案的加嚴，縮回 Core 層級是放寬，只有你能決定（`skills/dev-core/deltas.md` 的 no-regression definition）。
- 事實：
  - R-WRT-1 的詳細規則大多轉述自 Core v0.1.1 `wf-writing` 第 1 到 6 項（DL-017）。只有「繁中白話寫作條」和「每份 review 與 gate 報告都附 STE 聲明」是專案加嚴（DL-014，`deltas.md:37`）。
  - Core v0.5.0 的最低要求有三項：行動、對象、條件清楚；保留安全與限制；術語一致（`contracts/workflow.md:30-34`）。
  - Issue #106 Scope 7 寫的是「一般摘要用短的最低要求」。
- 選項：
  - **(a) 保留詳細規則，只加第二層。**（建議）
    - 內容：R-WRT-1 維持現有內容，補上 Core 的兩句新要求，在 DL-017 記為「相對 v0.5.0 是加嚴」。新增 R-WRT-2：文件本身是交付物或審查對象時，讀 `writing.md` 全文。寫作抽查移到 R-WRT-2，因為完整契約裡已有抽查。
    - 落差：第一層不會變短，和 Scope 7 的「短」不完全一致。
    - 理由（推論）：這些規則多半是轉述 Core，留著的成本低。
  - **(b) R-WRT-1 縮成 Core 的三項最低要求，再加上專案的兩條加嚴。**
    - 內容：轉述 Core v0.1.1 的部分刪掉；完整規則改由 `writing.md` 涵蓋。繁中白話條和 STE 聲明保留。
    - 放寬範圍：一般摘要不再適用「一句一主題、步驟有序」這類細則，只有在讀完整契約時才適用。這部分要你在本 session 打字確認。
  - **(c) (b) 再加上：連繁中白話條也只在完整契約時適用。**
    - 放寬範圍：比 (b) 多放寬 DL-014 的繁中部分。STE 聲明仍保留。
