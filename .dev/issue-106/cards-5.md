# Issue #106 卡片（PR-3 審查之後）

請在本 session 直接打字回答，例如「C8 d，C9 a」。

回答（使用者在本 session 的訊息，2026-11-10，為 PR-3 這次變更）：「C8 d，C9 a」。這兩題都是範圍決定；轉述的答案要你在本 session 確認後才算。

## I106-C8：push 的目的地要怎麼檢查？

- 問題：push 前要確認「推到哪裡」。要用哪一種檢查？
- 為什麼要你決定：PR-3 目前的寫法只接受 `https://github.com/<owner/name>`，用 SSH、GitHub Enterprise 或 GitLab 的使用者每次 push 都會停下，而且沒有放行的路。在 base 版本這些 push 會通過。這是相容性倒退，也牽涉 Issue 的「任何安裝者都能完成必要掃描」（審查發現 P3D-01、P3S-09）。
- 事實：
  - Core v0.5.0 `review-and-security.md:91`：檢查要針對「實際目的地」。`:97`：「Push 前須核對實際送出的所有 URL／refspec 及相關 rewrite，不能只憑 fetch remote」。這兩句都沒有說目的地必須等於「任務的 repo」。
  - base 的 push 步驟 2：`git remote get-url --push` 和 `git remote get-url` 必須相同，而且各只有一個（`skills/dev-core/references/push-scan.md`）。`get-url --push` 印的是套用 `pushInsteadOf`、`insteadOf` 之後的實際 URL（本 session 2026-11-09 用 git 2.54.0 實測）。
  - 步驟 7 會用 `ls-remote` 讀到的 ID 核對強制更新；push 和 fetch 指向同一處，這個核對才有意義。
- 推論：「push URL 等於 fetch URL」證明這次 push 送到這個 clone 讀取的那個 repo，而且讀的是實際 URL（含 rewrite），符合 `:97`。它不證明這個 clone 就是任務要的 repo（例如 clone 錯了 repo），但 Core 原文沒有要求這一點。
- 選項（並列優缺點）：
  - **(a) 只接受 https 形式，寫進文件。**
    - 優點：最嚴格，形式單純。
    - 缺點：SSH、GitHub Enterprise、GitLab 使用者每次 push 都停，比 base 倒退。
  - **(b) 再加上 github.com 的固定 SSH 形式。**
    - 優點：常見的 GitHub SSH 使用者可以用。
    - 缺點：GitHub Enterprise、GitLab 和其他寫法仍然全部停下；形式越加越多，還是可能漏。
  - **(c) 遇到其他形式時停下，由你在派掃描的 session 親自回答是否放行，像簽章一樣記下你的回答。**
    - 優點：任何主機都能用；少見的形式由你判斷。
    - 缺點：仍要維護一份「自動通過」的形式清單；每次少見形式的 push 都要問你。
  - **(d) 刪掉 PR-3 新加的網址形式檢查，回到 base：push URL 和 fetch URL 相同就通過；不同時停下，照 (c) 由你親自回答。**（建議）
    - 優點：不解析網址，任何主機、任何寫法都一樣處理，不會擋到別人；以刪減修正，比補更多形式簡單；符合 Core `:97`（讀的是實際 URL 和 rewrite）。
    - 缺點：不檢查這個 clone 是不是任務要的 repo；clone 錯 repo 的情況要靠其他步驟（例如 PR 的目的地 `--repo`）發現。
- 我的建議：(d)。理由：Core 要求的是核對實際送出的 URL 和 rewrite，(d) 做到了，而且不會因為網址寫法不同而擋人。

## I106-C9：PR 和 Issue 的其他 metadata 要不要掃描？

- 問題：貼 PR、Issue 或留言時，除了標題、內文和留言，還要不要掃描 label、milestone、assignee，以及 push 送出的分支和 tag 名稱？
- 為什麼要你決定：Issue #106 Scope 3 把「other PR and Issue metadata」列為要關閉或附理由記錄的候選；審查發現 P3D-03 (a)。
- 事實：
  - Core v0.5.0 `review-and-security.md:97`：「PR／Issue 等非 Git payload 須另查該次實際擬發內容與支援的必要 metadata」。
  - 目前 R-REV-9 只掃標題、內文、留言和 review 紀錄；push 步驟 4 只檢查 ref 名稱的字元，不看名稱裡有沒有私人資料（`skills/dev-core/references/push-scan.md`）。
- 選項：
  - **(a) 加一句：貼文設定的 label、milestone、assignee，以及 push 送出的 ref 名稱，也列入文字掃描。**（建議）
    - 優點：只加一句，對應 Core `:97` 的「必要 metadata」。
    - 缺點：每次掃描多看幾個欄位。
  - **(b) 維持現狀，寫明理由。**
    - 理由可以是：這些欄位很少用；分支名稱 push 後本來就公開。
    - 缺點：分支名稱裡如果有私人資料（例如人名），不會被掃到。
