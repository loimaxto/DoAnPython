from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic
import mysql.connector

class ChiTietHoaDon(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/ChiTietHoaDon.ui", self)
        self.show()

app = QApplication([])
ui = ChiTietHoaDon()
app.exec_()