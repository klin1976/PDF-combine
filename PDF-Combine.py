import os
import sys
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None


class ConversionError(Exception):
    """Raised for expected conversion failures shown to users."""


def configure_windows_text_stream(stream):
    if stream is None:
        return None

    try:
        stream.reconfigure(encoding='utf-8', errors='backslashreplace')
        return stream
    except AttributeError:
        import io
        buffer = getattr(stream, 'buffer', None)
        if buffer is not None:
            return io.TextIOWrapper(buffer, encoding='utf-8', errors='backslashreplace')

    return stream


# 在 Windows 上將 CLI 文字串流重新設定為 UTF-8（避免中文輸出亂碼）。
# PyInstaller --noconsole 模式下 stdout/stderr 可能為 None，需先檢查。
if os.name == 'nt':
    sys.stdout = configure_windows_text_stream(sys.stdout)
    sys.stderr = configure_windows_text_stream(sys.stderr)


def write_line(message, stream=None):
    stream = stream or sys.stdout
    if stream:
        print(message, file=stream)


def write_warning(message):
    write_line(f"警告：{message}", sys.stderr or sys.stdout)


def write_error(message):
    write_line(f"錯誤：{message}", sys.stderr or sys.stdout)


def choose_mode_with_tk():
    root = tk.Tk()
    root.withdraw()

    choice = messagebox.askyesnocancel(
        "選擇功能",
        "請選擇要執行的功能：\n\n是：圖片合併成 PDF\n否：PDF 轉成 PNG 圖檔"
    )
    if choice is None:
        messagebox.showinfo("提示", "已取消：未選擇功能。")
        sys.exit(0)

    return "images_to_pdf" if choice else "pdf_to_png"

def choose_image_to_pdf_paths_with_tk():
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

def choose_pdf_to_png_paths_with_tk():
    input_pdf = filedialog.askopenfilename(
        filetypes=[("PDF 檔案", "*.pdf")],
        title="選擇要轉換的 PDF 檔案",
        initialdir=os.getcwd()
    )
    if not input_pdf:
        messagebox.showinfo("提示", "已取消：未選擇 PDF 檔案。")
        sys.exit(0)

    output_folder = filedialog.askdirectory(
        title="選擇 PNG 輸出資料夾",
        initialdir=os.path.dirname(input_pdf) or os.getcwd()
    )
    if not output_folder:
        messagebox.showinfo("提示", "已取消：未選擇輸出資料夾。")
        sys.exit(0)

    if not os.path.isdir(output_folder):
        try:
            os.makedirs(output_folder, exist_ok=True)
        except Exception as e:
            messagebox.showerror("錯誤", f"無法建立輸出資料夾：{output_folder}\n{e}")
            sys.exit(1)

    dpi = simpledialog.askinteger(
        "輸出解析度",
        "請輸入輸出 DPI：",
        initialvalue=200,
        minvalue=72,
        maxvalue=600
    )
    if dpi is None:
        messagebox.showinfo("提示", "已取消：未設定輸出 DPI。")
        sys.exit(0)

    pages = simpledialog.askstring(
        "頁碼範圍",
        "請輸入頁碼範圍，例如 1-3,5。\n留空代表全部頁面："
    )
    if pages is None:
        messagebox.showinfo("提示", "已取消：未設定頁碼範圍。")
        sys.exit(0)

    return input_pdf, output_folder, dpi, pages.strip()

def parse_page_selection(selection, page_count):
    if not selection:
        return list(range(page_count))

    pages = set()
    for chunk in selection.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue

        if "-" in chunk:
            start_text, end_text = chunk.split("-", 1)
            try:
                start = int(start_text)
                end = int(end_text)
            except ValueError:
                raise ValueError(f"頁碼範圍格式不正確：{chunk}")
            if start > end:
                raise ValueError(f"頁碼範圍起始不可大於結束：{chunk}")
            pages.update(range(start, end + 1))
        else:
            try:
                pages.add(int(chunk))
            except ValueError:
                raise ValueError(f"頁碼格式不正確：{chunk}")

    invalid_pages = [page for page in pages if page < 1 or page > page_count]
    if invalid_pages:
        raise ValueError(f"頁碼超出 PDF 範圍：{invalid_pages}")

    return [page - 1 for page in sorted(pages)]

