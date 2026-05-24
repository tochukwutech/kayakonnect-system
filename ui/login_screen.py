import customtkinter as ctk
from PIL import Image
from database.db_connection import get_connection

NAVY   = "#1B2A6B"
ORANGE = "#F5A623"
WHITE  = "#FFFFFF"
LIGHT  = "#F0F4FF"


class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=LIGHT, corner_radius=0)
        self.parent = parent
        self._build()

    def _build(self):
        back_btn = ctk.CTkButton(
            self,
            text="←",
            font=ctk.CTkFont("Arial", 20),
            fg_color="transparent",
            text_color=NAVY,
            hover_color=LIGHT,
            width=40, height=40,
            command=lambda: self.parent.show_splash()
        )
        back_btn.place(x=20, y=20)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("ui/ui-elements/logokk.png"),
                dark_image=Image.open("ui/ui-elements/logokk.png"),
                size=(280, 90)
            )
            ctk.CTkLabel(container, image=logo_image,
                         text="").pack(pady=(0, 30))
        except Exception:
            ctk.CTkLabel(
                container,
                text="KayaKonnect",
                font=ctk.CTkFont("Arial", 28, "bold"),
                text_color=ORANGE
            ).pack(pady=(0, 30))

        ctk.CTkLabel(
            container,
            text="Login to your Account",
            font=ctk.CTkFont("Arial", 18, "bold"),
            text_color=NAVY
        ).pack(pady=(0, 24))

        ctk.CTkLabel(
            container,
            text="Email",
            font=ctk.CTkFont("Arial", 13),
            text_color=NAVY,
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        self.email_entry = ctk.CTkEntry(
            container,
            placeholder_text="Enter your email",
            width=480, height=50,
            font=ctk.CTkFont("Arial", 13),
            border_color="#D0D5DD",
            border_width=1,
            corner_radius=8
        )
        self.email_entry.pack(pady=(0, 16))

        ctk.CTkLabel(
            container,
            text="Password",
            font=ctk.CTkFont("Arial", 13),
            text_color=NAVY,
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        self.password_entry = ctk.CTkEntry(
            container,
            placeholder_text="Enter your password",
            width=480, height=50,
            font=ctk.CTkFont("Arial", 13),
            show="*",
            border_color="#D0D5DD",
            border_width=1,
            corner_radius=8
        )
        self.password_entry.pack(pady=(0, 8))

        self.error_label = ctk.CTkLabel(
            container, text="",
            font=ctk.CTkFont("Arial", 11),
            text_color="#E74C3C"
        )
        self.error_label.pack(pady=(0, 8))

        ctk.CTkButton(
            container,
            text="Login",
            fg_color=NAVY, text_color=WHITE,
            hover_color="#0f2538",
            font=ctk.CTkFont("Arial", 14, "bold"),
            width=480, height=50,
            corner_radius=8,
            command=self._login
        ).pack(pady=(0, 16))

        link_row = ctk.CTkFrame(container, fg_color="transparent")
        link_row.pack()

        ctk.CTkLabel(
            link_row,
            text="Dont have an account? ",
            font=ctk.CTkFont("Arial", 12),
            text_color=NAVY
        ).pack(side="left")

        signup_link = ctk.CTkLabel(
            link_row,
            text="Sign Up",
            font=ctk.CTkFont("Arial", 12, "bold"),
            text_color=ORANGE,
            cursor="hand2"
        )
        signup_link.pack(side="left")
        signup_link.bind("<Button-1>", lambda e: self.parent.show_customer_register())

    def _login(self):
        email    = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            self._show_error("Please fill in all fields.")
            return

        try:
            conn = get_connection()
            cur  = conn.cursor()
            cur.execute("SELECT id FROM customers WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                self._show_error("")
                self.parent.show_customer_dashboard(customer_id=user["id"])
            else:
                self._show_error("No customer account found with that email.")
        except Exception as e:
            self._show_error(f"Error: {str(e)}")

    def _show_error(self, message: str):
        self.error_label.configure(text=message)
