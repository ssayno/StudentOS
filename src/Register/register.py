from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QGridLayout,
    QGraphicsDropShadowEffect, QHBoxLayout
)
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator, QColor, QPalette, QValidator
import os
from Student.settings import QSS

class RegisterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        registerQss = os.path.join(
            QSS, 'register.css'
        )
        with open(registerQss) as f:
            self.setStyleSheet(f.read())
        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(4, 0, 4, 0)
        self.__layout.setSpacing(3)
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.__layout)
        """
        global variable
        """
        # map qlineedit with qlabel
        self.pls = {}
        # crate validator
        self.create_validator()
        # set ui usage
        self.setUI()
        # connect signal
        self.connect_signal_with_slot_func()

    def setUI(self):
        # Register banner
        self.registerBanner = QLabel("Register")
        self.registerBanner.setObjectName("register-banner")
        bannerGraphics = QGraphicsDropShadowEffect()
        bannerGraphics.setColor(QColor("#FC0"))
        bannerGraphics.setOffset(1, 0)
        bannerGraphics.setBlurRadius(10)
        self.registerBanner.setGraphicsEffect(bannerGraphics)
        self.__layout.addWidget(self.registerBanner)
        # username input
        self.userLabel = QLabel("Student Number")
        self.userLine = QLineEdit(self)
        self.userErrorLabel = QLabel()
        self.userErrorLabel.setObjectName("info-label")
        # set validator
        self.__layout.addWidget(self.userLabel)
        self.__layout.addWidget(self.userLine)
        self.__layout.addWidget(self.userErrorLabel)
        # password input
        self.passwdLabel = QLabel("Password")
        self.passwdLine = QLineEdit(self)
        self.passwdErrorLabel = QLabel()
        self.passwdErrorLabel.setObjectName("info-label")
        self.passwdLine.setEchoMode(QLineEdit.EchoMode.Password)
        self.__layout.addWidget(self.passwdLabel)
        self.__layout.addWidget(self.passwdLine)
        self.__layout.addWidget(self.passwdErrorLabel)
        self.rePasswdLabel = QLabel("Re-enter Password")
        self.rePasswdLine = QLineEdit(self)

        self.rePasswdLine.setEchoMode(QLineEdit.EchoMode.Password)
        self.__layout.addWidget(self.rePasswdLabel)
        self.__layout.addWidget(self.rePasswdLine)
        # error password
        self.rePErrorLabel = QLabel()
        self.rePErrorLabel.setObjectName("info-label")
        self.__layout.addWidget(self.rePErrorLabel)
        """
        realname and phone number layout
        """
        self.rpn = QGridLayout()
        self.realNameLabel = QLabel("Real Name")
        self.realNameLine = QLineEdit()
        self.reaNameErrorLabel = QLabel()
        self.reaNameErrorLabel.setObjectName("info-label")
        #
        self.phoneNumberLabel = QLabel("Phone Number")
        self.phoneNumberLine = QLineEdit()
        self.phoneNumberErrorLabel = QLabel()
        self.phoneNumberErrorLabel.setObjectName("info-label")
        self.rpn.addWidget(self.realNameLabel, 0, 0, 1, 1)
        self.rpn.addWidget(self.phoneNumberLabel, 0, 1, 1, 1)
        self.rpn.addWidget(self.realNameLine, 1, 0, 1, 1)
        self.rpn.addWidget(self.phoneNumberLine, 1, 1, 1, 1)
        self.rpn.addWidget(self.reaNameErrorLabel, 2, 0, 1, 1)
        self.rpn.addWidget(self.phoneNumberErrorLabel, 2, 1, 1, 1)
        self.__layout.addLayout(self.rpn)
        # progress label
        """
        create progress bar
        """
        phbox = QHBoxLayout()
        phbox.setContentsMargins(0, 0, 0, 0)

        for qLine in self.findChildren(QLineEdit):
            qLabel = QLabel()
            qLabel.setFixedHeight(6)
            qLabel.setAutoFillBackground(True)
            qLabel.setObjectName("progress-label")
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor('white'))
            qLabel.setPalette(palette)
            self.pls[qLine] = qLabel
            phbox.addWidget(qLabel)
        self.__layout.addLayout(phbox)
        # register button
        lg_layout = QHBoxLayout()
        lg_layout.setContentsMargins(0, 0, 0, 0)
        self.registerButton = QPushButton("Register")
        self.loginButton = QPushButton("Login")
        lg_layout.addWidget(self.registerButton, 5)
        lg_layout.addWidget(self.loginButton, 2)
        self.__layout.addLayout(lg_layout)

    def create_validator(self):
        # ascii regex validator, only ascii code can use as name or password
        self.stuNumberValidator = QRegularExpressionValidator(
            QRegularExpression(
                r'\d{6}'
            )
        )
        #
        self.ascii_regex = QRegularExpression("[\x00-\x7f]{8,18}")
        self.ascii_regex_validator = QRegularExpressionValidator(self.ascii_regex)
        #
        self.phoneNumberValidator = QRegularExpressionValidator(
            QRegularExpression(
                r'\d{11}'
            )
        )
        #
        self.name_validator = QRegularExpressionValidator(
            QRegularExpression(
                r'\w{6,20}'
            )
        )

    def connect_signal_with_slot_func(self):
        # connect user line with slot func
        self.userLine.editingFinished.connect(
            self.__stuNumberConnect
        )
        #
        self.passwdLine.editingFinished.connect(
            self.__firstPasswordConnect
        )
        #
        self.rePasswdLine.editingFinished.connect(
            self.__verifyPassword
        )
        #
        self.phoneNumberLine.editingFinished.connect(
            self.__phoneNumberConnect
        )
        #
        self.realNameLine.editingFinished.connect(
            self.__realNameConnect
        )

    def __stuNumberConnect(self):
        text = self.userLine.text()
        palette = QPalette()
        state = self.stuNumberValidator.validate(text, 0)[0]
        if state == QValidator.State.Acceptable:
            self.userErrorLabel.clear()
            palette.setColor(QPalette.ColorRole.Window, QColor('green'))
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor('white'))
            self.userErrorLabel.setText("Not validator input, must be six digits")
        self.pls[self.userLine].setPalette(palette)

    def __firstPasswordConnect(self):
        text = self.passwdLine.text()
        palette = QPalette()
        state = self.ascii_regex_validator.validate(text, 0)[0]
        if state == QValidator.State.Acceptable:
            self.passwdErrorLabel.clear()
            palette.setColor(QPalette.ColorRole.Window, QColor('green'))
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor('white'))
            self.passwdErrorLabel.setText("Ascii character with length 8 to 18")
        self.pls[self.passwdLine].setPalette(palette)

    def __verifyPassword(self):
        firstPassword = self.passwdLine.text()
        secondPassword = self.rePasswdLine.text()
        palette = QPalette()
        state = self.ascii_regex_validator.validate(secondPassword, 0)[0]
        if state == QValidator.State.Acceptable:
            self.passwdErrorLabel.clear()
            if firstPassword == secondPassword:
                self.rePErrorLabel.clear()
                palette.setColor(QPalette.ColorRole.Window, QColor('green'))
            else:
                palette.setColor(QPalette.ColorRole.Window, QColor('white'))
                self.rePErrorLabel.setText("Different Password")
        else:
            self.rePErrorLabel.setText("Ascii character with length 8 to 18")
        self.pls[self.rePasswdLine].setPalette(palette)

    def __realNameConnect(self):
        text = self.realNameLine.text()
        palette = QPalette()
        state = self.name_validator.validate(text, 0)[0]
        if state == QValidator.State.Acceptable:
            self.reaNameErrorLabel.clear()
            palette.setColor(QPalette.ColorRole.Window, QColor('green'))
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor('white'))
            self.reaNameErrorLabel.setText("Ascii code with length form 6 to 20")
        self.pls[self.realNameLine].setPalette(palette)

    def __phoneNumberConnect(self):
        text = self.phoneNumberLine.text()
        palette = QPalette()
        state = self.phoneNumberValidator.validate(text, 0)[0]
        if state == QValidator.State.Acceptable:
            self.phoneNumberErrorLabel.clear()
            palette.setColor(QPalette.ColorRole.Window, QColor('green'))
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor('white'))
            self.phoneNumberErrorLabel.setText("Eleven digits")
        self.pls[self.phoneNumberLine].setPalette(palette)





