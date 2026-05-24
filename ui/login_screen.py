"""
ui/login_screen.py
PLACEHOLDER — Replace with teammate's actual customer login file.
"""

import customtkinter as ctk
from tkinter import messagebox
from database.db_connection import get_connection

NAVY   = "#1B2A6B"
ORANGE = "#F5A623"
WHITE  = "#FFFFFF"
LIGHT  = "#F0F4FF"


class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=LIGHT, corner_radius=0)
        self.parent = parent

        # Centred card
        card = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=14, width=400, height=400)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text="KayaKonnect",
            font=ctk.CTkFont("Arial", 22, "bold"),
            text_color=ORANGE
        ).pack(pady=(30, 2))

        ctk.CTkLabel(
            card,
            text="Login to your Account",
            font=ctk.CTkFont("Arial", 13),
            text_color=NAVY
        ).pack(pady=(0, 20))

        # Email
        self.email_entry = ctk.CTkEntry(card, placeholder_text="Email address",
                                        width=300, height=38)
        self.email_entry.pack(pady=6)

        # Password
        self.pw_entry = ctk.CTkEntry(card, placeholder_text="Password",
                                     show="•", width=300, height=38)
        self.pw_entry.pack(pady=6)

        # Login button
        ctk.CTkButton(
            card,
            text="Login",
            fg_color=NAVY, text_color=WHITE,
            font=ctk.CTkFont("Arial", 13, "bold"),
            width=300, height=40, corner_radius=8,
            command=self._login
        ).pack(pady=(16, 6))

        # Register link
        ctk.CTkButton(
            card,
            text="Don't have an account? Register",
            fg_color="transparent", text_color=ORANGE,
            hover_color=LIGHT, font=ctk.CTkFont("Arial", 11),
            command=lambda: parent.show_customer_register()
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            card,
            text="[ PLACEHOLDER — replace with teammate's login_screen.py ]",
            font=ctk.CTkFont("Arial", 9),
            text_color="gray"
        ).pack(pady=(0, 10))

    def _login(self):
        email = self.email_entry.get().strip()
        pw    = self.pw_entry.get().strip()

        if not email or not pw:
            messagebox.showwarning("Missing Fields", "Please enter email and password.")
            return

        try:
            conn = get_connection()
            cur  = conn.cursor()
            cur.execute("SELECT id FROM customers WHERE email = %s", (email,))
            user = cur.fetchone()
            cur.close()
            conn.close()

            if user:
                self.parent.show_customer_dashboard(customer_id=user["id"])
            else:
                messagebox.showerror("Login Failed", "No customer found with that email.")
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
