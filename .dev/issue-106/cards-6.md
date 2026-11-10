# Issue #106 卡片 I106-C10（PR-3）

請在 Issue #106 的 session 直接打字回答，例如「C10 a」。轉述的答案不算：依卡片 I106-C5 (b)，改到檢查 script、reference 或釘住的 digest，要你在派 review 的那個 session 親自打字。這張卡在 PR-3 實作。

回答（使用者在本 session 的訊息，2026-11-10，為 PR-3 這次變更）：「C10 a」。

## I106-C10：紀錄的 id 拿掉 `st_dev`，接受版本提高到 3 嗎？

- 問題：紀錄的 id 目前用 clone 的 `.git` 資料夾的 realpath、`st_dev` 和 `st_ino` 算出來。要不要拿掉 `st_dev`，只留 realpath 和 `st_ino`？
- 為什麼要你決定：這會改到 `reviewer_acceptance.py`、`skills/dev-core/references/reviewer-acceptance.md` 和釘住的 digest，屬於 setup change（reference 的 Setup change 一節，卡片 I106-C3 (a)、I106-C5 (b)）。你的決定要寫明版本是否提高。
- 事實（orchestrator 查證，2026-11-10）：
  - 這台機器重開機後，這個磁碟的 `st_dev` 變了。
  - 紀錄檔還在，但 id 變了，所以 `check` 印出 `STOP NO_RECORD`，你要重跑 `accept`。
  - 照目前的設計，之後每次重開機都可能要重跑 `accept`。
- 修法：刪掉 id 裡的 `st_dev`。
- 版本：reference 裡描述 id 的文字被版本號綁住，改了就要把接受版本提高到 3（reference 的 Version rule）。PR-3 merge 之後，你要再跑一次 `accept`。
- 殘餘風險：同一個路徑改掛另一顆磁碟，而且 `.git` 資料夾的 inode 剛好相同時，舊紀錄會被沿用，檢查會印 `PASS`。realpath 已經區分了不同的掛載位置，所以這個機率低（推論，未驗證）。
- 選項：
  - **(a) 拿掉 `st_dev`，版本提高到 3，PR-3 merge 後重跑 `accept`。**（建議）
  - **(b) 維持現狀。** 每次重開機後如果 `st_dev` 改變，就要重跑 `accept`。
