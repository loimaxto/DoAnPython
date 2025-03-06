from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from view.app.app import Ui_MainWindow

from view.login.KLogin import Login
from view.phong_va_giaphong.ql_gia_phong_handle import gia_phong
from view.ql_dichvu.ql_dichvu_handle import ql_dichvu_handle
from view.tai_khoan.tai_khoan_handle import tai_khoan
from view.phong_va_giaphong.ql_phong_handle import ql_phong

class mainApp(Ui_MainWindow):
    def __init__(self, mainWindow):

        self.setupUi(mainWindow)

        # khởi tạo các trang giao diện
        self.man_hinh.setCurrentWidget(self.phong_screen)
        self.phong = ql_phong(self.phong_screen)
        self.gia = gia_phong(self.gia_screen)
        self.dichvu = ql_dichvu_handle(self.dichvu_screen)
        self.taikhoan = tai_khoan(self.taikhoan_screen)



        # sự kiện chuyển trang
        self.btn_phong.clicked.connect(lambda: self.chuyen_trang(1))
        self.btn_gia.clicked.connect(lambda: self.chuyen_trang(2))
        self.btn_dichvu.clicked.connect(lambda: self.chuyen_trang(3))
        self.btn_taikhoan.clicked.connect(lambda: self.chuyen_trang(4))



    def chuyen_trang(self, i):
        if i==1:
            self.man_hinh.setCurrentWidget(self.phong_screen)
        elif i==2:
            self.man_hinh.setCurrentWidget(self.gia_screen)
        elif i==3:
            self.man_hinh.setCurrentWidget(self.dichvu_screen)
        elif i==4:
            self.man_hinh.setCurrentWidget(self.taikhoan_screen)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainApp(MainWindow)
    log = Login(ui.taikhoan)
    MainWindow.show()
    log.show()
    sys.exit(app.exec())