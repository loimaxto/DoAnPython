import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication
from view.Menu.page1 import Page1
from view.Menu.page2 import Page2
from view.ql_dichvu import ql_dichvu_handle
from view.ql_dichvu.ql_dichvu import Ui_Form 
# class MainWindow(QtWidgets.QMainWindow):

from view.khach_hang.kh_handle import CustomerManagementWindow
from view.DatPhong.handle_dat_phong import DatPhongWindow
from view.Menu.menu_ui import Ui_MainWindow
class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # khai báo trang mới
        self.kh_page = CustomerManagementWindow()
        self.dp_page = DatPhongWindow()

        self.dvForm =  QtWidgets.QWidget()
        self.dv_page_ui = ql_dichvu_handle(self.dvForm)
        
        # thêm trang mới vào menumenu
        self.ui.stackedWidget.addWidget(self.dp_page)
        self.ui.stackedWidget.addWidget(self.kh_page)
        self.ui.stackedWidget.addWidget(self.dvForm)


        self.ui.stackedWidget.setCurrentWidget(self.kh_page)
        
        # lập trình chuyển trang
        self.ui.khachHangBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.kh_page))
        self.ui.datPhongBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.dp_page))
        self.ui.dichVuBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.dvForm))

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())