import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_path)
print(project_path)
from dto.dto import (
    PhongDTO
)
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (
    QPushButton,QHBoxLayout, QWidget,QSizePolicy,
    QWidget, QVBoxLayout, QLineEdit,
    QListWidget, QMessageBox
)
from PyQt6.QtCore import pyqtSignal

from view.DatPhong.dat_phong_ui import Ui_DatPhong_UI

from dao.khach_hang_dao import KhachHangDAO
from dao.phong_dao import PhongDAO


class DatPhongWindow(QtWidgets.QWidget, Ui_DatPhong_UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dao_phong = PhongDAO()
        self.dao_customer = KhachHangDAO()

        self.model = QtGui.QStandardItemModel(0, 5)  # rows, columns, added one for buttons
        self.model.setHorizontalHeaderLabels(["ID", "Tên phòng", "Loại phòng", "Tình trạng", "Hành động"])
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableView.verticalHeader().setVisible(False)
        self.load_table_data()

    def convertStatus(self, numb):
        if numb == 0:
            return "Trống"
        else:
            return "Đang sử dụng"

    def load_table_data(self):
        phong_data = self.dao_phong.get_all_phong_for_order()
        table_data = []
        for row in phong_data:
            table_data.append([row[0], row[1], row[2], self.convertStatus(row[3])])

        self.model.setRowCount(0)
        for row_index, row in enumerate(table_data):
            items = []
            for item in row:
                item_obj = QtGui.QStandardItem(str(item))
                item_obj.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item_obj.setFlags(item_obj.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                items.append(item_obj)
            self.model.appendRow(items + [QtGui.QStandardItem("")]) # Add empty cell for button widget
            widget = CellButtonWidget(row, row_index, self.tableView)
            self.tableView.setIndexWidget(self.model.index(row_index, 4), widget) # Set the widget

class CellButtonWidget(QWidget):
    """Custom widget that contains three buttons in a table cell, with row data."""

    buttonClicked = pyqtSignal(int, str)  # Signal to emit row and button name

    def __init__(self, row_data, row_index, parent=None):
        super().__init__(parent)
        self.row_data = row_data
        self.row_index = row_index

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.btn_dat_phong = QPushButton("Đặt phòng")
        self.btn_dat_phong.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_delete = QPushButton("Hủy")
        self.btn_delete.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_view = QPushButton("Chi tiết")
        self.btn_view.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.btn_dat_phong.setVisible(row_data[3] == "Trống")
        self.btn_delete.setVisible(row_data[3] == "Đang sử dụng")
        self.btn_view.setVisible(row_data[3] == "Đang sử dụng")

        layout.addWidget(self.btn_dat_phong)
        layout.addWidget(self.btn_view)
        layout.addWidget(self.btn_delete)

        self.btn_dat_phong.clicked.connect(lambda: self.handle_datphong(row_data))
        self.btn_delete.clicked.connect(lambda: self.handle_delete(row_data))
        self.btn_view.clicked.connect(lambda: self.handle_view(row_data))

        self.setLayout(layout)
    def handle_datphong(self, row_data):
        print("dat phong")
        print(row_data)
    def handle_delete(self, row_data):
        print("delete")
        print(row_data)
    def handle_view(self, row_data):
        print("view")
        print(row_data)

class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Search Dịch Vụ")

        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        layout.addWidget(self.search_input)

        self.search_input.returnPressed.connect(self.perform_search)

        self.setLayout(layout)

        self.db_connection = sqlite3.connect("dich_vu.db")  # Replace with your database path
        self.cursor = self.db_connection.cursor()

        # Create dummy data for testing
        self.cursor.execute("DROP TABLE IF EXISTS dich_vu")
        self.cursor.execute("""
            CREATE TABLE dich_vu (
                dv_id INTEGER PRIMARY KEY,
                ten_dv TEXT,
                gia INTEGER
            )
        """)
        self.cursor.executemany("INSERT INTO dich_vu (ten_dv, gia) VALUES (?, ?)",
                           [("Massage", 150000), ("Sauna", 100000), ("Haircut", 80000), ("Manicure", 50000), ("Pedicure", 60000)])
        self.db_connection.commit()

    def perform_search(self):
        search_term = self.search_input.text()
        query = "SELECT ten_dv FROM dich_vu WHERE ten_dv LIKE ?"
        self.cursor.execute(query, ('%' + search_term + '%',))
        results = self.cursor.fetchall()

        if results:
            self.show_results_popup(results)
        else:
            QMessageBox.information(self, "No Results", "No matching dịch vụ found.")

    def show_results_popup(self, results):
        popup = QWidget()
        popup_layout = QVBoxLayout()
        result_list = QListWidget()
        popup_layout.addWidget(result_list)
        popup.setLayout(popup_layout)

        for result in results:
            result_list.addItem(result[0])

        result_list.itemClicked.connect(lambda item: self.print_selected_item(item.text()))
        popup.show()

    def print_selected_item(self, item_text):
        print(f"Selected: {item_text}")

    def closeEvent(self, event):
        self.db_connection.close()
        event.accept()
               
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DatPhongWindow()
    window.show()
    sys.exit(app.exec())