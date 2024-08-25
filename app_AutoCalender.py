import customtkinter as ctk
from datetime import datetime, timedelta
import calendar

class AutoCalendarTool(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ウィンドウ設定
        self.title("自動カレンダーツール")
        self.geometry("800x600")
        ctk.set_appearance_mode("dark")  # テーマカラーの設定
        ctk.set_default_color_theme("blue")

        # ヘッダーラベル
        header_label = ctk.CTkLabel(self, text="勤怠カレンダー", fg_color="blue", text_color="white", height=40, anchor="center")
        header_label.pack(fill="x")

        # GUI設定メソッドの呼び出し
        self.setting_gui()

    def setting_gui(self):
        # カレンダーの表示
        self.create_calendar()

        # ラジオボタン
        self.radio_var = ctk.StringVar()
        radio_frame = ctk.CTkFrame(self)
        radio_frame.pack(pady=10)

        self.radio_options = {
            "オフィス": ("green", "オフィス"),
            "在宅": ("orange", "在宅"),
            "年休": ("red", "年休"),
            "研修": ("pink", "研修"),
            "出張": ("purple", "出張")
        }

        for text, (color, _) in self.radio_options.items():
            ctk.CTkRadioButton(radio_frame, text=text, variable=self.radio_var, value=color, bg_color=color).pack(side="left", padx=10)

        # ボタンの追加
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        change_button = ctk.CTkButton(button_frame, text="変更", fg_color="blue", command=self.update_calendar)
        change_button.pack(side="left", padx=10)

        load_button = ctk.CTkButton(button_frame, text="読込", fg_color="blue", command=self.load_outlook)
        load_button.pack(side="left", padx=10)

        apply_button = ctk.CTkButton(button_frame, text="反映", fg_color="red", command=self.apply_to_outlook)
        apply_button.pack(side="left", padx=10)

    def create_calendar(self):
        today = datetime.now()
        start_date = today - timedelta(days=today.weekday() + 1)  # 今週の日曜日を基準に5週間前からスタート

        self.calendar_frame = ctk.CTkFrame(self)
        self.calendar_frame.pack(pady=10)

        # カレンダーのヘッダー
        header_days = ["日", "月", "火", "水", "木", "金", "土"]
        for i, day in enumerate(header_days):
            ctk.CTkLabel(self.calendar_frame, text=day, width=60, anchor="center", fg_color="transparent", text_color="white").grid(row=0, column=i, padx=2, pady=2)

        self.dates = {}
        self.original_colors = {}  # 日付ごとの元の色を保存する辞書
        self.selected_date = None

        # カレンダーの日付
        for week in range(5):
            for day in range(7):
                date = start_date + timedelta(weeks=week, days=day)
                display_date = date.strftime("%m/%d") if (day == 0 and week == 0) or date.day == 1 else str(date.day)
                
                date_button = ctk.CTkButton(
                    self.calendar_frame, text=f"{display_date}\n\n", width=60, height=80,
                    fg_color="RoyalBlue1",  # デフォルトのRoyalBlue1を設定
                    text_color="black",       # 文字色を黒に設定
                    command=lambda d=date: self.on_date_selected(d)
                )
                date_button.grid(row=week + 1, column=day, padx=2, pady=2)

                # 初期設定の色を登録
                self.dates[date] = date_button
                self.dates[date].configure(fg_color="RoyalBlue1")
                self.original_colors[date] = "RoyalBlue1"

    def on_date_selected(self, selected_date):
        # 選択された日付セルの背景色を黄色に変更
        if self.selected_date:
            prev_button = self.dates[self.selected_date]
            prev_color = self.original_colors[self.selected_date]
            prev_button.configure(fg_color=prev_color)  # 元の背景色に戻す

        button = self.dates[selected_date]
        button.configure(fg_color="yellow")
        self.selected_date = selected_date

    def update_calendar(self):
        if self.selected_date:
            color = self.radio_var.get()
            valid_colors = [option[0] for option in self.radio_options.values()]
            if color not in valid_colors:
                return  # ラジオボタンの値が無効な場合は処理しない

            label = [label for clr, label in self.radio_options.values() if clr == color][0]
            button = self.dates[self.selected_date]
            button.configure(text=f"{button.cget('text').split('\n')[0]}\n{label}")
            self.original_colors[self.selected_date] = color

    # Outlookの予定を読込む処理 (仮想処理)
    def load_outlook(self):
        print(self.original_colors)
        pass

    # Outlookに予定を反映する処理 (仮想処理)
    def apply_to_outlook(self):
        # Outlookへの反映処理をここに追加
        for date in self.original_colors:
            color = self.original_colors[date]
            if color != "RoyalBlue1":
                label = [label for clr, label in self.radio_options.values() if clr == color][0]
                print(f"{date.strftime('%m/%d')} {label}")



            # # 現在のセルの背景色から予定を判別
            # color = button.cget("fg_color")
            # if color != self.original_colors[date]:  # デフォルト色以外の場合に処理
            #     label = self.radio_options[color][1]
            #     # 日付と予定をプリント
            #     print(f"{date.strftime('%m/%d')} {label}")

# メイン処理
if __name__ == "__main__":
    app = AutoCalendarTool()
    app.mainloop()
