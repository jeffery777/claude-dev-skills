# FU-005 不退化檢核表與 audit 缺口處理表（草稿 v3，2026-10-22）

配合 `fu005-spec.md` v3。base `main` 91f4e8c，另核對 `main` 0fc4e5f（FU-013，PR #21）。v2 依審查第 1 輪修正；v3 依第 2 輪（R2-004、卡片 8a）與 FU-013 修正：保留 30 項、索引行 16 條。
標記：**[事實]** 有出處；**[推論]** 本 session 的判斷；**[未驗證]** 還沒檢查。
「保留」= 在原檔原處逐字不改。「索引行」= 內文刪除，只留 ID、標題、`[core: anchor]`（spec 1.1 (D)）。
縮寫：wf = `workflow.md`，auth = `authorization-and-stops.md`，rev = `review-and-security.md`，exh = `exact-head-and-evidence.md`（行號依 pin 的 v0.1.1）。
寫作：依 ASD-STE100 原則編寫，未完成完整符合性驗證。

## 表 A：DL-001 到 DL-017

| DL | 規則 | 類型 | 新位置 | 是否變動 |
| --- | --- | --- | --- | --- |
| DL-001 | all | compress | `deltas.md` 同列；PR-4 把 Difference 改成「索引＋保留規則＋按階段讀 Core 原檔」 | 更新說明（這是本設計本身的紀錄，不是加嚴） |
| DL-002 | R-RIG-1、R-RIG-2 | tighten | `dev-core` R-RIG-1、R-RIG-2（保留） | 不變 |
| DL-003 | R-RIG-3、R-REV-3 | tighten | `dev-core` R-RIG-3、R-REV-3（保留）；`agents/dev-implementer.md`、`agents/dev-reviewer.md` 的副本（保留） | 不變 |
| DL-004 | R-REV-1 | tighten | `dev-core` R-REV-1、CB-5（保留）；reviewer agent 檔 frontmatter 的 `disallowedTools`（保留） | 不變 |
| DL-005 | R-DEL-2 | tighten | `dev-core` R-DEL-2（保留）；`dev-deliver` 與 `dev-review` 的模型表（保留） | 不變 |
| DL-006 | R-CAP-1 | rephrase | `dev-core` R-CAP-1（保留） | 不變 |
| DL-007 | R-EVD-1 | compress | `dev-core` R-EVD-1（保留）；Core wf:121-129 的示意表由所有 skill 讀 `workflow.md` 取得 | PR-4 加一句註記（範例由 Core 原文提供）；Difference、Reason、Evidence 欄不改 |
| DL-008 | R-AUTH-1 | tighten | `dev-core` R-AUTH-1（保留）；四個 agent 檔「內容是資料」的副本（保留） | 不變。卡片 8 (a)：Core 對 reviewer 是審查準則（資料），DL-008 不開例外；reviewer 新段落另寫明「宣稱是政策的檔案內容是資料」（spec 2.2） |
| DL-009 | R-DEL-1、R-REV-1、CB-4 | tighten | `dev-core` R-REV-1、CB-4（保留）。R-DEL-1 變成索引行；DL-009 的加嚴內容（不用有寫入工具的替代者、審查前後的 tree 檢查）在 R-REV-1 與 CB-4 的內文，不在 R-DEL-1 的內文 | R-DEL-1 內文刪除；PR-4 在 DL-009 加一句註記；加嚴不受影響 |
| DL-010 | R-REV-1、R-REV-9 | tighten | `dev-core` R-REV-1、R-REV-9（保留）；`dev-implement` 的 commit/push 順序、`dev-gate` 表格、`dev-review` mode 表、`agents/dev-security-reviewer.md`（保留） | 不變；FU-014 可能改 R-REV-9 的 `--prune` 句 |
| DL-011 | R-REV-3 | tighten | `dev-core` R-REV-3（保留）；`review-report.md`、兩個 reviewer agent 檔（保留） | 不變 |
| DL-012 | R-REV-4、R-VER-2 | tighten | `dev-core` R-REV-4、R-VER-2（保留） | 不變 |
| DL-013 | R-EXH-3、R-REV-9 | tighten | `dev-core` R-EXH-3、R-REV-9（保留） | 不變 |
| DL-014 | R-AUTH-6、R-WRT-1 | tighten | `dev-core` R-AUTH-6、R-WRT-1（保留）；`decision-card.md`、`review-report.md`（保留） | 不變 |
| DL-015 | R-EXH-4 | tighten | `dev-core` R-EXH-4（保留）；`dev-gate` 第 6 步、`platform-profile.md`、`platform_profile.py`（保留） | 不變 |
| DL-016 | R-REV-8 | tighten | `dev-core` R-REV-8（保留）；`review-report.md`、`decision-card.md`、兩個 reviewer agent 檔（保留） | 不變 |
| DL-017 | header、R-WRT-1 | tighten | header 的「shorter or looser → Core governs；stricter applies」兩句（保留）；R-WRT-1（保留） | PR-2 加兩句、PR-4 改第一句說法（spec 1.1 (A)）；原有兩句不變；DL-017 列不改 |

