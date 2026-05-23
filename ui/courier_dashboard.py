"""
KayaKonnect – Courier Dashboard UI
Branch : courier-module
File   : ui/courier_dashboard.py

Run    : python ui/courier_dashboard.py
Tested : Python 3.11 + customtkinter 5.x
"""

import sys
import os
import math
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox

# Allow running this file directly OR via `python -m`
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from models.courier import Courier

# ──────────────────────────────────────────────
#  BRAND PALETTE  (from KayaKonnect mockup)
# ──────────────────────────────────────────────
C_NAVY        = "#1B2A4A"   # sidebar / primary dark
C_NAVY_HOVER  = "#243660"
C_ORANGE      = "#F5A623"   # accent / active highlight
C_ORANGE_DIM  = "#D4891A"
C_WHITE       = "#FFFFFF"
C_BG_LIGHT    = "#F4F6FA"   # main area background
C_CARD        = "#FFFFFF"
C_TEXT_DARK   = "#1B2A4A"
C_TEXT_MID    = "#4A5568"
C_TEXT_LIGHT  = "#A0AEC0"
C_BORDER      = "#E2E8F0"
C_GREEN       = "#48BB78"
C_RED         = "#FC8181"
C_PENDING     = "#F6AD55"

FONT_HEAD  = ("Segoe UI", 22, "bold")
FONT_SUB   = ("Segoe UI", 13, "bold")
FONT_BODY  = ("Segoe UI", 11)
FONT_SMALL = ("Segoe UI", 9)
FONT_LOGO  = ("Segoe UI", 18, "bold")


# ──────────────────────────────────────────────
#  HELPER WIDGETS
# ──────────────────────────────────────────────

class SectionCard(ctk.CTkFrame):
    """White rounded card."""
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=C_CARD,
            corner_radius=12,
            border_width=1,
            border_color=C_BORDER,
            **kwargs,
        )


class NavButton(ctk.CTkButton):
    """Sidebar navigation item."""
    def __init__(self, master, text, icon="", command=None, active=False, **kwargs):
        color = C_ORANGE if active else "transparent"
        txt_color = C_WHITE
        super().__init__(
            master,
            text=f"  {icon}  {text}",
            fg_color=color,
            hover_color=C_NAVY_HOVER,
            text_color=txt_color,
            font=("Segoe UI", 12, "bold" if active else "normal"),
            anchor="w",
            height=42,
            corner_radius=8,
            command=command,
            **kwargs,
        )


class DonutCanvas(tk.Canvas):
    """Simple canvas donut chart for incentive progress."""
    def __init__(self, master, pct=75, size=140, **kwargs):
        super().__init__(master, width=size, height=size,
                         bg=C_CARD, highlightthickness=0, **kwargs)
        self._pct = pct
        self._size = size
        self._draw()

    def _draw(self):
        s = self._size
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
                        style="arc", outline=C_GREEN, width=14)
        # Centre text
        self.create_text(s // 2, s // 2,
                         text=f"{self._pct}%",
                         font=("Segoe UI", 16, "bold"),
                         fill=C_TEXT_DARK)

    def update_pct(self, pct):
        self._pct = pct
        self._draw()


# ──────────────────────────────────────────────
#  SCREEN: DASHBOARD
# ──────────────────────────────────────────────

