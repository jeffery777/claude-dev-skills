# Issue #101 決策卡 第 7 組：U1 實作審查第 3 輪的停止卡（2026-11-05）

依據：`reviews/impl-u1-round-3.md`。

- deep 審查報了一個新的 SHOULD-FIX（IR3-D-01），R-VER-2 的停止規則第五次成立。
- Security Diff Scan 沒有阻擋項，只有一個 NIT。
- 第 2 輪的問題幾乎都解決了；只有 IR2-D-02 部分解決，也就是這一項。
- U1 已 stage，沒有 commit。你回答之前，我不會修任何東西。

**先更正卡 I101-IR2-C1 (a) 的三句話。** 你是看著這些話回答的：
- 卡上寫「閱讀抓得到」PR #100 的 P3-T3。這句太寬：只有 reviewer 拿到的 diff 只含那次修正時才成立。修正和節點 stage 在一起時，閱讀也看不出來。
- 卡上寫 `--cached` 形式「兩位 reviewer 都實跑過」。實際上它們跑的是不加 `--cached` 的形式；`--cached` 形式是後來才第一次實跑，結果通過。
- 卡上寫 Merge Review 形式「已實測」。第 2 輪的紀錄查不到這件事；第 3 輪 deep reviewer 才實跑通過。

### 決策卡 I101-IR3-C1：閱讀核對的限制要怎麼處理

- **問題：** 「修正輪有沒有加自己的 `log.md` 列」這件事，閱讀核對只有在 reviewer 看到的 diff 只含那次修正時才有效。要把這個限制寫進規則就收尾，還是繼續補機制？
- **為什麼要你決定：**
  - R-VER-2 停下時，做法的重新評估要交給你決定。
  - 你選 IR2-C1 (a) 時看到的「閱讀抓得到」太寬，這張卡等於重新問你。
- **選項：**
  - **(a) 把限制寫進規則，不加機制（建議）**
    - 做法：
      - 規則改回卡上的用字「修正 diff」，並加一句：閱讀只在 target 顯示那次修正時有效；target 是累積的 diff 時，分不出輪次，報告要寫明。
      - 主代理能給修正 diff 時就給；這是「能給就給」，不是硬性順序。
      - 修掉三個 NIT，補齊 plan 的紀錄。
      - 做一次窄範圍確認（R-REV-4），然後 commit U1，進 U2。
    - 結果：
      - 規則只宣稱它做得到的事。
      - 缺陷 1 的改善是：寫入端的 brief 有明文規則，commit 前有搜尋清單和規則 1。
      - 累積 diff 上的第二次改動漏列，要靠寫入端遵守規則。
    - 風險：PR #100 那種漏列，在累積 target 上兩種檢查都可能漏掉。
    - 成本：一輪小修正和一次窄範圍確認。
  - **(b) 規定修正輪的審查一定要拿到修正 diff**
    - 做法：修正輪的改動留到審查跑完才 stage；上一輪沒過時也要先 stage，再做下一輪。
    - 結果：閱讀核對每一輪都有效。
    - 風險：這等於加回 IR2-C1 (a) 刪掉的順序，新檔和綁定的問題（IR2-S-02）可能回來；這個機制已經修了六輪。
    - 成本：一輪修正加一輪審查，可能再停。
  - **(c) 把 E1 拆到另一個 Issue**
    - 做法：這個 PR 只做 E2 和 E3，Issue #101 的完成條件改成缺陷 2、3。撤回 U1；刪除新檔之前會另外問你（R-AUTH-3）。
    - 結果：這個 PR 範圍最小。
    - 風險：缺陷 1 要等新 Issue；已做的 U1 審查白費。
    - 成本：多一個 Issue 和 PR。
- **建議：** (a)——寫清楚限制，比再加一層機制誠實，也符合 Issue 的「a rule or a deterministic check」。
- **如果你不決定：** U1 不能 commit，U2、U3 不能開始。
- **我走過的路徑（選項 (a)）：**
  - 第一個節點：stage 後跑 `--cached`，閱讀看整個節點 diff，有效。
  - 修正輪，target 是修正 diff：閱讀有效。
  - 修正輪，target 是累積 diff：閱讀分不出來；報告寫明限制，不算通過這一項。
  - 第二個修正輪：同上，看 target 是哪一種。
  - 沒有 commit 授權：沒有指令；規則與閱讀仍適用。
  - commit 接在其他 commit 之後：`--cached` 只看這個 commit，規則 1 有效。
  - Merge Review：三種形式已實跑；同一個 commit 裡的第二次改動抓不到。
  - PR #100 的 P3-T3：當時 target 是修正 diff，閱讀有效；累積 target 上抓不到。
- **證據：**
  - 事實：
    - deep reviewer 在 PR #100 的 tree 上實測：只含修正的 diff 列出 REQ-009，沒有 `log.md`；累積的 diff 有一列 `+|` 寫著 REQ-009，看起來沒問題（`reviews/impl-u1-round-3.md`）。主代理沒有重跑。
    - PR #100 第 2 輪的審查範圍是 "scoped to the fix diff of P3-T3"（`.dev/issue-96-pr3/plan.md:295`）。
    - Issue #101 "Done when"："a rule or a deterministic check, each with a test or a recorded example"。
  - 推論：把規則寫進 brief 之後，寫入端會少漏這類紀錄。
  - 未驗證：(a) 的窄範圍確認能否一次通過。
