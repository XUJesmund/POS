from main import POSApp
from PyQt6 import QtCore, QtGui, QtWidgets
import sys


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(420, 400)
        Dialog.setStyleSheet("background-color: #2b576d;")

        self.loginPanel = QtWidgets.QGroupBox(parent=Dialog)
        self.loginPanel.setGeometry(QtCore.QRect(80, 90, 251, 250))
        self.loginPanel.setStyleSheet("background-color: rgb(96, 150, 186);")
        self.loginPanel.setTitle("")
        self.loginPanel.setObjectName("loginPanel")

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.loginPanel)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 20, 211, 55))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.userName = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.userName.setFont(font)
        self.userName.setStyleSheet("color: white;")
        self.userName.setText("Username:")
        self.verticalLayout_2.addWidget(self.userName)

        self.txt_username = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget_2)
        self.txt_username.setStyleSheet("background-color: white; color: black;")
        self.verticalLayout_2.addWidget(self.txt_username)

        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.loginPanel)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(20, 80, 211, 55))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.passWord = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        font.setPointSize(12)
        font.setBold(True)
        self.passWord.setFont(font)
        self.passWord.setStyleSheet("color: white;")
        self.passWord.setText("Password:")
        self.verticalLayout_3.addWidget(self.passWord)

        self.txt_password = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget_3)
        self.txt_password.setStyleSheet("background-color: white; color: black;")
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.verticalLayout_3.addWidget(self.txt_password)

        self.loginBtn = QtWidgets.QPushButton(parent=self.loginPanel)
        self.loginBtn.setGeometry(QtCore.QRect(80, 150, 93, 28))
        font.setPointSize(10)
        self.loginBtn.setFont(font)
        self.loginBtn.setStyleSheet("background-color: rgb(39, 76, 119); color: white;")
        self.loginBtn.setText("Login")
        self.loginBtn.clicked.connect(self.login)

        self.lbl_status = QtWidgets.QLabel(parent=self.loginPanel)
        self.lbl_status.setGeometry(QtCore.QRect(30, 190, 191, 30))
        self.lbl_status.setFont(QtGui.QFont("Arial", 9))
        self.lbl_status.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_status.setStyleSheet("color: white;")
        self.lbl_status.setText("")

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def login(self):
        username = self.txt_username.text()
        password = self.txt_password.text()

        if username == "admin" and password == "admin123":
            self.lbl_status.setStyleSheet("color: lightgreen;")
            self.lbl_status.setText("Login successful!")

            QtCore.QTimer.singleShot(500, self.open_pos_window)
        else:
            self.lbl_status.setStyleSheet("color: red;")
            self.lbl_status.setText("Invalid username or password.")

    def open_pos_window(self):
        self.dialog.close()
        self.pos_window = POSApp()
        self.pos_window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.setWindowTitle("Login")
    Dialog.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()