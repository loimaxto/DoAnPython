from PyQt6 import QtCore, QtGui, QtWidgets
from view.tai_khoan.tai_khoan import Ui_Form
import sqlite3

class tai_khoan(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    
    def setData(self, row):
        self.user_id = row[0]


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = tai_khoan()
    ui.show()
    sys.exit(app.exec())