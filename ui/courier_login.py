import customtkinter as ctk
from PIL import Image
from services.auth_service import AuthService
from config import DB_CONFIG

class CourierLoginScreen:
    def __init__(self, root, on_login_success=None):
        self.root = root
        self.on_login_success = on_login_success
        self.auth = AuthService(DB_CONFIG)
        
        # Configure window
        self.root.title("KayaKonnect - Kaya Login")
        self.root.state("zoomed")
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
                light_image=Image.open("logokk.png")
            )
            logo_label = ctk.CTkLabel(main_frame, image=logo_image, text="")
            logo_label.image = logo_image
            logo_label.pack(pady=(30, 20))
        except Exception as e:
            print(f"Could not load logo: {e}")
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="KayaKonnect",
            font=("Segoe UI", 32, "bold"),
            text_color="#1a3a52"
        )
        title_label.pack(pady=(40, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Kaya Login",
            font=("Segoe UI", 14),
            text_color="#666"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Email field
        self.email_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Enter your email",
            width=300,
            height=45,
            font=("Segoe UI", 12),
            border_color="#ddd",
            border_width=1
        )
        self.email_entry.pack(padx=40, pady=(0, 20))
        
        # Password field
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
        self.password_entry.pack(padx=40, pady=(0, 20))
        
        # Error message label
        self.error_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=("Segoe UI", 10),
            text_color="#e74c3c"
        )
        self.error_label.pack(pady=(0, 15))
        
        # Login button
        login_button = ctk.CTkButton(
            main_frame,
            text="Login",
            width=300,
            height=45,
            font=("Segoe UI", 14, "bold"),
            fg_color="#1a3a52",
            hover_color="#0f2538",
            command=self.login_user
        )
        login_button.pack(pady=20)
        
        # Sign up link
        signup_frame = ctk.CTkFrame(main_frame, fg_color="white")
        signup_frame.pack(pady=20)
        
        signup_label = ctk.CTkLabel(
            signup_frame,
            text="Don't have an account? ",
            font=("Segoe UI", 11),
            text_color="#666"
        )
        signup_label.pack(side="left")
        
        signup_link = ctk.CTkLabel(
            signup_frame,
            text="Register as Kaya",
            font=("Segoe UI", 11, "bold"),
            text_color="#FF9500",
            cursor="hand2"
        )
        signup_link.pack(side="left")
        signup_link.bind("<Button-1>", self.on_signup_click)
    
    def login_user(self):
        """Handle login logic"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validation
        if not email or not password:
            self.show_error("Please fill in all fields")
            return
        
        # Call auth service
        success, message, user_data = self.auth.login_user(email, password)
        
        if success:
            # Check if user is courier
            if user_data.get('user_type') != 'courier':
                self.show_error("Invalid account type. Use Customer login.")
                return
            
            self.show_error("")
            if self.on_login_success:
                self.on_login_success(user_data)
            else:
                print(f"✅ Courier login successful! User: {user_data}")
        else:
            self.show_error(message)
    
    def show_error(self, message):
        """Display error message"""
        self.error_label.configure(text=message)
    
    def on_signup_click(self, event):
        """Handle signup link click - navigate to courier register"""
        from ui.courier_register import CourierRegisterScreen
        
        # Destroy login screen
        self.root.destroy()
        
        # Create new window for register
        new_root = ctk.CTk()
        register = CourierRegisterScreen(new_root)
        new_root.mainloop()


# Main app (for testing)
if __name__ == "__main__":
    root = ctk.CTk()
    login = CourierLoginScreen(root)
    root.mainloop()