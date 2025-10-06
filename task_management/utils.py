import string
import secrets

def generate_secure_password(length=12):
    """
    Generate a cryptographically secure random password.
    Includes uppercase, lowercase, digits, and symbols.
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password
