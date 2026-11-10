# Issue #106 卡片（PR-2 開始前）

請在本 session 直接打字回答，例如「C12 a」。

回答（使用者在本 session 的訊息，2026-11-10，為 PR-2 這次變更，即 branch `issue-106-pr2-vendor-bump` 的變更）：「C12 a」。

## I106-C12：push 會送出 Git LFS 物件或 push option 時，要怎麼處理？（MR108-01）

- 問題：push 掃描看不到 Git LFS 物件和 push option，目前卻仍然算通過。要改成停下，還是只記錄為和 Core 的落差？
- 為什麼要你決定：Core v0.5.0 `review-and-security.md:81` 規定，必要掃描的 coverage 不足，不能算通過；`:91`、`:99` 規定，push 前要檢查實際送出的內容，未知時要停下。目前的做法是 FU-007 (b) 在 Core v0.1.1 時你接受的殘餘風險。選 (b) 等於放寬 Core 的規定，必須由你親自打字。
- 事實：
  - push 步驟 3 已經規定指令列不能加其他 option，所以 `-o`／`--push-option` 本來就會停。沒有檢查到的是設定檔 `push.pushOption`：Git push 時會自動送出這個設定（本 session 實測，git 2.54.0：沒設定時 `git config --get-all push.pushOption` 什麼都不印，exit 1；有設定時會印出值）。
  - LFS 物件由 pre-push hook（`git lfs pre-push`）上傳。上傳的是這次 push 的 commit 裡 LFS pointer 檔指到的物件。pointer 檔的第一行是 `version https://git-lfs.github.com/spec/v1`（LFS 規格；這台機器沒有安裝 git-lfs，未實測）。
- 選項：
  - **(a) 會送出時就記為 `NOT_RUN` 並停下，由你決定。**（建議）
    - 做法：在 push 步驟裡加一道確定性檢查，由主 agent 執行，不改 reviewer 的 agent 檔。
      - `git config --get-all push.pushOption` 必須什麼都不印。
      - 步驟 8 的掃描輸出裡，不能有新增的 LFS pointer 行（`^+version https://git-lfs.github.com/spec/v1`）。
    - 同時從 `push-scan.md` 的「Not covered」清單拿掉這一項，並關閉 FU-007 (b)。
    - 優點：符合 Core；只加一道檢查；這個 repo 沒有使用 LFS，也沒有設定 push option，所以平常的 push 不受影響。
    - 缺點：有使用 LFS 的安裝者，每次推送 LFS 檔案都會停下。
  - **(b) 規則不改，記成和 Core 的落差，由你接受。**
    - 做法：在 `deltas.md` 新增一列 loosen，寫明來源、你的原話、理由和範圍。
    - 優點：完全不改程序。
    - 缺點：掃描仍然在沒看到的內容上算通過，和 Core 衝突；只是把衝突記下來。

## I106-C13：C12 (a) 的做法修正，以及剩下的 LFS 殘餘風險，你接受嗎？

回答（使用者在本 session 的訊息，2026-11-10，為 PR-2 這次變更）：「C13 a」。

- 問題：設計審查發現 C12 卡片上寫的 LFS 檢查方法有兩個漏洞，我已經在 (a) 的範圍內修改做法。修改後仍有兩種少見情況檢查不到，要不要記為你接受的殘餘風險？
- 為什麼要你決定：殘餘風險只有你能接受（R-REV-8）；做法和 C12 卡片上寫的不同，要讓你知道（審查紀錄 `reviews/pr2-design-round-1.md`）。
- 做法修正（仍在 (a) 的範圍內）：
  1. pre-push hook 在 dry-run 時就會執行，LFS 物件可能在檢查之前就送出（P2D-01）。所以 dry-run 改加 `--no-verify`，dry-run 時不執行任何 hook；真正 push 時仍照常執行。
  2. 卡片上的樣式只抓得到新增的 pointer 檔，抓不到最常見的「更新已追蹤的 LFS 檔」（P2D-02），強制彩色輸出時也會漏掉（P2D-03）。所以改抓 pointer 檔的 `oid sha256:` 行，不限新增、修改或刪除。
- 檢查不到的情況：
  - 遠端已經有的 commit 指到某個 LFS 物件，但 LFS 伺服器上還沒有這個物件。步驟 6a 只讀遠端還沒有的 commit。
  - diff 看不出來的 pointer，例如只改了檔名。
- 選項：
  - **(a) 接受。** 這兩種情況寫進 `push-scan.md` 的「Not covered」，取代原本「push options and Git LFS objects」那一項。（建議）
    - 優點：只是記錄，不增加檢查。這個 repo 沒有使用 LFS。
    - 缺點：這兩種情況仍然可能送出沒有掃描過的 LFS 物件。
  - **(b) 不接受。** 只要 repo 有 LFS 的 pre-push hook，每次 push 都停下。
    - 優點：沒有缺口。
    - 缺點：有使用 LFS 的安裝者，每次 push 都要停下來問你。
