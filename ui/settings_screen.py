"""
ui/settings_screen.py
Shared settings screen for both customers and couriers.
Sections: Change Password | Notifications | Courier availability toggle
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import hashlib

from ui.components.sidebar import Sidebar
from ui.components.header  import Header
from database import queries

NAVY    = "#1B2A6B"
ORANGE  = "#F5A623"
WHITE   = "#FFFFFF"
LIGHT   = "#F0F4FF"
CARD_BG = "#FFFFFF"
RED     = "#E74C3C"


def _hash_password(raw: str) -> str:
    """Simple SHA-256 hash. Replace with bcrypt in production."""
    return hashlib.sha256(raw.encode()).hexdigest()


class SettingsScreen(ctk.CTkFrame):
    """
    Settings screen shared by customers and couriers.

    Parameters
    ----------
    parent    : KayaKonnectApp root window
    user_id   : int
    user_type : 'customer' or 'courier'
    """

    def __init__(self, parent, user_id: int, user_type: str):
        super().__init__(parent, fg_color=LIGHT, corner_radius=0)

        self.parent    = parent
        self.user_id   = user_id
        self.user_type = user_type

        if user_type == "customer":
            self.user = queries.get_customer_by_id(user_id)
        else:
            self.user = queries.get_courier_by_id(user_id)

        self._build()

    # ══════════════════════════════════════════════════════════
    # BUILD
    # ══════════════════════════════════════════════════════════
    def _build(self):
        name = self.user.get("full_name", "User") if self.user else "User"
        role = "Customer" if self.user_type == "customer" else "Courier"

        nav_items = [
            ("← Dashboard", "📊",
             lambda: self.parent.show_customer_dashboard(self.user_id)
             if self.user_type == "customer"
             else self.parent.show_courier_dashboard(self.user_id)),
            ("Profile", "👤",
             lambda: self.parent.show_profile_screen(self.user_id, self.user_type))
        ]

        Sidebar(
            self,
            nav_items   = nav_items,
            active_item = "← Dashboard",
            user_name   = name,
            user_role   = role,
            on_signout  = self._sign_out
        ).pack(side="left", fill="y")

        right = ctk.CTkFrame(self, fg_color=LIGHT, corner_radius=0)
        right.pack(side="left", fill="both", expand=True)

        Header(
            right,
            greeting = "Settings",
            on_close = lambda: self.parent.destroy(),
            on_mini  = lambda: self.parent.iconify()
        ).pack(fill="x")

        scroll = ctk.CTkScrollableFrame(right, fg_color=LIGHT)
        scroll.pack(fill="both", expand=True, padx=30, pady=20)

        self._build_account_info(scroll, name, role)
        self._build_change_password(scroll)

        if self.user_type == "courier":
            self._build_availability_toggle(scroll)

        self._build_danger_zone(scroll)

    # ── Account info (read-only) ──────────────────────────────
    def _build_account_info(self, parent, name, role):
        card = self._section(parent, "Account Information")

        info_rows = [
            ("Name",  name),
            ("Email", self.user.get("email", "—") if self.user else "—"),
            ("Role",  role),
        ]
        for label, value in info_rows:
            row = ctk.CTkFrame(card, fg_color=LIGHT, corner_radius=8)
            row.pack(fill="x", padx=14, pady=4)
            ctk.CTkLabel(row, text=label,
                         font=ctk.CTkFont("Arial", 11),
                         text_color="gray", anchor="w", width=120).pack(side="left", padx=10, pady=8)
            ctk.CTkLabel(row, text=value,
                         font=ctk.CTkFont("Arial", 12, "bold"),
                         text_color=NAVY, anchor="w").pack(side="left")

        ctk.CTkButton(
            card, text="Edit Profile →",
            fg_color="transparent", text_color=ORANGE,
            font=ctk.CTkFont("Arial", 12),
            hover_color=LIGHT, anchor="w",
            command=lambda: self.parent.show_profile_screen(self.user_id, self.user_type)
        ).pack(anchor="w", padx=10, pady=(4, 10))

    # ── Change password ───────────────────────────────────────
    def _build_change_password(self, parent):
        card = self._section(parent, "Change Password")

        self._pw_fields = {}
        for label, key, placeholder in [
            ("Current Password",  "current",  "Enter current password"),
            ("New Password",      "new",      "Enter new password"),
            ("Confirm Password",  "confirm",  "Re-enter new password"),
        ]:
            ctk.CTkLabel(card, text=label,
                         font=ctk.CTkFont("Arial", 11),
                         text_color="gray", anchor="w").pack(
                fill="x", padx=14, pady=(6, 0))
            e = ctk.CTkEntry(card, placeholder_text=placeholder,
                             show="•", height=36)
            e.pack(fill="x", padx=14, pady=(2, 0))
            self._pw_fields[key] = e

        ctk.CTkButton(
            card, text="Update Password",
            fg_color=ORANGE, text_color=WHITE,
            font=ctk.CTkFont("Arial", 12, "bold"),
            height=38, corner_radius=8,
            command=self._change_password
        ).pack(fill="x", padx=14, pady=12)

    def _change_password(self):
        current = self._pw_fields["current"].get()
        new_pw  = self._pw_fields["new"].get()
        confirm = self._pw_fields["confirm"].get()

        if not current or not new_pw or not confirm:
            messagebox.showwarning("Missing Fields", "Please fill in all password fields.")
            return
        if new_pw != confirm:
            messagebox.showerror("Mismatch", "New passwords do not match.")
            return
        if len(new_pw) < 6:
            messagebox.showwarning("Too Short", "Password must be at least 6 characters.")
            return

        new_hash = _hash_password(new_pw)
        if self.user_type == "customer":
            queries.update_customer_password(self.user_id, new_hash)
        else:
            queries.update_courier_password(self.user_id, new_hash)

        messagebox.showinfo("Done", "Password updated successfully!")
        for f in self._pw_fields.values():
            f.delete(0, "end")

    # ── Courier availability toggle ───────────────────────────
    def _build_availability_toggle(self, parent):
        card = self._section(parent, "Availability")

        current = self.user.get("is_available", True) if self.user else True
        self._avail_var = tk.BooleanVar(value=current)

        row = ctk.CTkFrame(card, fg_color=LIGHT, corner_radius=8)
        row.pack(fill="x", padx=14, pady=8)

        ctk.CTkLabel(row, text="Available for Jobs",
                     font=ctk.CTkFont("Arial", 13),
                     text_color=NAVY).pack(side="left", padx=14, pady=10)

        ctk.CTkSwitch(
            row,
            text="",
            variable=self._avail_var,
            onvalue=True, offvalue=False,
            progress_color=ORANGE,
            command=self._toggle_availability
        ).pack(side="right", padx=14)

    def _toggle_availability(self):
        new_val = self._avail_var.get()
        queries.toggle_courier_availability(self.user_id, new_val)
        status = "available" if new_val else "unavailable"
        messagebox.showinfo("Availability Updated",
                            f"You are now marked as {status}.")

    # ── Danger zone ───────────────────────────────────────────
    def _build_danger_zone(self, parent):
        card = self._section(parent, "Sign Out")

        ctk.CTkButton(
            card, text="Sign Out",
            fg_color=RED, text_color=WHITE,
            font=ctk.CTkFont("Arial", 13, "bold"),
            height=40, corner_radius=8,
            command=self._sign_out
        ).pack(fill="x", padx=14, pady=14)

    def _sign_out(self):
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            self.parent.show_role_selection()

    # ── Helper ────────────────────────────────────────────────
    def _section(self, parent, title: str) -> ctk.CTkFrame:
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(wrapper, text=title,
                     font=ctk.CTkFont("Arial", 13, "bold"),
                     text_color=NAVY).pack(anchor="w", pady=(0, 6))
        card = ctk.CTkFrame(wrapper, fg_color=CARD_BG, corner_radius=12)
        card.pack(fill="x")
        return card
