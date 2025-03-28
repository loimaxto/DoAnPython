import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication
import sqlite3

from view.statistics.statistics_ui import Ui_StatisticsMainWindow
from view.statistics.overall_statistics_handle import OverallStatisticsWindow
class StatisticsMainWindow(QtWidgets.QWidget,Ui_StatisticsMainWindow):
    def __init__(self):      
        super().__init__()
        self.ui = Ui_StatisticsMainWindow()
        self.setupUi(self)
        self.ui.setupUi(self)
        
        # khai báo trang mới
        # self.kh_page = CustomerManagementWindow()
        # self.dp_page = DatPhongWindow()
        # self.nv_page = StaffManagementWindow()
        # self.dv_page = ql_dichvu_ui()
        # self.phong_gia_page = phong_giaphong_ui()
        # self.tk_page = None
        self.overall_page = OverallStatisticsWindow()
        # thêm trang mới vào menumenu
        # self.ui.stackedWidget.addWidget(self.dp_page)
        # self.ui.stackedWidget.addWidget(self.kh_page)
        # self.ui.stackedWidget.addWidget(self.nv_page)
        # self.ui.stackedWidget.addWidget(self.dv_page)
        # self.ui.stackedWidget.addWidget(self.phong_gia_page)
        # self.ui.stackedWidget.setCurrentWidget(self.kh_page)
        self.ui.stackedWidget.addWidget(self.overall_page)
        self.ui.stackedWidget.setCurrentWidget(self.overall_page)
        # lập trình chuyển trang
        # self.ui.nhanVienBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.nv_page))
        # self.ui.khachHangBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.kh_page))
        # self.ui.datPhongBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.dp_page))
        # self.ui.dichVuBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.dv_page))
        # self.ui.phongGiaBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.phong_gia_page))
        # self.ui.taiKhoanBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.tk_page))
        self.ui.TongQuanBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.overall_page))
        # self.ui.dangXuatBtn.clicked.connect(self.DangNhap)

        # self.show()
    

        # đăng nhập
        # self.tk = dangnhap(self)
    
    # hàm chuyển cửa sổ
    # def DangNhap(self):
    #     self.hide()
    #     self.tk.username.setText("")
    #     self.tk.password.setText("")
    #     # self.tk.show()
        



        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StatisticsMainWindow()
    window.show()
    sys.exit(app.exec())