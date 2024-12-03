import sqlite3
import os
from src.encryption import encrypt_password, decrypt_password

DB_NAME = "appdata/password_store.db"

def init_db():
    """Initialize SQLite database."""
    # Ensure the appdata folder exists
    if not os.path.exists('appdata'):
        os.makedirs('appdata')
    
    # Connect to the SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            username TEXT,
            password TEXT NOT NULL,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_account(account_name, username, password, note):
    """Add a new account to the database."""
    encrypted_password = encrypt_password(password)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO accounts (account_name, username, password, note) VALUES (?, ?, ?, ?)",
        (account_name, username, encrypted_password, note)
    )
    conn.commit()
    conn.close()

def fetch_all_accounts():
    """Fetch all accounts from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, account_name, username, password, note FROM accounts")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_account(account_id):
    """Delete an account from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts WHERE id=?", (account_id,))
    conn.commit()
    conn.close()

def update_account(account_id, account_name, username, password, note):
    """Update an existing account in the database."""
    encrypted_password = encrypt_password(password)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE accounts
        SET account_name=?, username=?, password=?, note=?
        WHERE id=?
    """, (account_name, username, encrypted_password, note, account_id))
    conn.commit()
    conn.close()