## 表 B：CB-1 到 CB-5

| CB | 內容 | 新位置 | 是否變動 |
| --- | --- | --- | --- |
| CB-1 | 狀態檔位置、`commit_state`、PR 後不 commit 紀錄 | `dev-core` CB-1（保留）。[事實] `tests/test_core_checks.py:216-217` 斷言其原文 | 不變（卡片 6b 若採用 (a)，加一行出處 D-010、REQ-015） |
| CB-2 | 需求位置 | `dev-core` CB-2（保留） | 不變（出處 D-003） |
| CB-3 | GitNexus advisory | `dev-core` CB-3（保留）；`agents/dev-explorer.md` 副本（保留） | 不變（出處 D-006） |
| CB-4 | agent 名稱、替代規則、審查前後的 tree 檢查 | `dev-core` CB-4（保留）。[事實] `tests/test_core_checks.py:203-214` 斷言其原文 | 不變（出處 DL-009） |
| CB-5 | reviewer 保留 Bash，唯讀靠指示 | `dev-core` CB-5（保留） | 不變（出處 DL-004） |

## 表 C：比 Core 嚴格（含字面上）但沒有 DL 列，或 DL 列沒有完整涵蓋

「新 DL 列」= PR-1 為該項新增 DL 列，只記錄，不改規則原文。其他項已在 skill、agent 或 script 中，位置不變。

