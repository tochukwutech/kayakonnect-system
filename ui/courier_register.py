
import customtkinter as ctk
from PIL import Image
import hashlib
from database.db_connection import get_connection

NAVY   = "#1B2A6B"
ORANGE = "#F5A623"
WHITE  = "#FFFFFF"
LIGHT  = "#F0F4FF"


class CourierRegister(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=WHITE)
        self.parent = parent
        self._build()

    def _build(self):
        card = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=14, width=420)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # ── Logo ──────────────────────────────────────────────
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("ui/ui-elements/logokk.png"),
                dark_image=Image.open("ui/ui-elements/logokk.png"),
                size=(160, 50)
            )
            ctk.CTkLabel(card, image=logo_image, text="").pack(pady=(30, 4))
        except Exception:
            ctk.CTkLabel(
                card,
                text="KayaKonnect",
                font=ctk.CTkFont("Segoe UI", 28, "bold"),
                text_color=ORANGE
            ).pack(pady=(30, 4))

        # ── Subtitle ──────────────────────────────────────────
        ctk.CTkLabel(
            card,
            text="Register as a Kaya!",
            font=ctk.CTkFont("Segoe UI", 14),
            text_color="#666"
        ).pack(pady=(0, 20))

        # ── Fields ────────────────────────────────────────────
        self.username_entry = ctk.CTkEntry(
            card, placeholder_text="Enter your username",
            width=300, height=45,
            font=ctk.CTkFont("Segoe UI", 12),
            border_color="#ddd", border_width=1
        )
        self.username_entry.pack(pady=(0, 12))

        self.email_entry = ctk.CTkEntry(
            card, placeholder_text="Enter your email",
            width=300, height=45,
            font=ctk.CTkFont("Segoe UI", 12),
            border_color="#ddd", border_width=1
        )
        self.email_entry.pack(pady=(0, 12))

        self.phone_entry = ctk.CTkEntry(
            card, placeholder_text="Enter your phone number",
            width=300, height=45,
            font=ctk.CTkFont("Segoe UI", 12),
            border_color="#ddd", border_width=1
        )
        self.phone_entry.pack(pady=(0, 12))

        self.vehicle_entry = ctk.CTkEntry(
            card, placeholder_text="Vehicle type (e.g. Motorcycle)",
            width=300, height=45,
            font=ctk.CTkFont("Segoe UI", 12),
            border_color="#ddd", border_width=1
        )
        self.vehicle_entry.pack(pady=(0, 12))

        self.password_entry = ctk.CTkEntry(
            card, placeholder_text="Enter your password",
            width=300, height=45,
            font=ctk.CTkFont("Segoe UI", 12),
            show="*",
            border_color="#ddd", border_width=1
        )
        self.password_entry.pack(pady=(0, 12))

        self.confirm_password_entry = ctk.CTkEntry(
            card, placeholder_text="Re-enter your password to confirm",
            width=300, height=45,
            font=ctk.CTkFont("Segoe UI", 12),
            show="*",
            border_color="#ddd", border_width=1
        )
        self.confirm_password_entry.pack(pady=(0, 8))

        # ── Error label ───────────────────────────────────────
        self.error_label = ctk.CTkLabel(
            card, text="",
            font=ctk.CTkFont("Segoe UI", 10),
            text_color="#e74c3c"
        )
        self.error_label.pack(pady=(0, 8))

        # ── Sign Up button ────────────────────────────────────
        ctk.CTkButton(
            card,
            text="Sign Up",
            width=300, height=45,
            font=ctk.CTkFont("Segoe UI", 14, "bold"),
            fg_color=NAVY, hover_color="#0f2538",
            command=self._submit
        ).pack(pady=(0, 16))

        # ── Login link ────────────────────────────────────────
        link_row = ctk.CTkFrame(card, fg_color=WHITE)
        link_row.pack(pady=(0, 30))

        ctk.CTkLabel(
            link_row,
            text="Already have an account? ",
            font=ctk.CTkFont("Segoe UI", 11),
            text_color="#666"
        ).pack(side="left")

        login_link = ctk.CTkLabel(
            link_row,
            text="Log in",
            font=ctk.CTkFont("Segoe UI", 11, "bold"),
            text_color=ORANGE,
            cursor="hand2"
        )
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.parent.show_courier_login())

    # ── Registration logic ────────────────────────────────────
    def _submit(self):
        username = self.username_entry.get().strip()
        email    = self.email_entry.get().strip()
        phone    = self.phone_entry.get().strip()
        vehicle  = self.vehicle_entry.get().strip()
        pw       = self.password_entry.get()
        pw2      = self.confirm_password_entry.get()

        if not all([username, email, pw, pw2]):
            self._show_error("Please fill in all fields.")
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
                INSERT INTO couriers
                    (full_name, email, phone, vehicle_type, password_hash)
                VALUES (%s, %s, %s, %s, %s)
            """, (username, email, phone, vehicle, pw_hash))
            conn.commit()
            cur.close()
            conn.close()
            self._show_error("")
            from tkinter import messagebox
            messagebox.showinfo("Success",
                                "Courier account created! Please login.")
            self.parent.show_courier_login()
        except Exception as e:
            self._show_error(f"Error: {str(e)}")

    def _show_error(self, message: str):
        self.error_label.configure(text=message)
