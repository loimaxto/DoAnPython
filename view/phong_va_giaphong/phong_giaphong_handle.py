from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget
# from phong_giaphong import Ui_Form
from view.phong_va_giaphong.phong_giaphong import Ui_Form
# from ql_phong_handle import ql_phong
from view.phong_va_giaphong.ql_phong_handle import ql_phong
# from ql_gia_phong_handle import gia_phong
from view.phong_va_giaphong.ql_gia_phong_handle import gia_phong

class phong_giaphong_ui(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # khởi tạo trang con
        self.phong = ql_phong()
        self.giaphong = gia_phong()
        # thêm trang con vào giao diện
        self.phong_giaphong.addWidget(self.phong)
        self.phong_giaphong.addWidget(self.giaphong)

        self.phong_giaphong.setCurrentWidget(self.phong)# mặc định ra giao diện quản lý phòng

        # lập trình chuyển trang
        self.phongBtn.clicked.connect(lambda: self.phong_giaphong.setCurrentWidget(self.phong))
        self.giaphongBtn.clicked.connect(lambda: self.phong_giaphong.setCurrentWidget(self.giaphong))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = phong_giaphong_ui()
    ui.show()
    sys.exit(app.exec())