import psycopg2
import bcrypt
import re
from datetime import datetime, timedelta
import jwt

class AuthService:
    def __init__(self, db_config):
        """Initialize database connection"""
        self.db_config = db_config
    
    def get_connection(self):
        """Create a new database connection"""
        return psycopg2.connect(**self.db_config)
    
    # ============ VALIDATION ============
    
    def validate_email(self, email):
        """Check if email format is valid"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_password(self, password):
        """Check password strength (at least 8 chars, mix of letters & numbers)"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        if not any(c.isalpha() for c in password):
            return False, "Password must contain at least one letter"
        return True, "Valid"
    
    def is_username_taken(self, username):
        """Check if username already exists"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result is not None
        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    def is_email_taken(self, email):
        """Check if email already exists"""
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result is not None
        except Exception as e:
            print(f"Database error: {e}")
            return False
    
    # ============ PASSWORD HASHING ============
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, stored_hash, entered_password):
        """Verify password against stored hash"""
        return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hash.encode('utf-8'))
    
    # ============ REGISTRATION ============
    
    def register_user(self, username, email, password, user_type):
        """
        Register a new user
        user_type: 'customer' or 'courier'
        Returns: (success, message, user_id)
        """
        # Validation
        if len(username) < 3:
            return False, "Username must be at least 3 characters", None
        
        if not self.validate_email(email):
            return False, "Invalid email format", None
        
        is_valid, msg = self.validate_password(password)
        if not is_valid:
            return False, msg, None
        
        if self.is_username_taken(username):
            return False, "Username already exists", None
        
        if self.is_email_taken(email):
            return False, "Email already registered", None
        
        if user_type not in ['customer', 'courier']:
            return False, "Invalid user type", None
        
        # Hash password and insert into database
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            hashed_pwd = self.hash_password(password)
            
            cur.execute("""
                INSERT INTO users (username, email, password_hash, user_type, created_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (username, email, hashed_pwd, user_type, datetime.now()))
            
            user_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            
            return True, "User registered successfully", user_id
        
        except Exception as e:
            return False, f"Registration error: {str(e)}", None
    
    # ============ LOGIN ============
    
    def login_user(self, username, password):
        """
        Authenticate user
        Returns: (success, message, user_data)
        """
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT id, username, email, password_hash, user_type 
                FROM users WHERE username = %s
            """, (username,))
            
            result = cur.fetchone()
            cur.close()
            conn.close()
            
            if not result:
                return False, "Username or password incorrect", None
            
            user_id, uname, email, pwd_hash, user_type = result
            
            # Verify password
            if not self.check_password(pwd_hash, password):
                return False, "Username or password incorrect", None
            
            user_data = {
                'id': user_id,
                'username': uname,
                'email': email,
                'user_type': user_type
            }
            
            return True, "Login successful", user_data
        
        except Exception as e:
            return False, f"Login error: {str(e)}", None
    
    # ============ OPTIONAL: TOKEN GENERATION ============
    
    def generate_token(self, user_id, secret_key, expires_in_hours=24):
        """Generate JWT token for session management"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=expires_in_hours)
        }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token
    
