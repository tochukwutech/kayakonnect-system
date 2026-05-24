import customtkinter as ctk
from tkinter import messagebox

from database                import queries
from services.pricing_engine import PricingEngine

NAVY     = "#1B2A6B"
ORANGE   = "#F5A623"
ORANGE_DK= "#E09010"
WHITE    = "#FFFFFF"
LIGHT    = "#F0F4FF"
CARD_BG  = "#FFFFFF"
GRAY_TEXT= "#8a9bb5"
OFFWHITE = "#f0f2f5"
FIELD_BG = "#f5f6f8"
FIELD_BOR= "#d0d5dd"


class CreateRequestScreen(ctk.CTkFrame):

    def __init__(self, parent, customer_id: int, on_done):
        super().__init__(parent, fg_color="transparent")

        self.customer_id    = customer_id
        self.on_done        = on_done
        self.pricing_engine = PricingEngine()

        self._build()

    def _build(self):
        card = ctk.CTkFrame(self, fg_color=CARD_BG, corner_radius=14)
        card.pack(fill="both", expand=True)
        card.grid_columnconfigure(0, weight=1)

        banner = ctk.CTkFrame(card, fg_color=NAVY, corner_radius=10, height=48)
        banner.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 0))
        banner.grid_propagate(False)
        ctk.CTkLabel(
            banner, text="New Courier Request",
            font=ctk.CTkFont("Helvetica", 14, "bold"),
            text_color=WHITE
        ).pack(side="left", padx=18, pady=10)

        self._section_label(card, "Load Size:", row=1)
        load_frame = ctk.CTkFrame(card, fg_color="transparent")
        load_frame.grid(row=2, column=0, sticky="ew", padx=24, pady=(2, 10))
        self.lead_size_var = ctk.StringVar(value="Small")
        self.lead_size_var.trace_add("write", lambda *_: self._update_price())
        for val in ("Small", "Medium", "Large"):
            self._pill_radio(load_frame, val, self.lead_size_var).pack(side="left", padx=6)

        self._divider(card, row=3)

        self._section_label(card, "Urgency Level:", row=4)
        urg_frame = ctk.CTkFrame(card, fg_color="transparent")
        urg_frame.grid(row=5, column=0, sticky="ew", padx=24, pady=(2, 10))
        self.urgency_var = ctk.StringVar(value="Fair")
        self.urgency_var.trace_add("write", lambda *_: self._update_price())
        for val in ("Slight", "Fair", "High"):
            self._pill_radio(urg_frame, val, self.urgency_var).pack(side="left", padx=6)

        self._divider(card, row=6)

        self._section_label(card, "Pickup Location:", row=7)
        self.pickup_entry = ctk.CTkEntry(
            card, placeholder_text="Enter your pickup location",
            fg_color=FIELD_BG, border_color=FIELD_BOR, border_width=1,
            text_color=NAVY, font=ctk.CTkFont("Helvetica", 11),
            corner_radius=8, height=38
        )
        self.pickup_entry.grid(row=8, column=0, sticky="ew", padx=24, pady=(2, 6))
        self.pickup_entry.bind("<KeyRelease>", lambda e: self._update_price())

        self._divider(card, row=9)


        self._section_label(card, "Destination:", row=10)
        self.dest_entry = ctk.CTkEntry(
            card, placeholder_text="Enter your destination",
            fg_color=FIELD_BG, border_color=FIELD_BOR, border_width=1,
            text_color=NAVY, font=ctk.CTkFont("Helvetica", 11),
            corner_radius=8, height=38
        )
        self.dest_entry.grid(row=11, column=0, sticky="ew", padx=24, pady=(2, 6))
        self.dest_entry.bind("<KeyRelease>", lambda e: self._update_price())

        self._divider(card, row=12)


        price_row = ctk.CTkFrame(card, fg_color="transparent")
        price_row.grid(row=13, column=0, sticky="ew", padx=24, pady=(10, 0))
        price_row.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            price_row, text="Recommended Price:",
            font=ctk.CTkFont("Helvetica", 12, "bold"),
            text_color=NAVY, anchor="w"
        ).grid(row=0, column=0, sticky="w")

        self.price_badge = ctk.CTkLabel(
            price_row, text="₦—",
            font=ctk.CTkFont("Helvetica", 13, "bold"),
            text_color=WHITE,
            fg_color=ORANGE, corner_radius=10,
            padx=14, pady=4
        )
        self.price_badge.grid(row=0, column=1, sticky="e", padx=(12, 0))

        self.price_note = ctk.CTkLabel(
            card, text="Enter locations to see price",
            font=ctk.CTkFont("Helvetica", 10),
            text_color=GRAY_TEXT, anchor="w"
        )
        self.price_note.grid(row=14, column=0, sticky="w", padx=26, pady=(2, 10))

        self._update_price()


        action_bar = ctk.CTkFrame(card, fg_color="transparent")
        action_bar.grid(row=16, column=0, sticky="ew", padx=24, pady=(4, 18))
        action_bar.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            action_bar, text="Cancel",
            fg_color=NAVY, hover_color="#0f2538",
            text_color=WHITE, font=ctk.CTkFont("Helvetica", 11, "bold"),
            corner_radius=8, height=38, width=140,
            command=self.on_done
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            action_bar, text="Create Request",
            fg_color=ORANGE, hover_color=ORANGE_DK,
            text_color=WHITE, font=ctk.CTkFont("Helvetica", 11, "bold"),
            corner_radius=8, height=38, width=140,
            command=self._submit
        ).grid(row=0, column=2, sticky="e")


    def _update_price(self, *args):
        pickup  = self.pickup_entry.get().strip()
        dest    = self.dest_entry.get().strip()
        size    = self.lead_size_var.get().lower()
        urgency = self._map_urgency(self.urgency_var.get())

        if pickup and dest:
            price = self.pricing_engine.calculate_price(size, urgency, pickup, dest)
            self.price_badge.configure(text=f"₦{price:,.0f}")
            self.price_note.configure(
                text=f"{size.capitalize()} load · {self.urgency_var.get()} urgency → price calculated"
            )
        else:
            self.price_badge.configure(text="₦—")
            self.price_note.configure(text="Enter locations to see price")

    def _map_urgency(self, val: str) -> str:
        """Map Daniel's urgency labels to Sean's engine labels."""
        return {"slight": "low", "fair": "normal", "high": "high"}.get(
            val.lower(), "normal"
        )


    def _submit(self):
        pickup = self.pickup_entry.get().strip()
        dest   = self.dest_entry.get().strip()

        if not pickup or not dest:
            messagebox.showwarning("Missing Fields",
                                   "Please enter pickup location and destination.")
            return

        size           = self.lead_size_var.get().lower()
        urgency_mapped = self._map_urgency(self.urgency_var.get())
        price_val      = self.pricing_engine.calculate_price(
            size, urgency_mapped, pickup, dest
        )

        req_id = queries.create_delivery_request(
            customer_id       = self.customer_id,
            lead_size         = size,
            urgency_level     = urgency_mapped,
            pickup_location   = pickup,
            destination       = dest,
            recommended_price = price_val
        )


        dlg = ctk.CTkToplevel(self)
        dlg.title("Request Submitted")
        dlg.geometry("340x180")
        dlg.configure(fg_color=NAVY)
        dlg.grab_set()

        ctk.CTkLabel(
            dlg, text="✓ Request Submitted!",
            font=ctk.CTkFont("Helvetica", 16, "bold"),
            text_color=ORANGE
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            dlg,
            text=f"Request {req_id} created · ₦{price_val:,.0f}",
            font=ctk.CTkFont("Helvetica", 11),
            text_color=WHITE
        ).pack()

        def finish():
            dlg.destroy()
            self.on_done()

        ctk.CTkButton(
            dlg, text="Back to Dashboard",
            fg_color=ORANGE, hover_color=ORANGE_DK,
            text_color=WHITE, corner_radius=8, height=36,
            command=finish
        ).pack(pady=20, padx=30, fill="x")


    def _pill_radio(self, parent, value, variable):
        def on_click():
            variable.set(value)
            for sibling in parent.winfo_children():
                if hasattr(sibling, '_pill_refresh'):
                    sibling._pill_refresh()

        btn = ctk.CTkButton(
            parent, text=value,
            fg_color=WHITE, border_color=GRAY_TEXT, border_width=1,
            text_color=GRAY_TEXT,
            hover_color=OFFWHITE, corner_radius=20,
            font=ctk.CTkFont("Helvetica", 11), height=32, width=90,
            command=on_click
        )

        def refresh():
            if variable.get() == value:
                btn.configure(fg_color=NAVY, border_color=NAVY,
                              border_width=1, text_color=WHITE)
            else:
                btn.configure(fg_color=WHITE, border_color=GRAY_TEXT,
                              border_width=1, text_color=GRAY_TEXT)

        btn._pill_refresh = refresh
        variable.trace_add("write", lambda *_: refresh())
        refresh()
        return btn

    def _section_label(self, parent, text, row):
        ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont("Helvetica", 12, "bold"),
            text_color=NAVY, anchor="w"
        ).grid(row=row, column=0, sticky="w", padx=24, pady=(10, 0))

    def _divider(self, parent, row):
        ctk.CTkFrame(parent, fg_color=FIELD_BOR, height=1).grid(
            row=row, column=0, sticky="ew", padx=16, pady=0)
