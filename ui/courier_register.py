import customtkinter as ctk
from PIL import Image
from services.auth_service import AuthService
from config import DB_CONFIG

class CourierRegisterScreen:
    def __init__(self, root, on_register_success=None):
        self.root = root
        self.on_register_success = on_register_success
        self.auth = AuthService(DB_CONFIG)
        
        # Configure window
        self.root.title("KayaKonnect - Register as a Kaya")
        self.root.geometry("1366x768")
        self.root.resizable(True, True)
        
        # Set theme
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all UI elements"""
        
        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="white")
        main_frame.pack(fill="both", expand=True)
        
                # Load and display logo image
        try:
            logo_image = ctk.CTkImage(
               light_image=Image.open("ui/ui-elements/logokk.png"),
                size=(250, 150)
            )
            logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
            logo_label.image = logo_image
            logo_label.pack(pady=(0, 0))
        except Exception as e:
            print(f"Could not load logo: {e}")
        
        # Logo/Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="KayaKonnect",
            font=("Segoe UI", 32, "bold"),
            text_color="#1a3a52"
        )
        title_label.pack(pady=(0,0))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Register as a Kaya!",
            font=("Segoe UI", 14),
            text_color="#666"
        )
        subtitle_label.pack(pady=(0, 30))
        
        self.username_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Enter your username",
            width=457,
            height=45,
            font=("Segoe UI", 12),
            border_color="#ddd",
            border_width=1
        )
        self.username_entry.pack(padx=40, pady=(0, 15))
        
        self.email_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Enter your email",
            width=457,
            height=45,
            font=("Segoe UI", 12),
            border_color="#ddd",
            border_width=1
        )
        self.email_entry.pack(padx=40, pady=(0, 15))
        
        self.password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Enter your password",
            width=457,
            height=45,
            font=("Segoe UI", 12),
            show="*",
            border_color="#ddd",
            border_width=1
        )
        self.password_entry.pack(padx=40, pady=(0, 15))
        
        
        
        self.confirm_password_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Re-enter your password to confirm it",
            width=457,
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
            width=242,
            height=45,
            font=("Segoe UI", 14, "bold"),
            fg_color="#1a3a52",
            hover_color="#0f2538",
            command=self.register_user
        )
        signup_button.pack(pady=10)
        
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