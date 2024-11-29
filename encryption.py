import os
from cryptography.fernet import Fernet

# Encryption key management
KEY_FILE = "encryption.key"

def load_key():
    """Load or generate an encryption key."""
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return key

ENCRYPTION_KEY = load_key()
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_password(password):
    """Encrypt a password."""
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(password):
    """Decrypt a password."""
    try:
        return cipher.decrypt(password.encode()).decode()
    except:
        return "[Decryption Error]"
