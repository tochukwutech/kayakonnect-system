import customtkinter as ctk
from PIL import Image

NAVY       = "#1B2A6B"
ORANGE     = "#F5A623"
WHITE      = "#FFFFFF"
LIGHT_GRAY = "#F0F0F0"
HOVER_BG   = "#243580"


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, nav_items: list, active_item: str,
                 user_name: str, user_role: str, on_signout):
        super().__init__(parent, fg_color=NAVY, width=200, corner_radius=0)
        self.pack_propagate(False)

        self.nav_items   = nav_items
        self.active_item = active_item
        self.on_signout  = on_signout
        self._buttons    = {}

        self._build_logo()
        self._build_user_info(user_name, user_role)
        self._build_nav()
        self._build_signout()

    def _build_logo(self):
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=16, pady=(20, 8))

        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("ui/ui-elements/logokk.png"),
                dark_image=Image.open("ui/ui-elements/logokk.png"),
                size=(160, 60)
            )
            ctk.CTkLabel(
                logo_frame,
                image=logo_image,
                text="",
                fg_color=WHITE,
                corner_radius=8
            ).pack(anchor="w")
        except Exception:
            print("Logo image not found, using text fallback.")
            ctk.CTkLabel(
                logo_frame,
                text="KayaKonnect",
                font=ctk.CTkFont("Arial", 20, "bold"),
                text_color=ORANGE
            ).pack(anchor="w")

    def _build_user_info(self, user_name, user_role):
        ctk.CTkFrame(self, fg_color=HOVER_BG, height=1).pack(fill="x", padx=12)

        info = ctk.CTkFrame(self, fg_color="transparent")
        info.pack(fill="x", padx=16, pady=10)

        ctk.CTkLabel(
            info,
            text=user_name,
            font=ctk.CTkFont("Arial", 13, "bold"),
            text_color=WHITE,
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            info,
            text=user_role,
            font=ctk.CTkFont("Arial", 11),
            text_color=ORANGE,
            anchor="w"
        ).pack(fill="x")

        ctk.CTkFrame(self, fg_color=HOVER_BG, height=1).pack(fill="x", padx=12)

    def _build_nav(self):
        nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, pady=10)

        for (label, icon, callback) in self.nav_items:
            is_active = (label == self.active_item)
            btn = ctk.CTkButton(
                nav_frame,
                text=f"  {icon}  {label}",
                font=ctk.CTkFont("Arial", 13),
                fg_color=ORANGE if is_active else "transparent",
                text_color=WHITE,
                hover_color=HOVER_BG,
                anchor="w",
                height=42,
                corner_radius=8,
                command=callback
            )
            btn.pack(fill="x", padx=12, pady=3)
            self._buttons[label] = btn

    def _build_signout(self):
        ctk.CTkFrame(self, fg_color=HOVER_BG, height=1).pack(fill="x", padx=12)
        ctk.CTkButton(
            self,
            text="  ⎋  Sign Out",
            font=ctk.CTkFont("Arial", 12),
            fg_color="transparent",
            text_color=WHITE,
            hover_color="#8B0000",
            anchor="w",
            height=40,
            corner_radius=8,
            command=self.on_signout
        ).pack(fill="x", padx=12, pady=12)

    def set_active(self, label: str):
        for lbl, btn in self._buttons.items():
            btn.configure(fg_color=ORANGE if lbl == label else "transparent")
        self.active_item = label