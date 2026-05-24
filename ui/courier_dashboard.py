"""
ui/courier_dashboard.py
Full Courier Dashboard for KayaKonnect.
Added from Paul's code:
  1. DonutCanvas — incentive progress ring
  2. Mark as Complete button on accepted jobs
  3. Decline button on available jobs
  5. "IN PROGRESS" status badge on accepted jobs
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from ui.components.sidebar    import Sidebar
from ui.components.header     import Header
from ui.components.data_table import DataTable
from database import queries

# color scheme
NAVY    = "#1B2A6B"
ORANGE  = "#F5A623"
WHITE   = "#FFFFFF"
LIGHT   = "#F0F4FF"
CARD_BG = "#FFFFFF"
GREEN   = "#27AE60"
RED     = "#FC8181"


# ══════════════════════════════════════════════════════════
# DONUT CANVAS — from Paul's code
# ══════════════════════════════════════════════════════════
class DonutCanvas(tk.Canvas):
    """Circular donut chart for incentive progress."""
    def __init__(self, master, pct=0, size=140, **kwargs):
        super().__init__(master, width=size, height=size,
                         bg=CARD_BG, highlightthickness=0, **kwargs)
        self._pct  = pct
        self._size = size
        self._draw()

    def _draw(self):
        s   = self._size
        pad = 14
        self.delete("all")
        # Grey track
        self.create_arc(pad, pad, s - pad, s - pad,
                        start=0, extent=360,
                        style="arc", outline="#E2E8F0", width=14)
        # Coloured arc
        extent = (self._pct / 100) * 360
        self.create_arc(pad, pad, s - pad, s - pad,
                        start=90, extent=-extent,
                        style="arc", outline=ORANGE, width=14)
        # Centre text
        self.create_text(s // 2, s // 2,
                         text=f"{self._pct}%",
                         font=("Arial", 16, "bold"),
                         fill=NAVY)

    def update_pct(self, pct):
        self._pct = pct
        self._draw()


# ══════════════════════════════════════════════════════════
# COURIER DASHBOARD
# ══════════════════════════════════════════════════════════
class CourierDashboard(ctk.CTkFrame):
    def __init__(self, parent, courier_id: int):
        super().__init__(parent, fg_color=LIGHT, corner_radius=0)

        self.parent     = parent
        self.courier_id = courier_id
        self.courier    = queries.get_courier_by_id(courier_id)
        self.current_tab = "Dashboard"

        self._build_layout()
        self._show_tab("Dashboard")

    # ══════════════════════════════════════════════════════════
    # LAYOUT
    # ══════════════════════════════════════════════════════════
    def _build_layout(self):
        name = self.courier.get("full_name", "Courier") if self.courier else "Courier"

        nav_items = [
            ("Dashboard",     "📊", lambda: self._show_tab("Dashboard")),
            ("Available Jobs","📋", lambda: self._show_tab("Available Jobs")),
            ("Connect",       "🤝", lambda: self._show_tab("Connect")),
            ("Profile",       "👤", lambda: self.parent.show_profile_screen(self.courier_id, "courier")),
            ("Settings",      "⚙️", lambda: self.parent.show_settings_screen(self.courier_id, "courier")),
        ]
        self.sidebar = Sidebar(
            self,
            nav_items   = nav_items,
            active_item = "Dashboard",
            user_name   = name,
            user_role   = "Courier",
            on_signout  = self._sign_out
        )
        self.sidebar.pack(side="left", fill="y")

        right = ctk.CTkFrame(self, fg_color=LIGHT, corner_radius=0)
        right.pack(side="left", fill="both", expand=True)

        import time
        hour   = int(time.strftime("%H"))
        period = "morning" if hour < 12 else ("afternoon" if hour < 17 else "evening")
        self.header = Header(
            right,
            greeting = f"Good {period}, {name.split()[0]} 👋",
            on_close = lambda: self.parent.destroy(),
            on_mini  = lambda: self.parent.iconify()
        )
        self.header.pack(fill="x")

        # Tab bar
        self.tab_bar = ctk.CTkFrame(right, fg_color=WHITE, height=46, corner_radius=0)
        self.tab_bar.pack(fill="x")
        self.tab_bar.pack_propagate(False)
        self._build_tab_bar()

        # Content area
        self.content = ctk.CTkFrame(right, fg_color=LIGHT, corner_radius=0)
        self.content.pack(fill="both", expand=True, padx=16, pady=12)

    # ── Tab bar ───────────────────────────────────────────────
    def _build_tab_bar(self):
        self._tab_buttons = {}
        tabs = ["Dashboard", "Available Jobs", "Connect"]
        for tab in tabs:
            btn = ctk.CTkButton(
                self.tab_bar, text=tab,
                font=ctk.CTkFont("Arial", 12),
                fg_color="transparent", text_color=NAVY,
                hover_color=LIGHT, corner_radius=0, height=44,
                command=lambda t=tab: self._show_tab(t)
            )
            btn.pack(side="left", padx=4)
            self._tab_buttons[tab] = btn

    def _highlight_tab(self, tab_name):
        for name, btn in self._tab_buttons.items():
            btn.configure(text_color=ORANGE if name == tab_name else NAVY,
                          fg_color=LIGHT if name == tab_name else "transparent")

    def _show_tab(self, tab_name):
        self.current_tab = tab_name
        self._highlight_tab(tab_name)
        self.sidebar.set_active(
            tab_name if tab_name in ["Dashboard", "Available Jobs", "Connect"]
            else "Dashboard"
        )
        for w in self.content.winfo_children():
            w.destroy()

        if tab_name == "Dashboard":
            self._build_dashboard_tab()
        elif tab_name == "Available Jobs":
            self._build_available_jobs_tab()
        elif tab_name == "Connect":
            self._build_connect_tab()

    # ══════════════════════════════════════════════════════════
    # TAB 1 — DASHBOARD
    # ══════════════════════════════════════════════════════════
    def _build_dashboard_tab(self):
        left = ctk.CTkFrame(self.content, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        right = ctk.CTkFrame(self.content, fg_color="transparent", width=280)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self._build_accepted_jobs(left)
        self._build_earnings_summary(right)
        self._build_earnings_chart(right)

    # ── Accepted Jobs (with IN PROGRESS badge + Mark Complete) ─
    def _build_accepted_jobs(self, parent):
        card = self._card(parent, "Accepted Jobs")
        jobs = queries.get_courier_accepted_jobs(self.courier_id)

        if not jobs:
            ctk.CTkLabel(card, text="No accepted jobs yet.",
                         text_color="gray").pack(pady=20)
            return

        scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=8, pady=8)

        for j in jobs:
            job_card = ctk.CTkFrame(scroll, fg_color=LIGHT, corner_radius=10)
            job_card.pack(fill="x", pady=6)

            # ── Header row with ID + IN PROGRESS badge ────────
            hdr = ctk.CTkFrame(job_card, fg_color=NAVY, corner_radius=8)
            hdr.pack(fill="x", padx=10, pady=(10, 0))

            ctk.CTkLabel(hdr, text=f"  {j['request_id']}",
                         font=ctk.CTkFont("Arial", 11, "bold"),
                         text_color=WHITE).pack(side="left", padx=4, pady=6)

            # Status badge — IN PROGRESS / COMPLETED
            status     = j.get("status", "accepted")
            badge_color = ORANGE if status in ("accepted", "in_progress") else GREEN
            badge_text  = "IN PROGRESS" if status in ("accepted", "in_progress") else "COMPLETED"
            ctk.CTkLabel(hdr, text=f"{badge_text}  ",
                         font=ctk.CTkFont("Arial", 9, "bold"),
                         text_color=WHITE,
                         fg_color=badge_color,
                         corner_radius=6).pack(side="right", padx=8, pady=6)

            # ── Body ──────────────────────────────────────────
            body = ctk.CTkFrame(job_card, fg_color="transparent")
            body.pack(fill="x", padx=14, pady=6)

            ctk.CTkLabel(body,
                         text=f"👤 {j.get('customer_name') or '—'}",
                         font=ctk.CTkFont("Arial", 11),
                         text_color=NAVY, anchor="w").pack(fill="x")
            ctk.CTkLabel(body,
                         text=f"📍 From: {j['pickup_location']}",
                         font=ctk.CTkFont("Arial", 10),
                         text_color="gray", anchor="w").pack(fill="x")
            ctk.CTkLabel(body,
                         text=f"🏁 To:    {j['destination']}",
                         font=ctk.CTkFont("Arial", 10),
                         text_color="gray", anchor="w").pack(fill="x")
            ctk.CTkLabel(body,
                         text=f"💰 ₦{j['price']:,.0f}",
                         font=ctk.CTkFont("Arial", 11, "bold"),
                         text_color=ORANGE, anchor="w").pack(fill="x", pady=(4, 0))

            # ── Mark Complete button (only if not completed) ──
            if status in ("accepted", "in_progress"):
                ctk.CTkButton(
                    job_card,
                    text="✔  Mark as Completed",
                    fg_color=GREEN, text_color=WHITE,
                    hover_color="#1E8449",
                    font=ctk.CTkFont("Arial", 11, "bold"),
                    height=34, corner_radius=8,
                    command=lambda rid=j["request_id"]: self._complete_job(rid)
                ).pack(anchor="e", padx=10, pady=(0, 10))

    def _complete_job(self, request_id):
        if messagebox.askyesno("Complete Job",
                               f"Mark job {request_id} as completed?"):
            queries.complete_job(self.courier_id, request_id)
            messagebox.showinfo("Job Completed",
                                f"Job {request_id} marked as completed!")
            self._show_tab("Dashboard")

    # ── Earnings Summary with Donut ───────────────────────────
    def _build_earnings_summary(self, parent):
        summary = queries.get_courier_earnings_summary(self.courier_id)
        card    = self._card(parent, "Earnings Summary")

        for label, value in [
            ("Total Jobs",     str(summary.get("total_jobs", 0))),
            ("Total Earnings", f"₦{summary.get('total_earnings', 0):,.0f}"),
        ]:
            row = ctk.CTkFrame(card, fg_color=LIGHT, corner_radius=8)
            row.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(row, text=label,
                         font=ctk.CTkFont("Arial", 11), text_color="gray",
                         anchor="w").pack(fill="x", padx=10, pady=(8, 0))
            ctk.CTkLabel(row, text=value,
                         font=ctk.CTkFont("Arial", 18, "bold"),
                         text_color=NAVY, anchor="w").pack(fill="x", padx=10, pady=(0, 8))

        # Donut chart for incentive/completion progress
        jobs  = summary.get("total_jobs", 0)
        total = max(jobs, 10)   # out of 10 jobs = 100%
        pct   = min(int((jobs / total) * 100), 100)

        ctk.CTkLabel(card, text="Incentive Progress",
                     font=ctk.CTkFont("Arial", 11), text_color="gray").pack(pady=(8, 4))

        donut = DonutCanvas(card, pct=pct, size=130)
        donut.pack(pady=(0, 10))

    # ── Earnings Bar Chart ────────────────────────────────────
    def _build_earnings_chart(self, parent):
        card    = self._card(parent, "Monthly Earnings")
        monthly = queries.get_courier_monthly_earnings(self.courier_id)

        canvas = tk.Canvas(card, bg=WHITE, height=160, highlightthickness=0)
        canvas.pack(fill="x", padx=10, pady=10)

        if not monthly:
            canvas.create_text(130, 80, text="No earnings data yet.",
                               fill="gray", font=("Arial", 11))
            return

        max_earn = max((m["earnings"] for m in monthly), default=1) or 1
        bar_w    = max(20, 200 // max(len(monthly), 1))
        x_start  = 30

        for i, m in enumerate(monthly):
            x0 = x_start + i * (bar_w + 8)
            x1 = x0 + bar_w
            h  = int((m["earnings"] / max_earn) * 120)
            y0 = 145 - h
            y1 = 145
            canvas.create_rectangle(x0, y0, x1, y1, fill=ORANGE, outline="")
            canvas.create_text((x0+x1)//2, 155,
                               text=m["month"][:3],
                               fill=NAVY, font=("Arial", 8))
            canvas.create_text((x0+x1)//2, y0 - 8,
                               text=f"₦{int(m['earnings'])//1000}k",
                               fill=NAVY, font=("Arial", 7))

    # ══════════════════════════════════════════════════════════
    # TAB 2 — AVAILABLE JOBS (Accept + Decline buttons)
    # ══════════════════════════════════════════════════════════
    def _build_available_jobs_tab(self):
        card = self._card(self.content, "Available Jobs")
        jobs = queries.get_available_jobs()

        if not jobs:
            ctk.CTkLabel(card, text="No available jobs right now.",
                         text_color="gray").pack(pady=20)
            return

        cols = ["Request ID", "Customer", "From", "To", "Size", "Urgency", "Price (₦)", "Actions"]
        header_frame = ctk.CTkFrame(card, fg_color=NAVY, corner_radius=8)
        header_frame.pack(fill="x", padx=2, pady=(2, 0))
        for ci, col in enumerate(cols[:-1]):
            ctk.CTkLabel(header_frame, text=col,
                         font=ctk.CTkFont("Arial", 11, "bold"),
                         text_color=WHITE, anchor="w").grid(
                row=0, column=ci, sticky="ew",
                padx=(12 if ci == 0 else 6), pady=8)
            header_frame.columnconfigure(ci, weight=1)

        scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=2, pady=2)
        for ci in range(len(cols)):
            scroll.columnconfigure(ci, weight=1)

        for ri, j in enumerate(jobs):
            bg = WHITE if ri % 2 == 0 else LIGHT
            cells = [
                j["request_id"],
                j.get("customer_name") or "—",
                j["pickup_location"],
                j["destination"],
                j["lead_size"].capitalize(),
                j["urgency_level"].capitalize(),
                f"₦{j['price']:,.0f}",
            ]
            for ci, cell in enumerate(cells):
                ctk.CTkLabel(scroll, text=str(cell),
                             font=ctk.CTkFont("Arial", 11),
                             text_color=NAVY, fg_color=bg,
                             anchor="w").grid(
                    row=ri, column=ci, sticky="ew",
                    padx=(12 if ci == 0 else 6), pady=5)

            # Actions frame with Accept + Decline
            actions = ctk.CTkFrame(scroll, fg_color=bg)
            actions.grid(row=ri, column=7, padx=6, pady=5)

            ctk.CTkButton(
                actions, text="Accept",
                fg_color=GREEN, text_color=WHITE,
                font=ctk.CTkFont("Arial", 10, "bold"),
                width=64, height=28, corner_radius=6,
                command=lambda rid=j["request_id"]: self._accept_job(rid)
            ).pack(side="left", padx=(0, 4))

            ctk.CTkButton(
                actions, text="Decline",
                fg_color=RED, text_color=WHITE,
                font=ctk.CTkFont("Arial", 10, "bold"),
                width=64, height=28, corner_radius=6,
                command=lambda rid=j["request_id"]: self._decline_job(rid)
            ).pack(side="left")

    def _accept_job(self, request_id):
        if messagebox.askyesno("Accept Job", f"Accept job {request_id}?"):
            queries.accept_job(self.courier_id, request_id)
            messagebox.showinfo("Job Accepted",
                                f"You have accepted job {request_id}!")
            self._show_tab("Available Jobs")

    def _decline_job(self, request_id):
        if messagebox.askyesno("Decline Job",
                               f"Decline job {request_id}?"):
            messagebox.showinfo("Job Declined",
                                f"Job {request_id} has been declined.")
            self._show_tab("Available Jobs")

    # ══════════════════════════════════════════════════════════
    # TAB 3 — CONNECT
    # ══════════════════════════════════════════════════════════
    def _build_connect_tab(self):
        card = self._card(self.content, "Connect with Customers")
        pending = queries.get_available_jobs()

        if not pending:
            ctk.CTkLabel(card, text="No customers to connect with right now.",
                         text_color="gray").pack(pady=20)
            return

        scroll = ctk.CTkScrollableFrame(card, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        seen = set()
        for j in pending:
            cname = j.get("customer_name") or "Unknown"
            if cname in seen:
                continue
            seen.add(cname)

            row = ctk.CTkFrame(scroll, fg_color=LIGHT, corner_radius=10)
            row.pack(fill="x", pady=5, padx=4)

            avatar = ctk.CTkFrame(row, fg_color=NAVY, width=48, height=48,
                                  corner_radius=24)
            avatar.pack(side="left", padx=12, pady=10)
            avatar.pack_propagate(False)
            ctk.CTkLabel(avatar, text=cname[0].upper(),
                         font=ctk.CTkFont("Arial", 18, "bold"),
                         text_color=WHITE).place(relx=0.5, rely=0.5, anchor="center")

            info = ctk.CTkFrame(row, fg_color="transparent")
            info.pack(side="left", fill="x", expand=True, pady=10)
            ctk.CTkLabel(info, text=cname,
                         font=ctk.CTkFont("Arial", 13, "bold"),
                         text_color=NAVY, anchor="w").pack(fill="x")
            ctk.CTkLabel(info,
                         text=f"From: {j['pickup_location']} → {j['destination']}",
                         font=ctk.CTkFont("Arial", 10),
                         text_color="gray", anchor="w").pack(fill="x")

            ctk.CTkButton(
                row, text="Connect",
                fg_color=ORANGE, text_color=WHITE,
                font=ctk.CTkFont("Arial", 11),
                width=85, height=32, corner_radius=8,
                command=lambda rid=j["request_id"]: self._accept_job(rid)
            ).pack(side="right", padx=12)

    # ══════════════════════════════════════════════════════════
    # NAVIGATION
    # ══════════════════════════════════════════════════════════
    def go_to_profile(self):
        self.parent.show_profile_screen(user_id=self.courier_id, user_type="courier")

    def go_to_settings(self):
        self.parent.show_settings_screen(user_id=self.courier_id, user_type="courier")

    def _sign_out(self):
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            self.parent.show_role_selection()

    # ══════════════════════════════════════════════════════════
    # HELPER
    # ══════════════════════════════════════════════════════════
    def _card(self, parent, title: str) -> ctk.CTkFrame:
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, pady=(0, 10))
        ctk.CTkLabel(wrapper, text=title,
                     font=ctk.CTkFont("Arial", 13, "bold"),
                     text_color=NAVY).pack(anchor="w", pady=(0, 4))
        card = ctk.CTkFrame(wrapper, fg_color=CARD_BG, corner_radius=10)
        card.pack(fill="both", expand=True)
        return card
