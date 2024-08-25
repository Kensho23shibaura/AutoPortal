import customtkinter as ctk
import subprocess
import os
import sys

# カレントディレクトリをプログラムの実行場所に設定
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# メニュー画面クラス
class MenuApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("メニュー画面")
        self.geometry("320x320")
        ctk.set_appearance_mode("dark")  # テーマカラーの設定
        ctk.set_default_color_theme("blue")

        # 各アプリケーションのパスを辞書で管理
        self.apps = {
            "タスクメモツール": "app_TaskMemo.py",
            "簡易メモツール": "app_SimpleMemo.py",
            "マクロ生成ツール": "app_ActionMaker.py",
            "マクロ実行ツール": "app_ActionPlayer.py",
            "自動複製ツール": "app_AutoCopy.py",
            "ソースカウンターツール": "app_SourceCounter.py",
            "デモデータ生成ツール": "",
            "自動カレンダーツール": "app_AutoCalender.py",
            "外部アプリケーション": "C:/path/to/your/application.exe",  # 例: exeファイルのパス
            "バッチファイル": "C:/path/to/your/script.bat"  # 例: batファイルのパス
        }

        # GUI設定メソッドの呼び出し
        self.setting_gui()

    def setting_gui(self):
        # メニューのラベルを追加
        label = ctk.CTkLabel(self, text="ツール一覧", font=ctk.CTkFont(size=16, weight="bold"), fg_color="blue4", text_color="white")
        label.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        # 各アプリへのボタンを作成
        for index, (app_name, app_path) in enumerate(self.apps.items()):
            button = ctk.CTkButton(self, text=app_name, command=lambda path=app_path: self.open_app(path))
            button.grid(row=((index // 2) + 1), column=(index % 2), padx=10, pady=10)

    def open_app(self, app_path):
        # アプリケーションがPythonスクリプトか.exeかを判定し、適切な方法で実行
        if app_path.endswith('.py'):
            subprocess.Popen([sys.executable, app_path])
        elif app_path.endswith('.exe') or app_path.endswith('.bat'):
            subprocess.Popen([app_path])

# メイン処理
if __name__ == "__main__":
    app = MenuApp()
    app.mainloop()
