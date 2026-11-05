# Issue #101 決策卡 第 12 組：U2 第 2 輪審查（2026-11-05）

依據：`reviews/impl-u2-round-2.md`。

- 第 2 輪：Security Diff Scan 1 個 MUST-FIX；兩份合計 3 個 SHOULD-FIX（其中一個是 REQ-GAP）、3 個 NIT。R-VER-2 的停止規則成立。
- 你回答之前，我不會修任何東西。
- 卡 U2S-C1 (a) 寫「同一句複製進 agent 檔」，實際放的是另一句。兩位 reviewer 都判定這仍在你的選項之內，因為它更嚴；但他們都不接受 plan 寫的理由，我會改掉。

**我擬的句子有錯。** 卡 U2S-C1 (a) 的文字是我擬的，兩個問題都出在那裡：
- 例外句用「誰寫的」劃界。你的私人指示檔也是你寫的，所以逐字引用反而過得了，只有轉述被擋。
- 類別沒有界線。照字面，連 repo 追蹤的 `CLAUDE.md`、agent 檔，以及別的專案裡 repo 外的 pack 檔都不能寫。

卡上走過的六條路徑，沒有一條試過被保護的內容本身。

### 決策卡 I101-U2R2-C1：R-AUTH-7 的新文字

- **問題：** R-AUTH-7 要換成用「內容從哪裡來」劃界的句子，還是用別的做法？
- **為什麼要你決定：** 這會改掉你選的 U2S-C1 (a) 的文字；新的隱私風險也由使用者決定（Core `authorization-and-stops.md:34`）。
- **選項：**
  - **(a) 改成用來源劃界，並刪掉例外句（建議）**
    - 做法：Never commit 清單最後一項改成：
      > or the content of native memory and of private files that this repository does not track (for example the user's instruction files). Files of this pack are not private files. When it is unclear whether a file is private, treat it as private.
    - 同時刪掉例外句，也刪掉 "chosen to publish"。agent 檔的句子用同一類的字，Never write 不變。
    - 結果：
      - 例外句不再需要：你在訊息裡說的話不是檔案，本來就不在這一類。
      - 私人指示檔的逐字引用和轉述都被擋下。
      - 「選擇公開」不用再解釋：你要公開，就自己在訊息裡給出那段文字。
    - 風險：「私人檔案」要靠判斷；不確定時當成私人，失敗方向是多擋。
    - 成本：一輪小修正和一輪範圍限定的審查。
  - **(b) 保留現在的句子，補上條件**
    - 做法：例外句限定「在 session 訊息裡說的話」，類別限定「repo 沒有追蹤的」，並補上 pack 檔例外和「選擇」的形式。
    - 結果：句子更長，有四個要解釋的條件。
    - 風險：同一機制已經修兩輪，每多一個條件就多一個邊界。
    - 成本：同 (a)，可能多一輪。
  - **(c) 把私人內容這一類拆到另一個 Issue**
    - 做法：這個 PR 的 R-AUTH-7 不動，紀錄寫明這類內容只靠 R-REV-9 掃描，開新 Issue。
    - 結果：U2 只剩 R-EVD-3，範圍回到 Issue 原本的內容。
    - 風險：新 Issue 完成前，保護只有一層；repo 是公開的，外洩無法收回。
    - 成本：多一個 Issue 和 PR。
- **建議：** (a)——它比現在的句子短，兩個 finding 的成因都拿掉。
- **如果你不決定：** U2 不能 commit，U3 不能開始。
- **我走過的路徑（選項 (a)）：**
  - 私人指示檔的逐字引用：擋下。這是上一張卡沒走的路徑。
  - 私人指示檔的轉述：擋下。
  - 原生記憶的內容：擋下。
  - repo 內被 ignore 的本機指示檔：沒有追蹤，擋下。
  - repo 追蹤的 `CLAUDE.md`、`AGENTS.md`、agent 檔：追蹤的，不算。
  - 別的專案裡 repo 外的 pack 檔：明寫不算，R-AUTH-6 可以引用。
  - 公開的第三方文件：不是私人檔案，不算。
  - 你的卡片回答和轉述的回答：不是檔案，不算。
  - floor check 的 model 和 effort：不是檔案內容，不算。
  - REQ 的 `doc`、`external` 來源：repo 內或公開的不算；私人文件留空引文（`requirements-wiki.md:23-26`）。
- **證據：**
  - 事實：`reviews/impl-u2-round-2.md`（U2R2-S-01、U2R2-S-03、U2R2-S-02）；`skills/dev-retro/SKILL.md:116-119`（pack 檔例外的先例）；`skills/dev-core/SKILL.md:99`（R-AUTH-6 要引用規則原文）。
  - 推論：用來源劃界就不需要例外句。
  - 未驗證：新文字還沒有審查。上面的路徑是我走的。

### 決策卡 I101-U2R2-C2：兩個 reviewer 檔要不要也加這一類

- **問題：** `dev-reviewer.md`、`dev-security-reviewer.md` 要不要也有這條規則？這是 REQ-GAP：需求沒有寫到 reviewer。
- **為什麼要你決定：** 只有使用者能加需求（R-REV-3）。
- **選項：**
  - **(a) 加需求（建議）**
    - 做法：REQ-029 加一項，兩個 reviewer 檔加上和其他 agent 檔同樣的類別句。
    - 結果：輸出會進紀錄的角色都有這條規則。
    - 風險：reviewer 檔又動一次。
    - 成本：兩行和一個測試。
  - **(b) 延後**
    - 做法：開 follow-up。
    - 結果：這個 PR 範圍較小。
    - 風險：reviewer 報告引用私人內容時，靠主代理和 R-REV-9 擋。
    - 成本：一個 follow-up。
  - **(c) 拒絕**
    - 做法：不加，記下理由。
    - 結果：維持現狀。
    - 風險：同 (b)，而且沒有後續。
    - 成本：無。
- **建議：** (a)——這次審查的 context 裡就有這類內容，而審查報告會 commit。
- **如果你不決定：** 照 (b) 記，不阻擋 U2。
- **證據：**
  - 事實：`agents/dev-reviewer.md:82-86`、`agents/dev-security-reviewer.md:61-65` 只有遮蔽句；`docs/requirements/REQ-024-agent-write-and-delete.md:67`。

## 修正輪一併處理、不需你決定的項目

- U2R2-S-05、U2R2-D-04：改掉 plan、REQ-029、D-030 不實的理由。
- U2R2-D-05：K4 三列改成 `historical`。
- U2R2-D-06：Files 表補上 R-AUTH-7 和新測試。
