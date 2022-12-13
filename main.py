import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox, QLabel
from src.Login.login import LoginWidget
from src.Register.register import RegisterWidget
from src.MainUI.mainui import MainUi
import pymysql
import os
from Student.settings import QSS

class StudentSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        mainQss = os.path.join(
            QSS, 'main.css'
        )
        with open(mainQss, 'r', encoding='U8') as f:
            self.setStyleSheet(f.read())
        self.resize(800, 1000)
        self.cw = QStackedWidget(self)
        self.setCentralWidget(self.cw)
        """
        use pymysql module to connect mysql
        """
        self.sql_connect = pymysql.connect(host='localhost',
                                           user='root',
                                           password='271xufei.GMAIL',
                                           database='studentOS',
                                           charset='utf8mb4')
        self.sql_cursor = self.sql_connect.cursor()
        # add login UI
        self.useLoginWidget()
        # add register UI
        self.useRegisterWidget()
        # add MainUI
        self.useMainUI()

    def useLoginWidget(self):
        self.loginWidget = LoginWidget(self)
        self.loginWidget.automaticButton.stateChanged.connect(
            self.automaticLoginWithRemember
        )
        self.loginWidget.loginButton.clicked.connect(
            self.loginVerify
        )
        # After register button is clicked, switch the register Widget
        self.loginWidget.registerButton.clicked.connect(
            self.switchToRegister
        )
        self.cw.addWidget(self.loginWidget)

    def useRegisterWidget(self):
        self.registerWidget = RegisterWidget(self)
        self.registerWidget.registerButton.clicked.connect(
            self.register
        )
        self.registerWidget.loginButton.clicked.connect(
            self.switchToLogin
        )
        self.cw.addWidget(self.registerWidget)

    def useMainUI(self):
        self.mainui = MainUi(self)
        self.cw.addWidget(self.mainui)

    def switchToRegister(self):
        if hasattr(self, 'registerWidget'):
            self.cw.setCurrentWidget(self.registerWidget)

    def switchToLogin(self):
        if hasattr(self, 'loginWidget'):
            self.cw.setCurrentWidget(self.loginWidget)

    def loginVerify(self):
        stuNumber = self.loginWidget.userLine.lineEdit().text()
        password = self.loginWidget.passwdLine.text()
        try:
            self.sql_cursor.execute(
                'select realname, phonenumber from users where stuNumber=%s and password=%s', (stuNumber, password)
            )
            self.sql_connect.commit()
            result = self.sql_cursor.fetchone()
            if result is None:
                print("User not exist")
            else:
                try:
                    self.sql_cursor.execute(
                        'insert into loginUsers values (%s)', stuNumber
                    )
                    self.sql_connect.commit()
                except:
                    print("When insert into login error")
                    self.sql_connect.rollback()
                self.mainui.setUI(
                    result[0], stuNumber, result[1]
                )
                self.cw.setCurrentWidget(self.mainui)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Sql error", f'{e}')
            self.sql_connect.rollback()

    def automaticLoginWithRemember(self, state):
        # print(state, type(state))
        """
        :param state: 0 unchecked, 1 triple state, 2 checked.
        :return:
        """
        if state == 2:
            self.loginWidget.rememberButton.setChecked(True)
        elif state == 0:
            self.loginWidget.rememberButton.setChecked(False)

    def register(self):
        info_labels = self.registerWidget.findChildren(QLabel, "info-label")
        if all(
                [not info_label.text() for info_label in info_labels]
        ):
            sn = self.registerWidget.userLine.text()
            pw = self.registerWidget.passwdLine.text()
            rn = self.registerWidget.realNameLine.text()
            pn = self.registerWidget.phoneNumberLine.text()
            if sn == "":
                QMessageBox.warning(self, "Invalid register informations", "Here something is error, please check it.")
                return
            self.__register(sn, pw, rn, pn)
        else:
            QMessageBox.warning(self, "Invalid register informations", "Here something is error, please check it.")

    def __register(self, stuNumber, password, realName, phoneNumber):
        try:
            self.sql_cursor.execute(
                'insert into users values (%s, %s, %s, %s)', (stuNumber, password, realName, phoneNumber)
            )
            self.sql_connect.commit()
            self.mainui.setUI(
                realName, stuNumber, phoneNumber
            )
            self.cw.setCurrentWidget(self.mainui)
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Sql error", f'{e}')
            self.sql_connect.rollback()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ss = StudentSystem()
    ss.show()
    sys.exit(app.exec())
