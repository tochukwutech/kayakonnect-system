<<<<<<< HEAD
import customtkinter as ctk
from services.auth_service import AuthService
from config import DB_CONFIG

class CourierRegisterScreen:
    def __init__(self, root, on_register_success=None):
        self.root = root
        self.on_register_success = on_register_success
        self.auth = AuthService(DB_CONFIG)
        
        # Configure window
        self.root.title("KayaKonnect - Register as a Kaya")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        
        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all UI elements"""
        
        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="white")
        main_frame.pack(fill="both", expand=True)
        
        # Logo/Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="KayaKonnect",
            font=("Segoe UI", 32, "bold"),
            text_color="#1a3a52"
        )
        title_label.pack(pady=(40, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Register as a Kaya!",
            font=("Segoe UI", 14),
            text_color="#666"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Username field
        username_label = ctk.CTkLabel(
            main_frame,
            text="Username",
            font=("Segoe UI", 12, "bold"),
            text_color="#333"
        )
        username_label.pack(anchor="w", padx=40, pady=(10, 5))
        
        self.username_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Enter your username",
            width=300,
            height=45,
            font=("Segoe UI", 12),
            border_color="#ddd",
            border_width=1
        )
        self.username_entry.pack(padx=40, pady=(0, 15))
        
        # Email field
        email_label = ctk.CTkLabel(
            main_frame,
            text="Email",
            font=("Segoe UI", 12, "bold"),
            text_color="#333"
        )
        email_label.pack(anchor="w", padx=40, pady=(10, 5))
        
        self.email_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Enter your email",
            width=300,
            height=45,
            font=("Segoe UI", 12),
            border_color="#ddd",
            border_width=1
        )
        self.email_entry.pack(padx=40, pady=(0, 15))
        
        # Password field
        password_label = ctk.CTkLabel(
            main_frame,
            text="Password",
            font=("Segoe UI", 12, "bold"),
            text_color="#333"
        )
        password_label.pack(anchor="w", padx=40, pady=(10, 5))
        
        self.password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Enter your password",
            width=300,
            height=45,
            font=("Segoe UI", 12),
            show="*",
            border_color="#ddd",
            border_width=1
        )
        self.password_entry.pack(padx=40, pady=(0, 15))
        
        # Confirm Password field
        confirm_pwd_label = ctk.CTkLabel(
            main_frame,
            text="Confirm Password",
            font=("Segoe UI", 12, "bold"),
            text_color="#333"
        )
        confirm_pwd_label.pack(anchor="w", padx=40, pady=(10, 5))
        
        self.confirm_password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Re-enter your password to confirm it",
            width=300,
            height=45,
            font=("Segoe UI", 12),
            show="*",
            border_color="#ddd",
            border_width=1
        )
        self.confirm_password_entry.pack(padx=40, pady=(0, 15))
        
        # Error message label
        self.error_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=("Segoe UI", 10),
            text_color="#e74c3c"
        )
        self.error_label.pack(pady=(0, 15))
        
        # Sign Up button
        signup_button = ctk.CTkButton(
            main_frame,
            text="Sign Up",
            width=300,
            height=45,
            font=("Segoe UI", 14, "bold"),
            fg_color="#1a3a52",
            hover_color="#0f2538",
            command=self.register_user
        )
        signup_button.pack(pady=20)
        
        # Login link
        login_frame = ctk.CTkFrame(main_frame, fg_color="white")
        login_frame.pack(pady=20)
        
        login_label = ctk.CTkLabel(
            login_frame,
            text="Already have an account? ",
            font=("Segoe UI", 11),
            text_color="#666"
        )
        login_label.pack(side="left")
        
        login_link = ctk.CTkLabel(
            login_frame,
            text="Log in",
            font=("Segoe UI", 11, "bold"),
            text_color="#FF9500",
            cursor="hand2"
        )
        login_link.pack(side="left")
        login_link.bind("<Button-1>", self.on_login_click)
    
    def register_user(self):
        """Handle registration logic"""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        
        # Validation
        if not username or not email or not password or not confirm_password:
            self.show_error("Please fill in all fields")
            return
        
        if password != confirm_password:
            self.show_error("Passwords do not match")
            return
        
        # Call auth service (note: 'courier' instead of 'customer')
        success, message, user_id = self.auth.register_user(username, email, password, 'courier')
        
        if success:
            self.show_error("")  # Clear error
            if self.on_register_success:
                self.on_register_success(user_id)
            else:
                print(f"✅ Courier registration successful! User ID: {user_id}")
        else:
            self.show_error(message)
    
    def show_error(self, message):
        """Display error message"""
        self.error_label.configure(text=message)
    
    def on_login_click(self, event):
        """Handle login link click"""
        print("Navigate to login screen")
        # This will be replaced with actual navigation


# Main app (for testing)
if __name__ == "__main__":
    root = ctk.CTk()
    register = CourierRegisterScreen(root)
    root.mainloop()
=======
"""
ui/courier_register.py
PLACEHOLDER — Replace with teammate's actual courier register file.
"""

import customtkinter as ctk
from tkinter import messagebox
import hashlib
from database.db_connection import get_connection

NAVY   = "#1B2A6B"
ORANGE = "#F5A623"
WHITE  = "#FFFFFF"
LIGHT  = "#F0F4FF"


class CourierRegister(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=LIGHT)
        self.parent = parent

        card = ctk.CTkFrame(self, fg_color=WHITE, corner_radius=14, width=420, height=560)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(
            card,
            text="KayaKonnect",
            font=ctk.CTkFont("Arial", 22, "bold"),
            text_color=ORANGE
        ).pack(pady=(30, 2))

        ctk.CTkLabel(
            card,
            text="Register as a Kaya",
            font=ctk.CTkFont("Arial", 13),
            text_color=NAVY
        ).pack(pady=(0, 16))

        # ── Fields defined individually (avoids loop binding issue) ──
        self.name_entry = ctk.CTkEntry(card, placeholder_text="Full Name",
                                       width=320, height=36)
        self.name_entry.pack(pady=4)

        self.email_entry = ctk.CTkEntry(card, placeholder_text="Email address",
                                        width=320, height=36)
        self.email_entry.pack(pady=4)

        self.phone_entry = ctk.CTkEntry(card, placeholder_text="Phone number",
                                        width=320, height=36)
        self.phone_entry.pack(pady=4)

        self.address_entry = ctk.CTkEntry(card, placeholder_text="Address",
                                          width=320, height=36)
        self.address_entry.pack(pady=4)

        self.vehicle_entry = ctk.CTkEntry(card, placeholder_text="Vehicle Type (e.g. Motorcycle)",
                                          width=320, height=36)
        self.vehicle_entry.pack(pady=4)

        self.pw_entry = ctk.CTkEntry(card, placeholder_text="Password",
                                     show="•", width=320, height=36)
        self.pw_entry.pack(pady=4)

        self.pw2_entry = ctk.CTkEntry(card, placeholder_text="Confirm Password",
                                      show="•", width=320, height=36)
        self.pw2_entry.pack(pady=4)

        ctk.CTkButton(
            card,
            text="Sign Up",
            fg_color=ORANGE, text_color=WHITE,
            font=ctk.CTkFont("Arial", 13, "bold"),
            width=320, height=40, corner_radius=8,
            command=self._submit
        ).pack(pady=(14, 6))

        ctk.CTkButton(
            card,
            text="Already have an account? Login",
            fg_color="transparent", text_color=NAVY,
            hover_color=LIGHT, font=ctk.CTkFont("Arial", 11),
            command=lambda: parent.show_courier_login()
        ).pack(pady=(0, 20))

        ctk.CTkLabel(
            card,
            text="[ PLACEHOLDER — replace with teammate's courier_register.py ]",
            font=ctk.CTkFont("Arial", 9),
            text_color="gray"
        ).pack(pady=(0, 10))

    def _submit(self):
        name    = self.name_entry.get().strip()
        email   = self.email_entry.get().strip()
        phone   = self.phone_entry.get().strip()
        addr    = self.address_entry.get().strip()
        vehicle = self.vehicle_entry.get().strip()
        pw      = self.pw_entry.get()
        pw2     = self.pw2_entry.get()

        if not all([name, email, pw, pw2]):
            messagebox.showwarning("Missing Fields", "Please fill in all required fields.")
            return
        if pw != pw2:
            messagebox.showerror("Mismatch", "Passwords do not match.")
            return

        pw_hash = hashlib.sha256(pw.encode()).hexdigest()

        try:
            conn = get_connection()
            cur  = conn.cursor()
            cur.execute("""
                INSERT INTO couriers
                    (full_name, email, phone, address, vehicle_type, password_hash)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, email, phone, addr, vehicle, pw_hash))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", "Courier account created! Please login.")
            self.parent.show_courier_login()
        except Exception as e:
            messagebox.showerror("Error", str(e))
>>>>>>> fcedbfb653d8341fa0c28c8dda0f6d78129628d9
