import customtkinter as ctk
from tkinter import filedialog
import os

# 自作ライブラリ
from popup import CustomMessageBox

# 簡易メモツールのアプリケーションクラス
class SimpleMemoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("簡易メモツール")
        self.geometry("500x400")
        ctk.set_appearance_mode("dark")  # テーマカラーの設定
        ctk.set_default_color_theme("blue")

        # GUIの初期設定
        self.setting_gui()

    def setting_gui(self):
        # 1行目: ヘッダーラベル
        header_label = ctk.CTkLabel(self, text="簡易メモ", font=("Arial", 20))
        header_label.pack(pady=10)

        # 2行目: 複数行のテキスト入力欄
        self.textbox = ctk.CTkTextbox(self, height=10)
        self.textbox.pack(pady=10, padx=20, fill="both", expand=True)

        # 3行目: 保存先ラベル
        save_location_label = ctk.CTkLabel(self, text="保存先", font=("Arial", 16))
        save_location_label.pack(pady=10)

        # 4行目: ファイルパス入力関連
        file_frame = ctk.CTkFrame(self)
        file_frame.pack(pady=5, padx=20, fill="x")

        file_path_label = ctk.CTkLabel(file_frame, text="ファイルパス")
        file_path_label.pack(side="left", padx=10)

        self.file_path_entry = ctk.CTkEntry(file_frame, width=300)
        self.file_path_entry.pack(side="left", padx=10)

        select_file_button = ctk.CTkButton(file_frame, text="選択", command=self.select_file)
        select_file_button.pack(side="left", padx=10)

        # 5行目: 読込ボタンと保存ボタン
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        load_button = ctk.CTkButton(button_frame, text="読込", command=self.load_file, fg_color="blue")
        load_button.pack(side="left", padx=20)

        save_button = ctk.CTkButton(button_frame, text="保存", command=self.save_file, fg_color="red")
        save_button.pack(side="left", padx=20)

    def select_file(self):
        # ファイル選択ダイアログを表示し、結果をファイルパス入力欄に反映する
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.file_path_entry.delete(0, ctk.END)
            self.file_path_entry.insert(0, file_path)

    def load_file(self):
        # ファイルを読込み、内容をテキスト入力欄に反映する
        file_path = self.file_path_entry.get()
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.textbox.delete("1.0", ctk.END)
                self.textbox.insert(ctk.END, content)
        else:
            CustomMessageBox.show_error(title="エラー", message="ファイルが存在しません。")

    def save_file(self):
        # テキスト入力欄の内容をファイルに保存する
        file_path = self.file_path_entry.get()
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                content = self.textbox.get("1.0", ctk.END)
                file.write(content)
            CustomMessageBox.show_info(title="保存完了", message="ファイルが保存されました。")
        else:
            CustomMessageBox.show_error(title="エラー", message="ファイルパスが指定されていません。")

# メイン処理
if __name__ == "__main__":
    app = SimpleMemoApp()
    app.mainloop()
