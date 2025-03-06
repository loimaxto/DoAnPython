from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from app import Ui_MainWindow
# from view.phong_va_giaphong.ql_phong_handle import ql_phong
import sys
import os
# Thêm thư mục cha vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'phong_va_giaphong')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ql_dichvu')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tai_khoan')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'login')))
from ql_phong_handle import ql_phong
from ql_gia_phong_handle import gia_phong
from ql_dichvu_handle import ql_dichvu_handle
from tai_khoan_handle import tai_khoan
from KLogin import Login

class mainApp(Ui_MainWindow):
    def __init__(self, mainWindow):
        # self.log = Login()
        # self.log.show()
        # bắt buộc đăng nhập
        # while(self.log.checkOk==False):
        #     if self.log.checkOk==True:
        #         self.hide()
        #         break

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
    
    def get_dang_nhap(self, dn):
        self.taikhoan.user_id = dn.us_id
        self.taikhoan.user_name = dn.us_name
        self.taikhoan.nv_id = dn.nv_id
        self.taikhoan.nv_name = dn.nv_name
        self.taikhoan.nv_email = dn.nv_email
        self.taikhoan.nv_sdt = dn.nv_sdt
        self.taikhoan.nv_diachi = dn.nv_diachi
        self.taikhoan.nv_chucvu = dn.nv_chucvu

    #         nv_email = ""
    # nv_sdt = ""
    # nv_diachi = ""
    # nv_chucvu = ""



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainApp(MainWindow)
    log = Login()
    log.show()
    ui.get_dang_nhap(log)
    MainWindow.show()
    sys.exit(app.exec())