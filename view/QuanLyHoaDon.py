import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

class QuanLyHoaDon(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/QuanLyHoaDon.ui", self)
        self.show()

app = QApplication([])
ui = QuanLyHoaDon()
app.exec_()