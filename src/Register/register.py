from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QIntValidator


Qss = '''\
QLabel{
outline: none;
}
'''


class RegisterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet(Qss)
        self.__layout = QVBoxLayout()
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.__layout)
        # ascii regex validator, only ascii code can use as name or password
        self.stuNumberValidator = QRegularExpressionValidator(
            QRegularExpression(
                r'\d{6}'
            )
        )
        self.ascii_regex = QRegularExpression("[\x00-\x7f]{8,18}")
        self.ascii_regex_validator = QRegularExpressionValidator(self.ascii_regex)
        self.setUI()

    def setUI(self):
        # username input
        self.userLabel = QLabel("Student Number")
        self.userLine = QLineEdit(self)
        self.userLine.setValidator(self.stuNumberValidator)
        # set validator
        self.__layout.addWidget(self.userLabel)
        self.__layout.addWidget(self.userLine)
        # password input
        self.passwdLabel = QLabel("Password")
        self.passwdLine = QLineEdit(self)
        # set validator
        self.passwdLine.setValidator(self.ascii_regex_validator)
        self.passwdLine.setEchoMode(QLineEdit.EchoMode.Password)
        self.__layout.addWidget(self.passwdLabel)
        self.__layout.addWidget(self.passwdLine)
        self.rePasswdLabel = QLabel("Re-enter Password")
        self.rePasswdLine = QLineEdit(self)
        """
        repassword connect to detect
        """
        self.rePasswdLine.editingFinished.connect(
            self.__verifyPassword
        )
        # set validator
        self.rePasswdLine.setValidator(self.ascii_regex_validator)
        self.rePasswdLine.setEchoMode(QLineEdit.EchoMode.Password)
        self.__layout.addWidget(self.rePasswdLabel)
        self.__layout.addWidget(self.rePasswdLine)
        # error password
        self.errorLabel = QLabel()
        self.__layout.addWidget(self.errorLabel)
        """
        realname and phone number layout
        """
        self.rpn = QGridLayout()
        self.realNameLabel = QLabel("Real Name")
        self.realNameLine = QLineEdit()
        #
        self.phoneNumberLabel = QLabel("Phone Number")
        self.phoneNumberLine = QLineEdit()
        self.rpn.addWidget(self.realNameLabel, 0, 0, 1, 1)
        self.rpn.addWidget(self.phoneNumberLabel, 0, 1, 1, 1)
        self.rpn.addWidget(self.realNameLine, 1, 0, 1, 1)
        self.rpn.addWidget(self.phoneNumberLine, 1, 1, 1, 1)
        self.__layout.addLayout(self.rpn)
        # register button
        self.registerButton = QPushButton("Register")
        self.__layout.addWidget(self.registerButton)

    def __verifyPassword(self):
        firstPassword = self.passwdLine.text()
        secondPassword = self.rePasswdLine.text()
        print(firstPassword, secondPassword)
        if firstPassword == secondPassword:
            self.errorLabel.setText("Same Password")
        else:
            self.errorLabel.setText("Different Password")
