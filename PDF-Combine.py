from PIL import Image
import os
import sys

# 在 Windows 上將 stdout 重新設定為 utf-8（避免編碼問題）
if os.name == 'nt':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def choose_paths_with_tk():
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

    # 確保輸出目錄存在
    out_dir = os.path.dirname(output_pdf)
    if out_dir and not os.path.isdir(out_dir):
        try:
            os.makedirs(out_dir, exist_ok=True)
        except Exception as e:
            print(f"無法建立輸出資料夾：{out_dir} ({e})")
            sys.exit(1)

    return image_folder, output_pdf

def choose_paths_cli():
    print("無法開啟圖形對話框，請於命令列輸入路徑與檔名。")
    image_folder = input("請輸入來源圖片資料夾（絕對或相對路徑）：").strip()
    if not image_folder:
        print("已取消：未輸入來源資料夾。")
        sys.exit(0)

    out_dir = input(f"請輸入輸出資料夾（留空使用來源資料夾：{image_folder}）：").strip()
    if not out_dir:
        out_dir = image_folder

    if not os.path.isdir(out_dir):
        try:
            os.makedirs(out_dir, exist_ok=True)
        except Exception as e:
            print(f"無法建立輸出資料夾：{out_dir} ({e})")
            sys.exit(1)

    filename = input("請輸入輸出 PDF 檔名（不含副檔名，留空使用 combined_images）：").strip()
    if not filename:
        filename = "combined_images"
    if not filename.lower().endswith(".pdf"):
        filename = f"{filename}.pdf"

    output_pdf = os.path.join(out_dir, filename)
    return image_folder, output_pdf

def main():
    # 選擇路徑（優先使用 tkinter 對話框，失敗則 CLI）
    try:
        image_folder, output_pdf = choose_paths_with_tk()
    except Exception:
        image_folder, output_pdf = choose_paths_cli()

    # 驗證來源資料夾
    if not os.path.isdir(image_folder):
        print(f"來源資料夾不存在：{image_folder}")
        sys.exit(1)

    # 支援的副檔名
    exts = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')
    image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(exts)])

    if not image_files:
        print("沒有找到任何可用的圖片檔案，請確認路徑和檔案格式。")
        sys.exit(1)

    images = []
    opened_paths = []
    for img_name in image_files:
        img_path = os.path.join(image_folder, img_name)
        try:
            img = Image.open(img_path).convert('RGB')
            images.append(img)
            opened_paths.append(img_path)
        except Exception as e:
            print(f"跳過無法開啟的檔案：{img_path}  ({e})")

    if not images:
        print("所有圖片均無法開啟，無法建立 PDF。")
        sys.exit(1)

    try:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"PDF 已成功建立：{output_pdf}")
    except Exception as e:
        print(f"儲存 PDF 時發生錯誤：{e}")
        sys.exit(1)
    finally:
        # 關閉所有已開啟的影像檔案物件
        for img in images:
            try:
                img.close()
            except Exception:
                pass

if __name__ == "__main__":
    main()