class DashboardScreen(ctk.CTkFrame):
    def __init__(self, master, courier: Courier, refresh_cb, **kwargs):
        super().__init__(master, fg_color=C_BG_LIGHT, **kwargs)
        self._courier = courier
        self._refresh = refresh_cb
        self._build()

    def _build(self):
        # Title row
        title = ctk.CTkLabel(self, text="Dashboard", font=FONT_HEAD,
                             text_color=C_TEXT_DARK)
        title.pack(anchor="w", padx=32, pady=(28, 4))
        sub = ctk.CTkLabel(self, text=f"Welcome back, {self._courier.name} 👋",
                           font=FONT_BODY, text_color=C_TEXT_MID)
        sub.pack(anchor="w", padx=32, pady=(0, 20))

        # Stats row
        stats_row = ctk.CTkFrame(self, fg_color="transparent")
        stats_row.pack(fill="x", padx=32, pady=(0, 20))
        stats_row.columnconfigure((0, 1, 2), weight=1, uniform="s")

        earn = self._courier.view_earnings()
        self._make_stat(stats_row, 0, "₦ {:,.0f}".format(earn["total_earnings"]),
                        "Total Earnings", C_ORANGE)
        self._make_stat(stats_row, 1, str(earn["jobs_completed"]),
                        "Jobs Completed", C_NAVY)
        self._make_stat(stats_row, 2,
                        str(len(self._courier.view_available_jobs())),
                        "Available Jobs", C_GREEN)

        # Two-column lower area
        lower = ctk.CTkFrame(self, fg_color="transparent")
        lower.pack(fill="both", expand=True, padx=32, pady=(0, 24))
        lower.columnconfigure(0, weight=3)
        lower.columnconfigure(1, weight=2)
        lower.rowconfigure(0, weight=1)

        # Accepted jobs list
        self._build_accepted(lower)
        # Incentive card
        self._build_incentive(lower)

    def _make_stat(self, parent, col, value, label, accent):
        card = SectionCard(parent)
        card.grid(row=0, column=col, padx=8, sticky="nsew")
        bar = ctk.CTkFrame(card, fg_color=accent, width=4, corner_radius=4)
        bar.pack(side="left", fill="y", padx=(12, 0), pady=12)
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(side="left", padx=14, pady=14)
        ctk.CTkLabel(inner, text=value, font=("Segoe UI", 20, "bold"),
                     text_color=C_TEXT_DARK).pack(anchor="w")
        ctk.CTkLabel(inner, text=label, font=FONT_SMALL,
                     text_color=C_TEXT_LIGHT).pack(anchor="w")

    def _build_accepted(self, parent):
        card = SectionCard(parent)
        card.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

        ctk.CTkLabel(card, text="Accepted Jobs",
                     font=FONT_SUB, text_color=C_TEXT_DARK).pack(
            anchor="w", padx=18, pady=(16, 8))

        jobs = self._courier.accepted_jobs
        if not jobs:
            ctk.CTkLabel(card, text="No accepted jobs yet.",
                         font=FONT_BODY, text_color=C_TEXT_LIGHT).pack(pady=30)
        else:
            for job in jobs:
                row = ctk.CTkFrame(card, fg_color=C_BG_LIGHT, corner_radius=8)
                row.pack(fill="x", padx=18, pady=4)
                ctk.CTkLabel(row, text=job["id"], font=("Segoe UI", 10, "bold"),
                             text_color=C_NAVY).pack(anchor="w", padx=10, pady=(8, 2))
                ctk.CTkLabel(row,
                             text=f"📍 {job['pickup']}  →  {job['destination']}",
                             font=FONT_SMALL, text_color=C_TEXT_MID).pack(
                    anchor="w", padx=10, pady=(0, 6))

                def make_complete(j=job):
                    def cb():
                        result = self._courier.complete_job(j["id"])
                        if result:
                            messagebox.showinfo("Job Completed",
                                                f"{j['id']} marked as complete!\n"
                                                f"₦{j['fare']:,} credited.")
                        self._refresh()
                    return cb

                ctk.CTkButton(row, text="Mark Complete",
                              fg_color=C_GREEN, hover_color="#38A169",
                              text_color=C_WHITE, font=FONT_SMALL,
                              height=28, corner_radius=6,
                              command=make_complete()).pack(
                    anchor="e", padx=10, pady=(0, 8))

    def _build_incentive(self, parent):
        card = SectionCard(parent)
        card.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        earn = self._courier.view_earnings()
        ctk.CTkLabel(card, text="Incentive Progress",
                     font=FONT_SUB, text_color=C_TEXT_DARK).pack(
            anchor="w", padx=18, pady=(16, 10))

        donut = DonutCanvas(card, pct=earn["incentive_progress"])
        donut.pack(pady=(0, 8))

        ctk.CTkLabel(card, text="Earnings Summary",
                     font=FONT_SMALL, text_color=C_TEXT_LIGHT).pack()

        ctk.CTkFrame(card, fg_color=C_BORDER, height=1).pack(
            fill="x", padx=18, pady=10)

        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=18)
        ctk.CTkLabel(row, text="Total:", font=FONT_BODY,
                     text_color=C_TEXT_MID).pack(side="left")
        ctk.CTkLabel(row, text="₦{:,.0f}".format(earn["total_earnings"]),
                     font=("Segoe UI", 12, "bold"),
                     text_color=C_ORANGE).pack(side="right")


# ──────────────────────────────────────────────
#  SCREEN: JOB DETAILS
# ──────────────────────────────────────────────

