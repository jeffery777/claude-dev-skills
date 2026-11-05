# Issue #101 決策卡 第 15 組：U3b 第 1 輪審查（2026-11-05）

依據：`reviews/impl-u3b-round-1.md`。

- deep：1 個 SHOULD-FIX、1 個 NIT。Security Diff Scan：1 個 SHOULD-FIX、1 個 NIT。兩份都讀回 `PASS`，都算數。
- 兩個 SHOULD-FIX 講同一件事：plan 裡有幾個 finding 的處置（disposition）沒寫完整。
- U3 第 1 輪和這一輪都報了新的 SHOULD-FIX，所以 R-VER-2 的第一個觸發條件照字面成立。兩輪的審查對象不同，但規則沒有排除這種情形，所以我從嚴算。
- U3b 已 stage，沒有 commit。你回答之前，我不會修任何東西。

**這次沒有問題的部分：** R-VER-2 和 base 相同，也沒有紀錄說它有改；U2 的三個 NIT 解決了；搜尋清單 357 列沒有差異；沒有私人資料；沒有改到規則、script、agent 檔或測試。

### 決策卡 I101-U3B-C1：怎麼收尾

- **問題：** 剩下的都是紀錄文字。要做一輪有上限的小修正後 commit，還是別的做法？
- **為什麼要你決定：** R-VER-2 停下時，要由你決定下一步。
- **選項：**
  - **(a) 只補處置，刪掉不需要的字；窄範圍確認後 commit（建議）**
    - 先依新方向判斷：這些是 agent 的紀錄錯誤，在威脅模型內；R-REV-3 和 `dev-gate` 第 4 步涵蓋它們，所以要處理。
    - 做法（主代理做，先過 floor check）：
      1. U3R1-D-03：記 `Rejected`（那些列在撤回的內容裡，這個 PR 沒有這些列）。
      2. U3R1-D-04：補上 re-review，就是 U3b 這一輪。
      3. PS3-01 到 PS3-03：`Fixed`，補上修正、驗證（PS4）和重掃。
      4. PS4-01、PS4-02：記 `Rejected`，寫明理由：PS4 的私人資料掃描通過，這兩項都不是 R-REV-9 清單裡的類別，不是私人路徑。
      5. U3B-S-02：從 D-030 的「使用者決定的內容」刪掉副本那半句（plan 已有這個事實），"superseded" 那句標 inference。
      6. U3B-D-02：不改 Issue #102 的文字，記 `Deferred`，目標是 Issue #102。理由：例外文字的修法確實沒做，改 Issue 又要一次掃描。
      7. U3b 的 commit 依據寫明是你這張卡的回答。
    - 然後：一次窄範圍確認（deep，opus/xhigh），範圍是這次修正 diff；接著 R-REV-9 commit scan、commit、push、開 PR。
    - **上限：**
      - 確認只報 NIT：只記處置，不開修正輪，直接 commit。
      - 確認報新的 MUST-FIX 或 SHOULD-FIX：再停下問你。
    - 結果：`dev-gate` 第 4 步的處置要求補齊；這個 PR 進入 push。
    - 風險：
      - 紀錄一直是停止規則最常見的來源；確認可能再報 NIT，上限讓它不再繞。
      - Merge Review 可能把 `Deferred` 的 U3R1-S-01（MUST-FIX）讀成未解。deep reviewer 判定不算，理由是文字已撤回，Core 也允許這四種處置（推論）。
    - 成本：一小輪修正和一次窄範圍確認。
  - **(b) 同 (a)，但不做窄範圍確認**
    - 做法：補完就 commit，由 Merge Review 涵蓋。
    - 結果：少一輪。
    - 風險：R-REV-4 規定修正後、push 前要窄範圍獨立確認，`dev-gate` 第 77 行也要；這等於放寬，我不建議。
    - 成本：放寬規則要多一筆決策紀錄。
- **建議：** (a)——修正幾乎都是處置字，沒有新機制。
- **如果你不決定：** U3b 不能 commit，PR 也開不了。
- **我走過的路徑（選項 (a)）：**
  - 確認沒有 finding：commit。
  - 確認只有 NIT：記處置；commit。
  - 確認有 SHOULD-FIX：停下開卡。
  - PS4-01 若其實是私人路徑：這是 MUST-FIX，Issue 文字要修並重掃。PS4 的報告寫「私人資料掃描：PASSED」，所以不是這種情形。
- **證據：**
  - 事實：
    - 四種處置：`skills/dev-core/SKILL.md:118-122`。
    - 缺處置是阻擋項：`skills/dev-gate/SKILL.md:74`。
    - 窄範圍確認：`skills/dev-core/SKILL.md:125`、`skills/dev-gate/SKILL.md:77`。
    - 其他 finding：`reviews/impl-u3b-round-1.md`。
    - 先判斷再修的方向：orchestrator 轉述你的決定（2026-11-05），本 session 沒有直接收到你的話。
  - 推論：U3b 的 commit 原本依卡 I101-C3 (a)；卡 I101-U3R1-C1 (b) 取代了它的 U3，所以這張卡的回答才是明確依據。
  - 未驗證：窄範圍確認會報什麼。
