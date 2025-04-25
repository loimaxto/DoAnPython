from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget,QMessageBox
import os
import sys
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
from view.khach_hang.kh_form_ui import Ui_khform
from recogni_face.models import FaceRecognitionWidget
from view.khach_hang.kh_handle import CustomerManagementWindow
from view.khach_hang.image_customer import FaceGalleryWidget
class kh_form_handle(QWidget,Ui_khform):
    def __init__(self,mainwindow):
        super().__init__()
        self.setupUi(self)
        self.customer = CustomerManagementWindow(mainwindow)
        
        self.stackedWidget.addWidget(self.customer)
        self.stackedWidget.setCurrentWidget(self.customer)
        self.customer.imageButton.clicked.connect(lambda:self.star_getImage())
        self.customer.customerTableView.clicked.connect(self.on_table_clicked)
    #hiển thị khách hàng khi bấm vào đường dẫn
    def on_table_clicked(self, index):
        if index.column() == 4:  # Cột hình ảnh
            # Kiểm tra model và item có tồn tại không
            if not self.customer.model or not index.isValid():
                return
                
            # Lấy thông tin từ model
            image_item = self.customer.model.item(index.row(), 4)
            id_item = self.customer.model.item(index.row(), 1)
            name_item = self.customer.model.item(index.row(), 2)
            
            # Kiểm tra các item có tồn tại không
            if not all([image_item, id_item, name_item]):
                QMessageBox.warning(self, "Lỗi", "Không thể lấy thông tin khách hàng")
                return
                
            image_path = image_item.text()
            id_customer = id_item.text()
            name_customer = name_item.text()
            
            try:
                if image_path and image_path.lower() != "none":
                    # Chuyển id_customer sang số nếu cần
                    try:
                        customer_id = int(id_customer)
                    except ValueError:
                        QMessageBox.warning(self, "Lỗi", "ID khách hàng không hợp lệ")
                        return
                        
                    self.imageFace = FaceGalleryWidget(id_customer=customer_id,name_customer=name_customer)
                    self.stackedWidget.addWidget(self.imageFace)
                    self.stackedWidget.setCurrentWidget(self.imageFace)
                    # Sửa kết nối signal để tránh gọi ngay lập tức
                    self.imageFace.back_btn1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.customer))
                else:
                    QMessageBox.information(self, "Thông báo", "Khách hàng chưa lưu hình ảnh")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra: {str(e)}")
    def back_customer(self):
        
        self.find_face.closeEvent()
        self.stackedWidget.setCurrentWidget(self.customer)
    def star_getImage(self):
        print (self.customer.selected_customer)
        
        if self.customer.selected_customer is None:
            self.show_not_selected_warning()
        else:
            self.find_face  = FaceRecognitionWidget()
            self.stackedWidget.addWidget(self.find_face)
            self.a = self.find_face.setup_ui()
            self.find_face.set_customer_id(self.customer.selected_customer.kh_id)
            #self.find_face.setup_ui()
            self.find_face.back_btn.clicked.connect(lambda: self.back_customer())
            self.stackedWidget.setCurrentWidget(self.find_face)
        
        
    def show_not_selected_warning(self):
        """Hiển thị thông báo khi chưa chọn khách hàng"""
        QMessageBox.warning(
            self, 
            "Chưa chọn khách hàng",
            "Vui lòng chọn một khách hàng bằng cách nhấn vào radio button trước khi thực hiện thao tác này!",
            QMessageBox.StandardButton.Ok
        )
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    ui = kh_form_handle()
    ui.show()
    sys.exit(app.exec())
