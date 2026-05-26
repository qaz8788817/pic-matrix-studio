import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import os
import glob
import platform
from PIL import Image

# 系統字型判定
if platform.system() == "Windows":
    main_font_family = "Segoe UI"
elif platform.system() == "Darwin":
    main_font_family = "PingFang TC"
else:
    main_font_family = "Arial"

ctk.set_appearance_mode("light")

class PicMatrixStudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 紫黃多巴胺配色
        self.bg_purple = "#C69FD5"      # 粉紫背景
        self.text_yellow = "#FDFDC9"    # 奶油黃字
        self.dark_purple = "#4A2E80"    # 深紫容器
        self.bar_bg = "#63439C"         # 進度條軌道底色
        self.macaron_green = "#BAFFC9"  # 執行成功/進度條高亮馬卡龍綠

        self.title("PicMatrix Studio - Batch Image Processor 🖼️")
        self.geometry("620x540") # 緊湊垂直黃金比例
        self.resizable(False, False)
        self.configure(fg_color=self.bg_purple)

        self.selected_folder = ""
        self.image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp"]

        self.title_font = ctk.CTkFont(family=main_font_family, size=18, weight="bold")
        self.body_font = ctk.CTkFont(family=main_font_family, size=13)
        self.btn_font = ctk.CTkFont(family=main_font_family, size=13, weight="bold")

        self.setup_ui()

    def setup_ui(self):
        # 主功能包覆外框
        main_frame = ctk.CTkFrame(self, fg_color=self.dark_purple, corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="🖼️ PicMatrix Image Processor", font=self.title_font, text_color=self.text_yellow).pack(pady=(20, 10))

        # =====================================================================
        # 📂 1. 來源資料夾選擇區
        # =====================================================================
        folder_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        folder_frame.pack(fill="x", padx=30, pady=10)

        self.lbl_folder_path = ctk.CTkLabel(folder_frame, text="No folder selected... 📁", font=self.body_font, text_color=self.text_yellow, anchor="w")
        self.lbl_folder_path.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_select = ctk.CTkButton(
            folder_frame, text="Browse Folder", font=self.btn_font, width=120,
            fg_color=self.bg_purple, hover_color="#B58BC4", text_color=self.dark_purple,
            command=self.select_folder
        )
        btn_select.pack(side="right")

        # =====================================================================
        # ⚙️ 2. 功能勾選面板 (一鍵複選你想觸發的操作)
        # =====================================================================
        ctk.CTkLabel(main_frame, text="Select Processing Operations:", font=self.btn_font, text_color=self.text_yellow).pack(anchor="w", padx=35, pady=(15, 2))
        
        options_panel = ctk.CTkFrame(main_frame, fg_color="#361B66", corner_radius=10)
        options_panel.pack(fill="x", padx=30, pady=5)

        # 功能 A：尺寸縮放
        self.check_resize = ctk.CTkCheckBox(options_panel, text="Batch Resize to 50%", font=self.body_font, text_color=self.text_yellow)
        self.check_resize.pack(anchor="w", padx=20, pady=12)

        # 功能 B：格式轉換
        self.check_convert = ctk.CTkCheckBox(options_panel, text="Batch Convert Format to PNG", font=self.body_font, text_color=self.text_yellow)
        self.check_convert.pack(anchor="w", padx=20, pady=12)

        # 功能 C：自動重新命名
        self.check_rename = ctk.CTkFrame(options_panel, fg_color="transparent")
        self.check_rename.pack(fill="x", anchor="w", padx=20, pady=(0, 12))
        
        self.var_rename = ctk.CTkCheckBox(self.check_rename, text="Auto Rename to:", font=self.body_font, text_color=self.text_yellow)
        self.var_rename.pack(side="left")
        
        self.ent_prefix = ctk.CTkEntry(self.check_rename, placeholder_text="e.g. project_img", width=160, height=26, fg_color="#FFFFFF", text_color="#000000")
        self.ent_prefix.pack(side="left", padx=10)
        self.ent_prefix.insert(0, "processed_img") # 預設檔名前綴

        # =====================================================================
        # 🚀 3. 進度條與核心執行按鈕
        # =====================================================================
        # 狀態文字提示
        self.lbl_status = ctk.CTkLabel(main_frame, text="Ready to process.", font=self.body_font, text_color="gray")
        self.lbl_status.pack(pady=(30, 2))

        # 馬卡龍色進度條
        self.progress_bar = ctk.CTkProgressBar(main_frame, height=12, progress_color=self.macaron_green, fg_color=self.bar_bg)
        self.progress_bar.pack(fill="x", padx=30, pady=5)
        self.progress_bar.set(0)

        # 核心執行大鈕
        self.btn_run = ctk.CTkButton(
            main_frame, text="🚀 Run Batch Processing", font=self.title_font, height=45,
            fg_color=self.text_yellow, hover_color="#EBEB9B", text_color=self.dark_purple, corner_radius=8,
            command=self.run_batch_processing
        )
        self.btn_run.pack(fill="x", padx=30, pady=(15, 25))

    def select_folder(self):
        folder = filedialog.askdirectory(parent=self)
        if folder:
            self.selected_folder = folder
            # 畫面顯示極簡縮短後的路徑
            display_path = folder if len(folder) <= 45 else f"...{folder[-42:]}"
            self.lbl_folder_path.configure(text=f"📁 {display_path}", text_color=self.macaron_green)
            self.lbl_status.configure(text="Folder loaded. Choose operations and run!", text_color="gray")

    # --- ⚙️ 核心批次影像處理邏輯 ---
    def run_batch_processing(self):
        if not self.selected_folder:
            messagebox.showwarning("Warning", "Please select a target folder first!", parent=self)
            return

        # 讀取使用者勾選了哪些功能
        do_resize = self.check_resize.get()
        do_convert = self.check_convert.get()
        do_rename = self.var_rename.get()
        prefix = self.ent_prefix.get().strip()

        if not (do_resize or do_convert or do_rename):
            messagebox.showwarning("Warning", "Please check at least one operation to perform!", parent=self)
            return

        # 蒐集該資料夾下所有支援的影像檔案
        files_to_process = []
        for ext in self.image_extensions:
            files_to_process.extend(glob.glob(os.path.join(self.selected_folder, ext)))
            files_to_process.extend(glob.glob(os.path.join(self.selected_folder, ext.upper()))) # 支援大寫字尾如 .PNG

        # 去除重複項
        files_to_process = list(set(files_to_process))
        total_files = len(files_to_process)

        if total_files == 0:
            messagebox.showinfo("No Images Found", "There are no supported image files in the selected folder.", parent=self)
            return

        # 建立獨立的輸出資料夾，防範無情覆蓋原始珍貴影像
        output_dir = os.path.join(self.selected_folder, "PicMatrix_Output")
        os.makedirs(output_dir, exist_ok=True)

        # 鎖定按鈕防止在處理中被重複點擊導致混亂
        self.btn_run.configure(state="disabled", text="Processing... ⏳")
        self.progress_bar.set(0)

        # 開始迴圈逐張處理
        for idx, file_path in enumerate(files_to_process):
            try:
                # 1. 讀取影像
                with Image.open(file_path) as img:
                    # 處理格式轉換暫存格式
                    orig_format = img.format
                    save_format = "PNG" if do_convert else orig_format
                    if save_format == "JPEG" and img.mode in ("RGBA", "P"):
                        img = img.convert("RGB") # JPG 不支援透明度，自動防呆轉換

                    # 2. 執行尺寸調整 (縮小 50%)
                    if do_resize:
                        new_w = max(1, round(img.width * 0.5))
                        new_h = max(1, round(img.height * 0.5))
                        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

                    # 3. 執行重新命名與決定新檔名
                    if do_rename and prefix:
                        ext_str = ".png" if do_convert else os.path.splitext(file_path)[1].lower()
                        new_name = f"{prefix}_{idx+1:02d}{ext_str}"
                    else:
                        if do_convert:
                            new_name = os.path.splitext(os.path.basename(file_path))[0] + ".png"
                        else:
                            new_name = os.path.basename(file_path)

                    # 4. 存檔輸出
                    final_output_path = os.path.join(output_dir, new_name)
                    img.save(final_output_path, format=save_format)

            except Exception as e:
                print(f"Error processing {file_path}: {e}") # 異常單張跳過，不中斷整批進程

            # 5. 更新馬卡龍色進度條與狀態文字 (UI 平滑連動)
            current_progress = (idx + 1) / total_files
            self.progress_bar.set(current_progress)
            self.lbl_status.configure(text=f"Processed: {idx+1} / {total_files} images...", text_color=self.text_yellow)
            self.update() # 強制刷新 Tkinter 畫面核心

        # 結束處理，恢復按鈕
        self.btn_run.configure(state="normal", text="🚀 Run Batch Processing")
        self.lbl_status.configure(text="All tasks completed successfully! 🎉", text_color=self.macaron_green)
        
        messagebox.showinfo("Success 🎉", f"Successfully processed {total_files} images!\nSaved to: PicMatrix_Output资料夹", parent=self)


if __name__ == "__main__":
    app = PicMatrixStudioApp()
    app.mainloop()