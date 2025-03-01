import mysql.connector
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

class DatPhong(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/DatPhong.ui", self)
        self.show()

if __name__ == "__main__":
    app = QApplication([])
    ui = DatPhong()
    app.exec_()