from database import init_db
from password_manager_app import PasswordManagerApp

init_db()

if __name__ == "__main__":
    app = PasswordManagerApp()
    app.check_update(False)
    app.mainloop()
