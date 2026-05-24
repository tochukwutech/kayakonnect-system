"""
ui/splash_screen.py
PLACEHOLDER — Replace with teammate's actual splash screen file.
"""

import customtkinter as ctk

NAVY   = "#1B2A6B"
ORANGE = "#F5A623"
WHITE  = "#FFFFFF"


class SplashScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=NAVY, corner_radius=0)
        self.parent = parent

        ctk.CTkLabel(
            self,
            text="KayaKonnect",
            font=ctk.CTkFont("Arial", 36, "bold"),
            text_color=ORANGE
        ).pack(expand=True, pady=(80, 10))

        ctk.CTkLabel(
            self,
            text="A market courier system connecting customers to available Kayas",
            font=ctk.CTkFont("Arial", 13),
            text_color=WHITE
        ).pack(pady=(0, 40))

        ctk.CTkButton(
            self,
            text="Get Connected as a Customer",
            fg_color=ORANGE, text_color=WHITE,
            font=ctk.CTkFont("Arial", 13, "bold"),
            width=260, height=42, corner_radius=10,
            command=lambda: parent.show_customer_login()
        ).pack(pady=8)

        ctk.CTkButton(
            self,
            text="Register as a Kaya (Courier)",
            fg_color="transparent", text_color=ORANGE,
            border_color=ORANGE, border_width=2,
            font=ctk.CTkFont("Arial", 13, "bold"),
            width=260, height=42, corner_radius=10,
            command=lambda: parent.show_courier_login()
        ).pack(pady=8)

        ctk.CTkLabel(
            self,
            text="[ PLACEHOLDER — replace with teammate's splash_screen.py ]",
            font=ctk.CTkFont("Arial", 10),
            text_color="gray"
        ).pack(pady=(40, 0))
