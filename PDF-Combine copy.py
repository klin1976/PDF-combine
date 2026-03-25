# ...existing code...
from PIL import Image
import os
import sys

# 在 Windows 上將 stdout 重新設定為 utf-8（避免 cp950 無法編碼特殊字元）
if os.name == 'nt':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 嘗試使用 tkinter 顯示選擇資料夾 / 儲存檔案對話框；若不可用則改用命令列輸入
try:
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()

    image_folder = filedialog.askdirectory(title="選擇來源圖片資料夾", initialdir=os.getcwd())
    if not image_folder:
        print("已取消：未選擇來源資料夾。")
        sys.exit(0)

    output_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF 檔案", "*.pdf")],
        title="選擇輸出 PDF 檔案位置與名稱",
        initialfile="combined_images.pdf",
        initialdir=os.path.expanduser("~")
    )
    if not output_pdf:
        print("已取消：未選擇輸出檔案。")
        sys.exit(0)

except Exception:
    # 若 tkinter 不可用，退回到命令列輸入
    print("無法開啟圖形對話框，請於命令列輸入路徑。")
    image_folder = input("請輸入來源圖片資料夾（絕對或相對路徑）：").strip()
    if not image_folder:
        print("已取消：未輸入來源資料夾。")
        sys.exit(0)
    output_pdf = input("請輸入輸出 PDF 檔案完整路徑（包含 .pdf 副檔名）：").strip()
    if not output_pdf:
        print("已取消：未輸入輸出檔案。")
        sys.exit(0)

# 驗證來源資料夾存在
if not os.path.isdir(image_folder):
    print(f"來源資料夾不存在：{image_folder}")
    sys.exit(1)

# 取得資料夾內所有圖片檔案，並依檔名排序
image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

# 讀取圖片並轉換為 RGB 格式（跳過無法開啟的檔案）
images = []
for img_name in image_files:
    img_path = os.path.join(image_folder, img_name)
    try:
        img = Image.open(img_path).convert('RGB')
        images.append(img)
    except Exception as e:
        print(f"跳過無法開啟的檔案：{img_path}  ({e})")

# 將第一張圖片作為起始，並附加其他圖片
if images:
    try:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"PDF 已成功建立：{output_pdf}")
    except Exception as e:
        print(f"儲存 PDF 時發生錯誤：{e}")
        sys.exit(1)
else:
    print("沒有找到任何可用的圖片檔案，請確認路徑和檔案格式。")
# ...existing code...