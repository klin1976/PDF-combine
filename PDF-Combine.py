import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# 在 Windows 上將 stdout 重新設定為 utf-8（避免編碼問題）
# PyInstaller --noconsole 模式下 sys.stdout 可能為 None，需先檢查
if os.name == 'nt' and sys.stdout is not None:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        if sys.stdout.buffer is not None:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def choose_paths_with_tk():
    root = tk.Tk()
    root.withdraw()

    image_folder = filedialog.askdirectory(title="選擇來源圖片資料夾", initialdir=os.getcwd())
    if not image_folder:
        messagebox.showinfo("提示", "已取消：未選擇來源資料夾。")
        sys.exit(0)

    output_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF 檔案", "*.pdf")],
        title="選擇輸出 PDF 檔案位置與名稱",
        initialfile="combined_images.pdf",
        initialdir=os.path.expanduser("~")
    )
    if not output_pdf:
        messagebox.showinfo("提示", "已取消：未選擇輸出檔案。")
        sys.exit(0)

    # 確保輸出目錄存在
    out_dir = os.path.dirname(output_pdf)
    if out_dir and not os.path.isdir(out_dir):
        try:
            os.makedirs(out_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror("錯誤", f"無法建立輸出資料夾：{out_dir}\n{e}")
            sys.exit(1)

    return image_folder, output_pdf

def main():
    try:
        image_folder, output_pdf = choose_paths_with_tk()
    except Exception as e:
        # 這裡用 messagebox 確保錯誤能被看見
        tk.Tk().withdraw()
        messagebox.showerror("錯誤", f"程式啟動失敗：{e}")
        sys.exit(1)

    # 驗證來源資料夾
    if not os.path.isdir(image_folder):
        messagebox.showerror("錯誤", f"來源資料夾不存在：{image_folder}")
        sys.exit(1)

    # 支援的副檔名
    exts = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')
    image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(exts)])

    if not image_files:
        messagebox.showwarning("警告", "沒有找到任何可用的圖片檔案，請確認路徑和檔案格式。")
        sys.exit(1)

    images = []
    for img_name in image_files:
        img_path = os.path.join(image_folder, img_name)
        try:
            img = Image.open(img_path).convert('RGB')
            images.append(img)
        except Exception as e:
            # 視窗模式下 print 看不到，但至少不中斷
            if sys.stdout:
                print(f"跳過無法開啟的檔案：{img_path} ({e})")

    if not images:
        messagebox.showerror("錯誤", "所有圖片均無法開啟，無法建立 PDF。")
        sys.exit(1)

    try:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        messagebox.showinfo("成功", f"PDF 已成功建立！\n位置：{output_pdf}")
    except Exception as e:
        messagebox.showerror("錯誤", f"儲存 PDF 時發生錯誤：{e}")
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