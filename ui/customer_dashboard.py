import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from ui.components.sidebar    import Sidebar
from ui.components.header     import Header
from ui.components.data_table import DataTable
from database                 import queries
from services.pricing_engine import PricingEngine

NAVY    = "#1B2A6B"
ORANGE  = "#F5A623"
WHITE   = "#FFFFFF"
LIGHT   = "#F0F4FF"
CARD_BG = "#FFFFFF"


class CustomerDashboard(ctk.CTkFrame):
    

    def __init__(self, parent, customer_id: int):
        super().__init__(parent, fg_color=LIGHT, corner_radius=0)

        self.parent         = parent
        self.customer_id    = customer_id
        self.customer       = queries.get_customer_by_id(customer_id)
        self.pricing_engine = PricingEngine()   # Sean's engine

        self._build_layout()
        self._show_page("Dashboard")
        
    def _build_layout(self):
        name = self.customer.get("full_name", "Customer") if self.customer else "Customer"

        nav_items = [
            ("Dashboard",    "📊",  lambda: self._show_page("Dashboard")),
            ("Business Jobs","📦", lambda: self._show_page("Business Jobs")),
            ("Profile",      "👤", lambda: self.parent.show_profile_screen(self.customer_id, "customer")),
            ("Settings",     "⚙️", lambda: self.parent.show_settings_screen(self.customer_id, "customer")),
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
        elif page_name == "Business Jobs":
            self._build_business_jobs_page()


    def _build_dashboard_page(self):
        left = ctk.CTkFrame(self.content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = ctk.CTkFrame(self.content, fg_color="transparent", width=340)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self._build_request_history(left)
        self._build_active_requests(left)
        self._build_new_request_form(right)


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


    def _build_new_request_form(self, parent):
        card = self._card(parent, "New Courier Request")
        PAD  = 14


        ctk.CTkLabel(card, text="Lead Size",
                     font=ctk.CTkFont("Arial", 11, "bold"),
                     text_color=NAVY, anchor="w").pack(fill="x", padx=PAD, pady=(12, 2))

        self.lead_size_var = tk.StringVar(value="medium")
        size_row = ctk.CTkFrame(card, fg_color=LIGHT, corner_radius=8)
        size_row.pack(fill="x", padx=PAD, pady=(0, 10))
        for s in ["Small", "Medium", "Large"]:
            ctk.CTkRadioButton(
                size_row, text=s,
                variable=self.lead_size_var, value=s.lower(),
                text_color=NAVY,
                command=self._update_price
            ).pack(side="left", padx=10, pady=8)


        ctk.CTkLabel(card, text="Urgency Level",
                     font=ctk.CTkFont("Arial", 11, "bold"),
                     text_color=NAVY, anchor="w").pack(fill="x", padx=PAD, pady=(0, 2))

        self.urgency_var = tk.StringVar(value="normal")
        ctk.CTkOptionMenu(
            card, values=["low", "normal", "high"],
            variable=self.urgency_var,
            fg_color=NAVY, button_color=ORANGE,
            command=lambda _: self._update_price()
        ).pack(fill="x", padx=PAD, pady=(0, 10))


        ctk.CTkLabel(card, text="Pickup Location",
                     font=ctk.CTkFont("Arial", 11, "bold"),
                     text_color=NAVY, anchor="w").pack(fill="x", padx=PAD, pady=(0, 2))
        self.pickup_entry = ctk.CTkEntry(card,
                                         placeholder_text="Enter pickup location",
                                         height=36)
        self.pickup_entry.pack(fill="x", padx=PAD, pady=(0, 10))
        # Update price as user types
        self.pickup_entry.bind("<KeyRelease>", lambda e: self._update_price())


        ctk.CTkLabel(card, text="Destination",
                     font=ctk.CTkFont("Arial", 11, "bold"),
                     text_color=NAVY, anchor="w").pack(fill="x", padx=PAD, pady=(0, 2))
        self.dest_entry = ctk.CTkEntry(card,
                                        placeholder_text="Enter destination",
                                        height=36)
        self.dest_entry.pack(fill="x", padx=PAD, pady=(0, 10))
        # Update price as user types
        self.dest_entry.bind("<KeyRelease>", lambda e: self._update_price())


        price_frame = ctk.CTkFrame(card, fg_color=NAVY, corner_radius=10)
        price_frame.pack(fill="x", padx=PAD, pady=(0, 10))

        ctk.CTkLabel(price_frame, text="Estimated Price",
                     font=ctk.CTkFont("Arial", 10),
                     text_color=LIGHT).pack(pady=(10, 0))

        self.price_label = ctk.CTkLabel(
            price_frame,
            text="₦—",
            font=ctk.CTkFont("Arial", 26, "bold"),
            text_color=ORANGE
        )
        self.price_label.pack()

        ctk.CTkLabel(price_frame,
                     text="Based on size · location · urgency",
                     font=ctk.CTkFont("Arial", 9),
                     text_color="gray").pack(pady=(0, 10))


        ctk.CTkButton(
            card, text="Submit Request",
            fg_color=ORANGE, text_color=WHITE,
            font=ctk.CTkFont("Arial", 13, "bold"),
            height=40, corner_radius=8,
            command=self._submit_request
        ).pack(fill="x", padx=PAD, pady=(0, 14))

    def _update_price(self, *args):
        """Recalculate price using Sean's engine whenever any input changes."""
        pickup  = self.pickup_entry.get().strip()
        dest    = self.dest_entry.get().strip()
        size    = self.lead_size_var.get()
        urgency = self.urgency_var.get()

        if pickup and dest:
            price = self.pricing_engine.calculate_price(size, urgency, pickup, dest)
            self.price_label.configure(text=f"₦{price:,.0f}")
        else:
            self.price_label.configure(text="₦—")

    def _submit_request(self):
        pickup  = self.pickup_entry.get().strip()
        dest    = self.dest_entry.get().strip()

        if not pickup or not dest:
            messagebox.showwarning("Missing Fields",
                                   "Please enter pickup location and destination.")
            return

        price_val = self.pricing_engine.calculate_price(
            self.lead_size_var.get(),
            self.urgency_var.get(),
            pickup, dest
        )
        req_id = queries.create_delivery_request(
            customer_id       = self.customer_id,
            lead_size         = self.lead_size_var.get(),
            urgency_level     = self.urgency_var.get(),
            pickup_location   = pickup,
            destination       = dest,
            recommended_price = price_val
        )
        messagebox.showinfo("Request Submitted",
                            f"Request {req_id} submitted!\nEstimated price: ₦{price_val:,.0f}")
        self._show_page("Dashboard")


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