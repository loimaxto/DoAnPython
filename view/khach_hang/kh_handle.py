import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_path)
print(project_path)
import random
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (
    
    QMessageBox,QRadioButton,QWidget,QHBoxLayout
)
from view.khach_hang.kh_ui import Ui_CustomerManagement # Assuming you saved the UI as kh_ui.py
from PyQt6.QtCore import Qt

from dto.dto import KhachHangDTO
from dao.khach_hang_dao import KhachHangDAO
from view.khach_hang.radiobutton import RadioButtonDelegate

class CustomerManagementWindow(QtWidgets.QWidget, Ui_CustomerManagement):
    def __init__(self, mainwindow):
        super().__init__()
        self.setupUi(self)
        self.dao_customer = KhachHangDAO()
        self.par = mainwindow
        
        # Thêm cột radio button (cột đầu tiên)
        self.model = QtGui.QStandardItemModel(0, 5)  # rows, columns (radio + ID + name + phone + image)
        self.model.setHorizontalHeaderLabels(["Chọn", "ID", "Họ và tên", "Số điện thoại", "Hình ảnh"])
        self.customerTableView.setModel(self.model)
        
        
        # Thiết lập delegate cho cột radio button
        self.customerTableView.setItemDelegateForColumn(0, RadioButtonDelegate(self.customerTableView))
        
        # Resize columns
        self.customerTableView.setColumnWidth(0, 50)  # Cột radio button
        self.customerTableView.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)  # ID
        self.customerTableView.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeMode.Stretch)  # Tên
        self.customerTableView.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)  # SĐT
        self.customerTableView.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)  # Hình ảnh
        
        self.customerTableView.verticalHeader().setVisible(False) 
        self.customerTableView.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.customerTableView.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self.customerTableView.selectionModel().selectionChanged.connect(self.row_selected_action)
        self.selected_customer = None
        # Load data
        self.load_fake_data()
        
        # Kết nối các nút
        self.addButton.clicked.connect(self.add_customer)
        self.updateButton.clicked.connect(self.update_customer)
        self.deleteButton.clicked.connect(self.delete_customer)
        self.clearButton.clicked.connect(self.clear_fields)
        self.searchButton.clicked.connect(self.search_customers)
        self.btn_confirm_update.clicked.connect(self.update_confirmed)
        self.btn_confirm_update.setVisible(False)
        
        self.is_update_state = 0
        self.selected_customer_id = None
        self.model.itemChanged.connect(self.handle_item_changed)
    #click path hiện hình ảnh
    
    def handle_item_changed(self, item):
        """Xử lý khi trạng thái của item thay đổi"""
        # Chỉ xử lý cho cột radio button (cột 0)
        if item.column() == 0 and item.isCheckable():
            row = item.row()
            
            # Nếu radio button được chọn
            if item.checkState() == Qt.CheckState.Checked:
                # Lưu thông tin khách hàng được chọn
                self.selected_customer = KhachHangDTO(
                    kh_id=self.model.item(row, 1).text(),
                    ten=self.model.item(row, 2).text(),
                    sdt=self.model.item(row, 3).text(),
                    image=self.model.item(row, 4).text()
                )
                print(self.selected_customer)
                # Cập nhật form
                self.update_form_with_selected_customer()
                
                # Bỏ chọn tất cả các radio button khác
                self.unselect_other_radios(row)
            else:
                # Nếu bỏ chọn radio button
                if self.selected_customer and self.selected_customer.kh_id == self.model.item(row, 1).text():
                    self.selected_customer = None
                    self.clear_form()
    
    def unselect_other_radios(self, selected_row):
        """Bỏ chọn tất cả radio button ngoại trừ hàng được chỉ định"""
        for row in range(self.model.rowCount()):
            if row != selected_row:
                item = self.model.item(row, 0)
                if item.checkState() == Qt.CheckState.Checked:
                    item.setCheckState(Qt.CheckState.Unchecked)
    
    def load_fake_data(self, search_term=None):
        """Tải dữ liệu khách hàng từ database"""
        self.selected_customer = None
        if search_term:
            customers = [self.dao_customer.get_khach_hang_by_id(search_term)]
        else:    
            customers = self.dao_customer.get_all_khach_hang()
        self.model.setRowCount(0)
        
        for row_index, row_data in enumerate(customers):
            # Tạo item cho cột radio button (cột 0)
            radio_item = QtGui.QStandardItem()
            radio_item.setCheckable(True)
            radio_item.setEditable(False)
            radio_item.setSelectable(False)
            radio_item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
            self.model.setItem(row_index, 0, radio_item)
            
            # Các cột thông tin
            self.model.setItem(row_index, 1, QtGui.QStandardItem(str(row_data.kh_id)))
            self.model.setItem(row_index, 2, QtGui.QStandardItem(row_data.ten))
            self.model.setItem(row_index, 3, QtGui.QStandardItem(row_data.sdt))
            self.model.setItem(row_index, 4, QtGui.QStandardItem(row_data.image))
            
            # Căn giữa nội dung các cột
            for col in range(1, 5):
                self.model.item(row_index, col).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_form_with_selected_customer(self):
        """Cập nhật form với thông tin khách hàng được chọn"""
        if self.selected_customer:
            self.nameLineEdit.setText(self.selected_customer.ten)
            self.phoneLineEdit.setText(self.selected_customer.sdt)
            self.label_imagePath.setText(self.selected_customer.image)

    def clear_form(self):
        """Xóa thông tin trên form"""
        self.nameLineEdit.clear()
        self.phoneLineEdit.clear()
        self.label_imagePath.clear()
    def on_radio_changed(self, state, row):
        if state == Qt.CheckState.Checked:
            # Bỏ chọn tất cả các radio button khác
            for i in range(self.model.rowCount()):
                if i != row:
                    self.model.item(i, 0).setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
            
            # Lưu ID khách hàng được chọn
            self.selected_customer_id = self.model.item(row, 1).text()
            
            # Hiển thị thông tin khách hàng lên form
            self.nameLineEdit.setText(self.model.item(row, 2).text())
            self.phoneLineEdit.setText(self.model.item(row, 3).text())
            self.label_imagePath.setText(self.model.item(row, 4).text())
    
       
    def add_customer(self):
        # giới hạn quyền
        try:
            if self.par.acc == 1:
                self.par.gioi_han_quyen()
                return
            # Add fake customer data
            new_id = self.dao_customer.get_khach_hang_next_id()
            new_name = self.nameLineEdit.text()
            new_phone = self.phoneLineEdit.text()
            new_image = self.label_imagePath.text() or "None"
            if not new_name or not new_phone:
                QMessageBox.information(self, "Cảnh báo", "Vui lòng điền đầy đủ thông tin khách hàng!")
                return
        except Exception as e:
            QMessageBox.critical(self,"cảnh báo",f"lỗi: {e}")
            return
        #stored_file = self.store_image(new_image, new_id)
        #if not stored_file:
        #    QMessageBox.critical(self,  "Lỗi", "Không thể lưu hình ảnh")
        #    return

        try:
            obj_kh = KhachHangDTO(kh_id=None, ten=new_name, sdt=new_phone,image="None")
            self.dao_customer.insert_khach_hang(obj_kh)
            
        except Exception as e:
            QMessageBox.critical(self,  "Lỗi", f"Không thể lưu thông tin khách hàng: {e}")
            return
        QMessageBox.information(self, "Thêm khách hàng", "Thông tin khách hàng đã được lưu thành công!")
        self.clear_fields()
        self.load_fake_data()
    def row_selected_action(self):
        if self.is_update_state:
            selected_indexes = self.customerTableView.selectionModel().selectedIndexes()
            if selected_indexes:
                row = selected_indexes[0].row()
                self.nameLineEdit.setText(self.model.item(row, 2).text())
                self.phoneLineEdit.setText(self.model.item(row, 3).text())
                self.dto_kh = KhachHangDTO(
                    self.model.item(row, 1).text(),
                    self.model.item(row, 2).text(),
                    self.model.item(row, 3).text(),
                    self.model.item(row, 4).text())
            
    def update_customer(self):
        try:    # giới hạn quyền
            if self.par.acc == 1:
                self.par.gioi_han_quyen()
                return
            self.is_update_state = 1 - self.is_update_state
            palette = self.btn_confirm_update.palette()
            if self.is_update_state == 1:
                self.btn_confirm_update.setVisible(True)
                palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor("blue"))
                selected_indexes = self.customerTableView.selectionModel().selectedIndexes()
                self.imageButton.setVisible(False)
                self.label_imagePath.setText("Không sửa ảnh")
                
                    # self.model.setItem(row, 3, QtGui.QStandardItem(self.imagePathLabel.text()))
            else:
                self.exit_update_state()
        except Exception as e:
            QMessageBox(self,"cảnh báo",f"lỗi: {e}")
            return 
    def update_confirmed(self):
        try:
            if not self.selected_customer:
                QMessageBox.warning(self, "Cảnh báo", "Hãy chọn một khách hàng để cập nhập thông tin")
                return

            try:   
                self.selected_customer.kh_id = 1
                self.selected_customer.ten = self.nameLineEdit.text()
                self.selected_customer.sdt = self.phoneLineEdit.text()
                self.dao_customer.update_khach_hang(self.selected_customer)
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể cập nhật thông tin khách hàng: {e}")
                return

            self.exit_update_state()
            self.load_fake_data()
        except Exception as e:
            QMessageBox(self,"cảnh báo",f"lỗi: {e}")
            return 
    def exit_update_state(self):
        self.btn_confirm_update.setVisible(False)
        self.imageButton.setVisible(True)
        self.label_imagePath.setText("")
        self.clear_fields()
        
    
    def delete_customer(self):
        # giới hạn quyền
        if self.par.acc == 1:
            self.par.gioi_han_quyen()
            return
        selected_indexes = self.selected_customer
        if selected_indexes:
            reply = QMessageBox.question(
            self,
            'Xác nhận',
            f'Bạn có chắc chắn muốn xóa dữ liệu khách hàng?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return
            deleted_id = selected_indexes.kh_id
            if deleted_id:
                try:
                    self.dao_customer.delete_khach_hang(int(deleted_id))
                    self.load_fake_data()
                    self.clear_fields()
                    QMessageBox.information(self, "Xóa thành công", f"Xóa khách hàng: {selected_indexes.ten}")
                except Exception as e:
                    QMessageBox.critical(self,  "Lỗi", f"Không thể xóa khách hàng: {e}")
            else:
                QMessageBox.critical(self,  "Lỗi", "Không thể xóa khách hàng: ID không hợp lệ")
        else:
            QMessageBox.information(self, "Cảnh báo", "Hãy chọn một khách hàng trước khi xóa!")

    def clear_fields(self):
        self.nameLineEdit.clear()
        self.phoneLineEdit.clear()
        self.label_imagePath.setText("None")

    def select_image(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.label_imagePath.setText(file_path)

    def search_customers(self):
        
        search_term = self.searchLineEdit.text().strip()
        if search_term!="":    
            try:
                if search_term.isdigit():
                    print(search_term,type(search_term))
                    self.load_fake_data(int(search_term))
                else:
                    QMessageBox.critical(self,  "ID không hợp lệ", "ID phải là số")
                    return
            except Exception as e:
                self.load_fake_data()
                QMessageBox.critical(self,  "ID không hợp lệ", "Hiện tại không tồn tại khách hàng này")
                return
        else:
            self.load_fake_data()
    def store_image(self,selected_path,customer_id):
        if selected_path:
            file_name = "customer_" + str(customer_id)
            storage_path = os.path.join(project_path, "data\\customer_image")
            if not os.path.exists(storage_path):
                os.makedirs(storage_path)
            destination_path = os.path.join(storage_path, file_name)
            try:
                with open(selected_path, 'rb') as source_file, open(destination_path, 'wb') as destination_file:
                    destination_file.write(source_file.read())

                # QMessageBox.information(self, "Image Stored", f"Image stored successfully")
                self.label_imagePath.clear()
                return file_name
            except Exception as e:
                QMessageBox.critical(self,  "Lỗi", f"Không thể lưu ảnh: {e}")
        else:
            QMessageBox.warning(self, "Cảnh báo", "Không có ảnh nào được chọn.")
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CustomerManagementWindow(app)
    window.show()
    sys.exit(app.exec())

# def store_image(selected_path,customer_id):
#         if selected_path:
#             file_name = os.path.basename(selected_path)
#             storage_path = os.path.join(project_path, "data\\customer_image")
#             if not os.path.exists(storage_path):
#                 os.makedirs(storage_path)
#                 print("create")
#             else:
#                 print("folder da ton tai")
#             # destination_path = os.path.join(storage_folder, file_name)
#             print(storage_path)
# # store_image("asd","a")
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))