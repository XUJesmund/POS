import re
import logging
from PyQt6 import QtCore, QtGui, QtWidgets
import sys, json, bcrypt, time


logging.basicConfig(
    filename='login_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_action(message):
    logging.info(message)


CREDENTIALS_FILE = "users.json"
MAX_ATTEMPTS = 3

def verify_user(username, password):
    try:
        with open(CREDENTIALS_FILE, "r") as f:
            users = json.load(f)
        if username in users:
            stored_hash = users[username].encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
        return False
    except Exception:
        return False

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
        Dialog.resize(1100, 650)
        Dialog.setStyleSheet("background-color: #007359;")

        # Main layout
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # === Left Panel: Login/Register Form ===
        self.panel = QtWidgets.QWidget()
        self.panel.setStyleSheet("""
            background-color: #007350;
            border-radius: 15px;
            padding: 10px;
        """)
        self.panel.setObjectName("panel")
        self.panel.setFixedSize(340, 600)


        panel_layout = QtWidgets.QVBoxLayout(self.panel)
        panel_layout.setContentsMargins(10, 10, 10, 10)
        panel_layout.setSpacing(10)

        # Logo Section
        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setFixedHeight(80)

        # Placeholder for logo image
        try:
            self.logo_pixmap = QtGui.QPixmap("711_logo.png")
            if not self.logo_pixmap.isNull():
                self.logo_label.setPixmap(self.logo_pixmap.scaled(
                    self.logo_label.size(),
                    QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                    QtCore.Qt.TransformationMode.SmoothTransformation
                ))
        except Exception as e:
            self.logo_label.setText("7/11 Logo Here")
            self.logo_label.setStyleSheet("color: white; font-size: 16pt; font-weight: bold;")
            self.logo_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        panel_layout.addWidget(self.logo_label)

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
        self.btn_switch.setStyleSheet("""
            color: red;
            background-color: white;
            padding: 6px;
            font-size: 9pt;
            border: 2px solid red;
            border-radius: 5px;
        """)
        self.btn_switch.clicked.connect(self.toggleView)
        panel_layout.addWidget(self.btn_switch, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        # Add panel to main layout
        main_layout.addWidget(self.panel)






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
        self.btn_login.setStyleSheet("""
            background-color: white;
            color: #007350;
            padding: 6px;
            font-weight: bold;
            border: 2px solid #007350;
            border-radius: 5px;
        """)
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

        # Password Requirements Guide (✅ This is new!)
        self.lbl_password_guide = QtWidgets.QLabel(
            "Password must be at least 8 characters and include:\n"
            "- Uppercase letter\n"
            "- Lowercase letter\n"
            "- Number\n"
            "- Special character (!@#$...)"
        )
        self.lbl_password_guide.setStyleSheet("color: lightgray; font-size: 8pt;")
        self.lbl_password_guide.setWordWrap(True)
        layout.addWidget(self.lbl_password_guide)

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
        self.btn_register.setStyleSheet("""
            background-color: white;
            color: #007350;
            padding: 6px;
            font-weight: bold;
            border: 2px solid #007350;
            border-radius: 5px;
        """)
        self.btn_register.clicked.connect(self.register)
        layout.addWidget(self.btn_register)

        # Status Label
        self.lbl_status_register = QtWidgets.QLabel("")
        self.lbl_status_register.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_status_register.setStyleSheet("color: white;")
        layout.addWidget(self.lbl_status_register)

        self.registerPage.setLayout(layout)

    def toggleView(self):
        current_index = self.stackedWidget.currentIndex()
        self.stackedWidget.setCurrentIndex(1 if current_index == 0 else 0)
        self.btn_switch.setText("Back to Login" if current_index == 0 else "Need an account? Register")

    def is_strong_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):  # At least one uppercase
            return False
        if not re.search(r"[a-z]", password):  # At least one lowercase
            return False
        if not re.search(r"[0-9]", password):  # At least one digit
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Special character
            return False
        return True

    def login(self):
        username = self.txt_username_login.text().strip()
        password = self.txt_password_login.text().strip()

        valid_user = "admin"
        valid_password = "Admin123!"

        if not username or not password:
            self.lbl_status_login.setStyleSheet("color: yellow;")
            self.lbl_status_login.setText("Both fields are required.")
            logging.warning("Empty login attempt.")
            return

        if username == valid_user and password == valid_password:
            self.lbl_status_login.setStyleSheet("color: lightgreen;")
            self.lbl_status_login.setText("Login successful!")
            QtCore.QTimer.singleShot(500, self.open_pos_window)
        else:
            self.lbl_status_login.setStyleSheet("color: yellow;")
            self.lbl_status_login.setText("Invalid credentials.")
            logging.warning(f"Failed login attempt: {username}")

    def register(self):
        username = self.txt_username_register.text().strip()
        password = self.txt_password_register.text().strip()
        confirm = self.txt_confirm_register.text().strip()

        if not username or not password or not confirm:
            self.lbl_status_register.setStyleSheet("color: yellow;")
            self.lbl_status_register.setText("All fields are required.")
            logging.warning("Empty registration attempt.")
            return

        if password != confirm:
            self.lbl_status_register.setStyleSheet("color: yellow;")
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
            self.lbl_status_register.setStyleSheet("color: yellow;")
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
                self.lbl_status_login.setStyleSheet("color: yellow;")
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
    dialog.setWindowTitle("7/11 Login")
    dialog.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
