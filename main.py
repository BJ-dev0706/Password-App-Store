from database import init_db
from password_manager_app import PasswordManagerApp

# Initialize the database
init_db()

# Start the GUI application
if __name__ == "__main__":
    app = PasswordManagerApp()
    app.check_update(False)
    app.mainloop()