class JobDetailsScreen(ctk.CTkFrame):
    def __init__(self, master, courier: Courier, refresh_cb, **kwargs):
        super().__init__(master, fg_color=C_BG_LIGHT, **kwargs)
        self._courier = courier
        self._refresh = refresh_cb
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Job Details", font=FONT_HEAD,
                     text_color=C_TEXT_DARK).pack(
            anchor="w", padx=32, pady=(28, 4))
        ctk.CTkLabel(self, text="Available jobs — accept to start delivery",
                     font=FONT_BODY, text_color=C_TEXT_MID).pack(
            anchor="w", padx=32, pady=(0, 20))

        jobs = self._courier.view_available_jobs()
        if not jobs:
            card = SectionCard(self)
            card.pack(fill="x", padx=32, pady=8)
            ctk.CTkLabel(card,
                         text="✅  No new jobs available right now. Check back soon!",
                         font=FONT_BODY, text_color=C_TEXT_MID).pack(pady=40)
            return

        for job in jobs:
            self._job_card(job)

    def _job_card(self, job):
        card = SectionCard(self)
        card.pack(fill="x", padx=32, pady=10)

        # Header bar
        hdr = ctk.CTkFrame(card, fg_color=C_NAVY, corner_radius=8)
        hdr.pack(fill="x", padx=14, pady=(14, 0))
        ctk.CTkLabel(hdr, text=f"  {job['id']}",
                     font=("Segoe UI", 11, "bold"),
                     text_color=C_WHITE).pack(side="left", padx=4, pady=6)

        # Body
        body = ctk.CTkFrame(card, fg_color="transparent")
        body.pack(fill="x", padx=14, pady=10)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=0)

        info = ctk.CTkFrame(body, fg_color="transparent")
        info.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(info, text="PICK-UP LOCATION:",
                     font=("Segoe UI", 9, "bold"),
                     text_color=C_TEXT_LIGHT).pack(anchor="w")
        ctk.CTkLabel(info, text=job["pickup"],
                     font=FONT_BODY, text_color=C_TEXT_DARK).pack(anchor="w")
        ctk.CTkFrame(info, fg_color=C_BORDER, height=1).pack(fill="x", pady=6)
        ctk.CTkLabel(info, text="DESTINATION:",
                     font=("Segoe UI", 9, "bold"),
                     text_color=C_TEXT_LIGHT).pack(anchor="w")
        ctk.CTkLabel(info, text=job["destination"],
                     font=FONT_BODY, text_color=C_TEXT_DARK).pack(anchor="w")

        # Fare + buttons
        fare_box = ctk.CTkFrame(body, fg_color=C_BG_LIGHT,
                                corner_radius=10, border_width=1,
                                border_color=C_BORDER)
        fare_box.grid(row=0, column=1, padx=(20, 0), sticky="n")
        ctk.CTkLabel(fare_box, text="Recommended Fare:",
                     font=FONT_SMALL, text_color=C_TEXT_LIGHT).pack(
            padx=14, pady=(10, 2))
        ctk.CTkLabel(fare_box, text=f"₦ {job['fare']:,}",
                     font=("Segoe UI", 14, "bold"),
                     text_color=C_ORANGE).pack(padx=14, pady=(0, 10))

        btn_row = ctk.CTkFrame(fare_box, fg_color="transparent")
        btn_row.pack(padx=14, pady=(0, 12))

        def make_accept(j=job):
            def cb():
                result = self._courier.accept_job(j["id"])
                if result:
                    messagebox.showinfo("Job Accepted",
                                        f"You accepted {j['id']}!\n"
                                        f"Head to: {j['pickup']}")
                self._refresh()
            return cb

        ctk.CTkButton(btn_row, text="Decline",
                      fg_color=C_RED, hover_color="#E53E3E",
                      text_color=C_WHITE, font=FONT_SMALL,
                      width=74, height=30, corner_radius=6,
                      command=lambda: None).pack(side="left", padx=(0, 6))

        ctk.CTkButton(btn_row, text="Accept",
                      fg_color=C_ORANGE, hover_color=C_ORANGE_DIM,
                      text_color=C_WHITE, font=("Segoe UI", 10, "bold"),
                      width=74, height=30, corner_radius=6,
                      command=make_accept()).pack(side="left")


# ──────────────────────────────────────────────
#  SCREEN: ACCEPTED JOBS
# ──────────────────────────────────────────────