| ID | 規則與內容 | Core 原文 | 新位置 |
| --- | --- | --- | --- |
| C-1 | R-AUTH-7：搬移、歸檔、**清理前都要 dry-run** | auth:50 只對清理要求 dry-run，搬移與歸檔要求「必要 preview」 | `dev-core` R-AUTH-7（保留）；新 DL 列；上游回饋（spec 第 8 節第 5 點）。[事實] Issue #18 round 3 R3-009 曾經誤刪，已還原 |
| C-2 | R-AUTH-7：不得 commit secrets、真實 logs、機器或使用者識別、私有路徑、runtime state、databases、caches，適用於**使用本 pack 的每個專案** | auth:52 寫「共用庫不收…」 | `dev-core` R-AUTH-7（保留）；新 DL 列，並註明與 CB-1（D-010）的關係與 CF-009 第 1 點 |
| C-3 | R-EXH-5：不在 runtime 抓 Core `main`；vendor 變更後跑 `scripts/verify_core.py` | exh:56 runtime 只用已組裝的固定文件；`verify_core.py` 是本專案的程序 | `dev-core` R-EXH-5（保留）；新 DL 列（type 由 PR-1 reviewer 判定） |
| C-4 | R-EXH-4：未選 profile 時，要讀回 change request 在 bound base 與 reviewed head 的 checks 才是 `NOT_CONFIGURED`；讀回失敗或不符是 `UNVERIFIED` | exh:44：「專案未選 profile 時 NOT_CONFIGURED 有效」 | `dev-core` R-EXH-4（保留）；`dev-gate` 第 6 步（保留）；新 DL 列引用 D-017、REQ-020、REQ-021（Q5、Q6）。[事實] DL-015 只寫已選 profile 的情形 |
| C-5 | R-STG-2：Discover 要讀「CLAUDE.md, AGENTS.md」兩者（審查 R1-001） | wf:13「讀有效指引」 | `dev-core` R-STG-2（保留，v1 誤列為索引行）；新 DL 列。[事實] `dev-plan/SKILL.md:17` 寫的是「CLAUDE.md or AGENTS.md」；`dev-implement` 第 1 步只寫「project instructions (R-STG-2)」 |
| C-6 | R-REV-2：finding 要有 file and line | rev:13「檔案／位置」 | `dev-core` R-REV-2（保留）；新 DL 列；`dev-review/SKILL.md:57` 與 agent 檔的 `path:line`（保留） |
| C-7 | R-EVD-1：無條件保留未解、安全與資料遺失事件紀錄，以及共享或仍被引用的證據 | wf:115「依專案有效要求及保護例外適當保留」 | `dev-core` R-EVD-1（保留）；新 DL 列；上游回饋（spec 第 8 節第 6 點） |
| C-8 | R-EVD-2：「Load indexes and summaries first」是命令句 | wf:117「可先載入索引」 | `dev-core` R-EVD-2（保留）；新 DL 列（type 由 PR-1 reviewer 判定；[推論] 屬效率規則，保守起見保留） |
| C-9 | R-DEL-2：receipt 記錄 requested settings，讀不回的是 `unknown` | wf:56 由接口核對實際生效設定 | `dev-core` R-DEL-2（保留）；`task-brief.md` receipt 範本（保留）；DL-005 是否涵蓋由 PR-1 reviewer 判定 |
| C-10 | `dev-reviewer`：never modify the tree；`dev-security-reviewer`：不跑 `git fetch` 或 `git push`、不安裝工具、不外傳資料 | rev:9（唯讀只講受審內容；CF-009 第 2 點）、rev:55 | agent 檔（保留）；FU-013 已加入 reviewer 不寫任何檔案（C-24） |
| C-11 | `dev-implementer`：不 delete owned paths 以外的東西 | auth:21-23 | agent 檔（保留）；FU-013 的補充見 C-23 |
| C-12 | `dev-deliver`：Phase 1 一次只有一個 writer | wf:60 允許 ownership 不重疊的多 writer | `dev-deliver` Loop 前言（保留） |
| C-13 | `dev-plan`：建立需求資料夾前先問使用者；不自行擴大需求；`REQ-GAP` 只有使用者決定後才成為需求 | Core 沒有需求 wiki | `dev-plan` 第 2 步（保留）；DL-011 涵蓋 `REQ-GAP` |
| C-14 | `dev-continue`：D-012 只涵蓋 checkpoint commit；PR-C1 card 1 只涵蓋該 PR comment；使用者確認後 handoff 才完成 | wf:20、auth:13 | `dev-continue`（保留） |
| C-15 | `dev-gate`：profile 只在 bound base 讀；checker 從 bound base 取；設定變更給決策卡片 | exh:46 | `dev-gate`、`platform-profile.md`、`platform_profile.py`（保留） |
| C-16 | `graph.py transition --evidence-file`：只接受專案內的一般檔案，只記路徑與 SHA-256 | auth:52 | `skills/dev-plan/scripts/graph.py`（保留）；D-015、FU-003 |
| C-17 | `dev-review` mode 表：commit/push scan 用 opus/high 以上；security 用 opus/xhigh 或 max | wf:56 | `dev-review`（保留）；DL-005 |
| C-18 | R-WRT-1 註記字面「…，未完成完整符合性驗證」 | wf:35「…，尚未完成…」 | `dev-core` R-WRT-1（保留）；DL-017；CF-009 第 3 點 |
| C-20 | R-REV-6：「including uncommitted changes」（R2-004） | rev:39「含適用未提交修改」 | `dev-core` R-REV-6（保留，v2 誤列為索引行）；新 DL 列；副本 `review-report.md:6`、`dev-gate` 第 1 步（保留）；上游回饋（spec 第 8 節第 6 點） |
| C-21 | R-EXH-2：「Run the repository's deterministic checks」（R2-004） | exh:22「專案提供且適用的 … offline checks」 | `dev-core` R-EXH-2（保留，v2 誤列為索引行）；新 DL 列；`dev-gate` 第 3 步（保留） |
| C-22 | R-REV-7：「executables」不帶限定詞（R2-004） | rev:47「具有安全影響的 executable」 | `dev-core` R-REV-7（保留，v2 誤列為索引行）；新 DL 列；`agents/dev-security-reviewer.md` 的邊界清單（保留） |
| C-23 | `dev-implementer` 與 `task-brief.md` Authority：永不刪除未追蹤或被忽略的檔案，即使在 owned paths 內；回報給主代理，由主代理問使用者（FU-013，REQ-024） | auth:23 要求不可逆刪除在操作當下取得明確確認；Core 沒有「subagent 永不刪」 | agent 檔與 `task-brief.md`（保留，`main` 0fc4e5f）。[推論] `dev-core` R-AUTH-3 比這些副本短（FU-013 merge 紀錄）；R-AUTH-3 成為索引行後，主 session 有 auth:23 原文，副本保持較嚴 |
| C-24 | 兩個 reviewer：任何地方都不寫檔（含 session scratchpad），只有 brief 指定的測試自己建立並刪除的系統暫存檔例外；Python 測試設 `PYTHONDONTWRITEBYTECODE=1` 與 `-p no:cacheprovider`（FU-013 card 3d） | rev:9 唯讀只講受審內容（CF-009 第 2 點） | 兩個 reviewer agent 檔（保留，`main` 0fc4e5f）。SR21B-001：security reviewer 的 Bash 允許清單沒有列 tests，與本段不一致；PR-3 的輸入 |
| C-19（卡片 5a、5b，已決定 (a)） | R-AUTH-5 與 R-VER-3 的專案讀法（spec 1.1 (D) 的英文文字） | auth:35、wf:76 | PR-1：R-AUTH-5、R-VER-3 的索引行各一句 Project reading，各一個新 DL 列 |

## 表 D：改成索引行的 16 條規則：逐句判定

判定方法 [推論]：逐句看 main 上的內文，找出每句在 Core 的對應位置；只要有一句沒有 Core 對應，而且比 Core 嚴格（含字面上），該規則就改列「保留」（v2 因此把 R-STG-2、R-REV-2、R-EVD-1、R-EVD-2 移到表 C；v3 依 R2-004 再移 R-REV-6、R-EXH-2、R-REV-7）。PR-4 的 reviewer 要再獨立做一次。

| 規則 | Core 來源 | 內文各句與 Core 的對應 | 比 Core 嚴格的句子 |
| --- | --- | --- | --- |
| R-STG-1 | wf:9、wf:11-20 | (1) 階段列表 = wf:11-20 表格；(2) 小工作可合併階段、重用證據 = wf:9；(3) 不能省略適用義務 = wf:9 | 無 |
| R-STG-3 | wf:14 | (1) 最小切片、唯一 writer 或不重疊 ownership、依賴、驗收、審查強度與時機 = wf:14；(2) 計畫不授權 = wf:14（Core 更具體：不授權修改、派工或外寫） | 無 |
| R-STG-4 | wf:15-16 | (1) 已授權能力、既有模式、保留無關修改 = wf:15；(2) 持續快速測試與廉價安全檢查 = wf:16；(3) 主代理獨立讀回 diff、受保護 tests、需求 = wf:16；(4) tests 不代替 review 或必要 scan = wf:16 | 無 |
| R-STG-5 | wf:20-22 | (1) 中斷前保存有界 checkpoint = wf:20；(2) 優先原 session、重查來源與 ownership = wf:20、22；(3) 結果不明先確認 = wf:20、22；(4) session 記憶 advisory = wf:20 | 無 |
| R-RIG-4 | wf:82-99 | 觸發條件 = wf:82；前提與反證 = wf:84；方案比較與紀錄 = wf:86；四種判讀 = wf:90-97；研究界限 = wf:99；管理措施與人工處理 = wf:88；各項限制 = wf:86、88、99 | 無（audit：weaker） |
| R-AUTH-2 | auth:11-15 | 委託範圍 = auth:11；逐項查外寫 = auth:13；不重問 = auth:13（較寬：Core 有「已授權且前置通過」）；局部選擇、等決策 = auth:13；他 repo 規則不默套 = auth:15 | 無（audit：looser） |
| R-AUTH-3 | auth:21-23 | 破壞性前置六項 = auth:21；不可逆刪除當下確認 = auth:23；先前概括同意不算 = auth:23 | 無。「a preview or dry run」對應 Core「可用且查核的 preview/diff/plan」；dry run 是 preview 的一種，不是加嚴 |
| R-AUTH-4 | auth:25 | 保留嘗試紀錄並讀回 = auth:25；不盲目重試、刪除、abort = auth:25；拒絕不是成功、不是繞道理由 = auth:25 | 無（較寬：沒寫 Core 允許的「合規替代」，也沒寫「先分類」） |
| R-AUTH-5 | auth:31-38 | 停止條件四項 = auth:33-36；風險名稱不是理由、唯讀研究可繼續、階段結束不是理由 = auth:38；修正後續行 = auth:38 | 無（現有 “and no safe fallback” 是較寬的讀法；卡片 5a） |
| R-REV-5 | rev:25-27 | 阻擋項 = rev:25；三種結果 = rev:25；不授權外寫 = rev:27 | 無（audit：缺結果內容） |
| R-EXH-1 | exh:9-16 | Merge Review 綁定項目 = exh:11-14；pre-commit verdict 只是輸入 = exh:9 | 無 |
| R-CAP-2 | wf:50 | 並行條件 = wf:50；相依、approval、mutation、wait 保持順序 = wf:50；逐項檢查、限制輸出 = wf:50 | 無（較寬：只寫每項，Core 另有「合計」） |
| R-CAP-3 | wf:48-49 | 重用前核對各項 = wf:48；PASS 不代替證據 = wf:48；文句縮短不證明改善、跨模型比較要配對量測 = wf:49 | 無 |
| R-DEL-1 | wf:60 | brief 欄位 = wf:60；writer 不共用、reviewer 唯讀 = wf:60；回報 blocker 與「one final receipt」 = wf:60「最後 receipt」；不繼承外寫權 = wf:60；主代理責任 = wf:60 | 無。`task-brief.md:18` 與 agent 檔的副本保留（card 7a） |
| R-VER-1 | wf:70 | 驗收依據 = wf:70；保留失敗與負面案例 = wf:70；synthetic fixture 的限度 = wf:70 | 無 |
| R-VER-3 | wf:76 | 中途需求修正 = wf:76；旁支問題簡答再續行 = wf:76 | 無（缺例外；卡片 5b） |

[推論] 刪除後，skill 內引用這些 ID 的地方（例如 `dev-gate` 第 4 步的 R-AUTH-5、R-REV-5）仍然有效：ID 還在，指向的 Core 原文已在同一個 context。

## 表 E：使用者決策 D-013 到 D-018，REQ-011 到 REQ-025

| 決策或需求 | 內容 | 新位置 | 是否變動 |
| --- | --- | --- | --- |
| D-001 | 平常只載入 `dev-core` | 由新的 D 決策取代（spec 1.3）；D-001 原文保留，加註 superseded | 記錄變更（這是本設計本身） |
| D-013 第 1 點 | 嚴重度門檻 | R-REV-3（保留）、`review-report.md`、`agents/dev-reviewer.md` | 不變 |
| D-013 第 2 點 | 修正前分類；管理措施條件 | R-REV-4（保留） | 不變 |
| D-013 第 3 點 | 新機制要對應需求 | R-RIG-3（保留） | 不變 |
| D-013 第 4 點 | 推送前的窄範圍確認；證據重用條件 | R-REV-4、R-EXH-3（保留） | 不變 |
| D-013 第 5 點 | 停止規則（兩種觸發） | R-VER-2（保留） | 不變 |
| D-013 第 6 點 | PR 後紀錄不進 PR branch | R-EXH-3、CB-1（保留） | 不變 |
| D-014 | 決策卡片、ASD-STE100 註記、中文簡明寫作 | R-AUTH-6、R-WRT-1（保留）；`decision-card.md` | 不變 |
| D-015 | 每次 commit 與 push 前掃描；遮罩 | R-REV-9、R-REV-1、R-REV-8（保留）；`dev-implement`、`dev-gate`、agent 檔 | 不變；FU-014 介面 |
| D-016 | `requirement_relation`、`REQ-GAP` | R-REV-3（保留）；`review-report.md`、`dev-plan` 第 2 步 | 不變 |
| D-017 | 最小 CI；未選 profile 的讀回 | `.github/workflows/ci.yml`、`scripts/validate.sh`；R-EXH-4（保留）；表 C 的 C-4 | 不變（C-4 補 DL 列） |
| D-018 | provider profile 讀回 | R-EXH-4（保留）、`dev-gate`、`platform-profile.md`、`platform_profile.py` | 不變 |
| REQ-011 | commit/push 前的安全審查 | 同 D-015 | 不變 |
| REQ-012 | review 收斂 | 同 D-013 | 不變 |
| REQ-013 | 決策卡片 | 同 D-014 | 不變 |
| REQ-014 | finding 與需求的關係 | 同 D-016 | 不變 |
| REQ-015 | 不做 agent memory | R-AUTH-7、CB-1（保留） | 不變 |
| REQ-016 | 部署與量測 | FU-004；卡片 7′ (a)：「使用本 pack」組在 PR-2 前、PR-4 後各跑一次 | 量測計畫延伸（PR-1 更新 FU-004 列） |
| REQ-017 | 自動交接評估 | `dev-continue`（保留） | 不變 |
| REQ-018 | CHANGELOG 記錄上游 Core 版本 | `CHANGELOG.md`；PR-2 與 PR-4 各加一筆（行為改變） | 新增條目 |
| REQ-019 | 回饋 Core | `docs/core-feedback.md`；spec 第 8 節 | 新增候選（使用者授權後） |
| REQ-020 | 最小 CI | CI 跑 `validate.sh`，會抓到對照表的錯誤路徑（`check_pack.py`） | 不變 |
| REQ-021 | profile 設定與讀回 | 同 D-018；[事實] `tests/test_platform_profile.py:389-422` 斷言 R-EXH-4 原文 | 不變 |
| REQ-022 | 規則單一來源、引用 ID | ID 都還有粗體定義；`test_rule_citations.py` 不用改；CB-1 到 CB-5 保留；R-REV-8 遮罩保留。non_goals「waits for FU-004」由卡片 7′ (a) 取代，記在 REQ-025 | 不變。[推論] 對照表不能用「section 數字」寫法 |
| REQ-023 | `dev-core` 不比 Core 弱；header；R-WRT-1 | header 的兩句保留；R-WRT-1 保留；audit 缺口由表 F 解決 | header 加兩句（PR-2）、第一句改說法（PR-4） |
| REQ-024 | agent 的寫入與刪除規則；FU-004 的官方工具組（FU-013） | agent 檔、`task-brief.md`（保留）；表 C 的 C-23、C-24；FU-004 列 | 不變 |
| REQ-025（新） | 按需載入（本設計） | PR-1 新增 | 新增 |

