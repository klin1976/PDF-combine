# PDF-combine CLI Spec

> 本文件是 PDF-combine 的 canonical CLI contract。README 負責使用者導向說明；本文件負責記錄可被腳本、文件與代理穩定依賴的命令列介面。

## 適用範圍

PDF-combine 目前提供兩個 CLI 子命令：

- `images-to-pdf`：將圖片資料夾合併成單一 PDF。
- `pdf-to-png`：將 PDF 頁面輸出為 PNG 圖檔。

若未提供子命令，程式會啟動 tkinter GUI 模式。

## 執行方式

```bash
python PDF-Combine.py <command> [options]
```

## images-to-pdf

### 語法

```bash
python PDF-Combine.py images-to-pdf --input-folder <folder> --output <pdf-file>
```

### 參數

| 參數 | 必填 | 說明 |
|---|---|---|
| `--input-folder` | 是 | 來源圖片資料夾。 |
| `--output` | 是 | 輸出的 PDF 檔案路徑。 |

### 支援圖片格式

依副檔名判斷，支援：

- `.png`
- `.jpg`
- `.jpeg`
- `.bmp`
- `.tif`
- `.tiff`

### 排序規則

圖片依檔名排序後合併。

### 成功輸出

成功時會建立指定的 PDF 檔案，並在 stdout 顯示：

```text
PDF 已成功建立：<output_pdf>
```

## pdf-to-png

### 語法

```bash
python PDF-Combine.py pdf-to-png --input <pdf-file> --output-folder <folder> [--dpi <dpi>] [--pages <selection>]
```

### 參數

| 參數 | 必填 | 預設 | 說明 |
|---|---|---|---|
| `--input` | 是 | 無 | 來源 PDF 檔案。 |
| `--output-folder` | 是 | 無 | PNG 輸出資料夾。 |
| `--dpi` | 否 | `200` | 輸出解析度，必須介於 `72` 到 `600`。 |
| `--pages` | 否 | 空字串 | 頁碼選擇；空字串代表全部頁面。 |

### 頁碼格式

`--pages` 使用 1-based 頁碼，支援單頁與範圍，以逗號分隔。

範例：

```text
1
1-3
1-3,5
```

不支援倒序範圍，例如 `5-3`。

### 輸出檔名

輸出檔名格式：

```text
<pdf_base_name>_page_<page_number>.png
```

頁碼會補零，最少 3 位數。範例：

```text
sample_page_001.png
sample_page_002.png
```

### 成功輸出

成功時會在指定資料夾建立 PNG 檔案，並在 stdout 顯示：

```text
已成功輸出 <count> 張 PNG 圖檔：<output_folder>
```

## 錯誤行為

- CLI 模式不使用 tkinter messagebox；適合 headless 或批次環境。
- 成功訊息輸出到 stdout；錯誤與警告輸出到 stderr。
- 來源資料夾不存在、來源 PDF 不存在、無可用圖片、DPI 超出範圍、頁碼格式錯誤或頁碼超出範圍時，程式會輸出錯誤並以非零狀態結束。
- `pdf-to-png` 需要 PyMuPDF；缺少套件時會提示安裝 PyMuPDF 並以非零狀態結束。
- 未提供子命令時才會啟動 tkinter GUI，GUI 模式仍使用 messagebox 顯示錯誤、提示與成功訊息。

## 相容性規則

- 移除或重新命名既有子命令前，必須先更新本文件與 README。
- 新增 CLI 參數時，必須補充本文件的語法、參數表與成功/錯誤行為。
- 變更輸出檔名格式時，必須視為破壞性變更並在 README 明確標示。