class AcceptedJobsScreen(ctk.CTkFrame):
    def __init__(self, master, courier: Courier, refresh_cb, **kwargs):
        super().__init__(master, fg_color=C_BG_LIGHT, **kwargs)
        self._courier = courier
        self._refresh = refresh_cb
        self._build()

    def _build(self):
        ctk.CTkLabel(self, text="Accepted Jobs", font=FONT_HEAD,
                     text_color=C_TEXT_DARK).pack(
            anchor="w", padx=32, pady=(28, 4))
        ctk.CTkLabel(self, text="Jobs you have accepted — complete them to earn",
                     font=FONT_BODY, text_color=C_TEXT_MID).pack(
            anchor="w", padx=32, pady=(0, 20))

        jobs = self._courier.accepted_jobs
        if not jobs:
            card = SectionCard(self)
            card.pack(fill="x", padx=32)
            ctk.CTkLabel(card, text="No accepted jobs. Go to Job Details to pick one!",
                         font=FONT_BODY, text_color=C_TEXT_LIGHT).pack(pady=40)
            return

        for job in jobs:
            card = SectionCard(self)
            card.pack(fill="x", padx=32, pady=10)

            hdr = ctk.CTkFrame(card, fg_color=C_ORANGE, corner_radius=8)
            hdr.pack(fill="x", padx=14, pady=(14, 0))
            ctk.CTkLabel(hdr, text=f"  {job['id']}  •  ₦{job['fare']:,}",
                         font=("Segoe UI", 11, "bold"),
                         text_color=C_WHITE).pack(side="left", pady=6, padx=4)
            ctk.CTkLabel(hdr, text="IN PROGRESS  ",
                         font=FONT_SMALL, text_color=C_WHITE).pack(
                side="right", pady=6)

            body = ctk.CTkFrame(card, fg_color="transparent")
            body.pack(fill="x", padx=14, pady=10)
            ctk.CTkLabel(body, text=f"📍 From: {job['pickup']}",
                         font=FONT_BODY, text_color=C_TEXT_DARK).pack(anchor="w")
            ctk.CTkLabel(body, text=f"🏁 To:     {job['destination']}",
                         font=FONT_BODY, text_color=C_TEXT_DARK).pack(anchor="w", pady=(4, 0))

            if "accepted_at" in job:
                ctk.CTkLabel(body, text=f"Accepted: {job['accepted_at']}",
                             font=FONT_SMALL, text_color=C_TEXT_LIGHT).pack(
                    anchor="w", pady=(6, 0))

            def make_complete(j=job):
                def cb():
                    result = self._courier.complete_job(j["id"])
                    if result:
                        messagebox.showinfo("Completed!",
                                            f"{j['id']} done!\n₦{j['fare']:,} added.")
                    self._refresh()
                return cb

            ctk.CTkButton(card, text="✔  Mark as Completed",
                          fg_color=C_GREEN, hover_color="#38A169",
                          text_color=C_WHITE, font=("Segoe UI", 11, "bold"),
                          height=36, corner_radius=8,
                          command=make_complete()).pack(
                anchor="e", padx=14, pady=(0, 14))


# ──────────────────────────────────────────────
#  MAIN WINDOW
# ──────────────────────────────────────────────

