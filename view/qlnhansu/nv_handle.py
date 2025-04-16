import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_path)
print(project_path)
import random
import pandas as pd
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel,QStandardItem
from PyQt6.QtWidgets import (
    QMessageBox,
    QFileDialog,
    QTableWidgetItem,
    QDialog, 
    QVBoxLayout, 
    QLabel, 
    QPushButton, 
    QHBoxLayout
)
import sqlite3
import os
import platform
import subprocess
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
        self.exportExcelBtn.clicked.connect(lambda: self.exportExcel(self.staffTableView))
        self.importExcelBtn.clicked.connect(self.importExcel)


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
            if self.is_update_state:
                selected_indexes = self.staffTableView.selectionModel().selectedIndexes()
            if selected_indexes:
                id = selected_indexes[0].row()
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
            if self.dao_staff.is_duplicate_staff(id+1,sdt=new_phone, email=new_email):
                QMessageBox.warning(self, "Cảnh báo","Số điện thoại hoặc email đã tồn tại!")
                return  # or raise error / show warning
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
        self.emailLineEdit.clear()
        self.adressLineEdit.clear()
        self.positionLineEdit.clear()

    def search_staffs(self):
        search_term = self.searchLineEdit.text()
        self.load_fake_data(search_term)

    def downloadTemplate(self):
        try:
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Lưu file mẫu", "hotel_file_template.xlsx", "Excel Files (*.xlsx);;All Files (*)"
            )
            if not save_path:
                return

            # Dữ liệu mẫu
            columns = ["_id", "hoten", "sodienthoai", "email", "diachi", "chucvu"]
            sample_data = [
                [None, "Nguyễn Văn A", "912345678", "email@example.com", "123 Đường A", "Nhân viên"]
            ]
            df = pd.DataFrame(sample_data, columns=columns)

            # Ghi ra file Excel
            df.to_excel(save_path, index=False)
            QMessageBox.information(self, "✅ Thành công", "Đã tạo file mẫu thành công.")
        except Exception as e:
            QMessageBox.critical(self, "❌ Lỗi", f"Không thể tạo file mẫu: {str(e)}")

    def importExcel(self):
        # Hiển thị câu hỏi trước
        dialog = ExcelChoiceDialog(self)
        result = dialog.exec()

        if result == 2:
            self.downloadTemplate()
            return

        elif result == 1:
            # tiếp tục xử lý import
            ...
        else:
            return  # hủy
        # ======= TIẾP TỤC XỬ LÝ NHẬP EXCEL =======
        try:

            file_path, _ = QFileDialog.getOpenFileName(
                self, "Chọn file Excel", "", "Excel Files (*.xlsx *.xls);;All Files (*)"
            )
            if not file_path:
                return

            # Đọc file
            try:
                df = pd.read_excel(file_path, header=None, dtype={2: str})
                expected_columns = ["_id", "hoten", "sodienthoai", "email", "diachi", "chucvu"]
                df.columns = expected_columns
                df.drop(columns=["_id"], inplace=True)
            except Exception as e:
                raise ValueError(f"Không thể đọc file Excel: {str(e)}")

            # Làm sạch dữ liệu
            df["hoten"] = df["hoten"].astype(str).str.strip()
            df["sodienthoai"] = ("0" + df["sodienthoai"]).astype(str).str.strip()
            df["email"] = df["email"].astype(str).str.strip().str.lower()
            df["diachi"] = df["diachi"].astype(str).str.strip()
            df["chucvu"] = df["chucvu"].astype(str).str.strip()

            # Kiểm tra dữ liệu
            for index, row in df.iterrows():
                if not row["hoten"]:
                    raise ValueError(f"Dòng {index + 1}: Thiếu họ tên.")
                if not row["sodienthoai"] or not row["sodienthoai"].isdigit():
                    raise ValueError(f"Dòng {index + 1}: SĐT không hợp lệ ({row['sodienthoai']}).")
                if not row["email"] or "@" not in row["email"]:
                    raise ValueError(f"Dòng {index + 1}: Email không hợp lệ ({row['email']}).")

            # Lấy dữ liệu sẵn có trong DB
            existing_sdt = set(self.dao_staff.get_all_sodienthoai() or [])
            existing_email = set(self.dao_staff.get_all_email() or [])
            last_id = self.dao_staff.get_last_id() or 0
            new_id = last_id + 1

            inserted, skipped = 0, 0
            dupes = []


            for _, row in df.iterrows():
                sdt = row["sodienthoai"]
                email = row["email"]


                if sdt in existing_sdt or email in existing_email:
                    skipped += 1
                    dupes.append((sdt, email))
                    continue


                try:
                    dto = NhanVienDTO(new_id, row["hoten"], email, sdt, row["diachi"], row["chucvu"])
                    self.dao_staff.insert_nhan_vien(dto)
                    inserted += 1
                    existing_sdt.add(sdt)
                    existing_email.add(email)
                    new_id += 1
                except Exception as e:
                    raise ValueError(f"Lỗi khi thêm {row['hoten']}: {str(e)}")

            # Thông báo kết quả
            if dupes:
                print("⚠️ Các dòng bị bỏ qua do trùng:")
                for sdt, email in dupes:
                    print(f" - {sdt} | {email}")


            QMessageBox.information(
                self,
                "✅ Thành công",
                f"Đã nhập {inserted} nhân viên mới từ Excel.\n"
                f"Bỏ qua {skipped} dòng do trùng SĐT hoặc Email."
            )

            self.load_fake_data()  # Cập nhật UI

        except ValueError as ve:
            QMessageBox.critical(self, "❌ Lỗi", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "❌ Lỗi", f"Lỗi khi nhập dữ liệu từ Excel:\n{str(e)}")


    def exportExcel(self, table_view):
        # Open file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Excel File", "", "Excel Files (*.xlsx);;All Files (*)"
        )

        if not file_path:
            return  # User canceled the save dialog

        # Ensure file has a .xlsx extension
        if not file_path.endswith(".xlsx"):
            file_path += ".xlsx"

        # Get the model from QTableView
        model = table_view.model()
        if not model:
            print("❌ No model found in QTableView!")
            return

        # Extract data from the model
        rows = model.rowCount()
        cols = model.columnCount()

        # Get column headers
        headers = [model.headerData(col, Qt.Orientation.Horizontal) for col in range(cols)]

        # Get table data
        data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                index = model.index(row, col)
                value = model.data(index)
                row_data.append(value if value is not None else "")  # Handle empty cells
            data.append(row_data)

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=headers)

        # Try to export to Excel
        try:
            with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
                workbook  = writer.book
                worksheet = writer.sheets['Sheet1']

                for i, col in enumerate(df.columns):
                    column_len = df[col].astype(str).map(len).max()
                    column_len = max(column_len, len(col)) + 2  # Add extra space
                    worksheet.set_column(i, i, column_len)
            print(f"✅ Exported table data to {file_path} successfully!")
            # Ask the user if they want to open the file
            reply = QMessageBox.question(
                self,
                "Open File?",
                "Xuất Excel thành công!\nBạn có muốn mở file vừa tạo không?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                if platform.system() == "Windows":
                    os.startfile(file_path)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", file_path])
                else:  # Linux
                    subprocess.run(["xdg-open", file_path])

        except Exception as e:
            print(f"❌ Error exporting to Excel: {e}")
class ExcelChoiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("❓ Bạn đã có file Excel?")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        label = QLabel("Bạn muốn sử dụng file Excel đã có sẵn, hay tải mẫu để điền dữ liệu?")
        label.setWordWrap(True)
        layout.addWidget(label)

        # Nút lựa chọn
        button_layout = QHBoxLayout()
        self.btn_import = QPushButton("📥 Nhập file Excel")
        self.btn_template = QPushButton("⬇️ Tải file mẫu")
        self.btn_cancel = QPushButton("❌ Hủy")

        # Căn giữa
        button_layout.addStretch()
        button_layout.addWidget(self.btn_import)
        button_layout.addWidget(self.btn_template)
        button_layout.addWidget(self.btn_cancel)
        button_layout.addStretch()

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Liên kết nút
        self.btn_import.clicked.connect(lambda: self.done(1))
        self.btn_template.clicked.connect(lambda: self.done(2))
        self.btn_cancel.clicked.connect(lambda: self.done(0))


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