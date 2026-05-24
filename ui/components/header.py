import customtkinter as ctk

NAVY       = "#1B2A6B"
ORANGE     = "#F5A623"
WHITE      = "#FFFFFF"
LIGHT_GRAY = "#F0F4FF"


class Header(ctk.CTkFrame):

    def __init__(self, parent, greeting: str, on_close=None, on_mini=None):
        super().__init__(parent, fg_color=WHITE, height=56, corner_radius=0)
        self.pack_propagate(False)

        # Greeting text
        ctk.CTkLabel(
            self,
            text=greeting,
            font=ctk.CTkFont("Arial", 15, "bold"),
            text_color=NAVY
        ).pack(side="left", padx=20, pady=10)

        # Right-side window controls
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(side="right", padx=12)

        if on_mini:
            ctk.CTkButton(
                controls, text="—", width=28, height=28,
                fg_color=LIGHT_GRAY, text_color=NAVY,
                hover_color="#D0D8FF", corner_radius=6,
                command=on_mini
            ).pack(side="left", padx=3)

        if on_close:
            ctk.CTkButton(
                controls, text="✕", width=28, height=28,
                fg_color=LIGHT_GRAY, text_color=NAVY,
                hover_color="#FFCCCC", corner_radius=6,
                command=on_close
            ).pack(side="left", padx=3)