class CourierDashboard(ctk.CTk):
    def __init__(self, courier: Courier):
        super().__init__()
        self._courier = courier
        self._active_screen = "dashboard"

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("KayaKonnect – Courier Dashboard")
        self.geometry("1366x768")
        self.resizable(False, False)
        self.configure(fg_color=C_BG_LIGHT)

        self._build_layout()
        self._show_screen("dashboard")

    # ── Layout ────────────────────────────────
    def _build_layout(self):
        # Master 2-column grid
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._sidebar = self._make_sidebar()
        self._sidebar.grid(row=0, column=0, sticky="nsew")

        self._content_area = ctk.CTkFrame(self, fg_color=C_BG_LIGHT,
                                          corner_radius=0)
        self._content_area.grid(row=0, column=1, sticky="nsew")
        self._content_area.grid_rowconfigure(0, weight=0)   # search bar
        self._content_area.grid_rowconfigure(1, weight=1)   # screen
        self._content_area.grid_columnconfigure(0, weight=1)

        self._search_bar = self._make_search_bar()
        self._search_bar.grid(row=0, column=0, sticky="ew")

        self._screen_frame = ctk.CTkFrame(self._content_area,
                                          fg_color=C_BG_LIGHT,
                                          corner_radius=0)
        self._screen_frame.grid(row=1, column=0, sticky="nsew")
        self._screen_frame.grid_rowconfigure(0, weight=1)
        self._screen_frame.grid_columnconfigure(0, weight=1)

        self._current_screen_widget = None

    def _make_sidebar(self):
        sb = ctk.CTkFrame(self, fg_color=C_NAVY, corner_radius=0, width=220)
        sb.grid_propagate(False)

        # Logo area
        logo_frame = ctk.CTkFrame(sb, fg_color="transparent")
        logo_frame.pack(fill="x", padx=18, pady=(28, 24))

        # Hexagon-style icon placeholder (orange box)
        icon_box = ctk.CTkFrame(logo_frame, fg_color=C_ORANGE,
                                width=36, height=36, corner_radius=6)
        icon_box.pack(side="left")
        icon_box.pack_propagate(False)
        ctk.CTkLabel(icon_box, text="K", font=("Segoe UI", 18, "bold"),
                     text_color=C_WHITE).place(relx=0.5, rely=0.5, anchor="center")

        name_frame = ctk.CTkFrame(logo_frame, fg_color="transparent")
        name_frame.pack(side="left", padx=(8, 0))
        ctk.CTkLabel(name_frame, text="Kaya", font=("Segoe UI", 16, "bold"),
                     text_color=C_WHITE).pack(anchor="w")
        ctk.CTkLabel(name_frame, text="Konnect", font=("Segoe UI", 10),
                     text_color=C_ORANGE).pack(anchor="w")

        ctk.CTkFrame(sb, fg_color="#2D4070", height=1).pack(
            fill="x", padx=16, pady=(0, 16))

        # Nav buttons
        self._nav_btns: dict[str, NavButton] = {}
        nav_items = [
            ("dashboard",  "⊞", "Dashboard"),
            ("job_details","≡", "Job Details"),
            ("accepted",   "✓", "Accepted Jobs"),
        ]
        for key, icon, label in nav_items:
            btn = NavButton(sb, text=label, icon=icon, active=(key == "dashboard"),
                            command=lambda k=key: self._show_screen(k))
            btn.pack(fill="x", padx=12, pady=3)
            self._nav_btns[key] = btn

        # Sign out at bottom
        sb.pack_propagate(False)
        sign_out = ctk.CTkButton(
            sb, text="⇥  Sign Out",
            fg_color="transparent", hover_color="#2D4070",
            text_color=C_TEXT_LIGHT, font=FONT_BODY,
            anchor="w", height=42, corner_radius=8,
            command=self._sign_out,
        )
        sign_out.place(relx=0, rely=1.0, anchor="sw",
                       relwidth=1.0, x=12, y=-16)

        return sb

    def _make_search_bar(self):
        bar = ctk.CTkFrame(self._content_area, fg_color=C_WHITE,
                           corner_radius=0, height=58,
                           border_width=0)
        bar.grid_propagate(False)

        inner = ctk.CTkFrame(bar, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=24, pady=10)

        search = ctk.CTkEntry(inner, placeholder_text="🔍  Search jobs, IDs…",
                              font=FONT_BODY, height=36,
                              fg_color=C_BG_LIGHT, border_color=C_BORDER,
                              text_color=C_TEXT_DARK,
                              corner_radius=8)
        search.pack(side="left", fill="x", expand=True)

        # Settings + profile icons
        for sym in ("⚙", "👤"):
            ctk.CTkButton(inner, text=sym, width=36, height=36,
                          fg_color=C_BG_LIGHT, hover_color=C_BORDER,
                          text_color=C_TEXT_DARK, corner_radius=8,
                          font=("Segoe UI", 14)).pack(side="right", padx=(6, 0))

        return bar

    # ── Screen switching ───────────────────────
    def _show_screen(self, name: str):
        self._active_screen = name

        # Update nav highlights
        for key, btn in self._nav_btns.items():
            btn.configure(fg_color=C_ORANGE if key == name else "transparent",
                          font=("Segoe UI", 12, "bold" if key == name else "normal"))

        # Destroy old screen
        if self._current_screen_widget:
            self._current_screen_widget.destroy()

        # Build new screen
        kwargs = dict(master=self._screen_frame,
                      courier=self._courier,
                      refresh_cb=lambda: self._show_screen(self._active_screen))

        if name == "dashboard":
            widget = DashboardScreen(**kwargs)
        elif name == "job_details":
            widget = JobDetailsScreen(**kwargs)
        elif name == "accepted":
            widget = AcceptedJobsScreen(**kwargs)
        else:
            widget = DashboardScreen(**kwargs)

        widget.grid(row=0, column=0, sticky="nsew")
        self._current_screen_widget = widget

    def _sign_out(self):
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            self.destroy()


# ──────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────

def main():
    demo_courier = Courier(
        courier_id=Courier.generate_id(),
        name="Paul",
        email="paul@kayakonnect.com",
    )
    # Seed some earnings for the demo
    demo_courier.earnings = 35_000
    demo_courier.completed_jobs = [{"id": "DEMO-001", "fare": 35000}]

    app = CourierDashboard(courier=demo_courier)
    app.mainloop()


if __name__ == "__main__":
    main()
