import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication
from view.Menu.page1 import Page1
from view.Menu.page2 import Page2
from view.ql_dichvu import ql_dichvu_handle
import sqlite3

# class MainWindow(QtWidgets.QMainWindow):
from view.qlnhansu.nv_handle import StaffManagementWindow
from view.khach_hang.kh_form_handle import kh_form_handle
from view.DatPhong.handle_dat_phong import DatPhongWindow
from view.Menu.menu_ui import Ui_MainWindow
from view.ql_dichvu.ql_dichvu_handle import ql_dichvu_ui
from view.phong_va_giaphong.ql_gia_phong_handle import gia_phong
# from view.phong_va_giaphong.ql_phong_handle import ql_phong
from view.tai_khoan.tai_khoan_handle import tai_khoan
from view.phong_va_giaphong.phong_giaphong_handle import phong_giaphong_ui
from view.login.dangnhap_handle import dangnhap
from view.check_in.checkin_handle import Checkin
from view.hoadon.hoadon_handle import hoadon
from view.DatPhong.handle_dat_phong import DatPhongWindow
from view.statistics.statistics_handle import StatisticsMainWindow
from view.datphong2.datphong2_handle import DatPhong2
class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    acc = 0 # acc = 0 nếu chưa login, =1 nếu login tk thường, =2 nếu là admin
    def __init__(self):
        
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # đăng nhập

        self.tk = dangnhap(self)
        
        # khai báo trang mới
        self.kh_page = kh_form_handle(self)
        self.phongSuDung_page = DatPhongWindow()
        self.dp_page = DatPhong2()
        self.dp_page = DatPhongWindow()
        self.dp2_page = DatPhong2()
        self.nv_page = StaffManagementWindow(self)
        self.dv_page = ql_dichvu_ui(self)
        self.phong_gia_page = phong_giaphong_ui(self)
        self.checkin_page = Checkin()
        self.hoadon_page = hoadon()
        self.thongke_page = StatisticsMainWindow()
        # thêm trang mới vào menumenu
        self.ui.stackedWidget.addWidget(self.phongSuDung_page)
        self.ui.stackedWidget.addWidget(self.dp_page)
        self.ui.stackedWidget.addWidget(self.kh_page)
        self.ui.stackedWidget.addWidget(self.nv_page)
        self.ui.stackedWidget.addWidget(self.checkin_page)
        self.ui.stackedWidget.addWidget(self.dp2_page)
        self.ui.stackedWidget.addWidget(self.dv_page)
        self.ui.stackedWidget.addWidget(self.phong_gia_page)
        self.ui.stackedWidget.addWidget(self.hoadon_page)
        self.ui.stackedWidget.addWidget(self.thongke_page)
        self.ui.stackedWidget.setCurrentWidget(self.kh_page)
        
        # lập trình chuyển trang
        self.ui.datphongg2_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.dp2_page))
        self.ui.nhanVienBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.nv_page))
        self.ui.khachHangBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.kh_page))
        self.ui.datPhongBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.dp_page))
        self.ui.dichVuBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.dv_page))
        self.ui.phongGiaBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.phong_gia_page))
        self.ui.taiKhoanBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.tk_page))
        self.ui.checkinBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.checkin_page))
        self.ui.hoadon_btn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.hoadon_page))
        self.ui.thongKeBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.thongke_page))
        self.ui.dangXuatBtn.clicked.connect(self.DangNhap)
        self.ui.phongSuDungBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.phongSuDung_page))
        
    
    
    # hàm chuyển cửa sổ
    def DangNhap(self):
        self.hide()
        self.tk.username.setText("")
        self.tk.password.setText("")
        self.tk.show()
    def gioi_han_quyen(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Giới hạn quyền")
        msg.setText("Chức năng này chỉ dành cho quản trị viên")
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.exec()
        



        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MainWindow()
    sys.exit(app.exec())