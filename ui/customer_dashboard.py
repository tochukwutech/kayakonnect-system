import customtkinter as ctk
from tkinter import messagebox

from ui.components.sidebar       import Sidebar
from ui.components.header        import Header
from ui.components.data_table    import DataTable
from ui.create_request_screen    import CreateRequestScreen
from database                    import queries

NAVY    = "#1B2A6B"
ORANGE  = "#F5A623"
ORANGE_DK = "#E09010"
WHITE   = "#FFFFFF"
LIGHT   = "#F0F4FF"
CARD_BG = "#FFFFFF"


class CustomerDashboard(ctk.CTkFrame):

    def __init__(self, parent, customer_id: int):
        super().__init__(parent, fg_color=LIGHT, corner_radius=0)

        self.parent      = parent
        self.customer_id = customer_id
        self.customer    = queries.get_customer_by_id(customer_id)

        self._build_layout()
        self._show_page("Dashboard")

    def _build_layout(self):
        name = self.customer.get("full_name", "Customer") if self.customer else "Customer"

        nav_items = [
            ("Dashboard",      "📊", lambda: self._show_page("Dashboard")),
            ("Create Request", "⊕",  lambda: self._show_page("Create Request")),
            ("Business Jobs",  "📦", lambda: self._show_page("Business Jobs")),
            ("Profile",        "👤", lambda: self.parent.show_profile_screen(self.customer_id, "customer")),
            ("Settings",       "⚙️", lambda: self.parent.show_settings_screen(self.customer_id, "customer")),
        ]
        self.sidebar = Sidebar(
            self,
            nav_items   = nav_items,
            active_item = "Dashboard",
            user_name   = name,
            user_role   = "Customer",
            on_signout  = self._sign_out
        )
        self.sidebar.pack(side="left", fill="y")

        self.right = ctk.CTkFrame(self, fg_color=LIGHT, corner_radius=0)
        self.right.pack(side="left", fill="both", expand=True)

        import time
        hour   = int(time.strftime("%H"))
        period = "morning" if hour < 12 else ("afternoon" if hour < 17 else "evening")
        Header(
            self.right,
            greeting = f"Good {period}, {name.split()[0]} 👋",
            on_close = lambda: self.parent.destroy(),
            on_mini  = lambda: self.parent.iconify()
        ).pack(fill="x")

        self.content = ctk.CTkFrame(self.right, fg_color=LIGHT, corner_radius=0)
        self.content.pack(fill="both", expand=True, padx=16, pady=12)

    def _show_page(self, page_name):
        self.sidebar.set_active(page_name)
        for w in self.content.winfo_children():
            w.destroy()

        if page_name == "Dashboard":
            self._build_dashboard_page()
        elif page_name == "Create Request":
            self._build_create_request_page()
        elif page_name == "Business Jobs":
            self._build_business_jobs_page()


    def _build_dashboard_page(self):
        left = ctk.CTkFrame(self.content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = ctk.CTkFrame(self.content, fg_color="transparent", width=300)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self._build_request_history(left)
        self._build_active_requests(left)
        self._build_quick_request_hint(right)


    def _build_request_history(self, parent):
        card = self._card(parent, "Request History")
        rows = queries.get_customer_request_history(self.customer_id)
        cols = ["Request ID", "Date", "Price (₦)", "Status", "From", "To"]
        data = [
            (
                r["request_id"],
                str(r["date_created"])[:10],
                f"₦{r['recommended_price']:,.0f}",
                r["status"],
                r["pickup_location"],
                r["destination"]
            )
            for r in rows
        ]
        if data:
            DataTable(card, columns=cols, rows=data).pack(fill="both", expand=True)
        else:
            ctk.CTkLabel(card, text="No request history yet.",
                         text_color="gray").pack(pady=20)


    def _build_active_requests(self, parent):
        card = self._card(parent, "Active Requests")

        toggle_row = ctk.CTkFrame(card, fg_color="transparent")
        toggle_row.pack(fill="x", padx=10, pady=(8, 4))

        self._active_filter_buttons = {}
        for label in ["All", "Pending", "Accepted", "In Progress"]:
            btn = ctk.CTkButton(
                toggle_row, text=label,
                font=ctk.CTkFont("Arial", 11),
                fg_color=ORANGE if label == "All" else LIGHT,
                text_color=WHITE if label == "All" else NAVY,
                width=80, height=28, corner_radius=14,
                command=lambda l=label: self._filter_active(l)
            )
            btn.pack(side="left", padx=3)
            self._active_filter_buttons[label] = btn

        self._active_table_frame = ctk.CTkFrame(card, fg_color="transparent")
        self._active_table_frame.pack(fill="both", expand=True, padx=4, pady=4)
        self._render_active_table(None)

    def _filter_active(self, label):
        for lbl, btn in self._active_filter_buttons.items():
            btn.configure(
                fg_color=ORANGE if lbl == label else LIGHT,
                text_color=WHITE if lbl == label else NAVY
            )
        status_map = {
            "All": None, "Pending": "pending",
            "Accepted": "accepted", "In Progress": "in_progress"
        }
        self._render_active_table(status_map.get(label))

    def _render_active_table(self, filter_status):
        for w in self._active_table_frame.winfo_children():
            w.destroy()

        rows = queries.get_customer_active_requests(self.customer_id)
        if filter_status:
            rows = [r for r in rows if r["status"] == filter_status]

        cols = ["Request ID", "Courier", "Price (₦)", "Status", "From", "To"]
        data = [
            (
                r["request_id"],
                r.get("courier_name") or "Unassigned",
                f"₦{r['recommended_price']:,.0f}",
                r["status"],
                r["pickup_location"],
                r["destination"]
            )
            for r in rows
        ]
        if data:
            DataTable(self._active_table_frame,
                      columns=cols, rows=data).pack(fill="both", expand=True)
        else:
            ctk.CTkLabel(self._active_table_frame,
                         text="No active requests.",
                         text_color="gray").pack(pady=12)


    def _build_quick_request_hint(self, parent):
        card = self._card(parent, "Need a Courier?")

        ctk.CTkLabel(
            card,
            text="Create a new delivery\nrequest quickly.",
            font=ctk.CTkFont("Arial", 12),
            text_color=NAVY, justify="center"
        ).pack(pady=(20, 16))

        ctk.CTkButton(
            card,
            text="⊕  Create Request",
            fg_color=ORANGE, text_color=WHITE,
            hover_color=ORANGE_DK,
            font=ctk.CTkFont("Arial", 13, "bold"),
            height=42, corner_radius=10,
            command=lambda: self._show_page("Create Request")
        ).pack(fill="x", padx=16, pady=(0, 20))


    def _build_create_request_page(self):
        CreateRequestScreen(
            self.content,
            customer_id = self.customer_id,
            on_done     = lambda: self._show_page("Dashboard")
        ).pack(fill="both", expand=True)


    def _build_business_jobs_page(self):
        card = self._card(self.content, "All Delivery Requests")
        rows = queries.get_customer_request_history(self.customer_id)
        cols = ["Request ID", "Date", "From", "To", "Size", "Urgency", "Price (₦)", "Status"]
        data = [
            (
                r["request_id"],
                str(r["date_created"])[:10],
                r["pickup_location"],
                r["destination"],
                r["lead_size"].capitalize(),
                r["urgency_level"].capitalize(),
                f"₦{r['recommended_price']:,.0f}",
                r["status"]
            )
            for r in rows
        ]
        if data:
            DataTable(card, columns=cols, rows=data).pack(fill="both", expand=True)
        else:
            ctk.CTkLabel(card, text="No requests found.",
                         text_color="gray").pack(pady=20)


    def _sign_out(self):
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            self.parent.show_role_selection()


    def _card(self, parent, title: str) -> ctk.CTkFrame:
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, pady=(0, 10))
        ctk.CTkLabel(wrapper, text=title,
                     font=ctk.CTkFont("Arial", 13, "bold"),
                     text_color=NAVY).pack(anchor="w", pady=(0, 4))
        card = ctk.CTkFrame(wrapper, fg_color=CARD_BG, corner_radius=10)
        card.pack(fill="both", expand=True)
        return card
