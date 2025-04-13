import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import (QTableWidgetItem, QMessageBox, QRadioButton, 
                             QWidget, 
                            QHBoxLayout)
from view.check_in.checkin_ui import Ui_Checkin
import sqlite3
from recogni_face.useModels import FaceRecognitionWidget
query_full_khach_hang = "SELECT * FROM khach_hang "
query_full_room = "SELECT * FROM phong "
class Checkin(QtWidgets.QWidget, Ui_Checkin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.id = []
        # chỉnh sửa table đẹp hơn
        self.view_customer.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.view_customer.verticalHeader().setVisible(False)
        self.view_room.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.view_room.verticalHeader().setVisible(False)

        # kết nối db
        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cursor = self.conn.cursor()
        #hiển thị tất cả khách hàng và phòng
        self.show_customer(query_full_khach_hang)
        self.show_room(query_full_room)
        # Sự kiện
        self.pushButton.clicked.connect(self.search_items)
        self.reset_btn.clicked.connect(self.reset_interface)
        self.checkin_button.clicked.connect(self.start_checkin)
        # Tạo button group cho radio buttons
        
    def reset_interface(self):
        self.show_customer(query_full_khach_hang)
        self.show_room(query_full_room)
        self.search_customer.clear()
        self.search_name.clear()
        self.search_room.clear()
        
    def show_customer(self, query, param=()):
        try:
            self.cursor.execute(query, param)
            data = self.cursor.fetchall()
            
            # Xóa các radio button cũ
            for button in self.radio_group.buttons():
                self.radio_group.removeButton(button)
            
            # Thiết lập số cột (thêm 1 cột cho radio button)
            self.view_customer.setColumnCount(5)  # 1 radio + 4 cột dữ liệu
            self.view_customer.setHorizontalHeaderLabels(["Chọn", "ID", "Họ tên",
                                                         "Số điện thoại", "Image"])
            self.view_customer.setRowCount(0)
            
            for row_index, row_data in enumerate(data):
                self.view_customer.insertRow(row_index)
                
                # Thêm radio button
                radio = QRadioButton()
                self.radio_group.addButton(radio, row_index)  # Gán ID bằng số dòng
                
                # Tạo widget chứa radio button (để căn giữa)
                radio_widget = QWidget()
                layout = QHBoxLayout(radio_widget)
                layout.addWidget(radio)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                radio_widget.setLayout(layout)
                
                self.view_customer.setCellWidget(row_index, 0, radio_widget)
                
                # Thêm dữ liệu vào các cột còn lại
                for col in range(4):  # 4 cột dữ liệu (ID, Họ tên, SĐT, Image)
                    item = QTableWidgetItem(str(row_data[col]))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.view_customer.setItem(row_index, col + 1, item)  # +1 vì cột đầu là radio
                    
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu khách hàng: {str(e)}")
    def show_room(self,query,param=()):
        self.cursor.execute(query,param)
        data = self.cursor.fetchall()
        self.view_room.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.view_room.insertRow(row_index)
            for column_index, item_data in enumerate(row_data):
                self.view_room.setItem(row_index, column_index, QTableWidgetItem(str(item_data)))
    def find_customer(self,id_room):
        self.show_customer(f"{query_full_khach_hang} kh\
                            JOIN dat_phong dp ON kh.kh_id=dp.kh_id\
                            JOIN phong ph ON ph.id=dp.phong_id\
                            where ph.id=?",(id_room,))
    def find_room(self,id_cus):
        self.show_room(f"{query_full_room} ph\
                            JOIN dat_phong dp ON ph.id=dp.phong_id\
                            JOIN khach_hang kh ON kh.kh_id=dp.kh_id\
                            where kh.kh_id=?",(id_cus,))
    def room_from_name(self,name):
        self.show_room(f"{query_full_room} ph\
                            JOIN dat_phong dp ON ph.id=dp.phong_id\
                            JOIN khach_hang kh ON kh.kh_id=dp.kh_id\
                            where ten LIKE ?", (f"%{name}%",))
    def search_items(self):
        id_cus = self.search_customer.text()
        name = self.search_name.text()
        id_room = self.search_room.text()
        try:
            # Tìm kiếm khách hàng
            if id_cus:
                self.show_customer(f"{query_full_khach_hang} WHERE kh_id=?", (id_cus,))
                self.find_room(id_cus)
            elif name:
                self.show_customer(f"{query_full_khach_hang} WHERE ten LIKE ?", (f"%{name}%",))
                self.room_from_name(name)
            # Tìm kiếm phòng
            elif id_room:
                self.show_room("SELECT * FROM phong WHERE id=?", (id_room,))
                self.find_customer(id_room)
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra khi tìm kiếm: {str(e)}")
    def start_checkin(self):
        # Lấy ID của radio button được chọn (-1 nếu không có radio nào được chọn)
        selected_row = self.radio_group.checkedId()
        
        if selected_row == -1:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một khách hàng")
            return
        
        # Lấy dữ liệu từ dòng được chọn
        customer_id = self.view_customer.item(selected_row, 1).text()  # Cột ID (index 1)
        customer_name = self.view_customer.item(selected_row, 2).text()  # Cột Họ tên (index 2)
        customer_phone = self.view_customer.item(selected_row, 3).text()  # Cột Số điện thoại (index 3)
        
        # Hiển thị thông tin khách hàng được chọn
        self.recognition_face = FaceRecognitionWidget(customer_id)
        self.verticalLayout_2.addWidget(self.recognition_face)
        self.recognition_face.show()
        # TODO: Thêm logic check-in ở đây
        self.view_customer.hide()
        self.view_room.hide()
        # Ví dụ: self.process_checkin(customer_id)
        self.checkin_button.hide()
        self.recognition_face.btn_back.clicked.connect(self.backward)
    def backward(self):
        self.recognition_face.hide()
        self.verticalLayout_2.removeWidget(self.recognition_face)
        
        self.recognition_face.closeEvent()
        self.view_customer.show()
        self.view_room.show()
        self.checkin_button.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Checkin()
    ui.show()
    sys.exit(app.exec())