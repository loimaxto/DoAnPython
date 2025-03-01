from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic


class ChiTietHoaDon(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/ChiTietHoaDon.ui", self)
        self.show()

app = QApplication([])
ui = ChiTietHoaDon()
app.exec()