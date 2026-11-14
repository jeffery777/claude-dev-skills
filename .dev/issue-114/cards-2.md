# Issue #114 決策卡片（實作審查後，第 2 組）

英文部分依 ASD-STE100 原則編寫，未完成完整符合性驗證；繁體中文部分採白話寫作，不主張符合 ASD-STE100。

來源：`reviews/impl-u2-round-1.md`（IRU2-D-02、IRU2-S-01、IRU2-D-03）。
回答方式：例如「C7 a」。卡片本身不授權任何動作，只有使用者的回答算數。

回答（轉述）：「C7 a」（使用者，2026-11-14，由 orchestrator session 轉述）。所以 C7 (a)：從 `check_pack.py` 的 allowlist 刪掉 `version`，加測試，REQ-030 與 REQ-028 跟著改，新節點 U3。

## C7：要不要讓 `check_pack` 在 manifest 出現 `version` 時失敗？

- **問題：** REQ-030 要求兩個 manifest 不設 `version`。要不要加一道機械檢查，讓以後加回 `version` 時 `scripts/validate.sh` 會失敗？
- **為什麼要你決定：** 這是需求缺口（`REQ-GAP`）。REQ-030 只寫了「不設 `version`」，沒有寫要不要用檢查來擋。只有你能新增需求。
- **事實：**
  - `scripts/check_pack.py:145`、`:147`（`MANIFEST_KEYS`）在 `plugin.json` 和 marketplace 的 plugin entry 都還允許 `version`。目前沒有任何檢查會因為 `version` 而失敗（兩位 U2 reviewer）。
  - `claude plugin validate` 在沒有 `version` 時會提示：「No version specified. Consider adding a version following semver」，exit 0（本 session 用 2.1.312 親自確認；U2 deep reviewer 用 2.1.310、2.1.311 也看到同樣的提示）。
  - 卡片 C2 (a) 保留 `dev-retro` 的「merge 到 `main` 就算 released」，前提是 manifest 沒有 `version`（REQ-026 Notes）。
  - REQ-028、`check_pack.py` 的註解、CB-7 和 DL-037 把 manifest 的 allowlist 描述成「the keys in use」（使用中的 key）；REQ-028 的清單裡還有 `version`（IRU2-D-03）。
- **推論：** 以後如果有人照 validator 的提示把 `version` 加回去，已安裝的副本又會停在那個字串上；`dev-retro` 的安全教訓發布規則會悄悄失效，沒有任何檢查會失敗。
- **選項：**
  - **(a) 從 allowlist 刪掉 `version`（建議）**
    - 做法：刪除 `check_pack.py` 兩組 `MANIFEST_KEYS` 裡的 `"version"`；在 `tests/test_core_checks.py` 的 `test_manifest_key_outside_the_allowlist_fails` 加兩個 `version` 案例；REQ-030 驗收加一條「`check_pack` 在 manifest 出現 `version` 時失敗」；REQ-028 的 key 清單拿掉 `version`；CHANGELOG 條目補一句；`log.md` 各加一列。先更新 Issue #114 的範圍（貼文前掃描）。
    - 結果：加回 `version` 時，本機 `validate.sh` 和 CI 都會失敗。「keys in use」的描述也重新成立。
    - 風險：低。以後真的要改回版本號，就要先改 REQ-030 和這個 allowlist（這是刻意的）。
    - 成本：一個新的寫入節點 U3（strict，deep review 加 Security Diff Scan），大約多一輪審查。
  - **(b) 不加檢查，只寫下理由**
    - 做法：REQ-030 Notes 加一句：`check_pack` 仍允許 `version`，validator 會提示加回，加回前要先改 REQ-030；REQ-028 加一句「`version` 允許但目前未使用」。
    - 結果：只靠文字和審查來防。
    - 風險：中。照 validator 提示加回 `version` 時，不會有檢查失敗。
    - 成本：兩個需求檔各一句，仍要一次窄確認。
  - **(c) 延後，開一個 follow-up**
    - 做法：新增 FU 列，觸發條件是「有變更加回 `version`，或你要求」。
    - 風險：和 (b) 相同，在處理之前沒有防護。
    - 成本：最小。
- **建議：** (a)。理由：只刪不加；成本是一輪審查；它擋住一條會讓安全規則前提悄悄失效的路徑，而且 validator 本身就在提示加回 `version`。
- **如果你不決定：** U2 停在審查完成、等待決定的狀態，不能 commit。U1 已審查完成。
- **證據：**
  - 事實：上面的行號；`claude plugin validate` 的輸出（本 session 親自執行）；`reviews/impl-u2-round-1.md`。
  - 推論：加回 `version` 之後的失效情境。
  - 未驗證：CI 釘的 Claude Code 2.1.304 對沒有 `version` 的 manifest 是否也只給警告（PR 的 CI run 會顯示）。

## 給你參考，不需要決定

- U2 deep reviewer 提醒：拿掉 `version` 之後，每個 merge 到 `main` 的變更，所有沒有釘選的 Claude Code 安裝在下次更新時都會拿到，中間沒有 release 關卡。卡片 C1 (c) 接受的「沒有穩定版通道」就是指這件事。
- 官方文件（`loading.md`）說，更新後舊版本的 cache 資料夾會在 14 天後刪除。orchestrator 的 brief 如果用 `cache/.../0.1.0/` 路徑指定 pack 檔案，更新後會找不到（推論）。
