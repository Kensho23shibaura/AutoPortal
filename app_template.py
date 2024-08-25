import customtkinter as ctk

# 自作ライブラリ
from popup import CustomMessageBox

# アプリケーション画面のベースクラス
class AppTemplate(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("アプリケーション名")
        self.geometry("400x300")
        ctk.set_appearance_mode("dark")  # テーマカラーの設定
        ctk.set_default_color_theme("blue")

        # GUI設定メソッドの呼び出し
        self.setting_gui()

    def setting_gui(self):
        # ここにGUI要素を追加する
        label = ctk.CTkLabel(self, text="このアプリケーションの画面")
        label.pack(pady=20)

        # 必要なウィジェットを追加
        button = ctk.CTkButton(self, text="ボタン", command=self.on_button_click)
        button.pack(pady=10)

    def on_button_click(self):
        # ボタン押下時の処理
        CustomMessageBox.show_info(title="情報", message="ボタンが押されました")

# メイン処理
if __name__ == "__main__":
    app = AppTemplate()
    app.mainloop()
