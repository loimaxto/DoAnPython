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


from dto.dto import KhachHangDTO
from dao.khach_hang_dao import KhachHangDAO
class CustomerManagementWindow(QtWidgets.QWidget, Ui_CustomerManagement):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dao_customer = KhachHangDAO()
        
        self.model = QtGui.QStandardItemModel(0, 4)  # rows, columns
        self.model.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Image"])
        self.customerTableView.setModel(self.model)
        # Resize columns
        self.customerTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.customerTableView.verticalHeader().setVisible(False) 
        self.customerTableView.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.customerTableView.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        # Load fake data
        self.load_fake_data()

       
        # Connect buttons to functions
        self.addButton.clicked.connect(self.add_customer)
        self.updateButton.clicked.connect(self.update_customer)
        self.deleteButton.clicked.connect(self.delete_customer)
        self.clearButton.clicked.connect(self.clear_fields)
        self.imageButton.clicked.connect(self.select_image)
        self.searchButton.clicked.connect(self.search_customers)
        self.btn_confirm_update.clicked.connect(self.update_confirmed)
        self.btn_confirm_update.setVisible(False)
        
        self.is_update_state = 0
    def load_fake_data(self, search_term=None):
        customer_data = self.dao_customer.get_all_khach_hang()
        table_data = [(kh.kh_id, kh.ten, kh.sdt, kh.image) for kh in customer_data]
        
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
            

    def add_customer(self):
        # Add fake customer data
        new_id = self.dao_customer.get_khach_hang_next_id()
        new_name = self.nameLineEdit.text()
        new_phone = self.phoneLineEdit.text()
        new_image = self.label_imagePath.text()
        if not new_name or not new_image:
            QMessageBox.information(self, "Warning", "Please fill in all fields")
            return

        stored_file = self.store_image(new_image, new_id)
        if not stored_file:
            QMessageBox.critical(self,  "Error", "Failed to store image")
            return

        try:
            obj_kh = KhachHangDTO(kh_id=None, ten=new_name, sdt=new_phone, image=stored_file)
            self.dao_customer.insert_khach_hang(obj_kh)
        except Exception as e:
            QMessageBox.critical(self,  "Error", f"Failed to add customer: {e}")
            return
        QMessageBox.information(self, "Add customer", "Customer added successfully")
        self.clear_fields()
        self.load_fake_data()

    def update_customer(self):
        self.is_update_state = 1 - self.is_update_state
        palette = self.btn_confirm_update.palette()
        if self.is_update_state == 1:
            self.btn_confirm_update.setVisible(True)
            palette.setColor(QtGui.QPalette.ColorRole.Button, QtGui.QColor("blue"))
            selected_indexes = self.customerTableView.selectionModel().selectedIndexes()
            self.imageButton.setVisible(False)
            self.label_imagePath.setText("Không sửa ảnh")
            if selected_indexes:
                row = selected_indexes[0].row()
                self.nameLineEdit.setText(self.model.item(row, 1).text())
                self.phoneLineEdit.setText(self.model.item(row, 2).text())
                self.dto_kh = KhachHangDTO(
                    int(self.model.item(row, 0).text()),
                    self.model.item(row, 1).text(),
                    self.model.item(row, 2).text(),
                    self.model.item(row, 3).text())
                # self.model.setItem(row, 3, QtGui.QStandardItem(self.imagePathLabel.text()))
        else:
            self.exit_update_state()
                
    def update_confirmed(self):
        if not self.dto_kh:
            QMessageBox.warning(self, "Warning", "No customer selected for update")
            return

        try:
            print(self.dto_kh)
            self.dao_customer.update_khach_hang(self.dto_kh)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update customer: {e}")
            return

        self.exit_update_state()
        self.load_fake_data()
        
    def exit_update_state(self):
        self.btn_confirm_update.setVisible(False)
        self.imageButton.setVisible(True)
        self.label_imagePath.setText("")
        self.clear_fields()
        
    
    def delete_customer(self):
        selected_indexes = self.customerTableView.selectionModel().selectedIndexes()
        if selected_indexes and selected_indexes[0].row() >= 0:
            deleted_id = self.model.itemFromIndex(selected_indexes[0]).text()
            if deleted_id:
                try:
                    self.dao_customer.delete_khach_hang(int(deleted_id))
                    self.load_fake_data()
                    QMessageBox.information(self, "Xóa thành công", f"Xóa khách hàng: {self.model.itemFromIndex(selected_indexes[1]).text()}")
                except Exception as e:
                    QMessageBox.critical(self,  "Error", f"Failed to delete customer: {e}")
            else:
                QMessageBox.critical(self,  "Error", "Failed to delete customer: invalid ID")
        else:
            QMessageBox.information(self, "Warning", "Please select a customer to delete")

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
                QMessageBox.critical(self,  "Error", f"Failed to store image: {e}")
        else:
            QMessageBox.warning(self, "Warning", "No image selected.")
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CustomerManagementWindow()
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