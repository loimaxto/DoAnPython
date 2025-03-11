import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication
from view.Menu.page1 import Page1
from view.Menu.page2 import Page2
from view.ql_dichvu import ql_dichvu_handle

# class MainWindow(QtWidgets.QMainWindow):

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
        
        self.ui.stackedWidget.addWidget(self.dp_page)
        self.ui.stackedWidget.addWidget(self.kh_page)
        
        self.ui.stackedWidget.setCurrentWidget(self.kh_page)
        
        self.ui.khachHangBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.kh_page))
        self.ui.datPhongBtn.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.dp_page))


        # Create instances of your page widgets
        self.page1 = Page1()
        self.page2 = Page2()
        # self.ql_dichvu = ql_dichvu_handle()

        # Add more page instances

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        # self.stacked_widget.addWidget()

        self.homeBtn = self.findChild(QtWidgets.QPushButton, "datPhongBtn")
        if self.homeBtn:
            self.homeBtn.clicked.connect(lambda: self.switch_page(0))

        self.roomBtn = self.findChild(QtWidgets.QPushButton, "dichVuBtn")
        if self.roomBtn:
            self.roomBtn.clicked.connect(lambda: self.switch_page(2))
        self.show()  # Show the main window

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())