def images_to_pdf(image_folder, output_pdf, notify=True):
    # 驗證來源資料夾
    if not os.path.isdir(image_folder):
        raise ConversionError(f"來源資料夾不存在：{image_folder}")

    # 支援的副檔名
    exts = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')
    image_files = sorted([f for f in os.listdir(image_folder) if f.lower().endswith(exts)])

    if not image_files:
        raise ConversionError("沒有找到任何可用的圖片檔案，請確認路徑和檔案格式。")

    images = []
    for img_name in image_files:
        img_path = os.path.join(image_folder, img_name)
        try:
            img = Image.open(img_path).convert('RGB')
            images.append(img)
        except Exception as e:
            if not notify:
                write_warning(f"跳過無法開啟的檔案：{img_path} ({e})")

    if not images:
        raise ConversionError("所有圖片均無法開啟，無法建立 PDF。")

    try:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        if notify:
            messagebox.showinfo("成功", f"PDF 已成功建立！\n位置：{output_pdf}")
        return output_pdf
    except Exception as e:
        raise ConversionError(f"儲存 PDF 時發生錯誤：{e}")
    finally:
        # 關閉所有已開啟的影像檔案物件
        for img in images:
            try:
                img.close()
            except Exception:
                pass

def pdf_to_png(input_pdf, output_folder, dpi=200, pages="", notify=True):
    if fitz is None:
        raise ConversionError("PDF 轉 PNG 需要安裝 PyMuPDF。請執行：pip install PyMuPDF")

    if dpi < 72 or dpi > 600:
        raise ConversionError("DPI 必須介於 72 到 600 之間。")

    if not os.path.isfile(input_pdf):
        raise ConversionError(f"PDF 檔案不存在：{input_pdf}")

    if not os.path.isdir(output_folder):
        try:
            os.makedirs(output_folder, exist_ok=True)
        except Exception as e:
            raise ConversionError(f"無法建立輸出資料夾：{output_folder}\n{e}")

    base_name = os.path.splitext(os.path.basename(input_pdf))[0]
    output_files = []
    document = None

    try:
        document = fitz.open(input_pdf)
        if document.page_count == 0:
            raise ConversionError("PDF 沒有可轉換的頁面。")

        page_indexes = parse_page_selection(pages, document.page_count)
        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)
        digits = max(3, len(str(document.page_count)))

        for page_index in page_indexes:
            page = document.load_page(page_index)
            pixmap = page.get_pixmap(matrix=matrix, alpha=False)
            output_path = os.path.join(
                output_folder,
                f"{base_name}_page_{page_index + 1:0{digits}d}.png"
            )
            pixmap.save(output_path)
            output_files.append(output_path)
    except ConversionError:
        raise
    except ValueError as e:
        raise ConversionError(str(e))
    except Exception as e:
        raise ConversionError(f"轉換 PDF 時發生錯誤：{e}")
    finally:
        if document is not None:
            document.close()

    if notify:
        messagebox.showinfo(
            "成功",
            f"已成功輸出 {len(output_files)} 張 PNG 圖檔！\n資料夾：{output_folder}"
        )

    return output_files

def main():
    parser = argparse.ArgumentParser(
        description="圖片合併 PDF，或將 PDF 頁面轉成 PNG 圖檔。未提供參數時會啟動 GUI。"
    )
    subparsers = parser.add_subparsers(dest="command")

    image_parser = subparsers.add_parser("images-to-pdf", help="將圖片資料夾合併成 PDF")
    image_parser.add_argument("--input-folder", required=True, help="來源圖片資料夾")
    image_parser.add_argument("--output", required=True, help="輸出 PDF 檔案")

    pdf_parser = subparsers.add_parser("pdf-to-png", help="將 PDF 每頁轉成 PNG")
    pdf_parser.add_argument("--input", required=True, help="來源 PDF 檔案")
    pdf_parser.add_argument("--output-folder", required=True, help="PNG 輸出資料夾")
    pdf_parser.add_argument("--dpi", type=int, default=200, help="輸出 DPI，預設 200")
    pdf_parser.add_argument("--pages", default="", help="頁碼範圍，例如 1-3,5；留空代表全部")

    args = parser.parse_args()

    try:
        if args.command == "images-to-pdf":
            output_pdf = images_to_pdf(args.input_folder, args.output, notify=False)
            write_line(f"PDF 已成功建立：{output_pdf}")
            return 0

        if args.command == "pdf-to-png":
            output_files = pdf_to_png(args.input, args.output_folder, args.dpi, args.pages, notify=False)
            write_line(f"已成功輸出 {len(output_files)} 張 PNG 圖檔：{args.output_folder}")
            return 0
    except ConversionError as e:
        write_error(str(e))
        return 1

    try:
        mode = choose_mode_with_tk()
        if mode == "images_to_pdf":
            image_folder, output_pdf = choose_image_to_pdf_paths_with_tk()
            images_to_pdf(image_folder, output_pdf)
        else:
            input_pdf, output_folder, dpi, pages = choose_pdf_to_png_paths_with_tk()
            pdf_to_png(input_pdf, output_folder, dpi, pages)
    except ConversionError as e:
        tk.Tk().withdraw()
        messagebox.showerror("錯誤", str(e))
        return 1
    except Exception as e:
        # 這裡用 messagebox 確保錯誤能被看見
        tk.Tk().withdraw()
        messagebox.showerror("錯誤", f"程式啟動失敗：{e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
