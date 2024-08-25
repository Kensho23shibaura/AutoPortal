import customtkinter as ctk

class CustomMessageBox:
    @staticmethod
    def show_info(title, message):
        info_box = ctk.CTkToplevel()
        info_box.title(title)
        info_box.attributes('-topmost', True)  # 最前面に表示
        ctk.CTkLabel(info_box, text=message, fg_color="blue", text_color="white", width=300, height=100).pack(padx=20, pady=20)
        ctk.CTkButton(info_box, text="OK", command=info_box.destroy, fg_color="blue").pack(pady=10)

    @staticmethod
    def show_error(title, message):
        error_box = ctk.CTkToplevel()
        error_box.title(title)
        error_box.attributes('-topmost', True)  # 最前面に表示
        ctk.CTkLabel(error_box, text=message, fg_color="red", text_color="white", width=300, height=100).pack(padx=20, pady=20)
        ctk.CTkButton(error_box, text="OK", command=error_box.destroy, fg_color="red").pack(pady=10)