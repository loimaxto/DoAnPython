import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication
from view.Menu.page1 import Page1
from view.Menu.page2 import Page2
from view.ql_dichvu import ql_dichvu_handle

# class MainWindow(QtWidgets.QMainWindow):
from view.qlnhansu.nv_handle import StaffManagementWindow
from view.khach_hang.kh_handle import CustomerManagementWindow
from view.DatPhong.handle_dat_phong import DatPhongWindow
from view.Menu.menu_ui import Ui_MainWindow
class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.kh_page = CustomerManagementWindow()
        self.dp_page = DatPhongWindow()
        self.nv_page = StaffManagementWindow()
        
        self.ui.stackedWidget.addWidget(self.dp_page)
        self.ui.stackedWidget.addWidget(self.kh_page)
        self.ui.stackedWidget.addWidget(self.nv_page)


        
        self.ui.stackedWidget.setCurrentWidget(self.kh_page)
        
        self.ui.khachHangBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.kh_page))
        self.ui.datPhongBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.dp_page))
        self.ui.nhanVienBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.nv_page))


        

    def switch_page(self, index):
        self.ui.stackedWidget.setCurrentIndex(index)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())