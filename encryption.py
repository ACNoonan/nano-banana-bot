import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY not found in environment variables. Please set it in your .env file.")

f = Fernet(ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> str:
    """Encrypts a string."""
    if not data:
        return ""
    return f.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Decrypts a string."""
    if not encrypted_data:
        return ""
    return f.decrypt(encrypted_data.encode()).decode()
