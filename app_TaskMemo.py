import customtkinter as ctk
import os
import yaml

# 自作ライブラリ
from popup import CustomMessageBox

# カレントディレクトリをプログラムの実行場所に設定
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 設定ファイルのパス
CONFIG_FILE = "setting.yml"

# タスクメモツールクラス
class TaskMemoTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("タスクメモツール")
        self.geometry("400x300")
        ctk.set_appearance_mode("dark")  # テーマカラーの設定
        ctk.set_default_color_theme("blue")

        # ファイルパスの読み込み
        self.file_path = self.load_file_path()

        # GUI設定メソッドの呼び出し
        self.setting_gui()

        # ファイル内容の読み込み
        self.load_file_content()

    def load_file_path(self):
        # setting.ymlからファイルパスを読み込む
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = yaml.safe_load(f)
            return config.get("TaskMemoTool", {}).get("file_path", "")
        return ""

    def setting_gui(self):
        # ウィンドウの行と列の重みを設定して、リサイズ時にウィジェットが拡大縮小するようにする
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)        

        # テキスト入力欄
        self.text_box = ctk.CTkTextbox(self, wrap="word", width=380, height=200)
        self.text_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # 保存ボタン
        save_button = ctk.CTkButton(self, text="保存", command=self.save_file_content, fg_color="red")
        save_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def load_file_content(self):
        # ファイルから内容を読み込んでテキストボックスに表示
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.text_box.insert("1.0", content)

    def save_file_content(self):
        # テキストボックスの内容をファイルに保存
        content = self.text_box.get("1.0", "end-1c")
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write(content)

# メイン処理
if __name__ == "__main__":
    app = TaskMemoTool()
    app.mainloop()
