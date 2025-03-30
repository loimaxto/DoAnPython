from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget
import os
import sys
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
from view.khach_hang.kh_form_ui import Ui_khform
from recogni_face.models import FaceRecognitionWidget
from view.khach_hang.kh_handle import CustomerManagementWindow
class kh_form_handle(QWidget,Ui_khform):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.customer = CustomerManagementWindow()
        
        self.stackedWidget.addWidget(self.customer)
        
       
        self.stackedWidget.setCurrentWidget(self.customer)
        
        self.customer.imageButton.clicked.connect(lambda:self.star_getImage())
        
    def back_customer(self):
        
        self.find_face.closeEvent()
        self.stackedWidget.setCurrentWidget(self.customer)
    def star_getImage(self):
        self.find_face  = FaceRecognitionWidget()
        self.stackedWidget.addWidget(self.find_face)
        self.a = self.find_face.setup_ui()
        self.find_face.set_customer_id(4)
        #self.find_face.setup_ui()
        self.find_face.back_btn.clicked.connect(lambda: self.back_customer())
        self.stackedWidget.setCurrentWidget(self.find_face)
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    ui = kh_form_handle()
    ui.show()
    sys.exit(app.exec())
