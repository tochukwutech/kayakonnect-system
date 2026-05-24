import customtkinter as ctk
from PIL import Image
import hashlib
from database.db_connection import get_connection

NAVY   = "#1B2A6B"
ORANGE = "#F5A623"
WHITE  = "#FFFFFF"
LIGHT  = "#F0F4FF"


class SignupScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=LIGHT, corner_radius=0)
        self.parent = parent
        self._build()

    def _build(self):
        ctk.CTkButton(
            self, text="←",
            font=ctk.CTkFont("Arial", 20),
            fg_color="transparent", text_color=NAVY,
            hover_color=LIGHT, width=40, height=40,
            command=lambda: self.parent.show_customer_login()
        ).place(x=20, y=20)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("ui/ui-elements/logokk.png"),
                dark_image=Image.open("ui/ui-elements/logokk.png"),
                size=(280, 90)
            )
            ctk.CTkLabel(container, image=logo_image,
                         text="").pack(pady=(0, 20))
        except Exception:
            ctk.CTkLabel(
                container,
                text="KayaKonnect",
                font=ctk.CTkFont("Arial", 28, "bold"),
                text_color=ORANGE
            ).pack(pady=(0, 20))

        ctk.CTkLabel(
            container,
            text="Create your Account",
            font=ctk.CTkFont("Arial", 18, "bold"),
            text_color=NAVY
        ).pack(pady=(0, 20))

        self.name_entry     = self._field(container, "Full Name",        "Enter your full name")
        self.email_entry    = self._field(container, "Email",            "Enter your email")
        self.phone_entry    = self._field(container, "Phone Number",     "Enter your phone number")
        self.address_entry  = self._field(container, "Address",          "Enter your address")
        self.pw_entry       = self._field(container, "Password",         "Enter your password",        secret=True)
        self.pw2_entry      = self._field(container, "Confirm Password", "Re-enter your password to confirm it", secret=True)

        self.error_label = ctk.CTkLabel(
            container, text="",
            font=ctk.CTkFont("Arial", 11),
            text_color="#E74C3C"
        )
        self.error_label.pack(pady=(4, 0))

        ctk.CTkButton(
            container,
            text="Sign Up",
            fg_color=NAVY, text_color=WHITE,
            hover_color="#0f2538",
            font=ctk.CTkFont("Arial", 14, "bold"),
            width=480, height=50,
            corner_radius=8,
            command=self._submit
        ).pack(pady=(12, 12))

        link_row = ctk.CTkFrame(container, fg_color="transparent")
        link_row.pack()

        ctk.CTkLabel(
            link_row,
            text="Already have an account? ",
            font=ctk.CTkFont("Arial", 12),
            text_color=NAVY
        ).pack(side="left")

        login_link = ctk.CTkLabel(
            link_row,
            text="Log In",
            font=ctk.CTkFont("Arial", 12, "bold"),
            text_color=ORANGE,
            cursor="hand2"
        )
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.parent.show_customer_login())

    def _field(self, parent, label, placeholder, secret=False):
        ctk.CTkLabel(
            parent, text=label,
            font=ctk.CTkFont("Arial", 13),
            text_color=NAVY, anchor="w"
        ).pack(fill="x", pady=(8, 2))

        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            width=480, height=46,
            font=ctk.CTkFont("Arial", 13),
            border_color="#D0D5DD",
            border_width=1,
            corner_radius=8,
            show="*" if secret else ""
        )
        entry.pack()
        return entry

    def _submit(self):
        name    = self.name_entry.get().strip()
        email   = self.email_entry.get().strip()
        phone   = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        pw      = self.pw_entry.get()
        pw2     = self.pw2_entry.get()

        if not all([name, email, pw, pw2]):
            self._show_error("Please fill in all required fields.")
            return
        if pw != pw2:
            self._show_error("Passwords do not match.")
            return
        if len(pw) < 6:
            self._show_error("Password must be at least 6 characters.")
            return

        pw_hash = hashlib.sha256(pw.encode()).hexdigest()

        try:
            conn = get_connection()
            cur  = conn.cursor()
            cur.execute("""
                INSERT INTO customers (full_name, email, phone, address, password_hash)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, phone, address, pw_hash))
            conn.commit()
            cur.close()
            conn.close()
            from tkinter import messagebox
            messagebox.showinfo("Success", "Account created! Please login.")
            self.parent.show_customer_login()
        except Exception as e:
            self._show_error(f"Error: {str(e)}")

    def _show_error(self, message: str):
        self.error_label.configure(text=message)