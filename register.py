import re
import logging
import sys
from PyQt6 import QtCore, QtGui, QtWidgets

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="auth_combined.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Import POSApp (from main.py) only when needed
POSApp = None

class Ui_LoginDialog(object):
    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("LoginDialog")
        Dialog.resize(1100, 650)  # Increased width for two panels
        Dialog.setStyleSheet("background-color: #2b576d;")

        # Main layout
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(30)

        # === Left Panel: Login/Register Form ===
        self.panel = QtWidgets.QWidget()
        self.panel.setStyleSheet("background-color: rgb(96, 150, 186); border-radius: 10px;")
        self.panel.setObjectName("panel")
        self.panel.setFixedSize(340, 500)

        panel_layout = QtWidgets.QVBoxLayout(self.panel)
        panel_layout.setContentsMargins(20, 20, 20, 20)
        panel_layout.setSpacing(10)

        # Stack Widget for switching views
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.stackedWidget.setFixedWidth(300)
        self.stackedWidget.setFixedHeight(450)

        # === Login Page ===
        self.loginPage = QtWidgets.QWidget()
        self.setupLoginPage()
        self.stackedWidget.addWidget(self.loginPage)

        # === Register Page ===
        self.registerPage = QtWidgets.QWidget()
        self.setupRegisterPage()
        self.stackedWidget.addWidget(self.registerPage)

        panel_layout.addWidget(self.stackedWidget)

        # Switch Button
        self.btn_switch = QtWidgets.QPushButton("Need an account? Register")
        self.btn_switch.setStyleSheet("color: white; background-color: rgb(39, 76, 119); padding: 5px; font-size: 9pt;")
        self.btn_switch.clicked.connect(self.toggleView)
        panel_layout.addWidget(self.btn_switch, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Add left panel to main layout
        main_layout.addWidget(self.panel)

        # === Right Panel: Password Requirements Guide ===
        self.right_panel = QtWidgets.QWidget()
        self.right_panel.setFixedWidth(320)
        self.right_panel.setStyleSheet("background-color: #3a6d8c; border-radius: 10px;")
        right_layout = QtWidgets.QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(20, 40, 20, 20)
        right_layout.setSpacing(15)

        # Title Label
        title_label = QtWidgets.QLabel("Password Requirements")
        title_label.setStyleSheet("color: white; font-size: 14pt; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(title_label)

        # Requirement Labels
        self.requirements = {
            "length": QtWidgets.QLabel("❌ At least 8 characters"),
            "uppercase": QtWidgets.QLabel("❌ At least one uppercase letter"),
            "lowercase": QtWidgets.QLabel("❌ At least one lowercase letter"),
            "digit": QtWidgets.QLabel("❌ At least one number"),
            "special": QtWidgets.QLabel("❌ At least one special character")
        }

        for label in self.requirements.values():
            label.setStyleSheet("color: red; font-size: 10pt;")
            right_layout.addWidget(label)

        # Add stretch to push everything up
        right_layout.addStretch()

        # Add right panel to main layout
        main_layout.addWidget(self.right_panel)

        Dialog.setLayout(main_layout)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def setupLoginPage(self):
        layout = QtWidgets.QVBoxLayout()

        # Username
        self.lbl_username_login = QtWidgets.QLabel("Username:")
        self.lbl_username_login.setStyleSheet("color: white; font-weight: bold;")
        self.txt_username_login = QtWidgets.QLineEdit()
        self.txt_username_login.setStyleSheet("background-color: white; color: black; padding: 5px;")
        layout.addWidget(self.lbl_username_login)
        layout.addWidget(self.txt_username_login)

        # Password
        self.lbl_password_login = QtWidgets.QLabel("Password:")
        self.lbl_password_login.setStyleSheet("color: white; font-weight: bold;")
        self.txt_password_login = QtWidgets.QLineEdit()
        self.txt_password_login.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txt_password_login.setStyleSheet("background-color: white; color: black; padding: 5px;")
        layout.addWidget(self.lbl_password_login)
        layout.addWidget(self.txt_password_login)

        # Login Button
        self.btn_login = QtWidgets.QPushButton("Login")
        self.btn_login.setStyleSheet("background-color: rgb(39, 76, 119); color: white; padding: 6px;")
        self.btn_login.clicked.connect(self.login)
        layout.addWidget(self.btn_login)

        # Status Label
        self.lbl_status_login = QtWidgets.QLabel("")
        self.lbl_status_login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_status_login.setStyleSheet("color: white;")
        layout.addWidget(self.lbl_status_login)

        self.loginPage.setLayout(layout)

    def setupRegisterPage(self):
        layout = QtWidgets.QVBoxLayout()

        # Username
        self.lbl_username_register = QtWidgets.QLabel("Username:")
        self.lbl_username_register.setStyleSheet("color: white; font-weight: bold;")
        self.txt_username_register = QtWidgets.QLineEdit()
        self.txt_username_register.setStyleSheet("background-color: white; color: black; padding: 5px;")
        layout.addWidget(self.lbl_username_register)
        layout.addWidget(self.txt_username_register)

        # Password
        self.lbl_password_register = QtWidgets.QLabel("Password:")
        self.lbl_password_register.setStyleSheet("color: white; font-weight: bold;")
        self.txt_password_register = QtWidgets.QLineEdit()
        self.txt_password_register.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txt_password_register.setStyleSheet("background-color: white; color: black; padding: 5px;")
        layout.addWidget(self.lbl_password_register)
        layout.addWidget(self.txt_password_register)

        # Confirm Password
        self.lbl_confirm_register = QtWidgets.QLabel("Confirm Password:")
        self.lbl_confirm_register.setStyleSheet("color: white; font-weight: bold;")
        self.txt_confirm_register = QtWidgets.QLineEdit()
        self.txt_confirm_register.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txt_confirm_register.setStyleSheet("background-color: white; color: black; padding: 5px;")
        layout.addWidget(self.lbl_confirm_register)
        layout.addWidget(self.txt_confirm_register)

        # Register Button
        self.btn_register = QtWidgets.QPushButton("Register")
        self.btn_register.setStyleSheet("background-color: rgb(39, 76, 119); color: white; padding: 6px;")
        self.btn_register.clicked.connect(self.register)
        layout.addWidget(self.btn_register)

        # Status Label
        self.lbl_status_register = QtWidgets.QLabel("")
        self.lbl_status_register.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_status_register.setStyleSheet("color: white;")
        layout.addWidget(self.lbl_status_register)

        self.registerPage.setLayout(layout)

        # Connect signal for real-time validation
        self.txt_password_register.textChanged.connect(self.update_requirements)

    def update_requirements(self):
        password = self.txt_password_register.text()

        checks = {
            "length": len(password) >= 8,
            "uppercase": re.search(r"[A-Z]", password) is not None,
            "lowercase": re.search(r"[a-z]", password) is not None,
            "digit": re.search(r"[0-9]", password) is not None,
            "special": re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is not None
        }

        for key, met in checks.items():
            label = self.requirements[key]
            text = label.text().split(" ", 1)[1]  # Keep rule part
            label.setText(f"{'✅' if met else '❌'} {text}")
            label.setStyleSheet("color: green;" if met else "color: red; font-size: 10pt;")

    def toggleView(self):
        current_index = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(1 if current_index == 0 else 0)
        self.btn_switch.setText("Back to Login" if current_index == 0 else "Need an account? Register")

    def is_strong_password(self, password):
        return (
            len(password) >= 8 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"[0-9]", password) and
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
        )

    def login(self):
        username = self.txt_username_login.text().strip()
        password = self.txt_password_login.text().strip()

        valid_user = "admin"
        valid_password = "Admin123!"

        if not username or not password:
            self.lbl_status_login.setStyleSheet("color: red;")
            self.lbl_status_login.setText("Both fields are required.")
            logging.warning("Empty login attempt.")
            return

        if username == valid_user and password == valid_password:
            self.lbl_status_login.setStyleSheet("color: lightgreen;")
            self.lbl_status_login.setText("Login successful!")
            QtCore.QTimer.singleShot(500, self.open_pos_window)
        else:
            self.lbl_status_login.setStyleSheet("color: red;")
            self.lbl_status_login.setText("Invalid credentials.")
            logging.warning(f"Failed login attempt: {username}")

    def register(self):
        username = self.txt_username_register.text().strip()
        password = self.txt_password_register.text().strip()
        confirm = self.txt_confirm_register.text().strip()

        if not username or not password or not confirm:
            self.lbl_status_register.setStyleSheet("color: red;")
            self.lbl_status_register.setText("All fields are required.")
            logging.warning("Empty registration attempt.")
            return

        if password != confirm:
            self.lbl_status_register.setStyleSheet("color: red;")
            self.lbl_status_register.setText("Passwords do not match.")
            logging.warning(f"Password mismatch during registration for {username}")
            return

        if not self.is_strong_password(password):
            self.lbl_status_register.setStyleSheet("color: orange;")
            self.lbl_status_register.setText("Password does not meet complexity requirements.")
            logging.warning(f"Weak password used by {username}.")
            return

        existing_users = ["admin"]
        if username in existing_users:
            self.lbl_status_register.setStyleSheet("color: red;")
            self.lbl_status_register.setText("Username already exists.")
            logging.warning(f"Duplicate username attempted: {username}")
            return

        self.lbl_status_register.setStyleSheet("color: lightgreen;")
        self.lbl_status_register.setText("Registration successful!")
        logging.info(f"User registered successfully: {username}")
        QtCore.QTimer.singleShot(1500, lambda: self.stackedWidget.setCurrentIndex(0))

    def open_pos_window(self):
        self.dialog.close()
        global POSApp
        if POSApp is None:
            try:
                from main import POSApp
            except ImportError as e:
                self.lbl_status_login.setStyleSheet("color: red;")
                self.lbl_status_login.setText("Error loading POS.")
                logging.error(f"Error importing POSApp: {str(e)}")
                return

        self.pos_window = POSApp()
        self.pos_window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_LoginDialog()
    ui.setupUi(dialog)
    dialog.setWindowTitle("7/11 Login / Register")
    dialog.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()