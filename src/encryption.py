import os
import platform
from cryptography.fernet import Fernet

# Determine key file location based on OS
if platform.system() == "Darwin":  # macOS
    KEY_FILE = os.path.expanduser('~/Library/Application Support/PswdManager/encryption.key')
elif platform.system() == "Windows":  # Windows
    KEY_FILE = r'C:\Program Files\PswdManager\encryption.key'
else:  # Default to appdata for other systems
    KEY_FILE = "appdata/encryption.key"

def load_key():
    """Load or generate an encryption key."""
    # Ensure the folder exists
    key_dir = os.path.dirname(KEY_FILE)
    if not os.path.exists(key_dir):
        os.makedirs(key_dir)

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
