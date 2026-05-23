"""
main.py
KayaKonnect — Central Application Controller

Controls all screen transitions.
Every screen calls self.master (or self.parent) methods to switch screens.

Screen flow:
  SplashScreen → RoleSelectionScreen (built into splash)
      ↓                    ↓
CustomerLogin          CourierLogin
CustomerRegister       CourierRegister
      ↓                    ↓
CustomerDashboard ←→  CourierDashboard
ProfileScreen          ProfileScreen
SettingsScreen         SettingsScreen
"""

import customtkinter as ctk

# ── Your teammates' screens (they must exist in ui/) ──────────
from ui.splash_screen      import SplashScreen
from ui.login_screen       import LoginScreen       # customer login
from ui.signup_screen      import SignupScreen       # customer register
from ui.courier_login      import CourierLogin       # courier login
from ui.courier_register   import CourierRegister    # courier register

# ── Your screens ──────────────────────────────────────────────
from ui.customer_dashboard import CustomerDashboard
from ui.courier_dashboard  import CourierDashboard
from ui.profile_screen     import ProfileScreen
from ui.settings_screen    import SettingsScreen

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


class KayaKonnectApp(ctk.CTk):
    """
    Root application window and screen manager.

    All screens receive `self` (the app) as their `parent`.
    They call self.parent.show_XYZ(...) to navigate.
    """

    def __init__(self):
        super().__init__()

        self.title("KayaKonnect")
        self.geometry("1366x768")
        self.minsize(1366, 768)

        # Track whichever frame is currently displayed
        self.current_screen = None

        # Start with splash
        self.show_splash()

    # ══════════════════════════════════════════════════════════
    # SCREEN MANAGER HELPERS
    # ══════════════════════════════════════════════════════════
    def _clear(self):
        """Destroy the currently visible screen."""
        if self.current_screen is not None:
            self.current_screen.destroy()
            self.current_screen = None

    def _show(self, screen_instance):
        """Pack a new screen and store reference."""
        self._clear()
        self.current_screen = screen_instance
        self.current_screen.pack(fill="both", expand=True)

    # ══════════════════════════════════════════════════════════
    # SPLASH
    # ══════════════════════════════════════════════════════════
    def show_splash(self):
        self._show(SplashScreen(self))

    # ══════════════════════════════════════════════════════════
    # ROLE SELECTION
    # (if your splash handles this inline, point both buttons
    #  at show_customer_login / show_courier_login directly)
    # ══════════════════════════════════════════════════════════
    def show_role_selection(self):
        """Called after sign-out to return to splash/role screen."""
        self.show_splash()

    # ══════════════════════════════════════════════════════════
    # CUSTOMER FLOW
    # ══════════════════════════════════════════════════════════
    def show_customer_login(self):
        self._show(LoginScreen(self))

    def show_customer_register(self):
        self._show(SignupScreen(self))

    def show_customer_dashboard(self, customer_id: int):
        self._show(CustomerDashboard(self, customer_id))

    # ══════════════════════════════════════════════════════════
    # COURIER FLOW
    # ══════════════════════════════════════════════════════════
    def show_courier_login(self):
        self._show(CourierLogin(self))

    def show_courier_register(self):
        self._show(CourierRegister(self))

    def show_courier_dashboard(self, courier_id: int):
        self._show(CourierDashboard(self, courier_id))

    # ══════════════════════════════════════════════════════════
    # SHARED SCREENS
    # ══════════════════════════════════════════════════════════
    def show_profile_screen(self, user_id: int, user_type: str):
        """
        user_type: 'customer' or 'courier'
        """
        self._show(ProfileScreen(self, user_id, user_type))

    def show_settings_screen(self, user_id: int, user_type: str):
        """
        user_type: 'customer' or 'courier'
        """
        self._show(SettingsScreen(self, user_id, user_type))


# ══════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = KayaKonnectApp()
    app.mainloop()