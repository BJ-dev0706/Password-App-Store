import os
import sqlite3
import customtkinter as ctk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
import secrets
import string

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

# Database Initialization
DB_NAME = "password_store.db"

def init_db():
    """Initialize SQLite database."""
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

# Password Generation Function
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

# CustomTkinter App
class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Manager")
        self.geometry("1000x550")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Main Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar (Left Section)
        self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        # Add Account Section
        ctk.CTkLabel(self.sidebar_frame, text="Add Account", font=("Arial", 18)).grid(row=0, column=0, padx=10, pady=(10, 20))

        ctk.CTkLabel(self.sidebar_frame, text="Account Name:").grid(row=1, column=0, padx=10, pady=5)
        self.account_name_entry = ctk.CTkEntry(self.sidebar_frame, width=250)
        self.account_name_entry.grid(row=2, column=0, padx=10, pady=5)

        ctk.CTkLabel(self.sidebar_frame, text="Username:").grid(row=3, column=0, padx=10, pady=5)
        self.username_entry = ctk.CTkEntry(self.sidebar_frame, width=250)
        self.username_entry.grid(row=4, column=0, padx=10, pady=5)

        ctk.CTkLabel(self.sidebar_frame, text="Password:").grid(row=5, column=0, padx=10, pady=5)
        self.password_entry = ctk.CTkEntry(self.sidebar_frame, show="*", width=250)
        self.password_entry.grid(row=6, column=0, padx=10, pady=5)

        ctk.CTkLabel(self.sidebar_frame, text="Note:").grid(row=7, column=0, padx=10, pady=5)
        self.note_entry = ctk.CTkEntry(self.sidebar_frame, width=250)
        self.note_entry.grid(row=8, column=0, padx=10, pady=5)

        # Add Account Button
        self.add_account_button = ctk.CTkButton(self.sidebar_frame, text="Add Account", command=self.add_account)
        self.add_account_button.grid(row=9, column=0, padx=10, pady=20)

        # Generate Password Button
        def insert_generated_password():
            try:
                generated_password = generate_password(length=12)  # Default length: 12
                self.password_entry.delete(0, 'end')  # Clear current password field
                self.password_entry.insert(0, generated_password)  # Insert generated password
                messagebox.showinfo("Password Generated", "A strong password has been generated!")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        self.generate_password_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Generate Password",
            command=insert_generated_password,
        )
        self.generate_password_button.grid(row=10, column=0, padx=10, pady=(10, 20))

        # Content Frame (Right Section)
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.content_frame, text="View Accounts", font=("Arial", 18)).pack(pady=10)

        # Treeview to display accounts
        self.tree = ttk.Treeview(self.content_frame, columns=("ID", "Account", "Username", "Password", "Note"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Account", text="Account Name")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.heading("Note", text="Note")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Account", width=150, anchor="center")
        self.tree.column("Username", width=150, anchor="center")
        self.tree.column("Password", width=150, anchor="center")
        self.tree.column("Note", width=200, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Add scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Buttons for managing accounts
        self.button_frame = ctk.CTkFrame(self.content_frame)
        self.button_frame.pack(fill="x", padx=10, pady=10)

        self.delete_button = ctk.CTkButton(self.button_frame, text="Delete Selected", command=self.delete_account)
        self.delete_button.pack(side="left", padx=10)

        self.update_button = ctk.CTkButton(self.button_frame, text="Update Selected", command=self.update_account)
        self.update_button.pack(side="left", padx=10)

        # Populate the Treeview
        self.populate_tree()

    def add_account(self):
        """Add a new account."""
        account_name = self.account_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        note = self.note_entry.get()

        if not account_name or not password:
            messagebox.showerror("Error", "Account Name and Password are required!")
            return

        encrypted_password = encrypt_password(password)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO accounts (account_name, username, password, note) VALUES (?, ?, ?, ?)",
            (account_name, username, encrypted_password, note)
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Account added successfully!")

        # Clear inputs and refresh the treeview
        self.account_name_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.note_entry.delete(0, 'end')
        self.populate_tree()

    def populate_tree(self):
        """Fetch and display accounts in the treeview."""
        # Clear the treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch data from the database
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, account_name, username, password, note FROM accounts")
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            decrypted_password = decrypt_password(row[3])
            self.tree.insert("", "end", values=(row[0], row[1], row[2], decrypted_password, row[4]))

    def delete_account(self):
        """Delete the selected account."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No account selected!")
            return

        account_id = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this account?")
        if confirm:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM accounts WHERE id=?", (account_id,))
            conn.commit()
            conn.close()
            self.populate_tree()
            messagebox.showinfo("Success", "Account deleted successfully!")

    def update_account(self):
        """Update the selected account."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No account selected!")
            return

        account_id, account_name, username, password, note = self.tree.item(selected_item)["values"]
        update_window = ctk.CTkToplevel(self)
        update_window.title("Update Account")
        update_window.geometry("400x400")

        ctk.CTkLabel(update_window, text="Account Name:").pack(pady=5)
        account_name_entry = ctk.CTkEntry(update_window, width=200)
        account_name_entry.pack(pady=5)
        account_name_entry.insert(0, account_name)

        ctk.CTkLabel(update_window, text="Username:").pack(pady=5)
        username_entry = ctk.CTkEntry(update_window, width=200)
        username_entry.pack(pady=5)
        username_entry.insert(0, username)

        ctk.CTkLabel(update_window, text="Password:").pack(pady=5)
        password_entry = ctk.CTkEntry(update_window, show="*", width=200)
        password_entry.pack(pady=5)
        password_entry.insert(0, password)

        ctk.CTkLabel(update_window, text="Note:").pack(pady=5)
        note_entry = ctk.CTkEntry(update_window, width=200)
        note_entry.pack(pady=5)
        note_entry.insert(0, note)

        def save_updated_account():
            updated_account_name = account_name_entry.get()
            updated_username = username_entry.get()
            updated_password = encrypt_password(password_entry.get())
            updated_note = note_entry.get()

            if not updated_account_name or not updated_password:
                messagebox.showerror("Error", "Account Name and Password are required!")
                return

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE accounts
                SET account_name=?, username=?, password=?, note=?
                WHERE id=?
            """, (updated_account_name, updated_username, updated_password, updated_note, account_id))
            conn.commit()
            conn.close()
            self.populate_tree()
            messagebox.showinfo("Success", "Account updated successfully!")
            update_window.destroy()

        ctk.CTkButton(update_window, text="Save Changes", command=save_updated_account).pack(pady=20)

# Initialize the app
if __name__ == "__main__":
    init_db()
    app = PasswordManagerApp()
    app.mainloop()
