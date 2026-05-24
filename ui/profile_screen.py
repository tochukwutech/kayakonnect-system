import customtkinter as ctk
from tkinter import messagebox

from ui.components.sidebar import Sidebar
from ui.components.header  import Header
from database import queries

NAVY    = "#1B2A6B"
ORANGE  = "#F5A623"
WHITE   = "#FFFFFF"
LIGHT   = "#F0F4FF"
CARD_BG = "#FFFFFF"


class ProfileScreen(ctk.CTkFrame):
    

    def __init__(self, parent, user_id: int, user_type: str):
        super().__init__(parent, fg_color=LIGHT, corner_radius=0)

        self.parent    = parent
        self.user_id   = user_id
        self.user_type = user_type

        # Load data
        if user_type == "customer":
            self.user = queries.get_customer_by_id(user_id)
        else:
            self.user = queries.get_courier_by_id(user_id)

        self._build()
        
    def _build(self):
        name = self.user.get("full_name", "User") if self.user else "User"
        role = "Customer" if self.user_type == "customer" else "Courier"

        # Back button
        nav_items = [
            ("← Dashboard", "📊",
             lambda: self.parent.show_customer_dashboard(self.user_id)
             if self.user_type == "customer"
             else self.parent.show_courier_dashboard(self.user_id))
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
            greeting    = "My Profile",
            on_close    = lambda: self.parent.destroy(),
            on_mini     = lambda: self.parent.iconify()
        ).pack(fill="x")


        outer = ctk.CTkFrame(right, fg_color=LIGHT)
        outer.pack(fill="both", expand=True, padx=40, pady=30)

        card = ctk.CTkFrame(outer, fg_color=CARD_BG, corner_radius=14)
        card.pack(fill="both", expand=True)


        avatar_frame = ctk.CTkFrame(card, fg_color=NAVY,
                                    width=80, height=80, corner_radius=40)
        avatar_frame.pack(pady=(30, 6))
        avatar_frame.pack_propagate(False)
        ctk.CTkLabel(avatar_frame,
                     text=name[0].upper(),
                     font=ctk.CTkFont("Arial", 32, "bold"),
                     text_color=WHITE).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(card, text=name,
                     font=ctk.CTkFont("Arial", 18, "bold"),
                     text_color=NAVY).pack()
        ctk.CTkLabel(card, text=role,
                     font=ctk.CTkFont("Arial", 12),
                     text_color=ORANGE).pack(pady=(0, 16))


        form = ctk.CTkFrame(card, fg_color="transparent")
        form.pack(fill="x", padx=40, pady=10)

        self._fields = {}

        field_defs = [
            ("Full Name",  "full_name",    name),
            ("Email",      "email",        self.user.get("email", "") if self.user else ""),
            ("Phone",      "phone",        self.user.get("phone", "") if self.user else ""),
            ("Address",    "address",      self.user.get("address", "") if self.user else ""),
        ]
        if self.user_type == "courier":
            field_defs.append(
                ("Vehicle Type", "vehicle_type",
                 self.user.get("vehicle_type", "") if self.user else "")
            )

        for label, key, default in field_defs:
            ctk.CTkLabel(form, text=label,
                         font=ctk.CTkFont("Arial", 12),
                         text_color="gray", anchor="w").pack(fill="x", pady=(8, 0))


            if key == "email":
                e = ctk.CTkEntry(form, height=36, state="disabled")
                e.pack(fill="x")
                e.configure(state="normal")
                e.insert(0, default)
                e.configure(state="disabled")
            else:
                e = ctk.CTkEntry(form, height=36)
                e.pack(fill="x")
                if default:
                    e.insert(0, default)
                self._fields[key] = e


        ctk.CTkButton(
            card, text="Save Changes",
            fg_color=ORANGE, text_color=WHITE,
            font=ctk.CTkFont("Arial", 13, "bold"),
            height=40, corner_radius=10,
            command=self._save
        ).pack(pady=(20, 30), padx=40, fill="x")


    def _save(self):
        full_name = self._fields.get("full_name", None)
        phone     = self._fields.get("phone", None)
        address   = self._fields.get("address", None)

        full_name_val = full_name.get().strip() if full_name else ""
        phone_val     = phone.get().strip()     if phone     else ""
        address_val   = address.get().strip()   if address   else ""

        if not full_name_val:
            messagebox.showwarning("Required", "Full name cannot be empty.")
            return

        if self.user_type == "customer":
            queries.update_customer_profile(
                self.user_id, full_name_val, phone_val, address_val
            )
        else:
            vehicle = self._fields.get("vehicle_type", None)
            vehicle_val = vehicle.get().strip() if vehicle else ""
            queries.update_courier_profile(
                self.user_id, full_name_val, phone_val, address_val, vehicle_val
            )

        messagebox.showinfo("Saved", "Your profile has been updated!")

    def _sign_out(self):
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            self.parent.show_role_selection()
