from services.auth_service import AuthService

from config import DB_CONFIG

# Create the auth object
from services.auth_service import AuthService
from config import DB_CONFIG

# Create the auth object
auth = AuthService(DB_CONFIG)
# Test registration
success, message, user_id = auth.register_user('testuser', 'test@example.com', 'Password123', 'customer')
print(f"Register: {success}, {message}, {user_id}")

# Test login
success, message, user_data = auth.login_user('testuser', 'Password123')
print(f"Login: {success}, {message}, {user_data}")
