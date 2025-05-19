from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDialog, QMessageBox
import hashlib
from controllers import controller as c

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Login")
        self.setFixedWidth(300)
        self.setFixedHeight(150)

        layout = QVBoxLayout()

        # Username input
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Password input
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.validate_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def validate_login(self):
        # Get the username and password from input fields
        username = self.username_input.text()
        password = self.password_input.text()

        # Hash the password for security
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Use controller method to validate login
        if c.validate_admin_login(username, hashed_password):
            self.accept()  # Close dialog and return QDialog.Accepted
        else:
            # Show error message
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setFocus()