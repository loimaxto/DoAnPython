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
from view.qlnhansu.nv_ui import Ui_StaffManagement # Assuming you saved the UI as kh_ui.py


from dto.dto import NhanVienDTO
from dao.nhan_vien_dao import NhanVienDAO
class StaffManagementWindow(QtWidgets.QWidget, Ui_StaffManagement):
    def __init__(self, mainwindow):
        super().__init__()
        self.setupUi(self)
        self.dao_staff = NhanVienDAO()
        self.dto_nv = None  # Initialize dto_nv to None
        self.par = mainwindow
        
        self.model = QtGui.QStandardItemModel(0, 6)  # rows, columns
        self.model.setHorizontalHeaderLabels(["ID", "Họ và tên", "Số điện thoại", "Email", "Địa chỉ", "Chức vụ"])
        self.staffTableView.setModel(self.model)
        # Resize columns
        self.staffTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.staffTableView.verticalHeader().setVisible(False) 
        self.staffTableView.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.staffTableView.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self.staffTableView.selectionModel().selectionChanged.connect(self.row_selected_action)

        # Load fake data
        self.load_fake_data()

       
        # Connect buttons to functions
        self.addButton.clicked.connect(self.add_staff)
        self.updateButton.clicked.connect(self.update_staff)
        self.deleteButton.clicked.connect(self.delete_staff)
        self.clearButton.clicked.connect(self.clear_fields)
        self.searchButton.clicked.connect(self.search_staffs)
        self.btn_confirm_update.clicked.connect(self.update_confirmed)
        self.btn_confirm_update.setVisible(False)
        
        self.is_update_state = 0
    def load_fake_data(self, search_term=None):
        staff_data = self.dao_staff.get_all_nhan_vien()
        table_data = [(nv.nv_id , nv.ten_nv , nv.sdt , nv.email , nv.dia_chi , nv.chuc_vu) for nv in staff_data]
        
        self.model.setRowCount(0)
        for row in table_data:
            if search_term:
                if search_term.lower() not in row[1].lower() and search_term not in row[2]:
                    continue
            items = []
            for item in row:
                item_obj = QtGui.QStandardItem(str(item))
                item_obj.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item_obj.setFlags(item_obj.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                items.append(item_obj)
            self.model.appendRow(items)
            
       
    def add_staff(self):
        # giới hạn quyền
        if self.par.acc == 1:
            self.par.gioi_han_quyen()
            return
        # Add fake staff data
        new_id = self.dao_staff.get_nhan_vien_next_id()
        new_name = self.nameLineEdit.text()
        new_phone = self.phoneLineEdit.text()
        new_address = self.adressLineEdit.text()
        new_position = self.positionLineEdit.text()
        new_email = self.emailLineEdit.text()
        
        # Check if all fields are filled
        if not new_name or not new_phone or not new_email or not new_address or not new_position:
            QMessageBox.information(self, "Cảnh báo", "Hãy điền đầy đủ thông tin nhân viên!")
            return
        # Check if name is filled
        if self.dao_staff.check_staff_exists(sdt=new_phone, email=new_email):
            QMessageBox.warning(self, "Cảnh báo", "Số điện thoại hoặc email đã tồn tại!")
            return
        # Check if phone number is valid
        if not new_phone.isdigit() or len(new_phone) != 10:
            QMessageBox.warning(self, "Cảnh báo", "Số điện thoại không hợp lệ!")
            return
        # Check if email is valid
        if "@" not in new_email or "." not in new_email.split("@")[-1]:
            QMessageBox.warning(self, "Cảnh báo", "Email không hợp lệ!")
            return

        try:
            obj_nv = NhanVienDTO(nv_id=new_id, ten_nv=new_name, email=new_email, sdt=new_phone, dia_chi=new_address, chuc_vu=new_position)
            self.dao_staff.insert_nhan_vien(obj_nv)
        except Exception as e:
            QMessageBox.critical(self,  "Lỗi", f"Không thể thêm nhân viên: {e}")
            return
        QMessageBox.information(self, "Thêm nhân viên", "Thông tin nhân viên đã được lưu thành công!")
        self.clear_fields()
        self.load_fake_data()
        
    def row_selected_action(self):
        if self.is_update_state:
            selected_indexes = self.staffTableView.selectionModel().selectedIndexes()
            if selected_indexes:
                row = selected_indexes[0].row()
                self.nameLineEdit.setText(self.model.item(row, 1).text())
                self.phoneLineEdit.setText(self.model.item(row, 2).text())
                self.emailLineEdit.setText(self.model.item(row, 3).text())
                self.adressLineEdit.setText(self.model.item(row, 4).text())
                self.positionLineEdit.setText(self.model.item(row, 5).text())
                self.dto_nv = NhanVienDTO(
                    self.model.item(row, 0).text(),
                    self.model.item(row, 1).text(),
                    self.model.item(row, 2).text(),
                    self.model.item(row, 4).text(),
                    self.model.item(row, 5).text())
    def update_staff(self):
        # giới hạn quyền
        if self.par.acc == 1:
            self.par.gioi_han_quyen()
            return
        self.is_update_state = 1 - self.is_update_state
        palette = self.btn_confirm_update.palette()
        if self.is_update_state == 1:
            self.btn_confirm_update.setVisible(True)
            palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor("blue"))
            selected_indexes = self.staffTableView.selectionModel().selectedIndexes()
            
                # self.model.setItem(row, 3, QtGui.QStandardItem(self.imagePathLabel.text()))
        else:
            self.exit_update_state()
                
    def update_confirmed(self):
        if not self.dto_nv:
            QMessageBox.warning(self, "Cảnh báo", "Hãy chọn nhân viên để cập nhật thông tin!")
            return

        try:   
            new_name = self.nameLineEdit.text()
            new_phone = self.phoneLineEdit.text()
            new_email = self.emailLineEdit.text()
            new_address = self.adressLineEdit.text()
            new_position = self.positionLineEdit.text()
            self.dto_nv.ten_nv = new_name
            self.dto_nv.sdt = new_phone
            self.dto_nv.email = new_email
            self.dto_nv.chuc_vu = new_position
            self.dto_nv.dia_chi = new_address

            # Check if all fields are filled
            if not new_name or not new_phone or not new_email or not new_address or not new_position:
                QMessageBox.information(self, "Cảnh báo", "Hãy điền đầy đủ thông tin nhân viên!")
                return
            # Check if phone number or email already exists
            if self.dao_staff.check_staff_exists(sdt=new_phone, email=new_email):
                QMessageBox.warning(self, "Cảnh báo", "Số điện thoại hoặc email đã tồn tại!")
                return
            # Check if phone number is valid
            if not new_phone.isdigit() or len(new_phone) != 10:
                QMessageBox.warning(self, "Cảnh báo", "Số điện thoại không hợp lệ!")
                return
            # Check if email is valid
            if "@" not in new_email or "." not in new_email.split("@")[-1]:
                QMessageBox.warning(self, "Cảnh báo", "Email không hợp lệ!")
                return
            self.dao_staff.update_nhan_vien(self.dto_nv)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể cập nhật thông tin nhân viên: {e}")
            return

        self.exit_update_state()
        self.load_fake_data()
        
    def exit_update_state(self):
        self.btn_confirm_update.setVisible(False)
        self.clear_fields()
        
    
    def delete_staff(self):
        # giới hạn quyền
        if self.par.acc == 1:
            self.par.gioi_han_quyen()
            return
        selected_indexes = self.staffTableView.selectionModel().selectedIndexes()
        if selected_indexes and selected_indexes[0].row() >= 0:
            deleted_id = self.model.itemFromIndex(selected_indexes[0]).text()
            if deleted_id:
                try:
                    self.dao_staff.delete_nhan_vien(int(deleted_id))
                    self.load_fake_data()
                    QMessageBox.information(self, "Xóa thành công", f"Xóa nhân viên: {self.model.itemFromIndex(selected_indexes[1]).text()}")
                except Exception as e:
                    QMessageBox.critical(self,  "Lỗi", f"Không thể xóa nhân viên: {e}")
            else:
                QMessageBox.critical(self,  "Lỗi", "Không thể xóa nhân viên: ID không hợp lệ!")
        else:
            QMessageBox.information(self, "Cảnh báo", "Hãy chọn một nhân viên trước khi xóa!")
        self.load_fake_data()

    def clear_fields(self):
        self.nameLineEdit.clear()
        self.phoneLineEdit.clear()

    def search_staffs(self):
        search_term = self.searchLineEdit.text()
        self.load_fake_data(search_term)
    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StaffManagementWindow()
    window.show()
    sys.exit(app.exec())

# def store_image(selected_path,staff_id):
#         if selected_path:
#             file_name = os.path.basename(selected_path)
#             storage_path = os.path.join(project_path, "data\\staff_image")
#             if not os.path.exists(storage_path):
#                 os.makedirs(storage_path)
#                 print("create")
#             else:
#                 print("folder da ton tai")
#             # destination_path = os.path.join(storage_folder, file_name)
#             print(storage_path)
# # store_image("asd","a")
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))