# Changelog

## v0.3.0 - 2026-07-12

- 發布 `OneDir` 版本執行檔，啟動速度由約 11 秒大幅提升至約 1.2 秒。
- 修正 Windows console 下 `--noconsole` 模式可能導致 `AttributeError` 的 stdout/stderr 編碼與 NoneType 處理問題。
- 新增 `measure_windows_startup.ps1` 用於測量執行檔啟動速度。
- 升級打包腳本 `build_windows.ps1` 支援多種 Layout 模式並加入 Clean 選項。
- 新增 GitHub Release notes：`docs/release_notes_v0.3.0.md`。

## v0.2.0 - 2026-07-07

- 新增 Windows 雙 exe 打包流程：`PDF-Combine-GUI.exe` 與 `PDF-Combine-CLI.exe`。
- 新增 `scripts/build_windows.ps1`，標準化 PyInstaller onefile 打包命令。
- 更新 README，說明 GUI exe 與 CLI exe 的用途差異。
- 更新 canonical CLI spec，將 `PDF-Combine-CLI.exe` 記錄為正式 CLI 入口。
- 新增 GitHub Release notes 草稿：`docs/release_notes_v0.2.0.md`。
