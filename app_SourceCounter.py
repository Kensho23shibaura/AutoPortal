import os
import customtkinter as ctk
from tkinter import filedialog

class SourceCounterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("ソースカウンターツール")
        self.geometry("600x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # GUI設定
        self.setting_gui()

    def setting_gui(self):
        # ヘッダー行を青くする
        header1 = ctk.CTkLabel(self, text="計測対象", font=ctk.CTkFont(size=16, weight="bold"), fg_color="blue4", text_color="white")
        header1.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

        folder_path_label = ctk.CTkLabel(self, text="フォルダパス")
        folder_path_label.grid(row=1, column=0, padx=10, sticky="e")
        self.folder_path_entry = ctk.CTkEntry(self, width=300)
        self.folder_path_entry.grid(row=1, column=1, padx=10)
        folder_path_button = ctk.CTkButton(self, text="選択", command=lambda: self.select_folder(self.folder_path_entry))
        folder_path_button.grid(row=1, column=2, padx=10)

        exclude_list_label = ctk.CTkLabel(self, text="除外対象")
        exclude_list_label.grid(row=2, column=0, padx=10, sticky="e")
        self.exclude_list_entry = ctk.CTkEntry(self, width=300)
        self.exclude_list_entry.grid(row=2, column=1, padx=10)

        ext_list_label = ctk.CTkLabel(self, text="計測拡張子")
        ext_list_label.grid(row=3, column=0, padx=10, sticky="e")
        self.ext_list_entry = ctk.CTkEntry(self, width=300)
        self.ext_list_entry.grid(row=3, column=1, padx=10)

        measure_button = ctk.CTkButton(self, text="計測", command=self.measure, fg_color="red4")
        measure_button.grid(row=3, column=2, padx=10)

        header2 = ctk.CTkLabel(self, text="計測結果", font=ctk.CTkFont(size=16, weight="bold"), fg_color="blue4", text_color="white")
        header2.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")

        self.result_text = ctk.CTkTextbox(self, width=400, height=150)
        self.result_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    def select_folder(self, entry_widget):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, folder_path)

    def measure(self):
        folder_path = self.folder_path_entry.get()
        exclude_list = [item.strip() for item in self.exclude_list_entry.get().split(",")]
        ext_list = [item.strip().lower() for item in self.ext_list_entry.get().split(",")]
        result = self.count_source_lines(folder_path, exclude_list, ext_list)

        display_result = ""
        for ext, counts in result.items():
            display_result += (
                f"拡張子: .{ext}\n"
                f"ファイル数: {counts['file_count']}\n"
                f"全体行数: {counts['total_lines']}\n"
                f"コメント行数: {counts['comment_lines']}\n"
                f"空行数: {counts['empty_lines']}\n\n"
            )
        self.result_text.delete(1.0, ctk.END)
        self.result_text.insert(ctk.END, display_result)

    def count_source_lines(self, folder_path, exclude_list, ext_list):
        ext_counts = {ext: {"file_count": 0, "total_lines": 0, "comment_lines": 0, "empty_lines": 0} for ext in ext_list}

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)

                # 除外対象リストが空でない場合にのみチェック
                if exclude_list != [''] and any(exclude in file_path for exclude in exclude_list):
                    continue

                # 拡張子の確認と処理
                file_ext = os.path.splitext(file)[1][1:].lower()
                if file_ext in ext_list:
                    print(file_path)
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    total_lines = len(lines)
                    blank_lines = sum(1 for line in lines if not line.strip())
                    comment_lines = sum(1 for line in lines if line.strip().startswith("#"))

                    ext_counts[file_ext]["file_count"] += 1
                    ext_counts[file_ext]["total_lines"] += total_lines
                    ext_counts[file_ext]["empty_lines"] += blank_lines
                    ext_counts[file_ext]["comment_lines"] += comment_lines

        return ext_counts

if __name__ == "__main__":
    app = SourceCounterApp()
    app.mainloop()
