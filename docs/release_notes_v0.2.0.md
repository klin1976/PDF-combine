# PDF-combine v0.2.0 - Windows GUI and CLI executables

本版重點是提供兩種 Windows 執行檔，讓一般雙擊使用與命令列批次使用各自有清楚入口。

## 下載選擇

- `PDF-Combine-GUI.exe`：適合一般使用者雙擊啟動，使用 tkinter 圖形化介面，不顯示 console 視窗。
- `PDF-Combine-CLI.exe`：適合命令列、批次檔與排程工作，支援 stdout、stderr 與 exit code。

## CLI 範例

圖片合併成 PDF：

```bash
PDF-Combine-CLI.exe images-to-pdf --input-folder .\images --output .\combined_images.pdf
```

PDF 轉 PNG：

```bash
PDF-Combine-CLI.exe pdf-to-png --input .\sample.pdf --output-folder .\output_png --dpi 200
```

指定頁碼：

```bash
PDF-Combine-CLI.exe pdf-to-png --input .\sample.pdf --output-folder .\output_png --dpi 300 --pages 1-3,5
```

## 已驗證項目

- Python 腳本可通過語法編譯與相依套件 import 檢查。
- `images-to-pdf` 可將範例圖片輸出為 PDF。
- `pdf-to-png` 可將 PDF 輸出為 PNG。
- CLI 錯誤案例會回傳非零狀態碼，錯誤訊息輸出到 stderr。
- `PDF-Combine-CLI.exe` 維持與 Python CLI 相同的命令列行為。
- `PDF-Combine-GUI.exe` 可無參數啟動 GUI，不顯示 console 視窗。

## Known Issue

- PyInstaller `--onefile` exe 第一次啟動可能需要較久時間，尤其在雲端同步資料夾或防毒掃描較積極的環境。此版保留 onefile 交付，不新增 onedir 版。
