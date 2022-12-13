import os
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QCheckBox, QVBoxLayout, QHBoxLayout,
    QPushButton, QGraphicsDropShadowEffect, QComboBox
)
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QColor
import pymysql
from Student.settings import QSS


class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        loginQss = os.path.join(
            QSS, 'login.css'
        )
        with open(loginQss) as f:
            self.setStyleSheet(f.read())
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
        # welcome login banner
        self.loginBanner = QLabel("Welcome to login")
        bannerGraphics = QGraphicsDropShadowEffect()
        bannerGraphics.setColor(QColor("#FC0"))
        bannerGraphics.setOffset(1, 0)
        bannerGraphics.setBlurRadius(10)
        self.loginBanner.setGraphicsEffect(bannerGraphics)
        self.__layout.addWidget(self.loginBanner)
        self.loginBanner.setObjectName("login-banner")
        # username input
        self.userLabel = QLabel("Student Number")
        self.userLine = QComboBox()
        self.addLoginedUsers()
        self.userLine.setEditable(True)
        # self.userLine = QLineEdit(self)
        # self.userLine.setPlaceholderText("Six digits")
        # self.userLine.setValidator(self.stuNumberValidator)
        # set validator
        self.__layout.addWidget(self.userLabel)
        self.__layout.addWidget(self.userLine)
        # password input
        self.passwdLabel = QLabel("Password")
        self.passwdLine = QLineEdit(self)
        self.passwdLine.setPlaceholderText("8 to 18 digits")
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

    def addLoginedUsers(self):
        with pymysql.connect(host='localhost',
                                           user='root',
                                           password='271xufei.GMAIL',
                                           database='studentOS',
                                           charset='utf8mb4') as connect:
            cursor = connect.cursor()
            try:
                cursor.execute(
                    'select stuNumber from loginUsers'
                )
                results = cursor.fetchall()
                for result in results:
                    self.userLine.addItem(result[0])
            except:
                print("Showing error when add login user")
            cursor.close()
