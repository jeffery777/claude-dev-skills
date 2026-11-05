# Issue #101 決策卡 第 10 組：NC3 之後怎麼走（2026-11-05）

依據：`reviews/impl-u1-nc3.md`。

- 第 3 次窄範圍確認：0 個 MUST-FIX、0 個 SHOULD-FIX、1 個 NIT（NC3-01）。NC2 的三項都已處理。
- 卡 I101-NC2-C1 (a) 說任何新 finding 都要停，所以我停下。
- 這次的 target 只含修正，沒有查不到的部分。

**NC3-01：** DL-047、REQ-029 的來源欄和 D-030 寫「NIT 例外提早用了一次」或類似的話，但實際上例外沒有用。這是你後來選 NC2-C1 (a) 造成的：那張卡讓舊句子不再成立。

**為什麼這張卡不再建議「修完再確認」：** 每修一次副本就要再確認一次，每次確認都可能再找到一個副本。這個循環已經走了三次（NC1、NC2、NC3）。U2 本來就要改這些紀錄，也會有完整的實作審查。

### 決策卡 I101-NC3-C1：這個 NIT 怎麼處置

- **問題：** NC3-01 要現在修再確認一次，還是記成 `Deferred`，先 commit U1，由 U2 修？
- **為什麼要你決定：** 卡 I101-NC2-C1 (a) 說這種情形要停下，由你決定下一步。
- **選項：**
  - **(a) 記成 `Deferred`，先 commit U1，由 T2 修（建議）**
    - 做法：
      - NC3-01 的 disposition 記為 `Deferred`，欄位寫齊：目標 T2（U2）、負責人主代理、理由、剩餘風險、驗證方式（U2 的實作審查，brief 點名這一項）、升級條件（U2 沒修好就阻擋 push）。
      - stage 目前內容，跑含 K18–K23 的 `--cached` 檢查，做 R-REV-9 掃描，commit U1。
      - T2 把這幾句改成帶條件的寫法，並搜尋舊卡 ID 的其他摘要。
    - 結果：循環結束，U2 可以開始。這個 NIT 在 push 之前修好，公開的 PR 不會帶著它。
    - 風險：U1 的本機 commit 暫時留著一句不實的敘述，直到 U2 commit；它不會單獨 push。
    - 成本：沒有額外的審查輪次。
  - **(b) 現在修，再做一次窄範圍確認**
    - 做法：改這幾句，再派一次確認。
    - 結果：U1 的 commit 沒有這句。
    - 風險：可能再找到下一個副本，又要停。
    - 成本：一輪修正和一次確認，也許更多。
  - **(c) 把 E1 拆到另一個 Issue**
    - 做法：這個 PR 只做 E2 和 E3，Issue #101 的完成條件改成缺陷 2、3。撤回 U1；刪除新檔之前會另外問你（R-AUTH-3）。
    - 結果：這個 PR 範圍最小。
    - 風險：缺陷 1 要等新 Issue；已做的 U1 審查白費。
    - 成本：多一個 Issue 和 PR。
- **建議：** (a)——NIT 有完整 disposition 就不阻擋（R-REV-3），而且 U2 本來就要動這些紀錄。
- **如果你不決定：** U1 不能 commit，U2、U3 不能開始。
- **我走過的路徑（選項 (a)）：**
  - commit U1：commit gate 看 disposition，`Deferred` 欄位齊全就不阻擋。
  - T2：brief 點名 NC3-01；U2 實作審查核對。
  - U2 沒修好：升級條件成立，push 前停下。
  - push：U1、U2、U3 的 commit 一起 push，NC3-01 已修。
- **證據：**
  - 事實：
    - `skills/dev-core/SKILL.md:124`（R-REV-3："A NIT does not block once it has a disposition"）。
    - `skills/dev-core/SKILL.md:121`（`Deferred` 要有目標、負責人、理由、剩餘風險、驗證方式、升級條件）。
    - NC3-01 的內容：`reviews/impl-u1-nc3.md`。
  - 推論：這個循環再修一次也可能再出現一個副本。
