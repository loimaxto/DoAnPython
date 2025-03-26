import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication
from view.Menu.page1 import Page1
from view.Menu.page2 import Page2
from view.ql_dichvu import ql_dichvu_handle
import sqlite3

# class MainWindow(QtWidgets.QMainWindow):
from view.qlnhansu.nv_handle import StaffManagementWindow
from view.khach_hang.kh_handle import CustomerManagementWindow
from view.DatPhong.handle_dat_phong import DatPhongWindow
from view.Menu.menu_ui import Ui_MainWindow
from view.ql_dichvu.ql_dichvu_handle import ql_dichvu_ui
from view.phong_va_giaphong.ql_gia_phong_handle import gia_phong
# from view.phong_va_giaphong.ql_phong_handle import ql_phong
from view.tai_khoan.tai_khoan_handle import tai_khoan
from view.phong_va_giaphong.phong_giaphong_handle import phong_giaphong_ui
from view.login.dangnhap_handle import dangnhap

class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # khai báo trang mới
        self.kh_page = CustomerManagementWindow()
        self.dp_page = DatPhongWindow()
        self.nv_page = StaffManagementWindow()
        self.dv_page = ql_dichvu_ui()
        self.phong_gia_page = phong_giaphong_ui()
        self.tk_page = tai_khoan()
        
        # thêm trang mới vào menumenu
        self.ui.stackedWidget.addWidget(self.dp_page)
        self.ui.stackedWidget.addWidget(self.kh_page)
        self.ui.stackedWidget.addWidget(self.nv_page)


        self.ui.stackedWidget.addWidget(self.dv_page)
        self.ui.stackedWidget.addWidget(self.phong_gia_page)
        self.ui.stackedWidget.addWidget(self.tk_page)
        

        self.ui.stackedWidget.setCurrentWidget(self.kh_page)
        
        # lập trình chuyển trang
        self.ui.nhanVienBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.nv_page))
        self.ui.khachHangBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.kh_page))
        self.ui.datPhongBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.dp_page))
        self.ui.dichVuBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.dv_page))
        self.ui.phongGiaBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.phong_gia_page))
        self.ui.taiKhoanBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.tk_page))

        self.ui.dangXuatBtn.clicked.connect(self.DangNhap)

        self.show()
    

        # đăng nhập
        # self.tk = dangnhap(self)
    
    # hàm chuyển cửa sổ
    def DangNhap(self):
        self.hide()
        self.tk.username.setText("")
        self.tk.password.setText("")
        # self.tk.show()
        



        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec())