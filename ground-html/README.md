# 寬達生技 Ground Biotech — 公司 HTML 鏡像

OneDrive 正本的 GitHub 鏡像。**入口頁：`index.html`**（下載或 clone 後直接用瀏覽器開啟）。

- 資料夾結構與 OneDrive 相同（`(A) 客戶資料 Clients/…`、`掃描/(G) 彰化倉庫紀錄文件/…`），方便對照正本。
- 「雲端即時」類面板（A2-1a、A3-3、A4-2、A6-1、B1-1…）開啟後即連 Supabase 讀最新資料；「單檔快照」類（F5、G2-2、A8-3…）資料截至同步日。
- 正本仍在 OneDrive；修改請依 html-maintenance SOP 改正本後再同步到這裡。

## 更新方式

1. 從 OneDrive 複製最新 HTML 到本 repo 的相同相對路徑（可執行 `python _site/sync_from_onedrive.py`，預設讀 `C:\Users\<你>\OneDrive`）。
2. 新增或搬移檔案時，編輯 `_site/catalog.json`。
3. 執行 `python _site/build_index.py` 重新產生 `index.html`（找不到檔案會報錯）。
4. `git add -A && git commit && git push`。

## 未納入

- `彰化廠區_倉儲操作介面.html`（340 MB，超過 GitHub 單檔 100 MB 上限）
- (F) 財務夾的中華電信電子發票 `.htm`（憑證，不是工具）
- `(E) Claude/Backups` 下的改版備份

本 repo 為私有；內含財務儀表板與供應商資料，請勿改為公開或開啟 GitHub Pages。
