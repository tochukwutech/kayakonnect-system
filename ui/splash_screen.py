import customtkinter as ctk
from PIL import Image

NAVY   = "#1B2A6B"
ORANGE = "#F5A623"
WHITE  = "#FFFFFF"
LIGHT  = "#F0F4FF"


class SplashScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=WHITE, corner_radius=0)
        self.parent = parent
        self._build()

    def _build(self):
        try:
            collage = ctk.CTkImage(
                light_image=Image.open("ui/ui-elements/splash-collage.png"),
                dark_image=Image.open("ui/ui-elements/splash-collage.png"),
                size=(680, 300)
            )
            ctk.CTkLabel(self, image=collage, text="").pack(pady=(40, 20))
        except Exception:
            ctk.CTkFrame(self, fg_color=LIGHT, width=680, height=300,
                         corner_radius=20).pack(pady=(40, 20))


        ctk.CTkLabel(
            self,
            text="Introducing...",
            font=ctk.CTkFont("Helvetica", 28, "bold"),
            text_color=ORANGE
        ).pack(pady=(0, 8))


        ctk.CTkLabel(
            self,
            text="a market courier system designed to connect customers\nto available kayas!",
            font=ctk.CTkFont("Helvetica", 14),
            text_color=NAVY,
            justify="center"
        ).pack(pady=(0, 4))


        welcome_frame = ctk.CTkFrame(self, fg_color="transparent")
        welcome_frame.pack(pady=(0, 30))

        ctk.CTkLabel(
            welcome_frame,
            text="Welcome to... ",
            font=ctk.CTkFont("Helvetica", 16, "bold"),
            text_color=NAVY
        ).pack(side="left")

        ctk.CTkLabel(
            welcome_frame,
            text="Kaya",
            font=ctk.CTkFont("Helvetica", 16, "bold"),
            text_color=NAVY
        ).pack(side="left")

        ctk.CTkLabel(
            welcome_frame,
            text="Konnect",
            font=ctk.CTkFont("Helvetica", 16, "bold"),
            text_color=ORANGE
        ).pack(side="left")

        ctk.CTkLabel(
            welcome_frame,
            text="!",
            font=ctk.CTkFont("Helvetica", 16, "bold"),
            text_color=NAVY
        ).pack(side="left")


        ctk.CTkButton(
            self,
            text="Get Started as a Customer",
            fg_color=ORANGE, text_color=WHITE,
            hover_color="#D4891A",
            font=ctk.CTkFont("Helvetica", 14, "bold"),
            width=340, height=48, corner_radius=10,
            command=lambda: self.parent.show_customer_login()
        ).pack(pady=(0, 12))

        ctk.CTkButton(
            self,
            text="Register as a Kaya",
            fg_color=WHITE, text_color=NAVY,
            hover_color=LIGHT,
            border_color=NAVY, border_width=2,
            font=ctk.CTkFont("Helvetica", 14, "bold"),
            width=340, height=48, corner_radius=10,
            command=lambda: self.parent.show_courier_login()
        ).pack(pady=(0, 40))