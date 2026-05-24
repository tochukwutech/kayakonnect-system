import customtkinter as ctk
from ui.components.sidebar import Sidebar

app = ctk.CTk()
app.geometry("1366x768")
ctk.set_appearance_mode("Light")

# ── Change this to preview different components ──
sidebar = Sidebar(
    app,
    nav_items=[
        ("Dashboard",    "⊞", lambda: print("Dashboard clicked")),
        ("Business Jobs","📦", lambda: print("Business Jobs clicked")),
        ("Profile",      "👤", lambda: print("Profile clicked")),
        ("Settings",     "⚙️", lambda: print("Settings clicked")),
    ],
    active_item = "Dashboard",
    user_name   = "David Offor",
    user_role   = "Customer",
    on_signout  = lambda: print("Sign out clicked")
)
sidebar.pack(side="left", fill="y")

app.mainloop()