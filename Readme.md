# Application Features

This application provides a user-friendly interface for securely managing your accounts and passwords. Below is an overview of its key features.

## 1. Add a New Account

In the **Add Account** section (located on the left sidebar), you can add new accounts by entering the following details:

- **Account Name**: The name of the account (e.g., Gmail, Facebook).
- **Username**: The username associated with the account (e.g., your email address).
- **Password**: The password for the account. You can either manually enter a password or use the "Generate Password" button to create a strong, random password.
- **Note**: Optionally, you can store any additional notes related to the account.

Click the **Add Account** button to save the account details.

## 2. Generate a Strong Password

The application includes a **Generate Password** feature, which allows you to create a secure, random password. By clicking this button, a strong password is automatically populated in the password field, ensuring security.

## 3. View Stored Accounts

In the **View Accounts** section (on the right side), you can see a table that lists all the accounts you have saved. Each row contains the following information:

- **Account ID**: A unique identifier for the account.
- **Account Name**: The name of the account (e.g., Gmail, Facebook).
- **Username**: The username associated with the account.
- **Password**: The decrypted password (displayed for you to view).
- **Note**: Any additional notes associated with the account.

The list updates automatically as you add or modify accounts.

## 4. Update an Account

To modify an existing account, click on the account you wish to update from the list and then click the **Update Selected** button. A new window will appear where you can edit the following fields:

- Account Name
- Username
- Password
- Notes

After making the necessary changes, click the **Save Changes** button to update the account details.

## 5. Delete an Account

To remove an account, select the account from the list and click **Delete Selected**. You will be prompted to confirm the deletion before the account is permanently removed.

## 6. Database Management

The application uses an **SQLite database** (`password_store.db`) to store account information, including encrypted passwords. This database is created automatically in the same directory as the application’s executable file when the app is first run. You do not need to interact with the database directly; all operations are handled via the app interface.

**Important**: If the `.exe` file is moved to a different folder, the application will continue to use the same database file located in that folder.

## 7. Encryption

Passwords are securely encrypted using the **cryptography library** and **Fernet encryption** to protect your sensitive data. The encryption key is stored in a separate file called `encryption.key`, which is required to decrypt your passwords.

**Important**: The encryption key must be kept safe. If the key is lost, the encrypted passwords will be inaccessible.

## 8. Backup

It is highly recommended to back up your data regularly. Specifically, make sure to copy the following files to a secure location:

- `password_store.db`
- `encryption.key`

These files can be backed up to external storage or cloud services to ensure you don't lose critical data.

## 9. Error Handling and Feedback

In the event of an error (e.g., missing fields, issues with encryption), the application will display an error message detailing the issue. If there is a problem with encryption or decryption (e.g., corrupted key), the application will notify you with an error message such as "[Decryption Error]".

---

For more details or troubleshooting, please refer to the application’s documentation or contact support.
