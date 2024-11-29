import secrets
import string

def generate_password(length=12):
    """Generate a strong random password."""
    if length < 8:
        raise ValueError("Password length should be at least 8 characters.")

    # Character pools
    char_pool = string.ascii_letters + string.digits + string.punctuation

    # Ensure the password contains at least one lowercase, uppercase, digit, and special character
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]

    # Fill the rest of the password length
    password += [secrets.choice(char_pool) for _ in range(length - 4)]

    # Shuffle to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)
