from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout


class MainUi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)

    def setUI(self, realname, stuNumber, phoneNumber):
        self.__layout.addWidget(QLabel(realname))
        self.__layout.addWidget(QLabel(stuNumber))
        self.__layout.addWidget(QLabel(phoneNumber))

