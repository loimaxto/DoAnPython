from PyQt6 import QtCore, QtGui, QtWidgets
from tai_khoan import Ui_Form
import sqlite3

class tai_khoan(Ui_Form):
    def __init__(self, Form):
        self.setupUi(Form)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = tai_khoan(Form)
    Form.show()
    sys.exit(app.exec())