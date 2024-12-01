import customtkinter as ctk
from tkinter import ttk, messagebox, PhotoImage
from database import add_account, fetch_all_accounts, delete_account, update_account
from utils import generate_password
from encryption import decrypt_password
from PIL import Image, ImageTk
class PasswordManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Password Manager App")
        self.geometry("1200x510")
        self.minsize(1200, 520)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.center_window()
        
        icon_path = "img/clipboard.ico"
        original_image = Image.open(icon_path)
        icon_size = (20, 20)
        resized_image = original_image.resize(icon_size, Image.Resampling.LANCZOS)

        self.copy_icon = ctk.CTkImage(resized_image, size=icon_size)


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
        self.sidebar_frame.grid_rowconfigure(7, weight=0)  # Reveal/Hide Password button
        self.sidebar_frame.grid_rowconfigure(8, weight=0)  # Note label
        self.sidebar_frame.grid_rowconfigure(9, weight=0)  # Note entry
        self.sidebar_frame.grid_rowconfigure(10, weight=0) # Generate Password button
        self.sidebar_frame.grid_rowconfigure(11, weight=0) # Add Account button
        self.sidebar_frame.grid_rowconfigure(12, weight=1) # Stretch bottom space

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
        
        # Reveal/Hide Password Checkbox
        def toggle_password_visibility():
            if self.show_password_checkbox.get():
                self.password_entry.configure(show="")  # Show password
            else:
                self.password_entry.configure(show="*")  # Hide password

        self.show_password_checkbox = ctk.CTkCheckBox(
            self.sidebar_frame,
            text="Show Password",
            command=toggle_password_visibility,
        )
        self.show_password_checkbox.grid(row=7, column=0, padx=10, pady=5)

        ctk.CTkLabel(self.sidebar_frame, text="Note:").grid(row=8, column=0, padx=10, pady=5)
        self.note_entry = ctk.CTkEntry(self.sidebar_frame, width=250)
        self.note_entry.grid(row=9, column=0, padx=10, pady=0)


        # Generate Password Button
        def insert_generated_password():
            try:
                generated_password = generate_password(length=12)  # Default length: 12
                self.password_entry.delete(0, 'end')  # Clear current password field
                self.password_entry.insert(0, generated_password)  # Insert generated password
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        self.generate_password_button = ctk.CTkButton(
            self.sidebar_frame,
            text="Generate Password",
            command=insert_generated_password,
        )
        self.generate_password_button.grid(row=10, column=0, padx=10, pady=10)

        # Add Account Button
        self.add_account_button = ctk.CTkButton(self.sidebar_frame, text="Add Account", command=self.add_account)
        self.add_account_button.grid(row=11, column=0, padx=10, pady=5)


        # Content Frame (Right Section)
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.content_frame, text="View Accounts", font=("Arial", 18)).pack(pady=10)

        # Create a frame for the Treeview and Scrollbar to align them properly
        tree_frame = ctk.CTkFrame(self.content_frame, fg_color="#fff")
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

        # Bind the double-click event to the method to update account
        self.tree.bind("<Double-1>", self.on_double_click)
        # Bind the new selection change event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_selection_change)

    def on_double_click(self, event):
        """Handle double-click to edit an account."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select an account to update!")
            return

        # Get the selected account data
        account_data = self.tree.item(selected_item)["values"]
        
        # Call the method to update account with the selected data
        self.update_account(account_data)

    def update_account(self, account=None):
        """Open an update interface for the selected account."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select an account to update!")
            return

        account_data = self.tree.item(selected_item)["values"]
        account_id = account_data[0]

        # Fetch the actual account details including the decrypted password
        actual_account = next((a for a in fetch_all_accounts() if a[0] == account_id), None)

        if not actual_account:
            messagebox.showerror("Error", "Unable to fetch account details!")
            return

        account_name, username, decrypted_password, note = actual_account[1], actual_account[2], decrypt_password(actual_account[3]), actual_account[4]

        # Create a new Toplevel window
        update_window = ctk.CTkToplevel(self)
        update_window.title("Update Account")

        # Consistent window size
        screen_width = update_window.winfo_screenwidth()
        screen_height = update_window.winfo_screenheight()
        window_width = 450
        window_height = 400
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        update_window.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        update_window.grab_set()

        # Function to copy text to clipboard
        def copy_to_clipboard(value):
            self.clipboard_clear()
            self.clipboard_append(value)
            self.update()

        ctk.CTkLabel(update_window, text="Update Account", font=("Arial", 20, "bold")).pack(pady=20)

        def create_field(label_text, default_value, parent_frame, show=""):
            field_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
            field_frame.pack(fill="x", pady=10, padx=20)

            ctk.CTkLabel(field_frame, text=label_text, anchor="w", width=100).pack(side="left", padx=5)
            entry = ctk.CTkEntry(field_frame, width=250, show=show)
            entry.insert(0, default_value)
            entry.pack(side="left", padx=5)

            copy_button = ctk.CTkButton(
                field_frame,
                text="",
                width=60,
                corner_radius=8,
                image=self.copy_icon,
                compound="left",
                command=lambda: copy_to_clipboard(entry.get()))
            copy_button.pack(side="right", padx=5)

            return entry

        # Parent frame for all fields
        fields_frame = ctk.CTkFrame(update_window, fg_color="transparent")
        fields_frame.pack(fill="both", expand=True)

        # Account Name Field
        account_name_entry = create_field("Website Url:", account_name, fields_frame)

        # Username Field
        username_entry = create_field("Username:", username, fields_frame)

        # Password Field
        password_entry = create_field("Password:", decrypted_password, fields_frame, show="*")

        # Toggle Password Visibility
        password_visibility = ctk.BooleanVar(value=False)

        def toggle_password_visibility():
            if password_visibility.get():
                password_entry.configure(show="")
            else:
                password_entry.configure(show="*")

        ctk.CTkCheckBox(fields_frame, text="Show Password", variable=password_visibility, 
                        command=toggle_password_visibility).pack(pady=10, padx=20)

        # Note Field
        note_entry = create_field("Note:", note, fields_frame)

        # Buttons Frame
        buttons_frame = ctk.CTkFrame(update_window, fg_color="transparent")
        buttons_frame.pack(pady=20, padx=20, fill="x")

        # Regenerate Password Button
        def regenerate_password():
            new_password = generate_password(length=12)  # Default length: 12
            password_entry.delete(0, 'end')  # Clear the current password field
            password_entry.insert(0, new_password)  # Insert the new generated password

        reset_password_button = ctk.CTkButton(buttons_frame, text="Regenerate", command=regenerate_password, 
                                            corner_radius=8, width=180, height=40)
        reset_password_button.pack(side="left", padx=10)

        # Update Button
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

        confirm_change_button = ctk.CTkButton(buttons_frame, text="Confirm Update", command=update, 
                                            corner_radius=8, width=180, height=40)
        confirm_change_button.pack(side="right", padx=10)

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
        """Load all accounts into the Treeview with masked passwords."""
        # Clear existing rows in the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch all accounts and insert them with masked passwords
        accounts = fetch_all_accounts()
        for account in accounts:
            # Create a masked password with the same number of characters as the actual password
            decrypted_password = decrypt_password(account[3])
            masked_password = '*' * len(decrypted_password)
            
            # Insert data into the Treeview
            self.tree.insert("", "end", values=(account[0], account[1], account[2], masked_password, account[4]))

    # Changed delete_account to handle multi-selection and disable update_button
    def delete_account(self):
        """Delete selected accounts from the database."""
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select one or more accounts to delete!")
            return

        # Confirm deletion
        confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected accounts?")
        if not confirmation:
            return

        # Delete all selected accounts
        for item in selected_items:
            account_id = self.tree.item(item)["values"][0]
            delete_account(account_id)

        self.load_accounts()
        messagebox.showinfo("Success", "Selected accounts deleted successfully!")

    # Override Treeview selection binding to handle multiple selections
    def on_tree_selection_change(self, event):
        """Handle changes in Treeview selection."""
        selected_items = self.tree.selection()

        # Disable update button if multiple items are selected
        if len(selected_items) > 1:
            self.update_button.configure(state="disabled")
        else:
            self.update_button.configure(state="normal")

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
