"""
ui/components/data_table.py
Reusable scrollable table widget for displaying database records.
"""

import customtkinter as ctk

NAVY       = "#1B2A6B"
ORANGE     = "#F5A623"
WHITE      = "#FFFFFF"
LIGHT_GRAY = "#F0F4FF"
ROW_ALT    = "#F8F9FF"
HEADER_BG  = "#1B2A6B"


# Status colour map
STATUS_COLORS = {
    "completed":   "#27AE60",
    "accepted":    "#2980B9",
    "in_progress": "#8E44AD",
    "pending":     "#E67E22",
    "cancelled":   "#E74C3C",
}


class DataTable(ctk.CTkFrame):
    """
    Scrollable table with coloured status badges.

    Parameters
    ----------
    parent  : parent widget
    columns : list of column header strings
    rows    : list of tuples/lists — one per row, matching columns order
    """

    def __init__(self, parent, columns: list, rows: list, **kwargs):
        super().__init__(parent, fg_color=WHITE, corner_radius=10, **kwargs)

        self.columns = columns
        self._build(rows)

    def _build(self, rows):
        # ── Column headers ────────────────────────────────────
        header_frame = ctk.CTkFrame(self, fg_color=HEADER_BG, corner_radius=8)
        header_frame.pack(fill="x", padx=2, pady=(2, 0))

        col_weights = self._col_weights()
        for i, col in enumerate(self.columns):
            ctk.CTkLabel(
                header_frame,
                text=col,
                font=ctk.CTkFont("Arial", 11, "bold"),
                text_color=WHITE,
                anchor="w"
            ).grid(row=0, column=i, sticky="ew",
                   padx=(12 if i == 0 else 6), pady=8)
            header_frame.columnconfigure(i, weight=col_weights[i])

        # ── Scrollable rows ───────────────────────────────────
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=2, pady=2)

        for ci in range(len(self.columns)):
            scroll.columnconfigure(ci, weight=col_weights[ci])

        for ri, row in enumerate(rows):
            bg = WHITE if ri % 2 == 0 else ROW_ALT
            for ci, cell in enumerate(row):
                cell_str = str(cell) if cell is not None else "—"
                # Status badge
                if ci == self.columns.index("Status") if "Status" in self.columns else -1:
                    color = STATUS_COLORS.get(cell_str.lower(), NAVY)
                    lbl = ctk.CTkLabel(
                        scroll,
                        text=cell_str.capitalize(),
                        font=ctk.CTkFont("Arial", 10, "bold"),
                        text_color=WHITE,
                        fg_color=color,
                        corner_radius=6,
                        width=80
                    )
                else:
                    lbl = ctk.CTkLabel(
                        scroll,
                        text=cell_str,
                        font=ctk.CTkFont("Arial", 11),
                        text_color=NAVY,
                        fg_color=bg,
                        anchor="w"
                    )
                lbl.grid(row=ri, column=ci, sticky="ew",
                         padx=(12 if ci == 0 else 6), pady=4)

    def _col_weights(self):
        """Give wider columns more weight."""
        n = len(self.columns)
        return [2 if i in (0, 1) else 1 for i in range(n)]

    def refresh(self, new_rows: list):
        """Destroy and rebuild the table with new data."""
        for widget in self.winfo_children():
            widget.destroy()
        self._build(new_rows)
