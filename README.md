# PDF-Combine

一個簡單易用的 Python 工具，可將多張圖片合併成 PDF，也可將 PDF 頁面轉成 PNG 圖檔。支援圖形化介面 (GUI) 與命令列介面 (CLI)。

## 功能特色

- **圖片合併 PDF**：支援 `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tif`, `.tiff` 等常見圖片格式。
- **PDF 轉 PNG**：可將 PDF 指定頁面輸出為 PNG 圖檔。
- **頁碼範圍**：PDF 轉 PNG 支援全部頁面，或指定 `1-3,5` 這類頁碼範圍。
- **解析度設定**：PDF 轉 PNG 可設定 DPI，預設為 200。
- **雙模式選取**：
  - **GUI 模式**：啟動後選擇「圖片合併成 PDF」或「PDF 轉成 PNG 圖檔」。
  - **CLI 模式**：提供 `images-to-pdf` 與 `pdf-to-png` 子命令，錯誤輸出到 stderr，適合批次與 headless 環境。
- **自動排序**：圖片合併 PDF 時依檔案名稱排序。
- **路徑防錯**：自動建立不存在的輸出資料夾。
- **編碼優化**：針對 Windows 環境優化 UTF-8 輸出，避免中文字元亂碼。

## 開發環境與相依套件

- **Python 版本**：建議 Python 3.9+
- **主要套件**：
  - `Pillow` (PIL)：圖片處理與 PDF 合併。
  - `PyMuPDF`：PDF 頁面渲染與 PNG 輸出。
  - `tkinter`：提供資料夾選取對話框。

### 安裝相依套件

使用 `pip` 安裝必要套件：

```bash
pip install -r requirements.txt
```

或手動安裝：

```bash
pip install Pillow PyMuPDF
```

## Windows 執行檔 (.exe)

對於不方便安裝 Python 環境的 Windows 使用者，可以使用 GitHub Release 提供的已封裝執行檔：

- `PDF-Combine-GUI.exe`：給一般使用者雙擊啟動，會開啟圖形化介面，不顯示 console 視窗。
- `PDF-Combine-CLI.exe`：給命令列、批次檔或排程使用，支援 `images-to-pdf` 與 `pdf-to-png` 子命令，輸出 stdout/stderr 與 exit code。

開發者可用下列指令在 Windows 重新打包兩個 exe：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build_windows.ps1
```

打包需要先安裝 PyInstaller：

```bash
pip install pyinstaller
```

## 使用方法

### GUI 模式

1. **執行腳本**：
   ```bash
   python PDF-Combine.py
   ```
2. **選擇功能**：
   - 選「是」：圖片合併成 PDF。
   - 選「否」：PDF 轉成 PNG 圖檔。
3. **依提示選取來源與輸出位置**。
4. **完成**：程式會顯示輸出檔案或輸出資料夾。

若使用 Windows 發布版，雙擊 `PDF-Combine-GUI.exe` 即可進入相同流程。

### CLI 模式

圖片合併成 PDF：

```bash
python PDF-Combine.py images-to-pdf --input-folder ./images --output ./combined_images.pdf
```

Windows console exe 也支援相同參數：

```bash
PDF-Combine-CLI.exe images-to-pdf --input-folder ./images --output ./combined_images.pdf
```

PDF 全部頁面轉 PNG：

```bash
python PDF-Combine.py pdf-to-png --input ./sample.pdf --output-folder ./output_png --dpi 200
```

PDF 指定頁面轉 PNG：

```bash
python PDF-Combine.py pdf-to-png --input ./sample.pdf --output-folder ./output_png --dpi 300 --pages 1-3,5
```

輸出檔名格式為：

```text
sample_page_001.png
sample_page_002.png
```

CLI 模式成功訊息會輸出到 stdout；錯誤與警告會輸出到 stderr，並以非零狀態結束，不會彈出 tkinter messagebox。

## 專案結構

- `PDF-Combine.py`：主程式腳本。
- `scripts/build_windows.ps1`：Windows 雙 exe 打包腳本。
- `requirements.txt`：Python 相依套件。
- `README.md`：專案說明文件。
- `docs/cli_spec.md`：穩定 CLI 合約。
- `docs/release_notes_v0.2.0.md`：v0.2.0 GitHub Release notes 草稿。
- `.gitignore`：排除不需要上傳至版本控制的檔案。
- `REMINDER.txt`、`ConversationRecord.txt`、`ConversationRecord.md`：歷史開發紀錄；目前進度請以 Obsidian 專案駕駛艙為準。

## 授權

此專案僅供學習與個人開發使用。
