# Issue #106 卡片（PR-3 第 2 輪確認之後）

請在本 session 直接打字回答，例如「C11 a」。

回答（使用者在本 session 的訊息，2026-11-10，為 PR-3 這次變更）：「C11 a」。這題會改 C8 (d) 的後半，所以要你本人回答。

## I106-C11：push URL 和 fetch URL 不同時，可以由你放行嗎？

- 問題：C8 (d) 讓你在 push URL 和 fetch URL 不同時親自放行。第 2 輪確認發現這樣會漏掃描。要怎麼處理？
- 為什麼要你決定：這會改掉你在 C8 (d) 選的「不同時由你親自回答」。
- 事實：
  - push 步驟 6 用 `git ls-remote` 列出遠端已有的 commit，步驟 8 把它們排除在掃描外（`skills/dev-core/references/push-scan.md`）。`ls-remote` 讀的是 fetch 那一邊（git-ls-remote(1)；推論，這次未實測）。
  - 如果 push 送到另一個地方，fetch 那邊有、push 目的地沒有的 commit 會沒被掃描就公開。pack 先前就記錄並重現過這個問題（`.dev/followups.md` FU-015 第 (1) 項），當初是用步驟 2「push 和 fetch 必須相同」修掉的。
  - 一個 remote 有好幾個 push URL 時，步驟 2 也會停下，而 push 會送到每一個 URL（git-push(1)）。
- 選項：
  - **(a) 刪掉放行：步驟 2 停下後，只能由你改設定，讓 push 和 fetch 一致，再從步驟 1 重來。**（建議）
    - 這就是 base 的做法；C8 (d) 的前半（不檢查網址形式，任何主機都能用）保留。
    - 優點：以刪減修正，不會漏掃描；不必在對話裡顯示 URL（第 2 輪的 P3R2-02、P3R2-03 跟著消失）。
    - 缺點：push 和 fetch 刻意不同的人（例如從內部 mirror 抓、推到公開 repo），要先改 remote 設定。
  - **(b) 保留放行，但放行時掃描完整歷史。** 步驟 6 不排除任何 commit；步驟 7 會因此擋下既有分支的更新，只能推新分支。
    - 缺點：規則變複雜，可用性很低。
  - **(c) 保留放行，改從 push 目的地讀已有的 commit。** 要新增指令，也要處理 rewrite 和多個 URL。
    - 缺點：新機制，要另外設計和審查。