## 表 F：audit Deferred 缺口 → Core 原文 → 由誰讀進 context

對照表（spec 1.2）的事實：**所有 dev-* skill 都讀 `authorization-and-stops.md` 與 `workflow.md`。** 讀 `review-and-security.md` 的有 plan、implement、review、gate、deliver；讀 `exact-head-and-evidence.md` 的有 docs、gate（＋vendor 變更觸發）。

| 缺口（audit 或 finding） | Core 原文 | 執行該規則的讀者 | 是否讀進 context |
| --- | --- | --- | --- |
| R-STG-2（R1-001 部分、R1 S4、R2 S1） | wf:13、wf:46 | 所有 skill | 是（R-STG-2 本身保留） |
| R-STG-4 | wf:15-16 | 所有 skill（implement 為主） | 是 |
| R-STG-5（R1 S2） | wf:20、wf:22 | `dev-continue` | 是 |
| Docs Sync（無規則） | wf:18 | `dev-docs` | 是 |
| R-RIG-2 | rev:33 | `dev-plan`、`dev-deliver`、`dev-implement` | 是 |
| R-RIG-4（R3-003、R1 S3、R3 suspicion wf:82） | wf:82-99 | 所有 skill；reviewer 經 rev:15 | 是 |
| R-AUTH-1（R1 S4） | auth:9、11、15 | 所有 skill；security reviewer（準則） | 是 |
| R-AUTH-2（R3-007、R2 S2、R3 suspicion exh:30） | auth:11-15、exh:30 | 所有 skill（auth）；merge 授權在 `dev-gate`（exh） | 是 |
| R-AUTH-3（R1-001） | auth:21-23 | 所有 skill（implementer 不讀 Core，卡片 8 (a)；FU-013 副本） | 是 |
| R-AUTH-4 | auth:25 | 所有 skill | 是 |
| R-AUTH-5（R1 S1、R3 suspicion vs CB-4） | auth:35 | 所有 skill | 讀進了，但 Core 本身有兩種讀法 → **卡片 5a** |
| R-AUTH-7（R1-001、R2-002） | auth:46-52、wf:119 | 所有 skill | 是 |
| R-REV-1（R3-007） | rev:9 | `dev-review`、reviewer | 是 |
| R-REV-4（R3-005） | rev:15 | `dev-review`、`dev-deliver` | 是 |
| R-REV-5（R1 S5） | rev:25 | `dev-gate` | 是 |
| R-REV-6 | rev:33-39 | `dev-plan`、`dev-deliver`、`dev-review` | 是（R-REV-6 本身保留） |
| R-REV-7（R1-001 rev:47、R3 suspicion rev:45） | rev:45-47 | `dev-review`、`dev-gate`、security reviewer（準則） | 是（R-REV-7 本身保留） |
| R-REV-8（R3-007） | rev:63-69 | `dev-review`、`dev-gate`、兩個 reviewer | 是 |
| R-EXH-1（R3 suspicion exh:9） | exh:9-12 | `dev-gate`；Merge Review 的 reviewer | 是 |
| R-EXH-2 | exh:22-24 | `dev-docs`、`dev-gate`；Merge Review 的 reviewer（準則） | 是（R-EXH-2 本身保留） |
| R-EXH-4（R3-001） | exh:48 | `dev-gate` | 是 |
| R-EXH-5（R1-002、R2 S6） | exh:56-60（含 exh:58） | 觸發列：修改 `vendor/` 或 Core pin | 是（依觸發列；R-EXH-5 本身保留） |
| R-CAP-1（R3-002） | wf:45-47 | 所有 skill | 是 |
| R-CAP-2（R3-007） | wf:50 | 所有 skill | 是 |
| R-CAP-3（R2-003） | wf:48 | 所有 skill | 是 |
| R-DEL-1、R-DEL-2 | wf:56、60、62 | 所有 skill（deliver 為主） | 是 |
| R-VER-1（R2 S5） | wf:70、rev:71 | wf：所有 skill；rev:71：plan、implement、review、gate、deliver | 是。[推論] `dev-docs`、`dev-continue` 不讀 rev:71；它們不做完成判定 |
| R-VER-2 | wf:72 | 所有 skill | 是 |
| R-VER-3（R3-004、R2-001、R1 S6） | wf:76 | 所有 skill | 讀進了，但讀法有爭議 → **卡片 5b** |
| 改善驗收（無規則） | wf:74 | 所有 skill | 是 |
| R-EVD-1（R2-002、R1 S6） | wf:107-115 | 所有 skill | 是（R-EVD-1 本身保留） |
| R-EVD-2（R3-008） | wf:105、117-119 | 所有 skill | 是（R-EVD-2 本身保留） |
| wf:49 必要 artifacts 仍須產出（R2 S3） | wf:49 | 所有 skill | 是 |
| implementer 可能刪除未追蹤檔案（R2 S4） | auth:23 | implementer | FU-013 已加入（`main` 0fc4e5f，表 C 的 C-23）；implementer 不讀 Core（卡片 8 (a)） |
| R3-006 `--prune` | auth:21 | — | **FU-014**，不在本設計 |
| CB-1 runtime state（R3 suspicion） | auth:52 | — | CB-1 保留（D-010）；CF-009 第 1 點上游回饋 |

（本表的 R1-001、R1-002、R2-*、R3-* 指 Issue #18 audit 的 findings，不是本規格審查的 findings。）

[未驗證] 表 F 假設「讀進 context 的 Core 原文會被遵循」。這個假設沒有量測；FU-004 的前後比較是唯一的檢驗方式。
