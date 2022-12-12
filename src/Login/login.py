from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QCheckBox, QVBoxLayout, QHBoxLayout, QPushButton
)
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator


Qss = '''\
QLabel{
outline: none;
}
'''


class LoginWidget(QWidget):
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
        self.ascii_regex = QRegularExpression("[\x00-\x7f]+")
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
        ## other
        self.__hbox = QHBoxLayout()
        self.__hbox.setContentsMargins(0, 0, 0, 0)
        # remember me button
        self.rememberButton = QCheckBox("Remember Me!")
        self.__hbox.addWidget(self.rememberButton, 0, Qt.AlignmentFlag.AlignLeft)
        # automatic login button
        self.automaticButton = QCheckBox("Automatic Login!")
        self.automaticButton.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.__hbox.addWidget(self.automaticButton, 0, Qt.AlignmentFlag.AlignLeft)
        #
        self.__layout.addLayout(self.__hbox)
        ## login and register button
        self.lg_layout = QHBoxLayout()
        self.lg_layout.setContentsMargins(0, 0, 0, 0)
        self.loginButton = QPushButton("Login")
        self.registerButton = QPushButton("Register")
        self.lg_layout.addWidget(self.loginButton, 5)
        self.lg_layout.addWidget(self.registerButton, 2)
        self.__layout.addLayout(self.lg_layout)

