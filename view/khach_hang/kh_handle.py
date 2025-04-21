import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_path)
print(project_path)
import random
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (
    
    QMessageBox,
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

    def load_fake_data(self, search_term=None):
        """Tải dữ liệu khách hàng từ database"""
        customers = self.dao_customer.get_all_khach_hang()
        self.model.setRowCount(0)
        self.model.itemChanged.connect(self.handle_selection_change)
        for row, customer in enumerate(customers):
            # Cột radio button
            radio_item = QtGui.QStandardItem()
            radio_item.setCheckable(True)
            radio_item.setEditable(False)
            radio_item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
            self.model.setItem(row, 0, radio_item)
            
            # Các cột thông tin
            self.model.setItem(row, 1, QtGui.QStandardItem(str(customer.kh_id)))
            self.model.setItem(row, 2, QtGui.QStandardItem(customer.ten))
            self.model.setItem(row, 3, QtGui.QStandardItem(customer.sdt))
            self.model.setItem(row, 4, QtGui.QStandardItem(customer.image))
            
            # Căn giữa nội dung các cột
            for col in range(1, 5):
                self.model.item(row, col).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    def handle_selection_change(self, item):
        """Xử lý khi radio button được chọn/bỏ chọn với cơ chế ổn định"""
        
        # Chỉ xử lý cho cột radio button (cột 0)
        if item.column() != 0 or not item.isCheckable():
            return
        
        # Sử dụng blockSignals để tránh lặp vô hạn
        self.model.blockSignals(True)
        try:
            current_state = item.checkState()
            
            if current_state == Qt.CheckState.Checked:
                # Xử lý khi được chọn
                row = item.row()
                self.selected_customer = KhachHangDTO(
                    kh_id=self.model.item(row, 1).text(),
                    ten=self.model.item(row, 2).text(),
                    sdt=self.model.item(row, 3).text(),
                    image=self.model.item(row, 4).text()
                )
                
                # Cập nhật giao diện
                self.update_form_with_selected_customer()
                
                # Bỏ chọn các radio khác
                self.unselect_other_radios(row)
                
                print(f"Đã chọn khách hàng: {self.selected_customer.ten}")
            else:
                # Xử lý khi bỏ chọn
                if self.selected_customer and self.selected_customer.kh_id == self.model.item(item.row(), 1).text():
                    self.selected_customer = None
                    self.clear_form()
                    print("Đã bỏ chọn khách hàng")
        finally:
            self.model.blockSignals(False)

    def unselect_other_radios(self, selected_row):
        """Bỏ chọn tất cả radio button khác một cách an toàn"""
        for row in range(self.model.rowCount()):
            if row != selected_row:
                item = self.model.item(row, 0)
                if item.checkState() == Qt.CheckState.Checked:
                    item.setCheckState(Qt.CheckState.Unchecked)

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
        if self.par.acc == 1:
            self.par.gioi_han_quyen()
            return
        # Add fake customer data
        new_id = self.dao_customer.get_khach_hang_next_id()
        new_name = self.nameLineEdit.text()
        new_phone = self.phoneLineEdit.text()
        new_image = self.label_imagePath.text() or "không có ảnh"
        if not new_name or not new_phone:
            QMessageBox.information(self, "Cảnh báo", "Vui lòng điền đầy đủ thông tin khách hàng!")
            return

        #stored_file = self.store_image(new_image, new_id)
        #if not stored_file:
        #    QMessageBox.critical(self,  "Lỗi", "Không thể lưu hình ảnh")
        #    return

        try:
            obj_kh = KhachHangDTO(kh_id=None, ten=new_name, sdt=new_phone)
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
        # giới hạn quyền
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
                
    def update_confirmed(self):
        if not self.dto_kh:
            QMessageBox.warning(self, "Cảnh báo", "Hãy chọn một khách hàng để cập nhập thông tin")
            return

        try:   
            self.dto_kh.ten = self.nameLineEdit.text()
            self.dto_kh.sdt = self.phoneLineEdit.text()
            self.dao_customer.update_khach_hang(self.dto_kh)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể cập nhật thông tin khách hàng: {e}")
            return

        self.exit_update_state()
        self.load_fake_data()
        
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
        selected_indexes = self.customerTableView.selectionModel().selectedIndexes()
        if selected_indexes and selected_indexes[0].row() >= 0:
            deleted_id = self.model.itemFromIndex(selected_indexes[0]).text()
            if deleted_id:
                try:
                    self.dao_customer.delete_khach_hang(int(deleted_id))
                    self.load_fake_data()
                    QMessageBox.information(self, "Xóa thành công", f"Xóa khách hàng: {self.model.itemFromIndex(selected_indexes[1]).text()}")
                except Exception as e:
                    QMessageBox.critical(self,  "Lỗi", f"Không thể xóa khách hàng: {e}")
            else:
                QMessageBox.critical(self,  "Lỗi", "Không thể xóa khách hàng: ID không hợp lệ")
        else:
            QMessageBox.information(self, "Cảnh báo", "Hãy chọn một khách hàng trước khi xóa!")

    def clear_fields(self):
        self.nameLineEdit.clear()
        self.phoneLineEdit.clear()
        self.label_imagePath.setText("Không có ảnh")

    def select_image(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.label_imagePath.setText(file_path)

    def search_customers(self):
        search_term = self.searchLineEdit.text()
        self.load_fake_data(search_term)
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