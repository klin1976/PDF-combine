# PDF-Combine 🖼️ ➡️ 📄

一個簡單易用的 Python 工具，用於將多張圖片合併成一個 PDF 檔案。支援圖形化介面 (GUI) 與命令列介面 (CLI)。

## 🚀 功能特色

- **多種格式支援**：支援 `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tif`, `.tiff` 等常見圖片格式。
- **雙模式選取**：
  - **GUI 模式**：使用視窗選取來源資料夾與設定輸出路徑。
  - **CLI 模式**：若環境不支援圖形介面，自動切換至命令行輸入。
- **自動排序**：依檔案名稱排序圖片，確保合併順序與資料夾內一致。
- **路徑防錯**：自動建立不存在的輸出資料夾。
- **編碼優化**：針對 Windows 環境優化 UTF-8 輸出，避免中文字元亂碼。

## 🛠️ 開發環境與相依套件

- **Python 版本**：建議 Python 3.6+
- **主要套件**：
  - `Pillow` (PIL)：圖片處理與 PDF 合併。
  - `tkinter`：提供資料夾選取對話框。

### 安裝相依套件

使用 `pip` 安裝必要套件：

```bash
pip install Pillow
```

## 📦 Windows 執行檔 (.exe)

對於不方便安裝 Python 環境的 Windows 使用者，可以使用已封裝好的 `PDF-Combine.exe`：

1. **取得檔案**：從 `dist/` 目錄中找到 `PDF-Combine.exe`。
2. **直接執行**：雙擊即可啟動，功能與腳本完全一致。

## 📖 使用方法

1. **執行腳本**：
   ```bash
   python PDF-Combine.py
   ```
2. **選取來源**：彈出視窗後，選取存放圖片的資料夾。
3. **儲存 PDF**：設定輸出的 PDF 檔名（預設為 `combined_images.pdf`）與儲存位置。
4. **完成**：腳本會自動合併圖片並輸出 PDF。

## 📂 專案結構

- `PDF-Combine.py`：主程式腳本。
- `README.md`：專案說明文件。
- `.gitignore`：排除不需要上傳至版本控制的檔案。
- `REMINDER.txt` & `ConversationRecord.txt`：開發維護紀錄。

## 📝 授權

此專案僅供學習與個人開發使用。
