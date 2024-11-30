import customtkinter as ctk
from tkinter import ttk, messagebox
from database import add_account, fetch_all_accounts, delete_account, update_account
from utils import generate_password
from encryption import decrypt_password

class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Manager App")
        self.geometry("1200x510")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        

        self.center_window()

        # Main Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar (Left Section)
        self.sidebar_frame = ctk.CTkFrame(self, width=300, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw", padx=20, pady=20)

        # Configure grid rows to behave properly
        self.sidebar_frame.grid_rowconfigure(0, weight=0)  # Add Account label
        self.sidebar_frame.grid_rowconfigure(1, weight=0)  # Website Url label
        self.sidebar_frame.grid_rowconfigure(2, weight=0)  # Website Url entry
        self.sidebar_frame.grid_rowconfigure(3, weight=0)  # Username label
        self.sidebar_frame.grid_rowconfigure(4, weight=0)  # Username entry
        self.sidebar_frame.grid_rowconfigure(5, weight=0)  # Password label
        self.sidebar_frame.grid_rowconfigure(6, weight=0)  # Password entry
        self.sidebar_frame.grid_rowconfigure(7, weight=0)  # Note label
        self.sidebar_frame.grid_rowconfigure(8, weight=0)  # Note entry
        self.sidebar_frame.grid_rowconfigure(9, weight=0)  # Add Account button
        self.sidebar_frame.grid_rowconfigure(10, weight=0) # Generate Password button
        self.sidebar_frame.grid_rowconfigure(11, weight=1) # Stretch bottom space

        # Add Account Section
        ctk.CTkLabel(self.sidebar_frame, text="Add Account", font=("Arial", 18)).grid(row=0, column=0, padx=10, pady=(10, 20))

        ctk.CTkLabel(self.sidebar_frame, text="Website Url:").grid(row=1, column=0, padx=10, pady=5)
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

        # Create a frame for the Treeview and Scrollbar to align them properly
        tree_frame = ctk.CTkFrame(self.content_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview to display accounts
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Account", "Username", "Password", "Note"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Account", text="Website Url")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password")
        self.tree.heading("Note", text="Note")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Account", width=150, anchor="center")
        self.tree.column("Username", width=150, anchor="center")
        self.tree.column("Password", width=150, anchor="center")
        self.tree.column("Note", width=200, anchor="center")
        self.tree.pack(fill="both", expand=True, side="left")

        # Add scrollbar for the Treeview and link it to the Treeview widget
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Create a frame for the buttons
        button_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", corner_radius=0, bg_color="transparent")

        # Pack the button_frame within content_frame
        button_frame.pack(pady=20, anchor="center")

        # Delete Button
        self.delete_button = ctk.CTkButton(button_frame, text="Delete Account", command=self.delete_account)
        self.delete_button.pack(side="left", padx=10)

        # Update Button
        self.update_button = ctk.CTkButton(button_frame, text="Update Account", command=self.update_account)
        self.update_button.pack(side="left", padx=10)

        # Refresh Button
        self.refresh_button = ctk.CTkButton(button_frame, text="Refresh Data", command=self.refresh_data)
        self.refresh_button.pack(side="left", padx=10)

        # Load accounts into the Treeview
        self.load_accounts()

    def show_loading_screen(self):
        """Show a loading screen."""
        self.loading_screen = ctk.CTkToplevel(self)
        self.loading_screen.title("Refreshing Data")
        self.loading_screen.geometry("300x150")
        self.loading_screen.resizable(False, False)
        self.loading_screen.grab_set()

        label = ctk.CTkLabel(self.loading_screen, text="Refreshing data, please wait...", font=("Arial", 14))
        label.pack(pady=40)

        self.loading_screen.update()

    def hide_loading_screen(self):
        """Hide the loading screen."""
        if hasattr(self, "loading_screen"):
            self.loading_screen.destroy()

    def refresh_data(self):
        """Refresh the data in the Treeview."""
        self.show_loading_screen()  # Show loading screen
        self.load_accounts()        # Reload accounts
        self.hide_loading_screen()  # Hide loading screen
        messagebox.showinfo("Success", "Data refreshed successfully!")

    def add_account(self):
        """Add an account to the database."""
        account_name = self.account_name_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        note = self.note_entry.get()

        if not account_name or not username or not password:
            messagebox.showerror("Input Error", "Website Url, Username, and Password are required!")
            return

        add_account(account_name, username, password, note)
        messagebox.showinfo("Success", "Account added successfully!")
        self.load_accounts()

    def load_accounts(self):
        """Load all accounts into the Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        accounts = fetch_all_accounts()
        for account in accounts:
            decrypted_password = decrypt_password(account[3])  # Decrypt the password
            self.tree.insert("", "end", values=(account[0], account[1], account[2], decrypted_password, account[4]))

    def delete_account(self):
        """Delete an account from the database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select an account to delete!")
            return

        account_id = self.tree.item(selected_item)["values"][0]
        delete_account(account_id)
        self.load_accounts()
        messagebox.showinfo("Success", "Account deleted successfully!")

    def update_account(self):
        """Open an update interface for the selected account."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select an account to update!")
            return

        account_data = self.tree.item(selected_item)["values"]
        account_id, account_name, username, password, note = account_data

        # Create a new Toplevel window
        update_window = ctk.CTkToplevel(self)
        update_window.title("Update Account")
        update_window.geometry("400x500")
        update_window.grab_set()

        # Labels and Entries for updating
        ctk.CTkLabel(update_window, text="Update Account", font=("Arial", 18)).pack(pady=10)

        ctk.CTkLabel(update_window, text="Website Url:").pack(pady=5)
        account_name_entry = ctk.CTkEntry(update_window, width=300)
        account_name_entry.insert(0, account_name)  # Pre-fill with current data
        account_name_entry.pack(pady=5)

        ctk.CTkLabel(update_window, text="Username:").pack(pady=5)
        username_entry = ctk.CTkEntry(update_window, width=300)
        username_entry.insert(0, username)
        username_entry.pack(pady=5)

        ctk.CTkLabel(update_window, text="Password:").pack(pady=5)
        password_entry = ctk.CTkEntry(update_window, show="*", width=300)
        password_entry.insert(0, password)
        password_entry.pack(pady=5)

        ctk.CTkLabel(update_window, text="Note:").pack(pady=5)
        note_entry = ctk.CTkEntry(update_window, width=300)
        note_entry.insert(0, note)
        note_entry.pack(pady=5)

        def update():
            updated_account_name = account_name_entry.get()
            updated_username = username_entry.get()
            updated_password = password_entry.get()
            updated_note = note_entry.get()

            if not updated_account_name or not updated_username or not updated_password:
                messagebox.showerror("Input Error", "Website Url, Username, and Password are required!")
                return

            update_account(account_id, updated_account_name, updated_username, updated_password, updated_note)
            messagebox.showinfo("Success", "Account updated successfully!")
            self.load_accounts()
            update_window.destroy()

        # Update Button
        update_button = ctk.CTkButton(update_window, text="Update", command=update)
        update_button.pack(pady=20)
        
    def center_window(self):
        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Get the window width and height
        window_width = 1200
        window_height = 550

        # Calculate the position to center the window
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # Set the position of the window
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    
if __name__ == "__main__":
    app = PasswordManagerApp()
    app.mainloop()
