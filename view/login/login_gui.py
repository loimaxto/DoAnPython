# gui/login_window.py
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from dao.user_dao import UserDAO
from myMain import  MainWindow


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("gui/login_draw.ui", self)  # Load the UI file
        self.setWindowTitle("Login")
        self.user_dao = UserDAO()  # Initialize UserDAO

        # Connect buttons
        self.loginButton = self.findChild(QtWidgets.QPushButton, "loginButton")
        self.registerButton = self.findChild(QtWidgets.QPushButton, "registerButton")

        if self.loginButton:
            self.loginButton.clicked.connect(self.login)
        if self.registerButton:
            self.registerButton.clicked.connect(self.register)

    def login(self):
        username = self.findChild(QtWidgets.QLineEdit, "usernameLineEdit").text()
        password = self.findChild(QtWidgets.QLineEdit, "passwordLineEdit").text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        user = self.user_dao.get_user_by_username(username)

        if user and user.password == password:  # Basic password check (hash for production!)
            QMessageBox.information(self, "Success", f"Login successful! Welcome, {username}!")
            self.open_main_window(user)
            self.close() # Close the login window after successful login
        else:
            QMessageBox.critical(self, "Error", "Invalid username or password.")


    def register(self):
        username = self.findChild(QtWidgets.QLineEdit, "usernameLineEdit").text()
        password = self.findChild(QtWidgets.QLineEdit, "passwordLineEdit").text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password to register.")
            return

        existing_user = self.user_dao.get_user_by_username(username)
        if existing_user:
            QMessageBox.warning(self, "Error", "Username already exists. Please choose another.")
            return

        self.user_dao.create_user(username, password)  # Basic password storage (hash for production!)
        QMessageBox.information(self, "Success", "Registration successful! You can now log in.")


    def open_main_window(self, user):
        self.main_window = MainWindow(user)  # Pass user info to main window
        self.main_window.show()