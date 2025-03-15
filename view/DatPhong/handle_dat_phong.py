
import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_path)
print(project_path)

from PyQt6 import QtWidgets, QtCore, QtGui
from view.DatPhong.dat_phong_ui import Ui_dat_phong

from dao.khach_hang_dao import KhachHangDAO
class DatPhongWindow(QtWidgets.QWidget, Ui_dat_phong):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DatPhongWindow()
    window.show()
    sys.exit(app.exec())# dat la dat ten