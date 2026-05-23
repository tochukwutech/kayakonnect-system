"""
ui/signup_screen.py
PLACEHOLDER — Replace with teammate's actual customer register file.
"""

import customtkinter as ctk
from tkinter import messagebox
import hashlib
from database.db_connection import get_connection

NAVY   = "#1B2A6B"
ORANGE = "#F5A623"
WHITE  = "#FFFFFF"
LIGHT  = "#F0F4FF"


class SignupScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=LIGHT)
        self.parent = parent

        card = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=14, width=420, height=520)
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
            text="Create your Account",
            font=ctk.CTkFont("Arial", 13),
            text_color=NAVY
        ).pack(pady=(0, 16))

        # ── Fields defined individually (avoids loop binding issue) ──
        self.name_entry = ctk.CTkEntry(card, placeholder_text="Full Name",
                                       width=320, height=36)
        self.name_entry.pack(pady=4)

        self.email_entry = ctk.CTkEntry(card, placeholder_text="Email address",
                                        width=320, height=36)
        self.email_entry.pack(pady=4)

        self.phone_entry = ctk.CTkEntry(card, placeholder_text="Phone number",
                                        width=320, height=36)
        self.phone_entry.pack(pady=4)

        self.address_entry = ctk.CTkEntry(card, placeholder_text="Address",
                                          width=320, height=36)
        self.address_entry.pack(pady=4)

        self.pw_entry = ctk.CTkEntry(card, placeholder_text="Password",
                                     show="•", width=320, height=36)
        self.pw_entry.pack(pady=4)

        self.pw2_entry = ctk.CTkEntry(card, placeholder_text="Confirm Password",
                                      show="•", width=320, height=36)
        self.pw2_entry.pack(pady=4)

        ctk.CTkButton(
            card,
            text="Sign Up",
            fg_color=ORANGE, text_color=WHITE,
            font=ctk.CTkFont("Arial", 13, "bold"),
            width=320, height=40, corner_radius=8,
            command=self._submit
        ).pack(pady=(14, 6))

        ctk.CTkButton(
            card,
            text="Already have an account? Login",
            fg_color="transparent", text_color=NAVY,
            hover_color=LIGHT, font=ctk.CTkFont("Arial", 11),
            command=lambda: parent.show_customer_login()
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            card,
            text="[ PLACEHOLDER — replace with teammate's signup_screen.py ]",
            font=ctk.CTkFont("Arial", 9),
            text_color="gray"
        ).pack(pady=(0, 10))

    def _submit(self):
        name  = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        addr  = self.address_entry.get().strip()
        pw    = self.pw_entry.get()
        pw2   = self.pw2_entry.get()

        if not all([name, email, pw, pw2]):
            messagebox.showwarning("Missing Fields", "Please fill in all required fields.")
            return
        if pw != pw2:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return

        pw_hash = hashlib.sha256(pw.encode()).hexdigest()

        try:
            conn = get_connection()
            cur  = conn.cursor()
            cur.execute("""
                INSERT INTO customers (full_name, email, phone, address, password_hash)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, phone, addr, pw_hash))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", "Account created! Please login.")
            self.parent.show_customer_login()
        except Exception as e:
            messagebox.showerror("Error", str(e))
