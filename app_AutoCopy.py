import customtkinter as ctk
from tkinter import filedialog, messagebox
import shutil
import os
import openpyxl

# 自作ライブラリ
from popup import CustomMessageBox

class AutoCopyTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("自動複製ツール")
        self.geometry("600x550")
        ctk.set_appearance_mode("dark")  # テーマカラーの設定
        ctk.set_default_color_theme("blue")

        # GUI設定メソッドの呼び出し
        self.setting_gui()

    def setting_gui(self):
        # フォルダ複製セクション
        header1 = ctk.CTkLabel(self, text="フォルダ複製", font=ctk.CTkFont(size=16, weight="bold"), fg_color="blue4", text_color="white")
        header1.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

        folder_path_label = ctk.CTkLabel(self, text="フォルダパス")
        folder_path_label.grid(row=1, column=0, padx=10, sticky="e")
        self.folder_path_entry = ctk.CTkEntry(self, width=300)
        self.folder_path_entry.grid(row=1, column=1, padx=10)
        folder_path_button = ctk.CTkButton(self, text="選択", command=lambda: self.select_folder(self.folder_path_entry))
        folder_path_button.grid(row=1, column=2, padx=10)

        copy_folder_name_label = ctk.CTkLabel(self, text="複製フォルダ名")
        copy_folder_name_label.grid(row=2, column=0, padx=10, sticky="e")
        self.copy_folder_name_entry = ctk.CTkEntry(self, width=300)
        self.copy_folder_name_entry.grid(row=2, column=1, padx=10)

        copy_list_label = ctk.CTkLabel(self, text="複製リスト")
        copy_list_label.grid(row=3, column=0, padx=10, sticky="e")
        self.copy_list_entry = ctk.CTkEntry(self, width=300)
        self.copy_list_entry.grid(row=3, column=1, padx=10)
        copy_button = ctk.CTkButton(self, text="複製", command=self.copy_folder, fg_color="red4")
        copy_button.grid(row=3, column=2, padx=10)

        # ファイル複製セクション
        header2 = ctk.CTkLabel(self, text="ファイル複製", font=ctk.CTkFont(size=16, weight="bold"), fg_color="blue4", text_color="white")
        header2.grid(row=4, column=0, columnspan=3, pady=20, sticky="ew")

        file_folder_path_label = ctk.CTkLabel(self, text="フォルダパス")
        file_folder_path_label.grid(row=5, column=0, padx=10, sticky="e")
        self.file_folder_path_entry = ctk.CTkEntry(self, width=300)
        self.file_folder_path_entry.grid(row=5, column=1, padx=10)
        file_folder_path_button = ctk.CTkButton(self, text="選択", command=lambda: self.select_folder(self.file_folder_path_entry))
        file_folder_path_button.grid(row=5, column=2, padx=10)

        copy_file_name_label = ctk.CTkLabel(self, text="複製ファイル名")
        copy_file_name_label.grid(row=6, column=0, padx=10, sticky="e")
        self.copy_file_name_entry = ctk.CTkEntry(self, width=300)
        self.copy_file_name_entry.grid(row=6, column=1, padx=10)

        file_copy_list_label = ctk.CTkLabel(self, text="複製リスト")
        file_copy_list_label.grid(row=7, column=0, padx=10, sticky="e")
        self.file_copy_list_entry = ctk.CTkEntry(self, width=300)
        self.file_copy_list_entry.grid(row=7, column=1, padx=10)
        file_copy_button = ctk.CTkButton(self, text="複製", command=self.copy_file, fg_color="red4")
        file_copy_button.grid(row=7, column=2, padx=10)

        # Excelシート複製セクション
        header3 = ctk.CTkLabel(self, text="Excelシート複製", font=ctk.CTkFont(size=16, weight="bold"), fg_color="blue4", text_color="white")
        header3.grid(row=8, column=0, columnspan=3, pady=20, sticky="ew")

        excel_file_path_label = ctk.CTkLabel(self, text="Excelファイル")
        excel_file_path_label.grid(row=9, column=0, padx=10, sticky="e")
        self.excel_file_path_entry = ctk.CTkEntry(self, width=300)
        self.excel_file_path_entry.grid(row=9, column=1, padx=10)
        excel_file_path_button = ctk.CTkButton(self, text="選択", command=lambda: self.select_excel_file(self.excel_file_path_entry))
        excel_file_path_button.grid(row=9, column=2, padx=10)

        copy_sheet_name_label = ctk.CTkLabel(self, text="複製シート名")
        copy_sheet_name_label.grid(row=10, column=0, padx=10, sticky="e")
        self.copy_sheet_name_entry = ctk.CTkEntry(self, width=300)
        self.copy_sheet_name_entry.grid(row=10, column=1, padx=10)

        excel_copy_list_label = ctk.CTkLabel(self, text="複製リスト")
        excel_copy_list_label.grid(row=11, column=0, padx=10, sticky="e")
        self.excel_copy_list_entry = ctk.CTkEntry(self, width=300)
        self.excel_copy_list_entry.grid(row=11, column=1, padx=10)
        excel_copy_button = ctk.CTkButton(self, text="複製", command=self.copy_excel_sheet, fg_color="red4")
        excel_copy_button.grid(row=11, column=2, padx=10)

    def select_folder(self, entry_widget):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, folder_path)

    def select_excel_file(self, entry_widget):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, file_path)

    def copy_folder(self):
        folder_path = self.folder_path_entry.get()
        folder_name = self.copy_folder_name_entry.get()
        copy_list = self.copy_list_entry.get().split(',')

        if not os.path.exists(os.path.join(folder_path, folder_name)):
            CustomMessageBox.show_error("エラー", "指定したフォルダが存在しません。")
            return

        for name in copy_list:
            new_folder_path = os.path.join(folder_path, name.strip())
            try:
                shutil.copytree(os.path.join(folder_path, folder_name), new_folder_path)
            except Exception as e:
                CustomMessageBox.show_error("エラー", f"フォルダの複製に失敗しました: {e}")
                return

        CustomMessageBox.show_info("成功", "フォルダの複製が完了しました。")

    def copy_file(self):
        folder_path = self.file_folder_path_entry.get()
        file_name = self.copy_file_name_entry.get()
        copy_list = self.file_copy_list_entry.get().split(',')

        if not os.path.exists(os.path.join(folder_path, file_name)):
            CustomMessageBox.show_error("エラー", "指定したファイルが存在しません。")
            return

        for name in copy_list:
            base, ext = os.path.splitext(file_name)
            new_file_path = os.path.join(folder_path, f"{name.strip()}{ext}")
            try:
                shutil.copy(os.path.join(folder_path, file_name), new_file_path)
            except Exception as e:
                CustomMessageBox.show_error("エラー", f"ファイルの複製に失敗しました: {e}")
                return

        CustomMessageBox.show_info("成功", "ファイルの複製が完了しました。")

    def copy_excel_sheet(self):
        file_path = self.excel_file_path_entry.get()
        sheet_name = self.copy_sheet_name_entry.get()
        copy_list = self.excel_copy_list_entry.get().split(',')

        if not os.path.exists(file_path):
            CustomMessageBox.show_error("エラー", "指定したExcelファイルが存在しません。")
            return

        try:
            wb = openpyxl.load_workbook(file_path)
            if sheet_name not in wb.sheetnames:
                CustomMessageBox.show_error("エラー", "指定したシートが存在しません。")
                return

            sheet = wb[sheet_name]
            for name in copy_list:
                new_sheet_name = name.strip()
                wb.copy_worksheet(sheet).title = new_sheet_name

            wb.save(file_path)
            wb.close()

            CustomMessageBox.show_info("成功", "Excelシートの複製が完了しました。")
        except Exception as e:
            CustomMessageBox.show_error("エラー", f"Excelシートの複製に失敗しました: {e}")

# メイン処理
if __name__ == "__main__":
    app = AutoCopyTool()
    app.mainloop()
