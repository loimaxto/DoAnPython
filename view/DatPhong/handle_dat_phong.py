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
    QPushButton,QHBoxLayout, QWidget,QSizePolicy
)
from PyQt6.QtCore import pyqtSignal

from view.DatPhong.dat_phong_ui import Ui_DatPhong_UI

from dao.khach_hang_dao import KhachHangDAO
from dao.phong_dao import PhongDAO

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

        self.btn_dat_phong.clicked.connect(lambda: self.handle_button_click("Edit"))
        self.btn_delete.clicked.connect(lambda: self.handle_button_click("Delete"))
        self.btn_view.clicked.connect(lambda: self.handle_button_click("View"))

        self.setLayout(layout)

    def handle_button_click(self, button_name):
        print(f"Button {button_name} clicked in row {self.row_index}, data: {self.row_data}")
        self.buttonClicked.emit(self.row_index, button_name)

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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DatPhongWindow()
    window.show()
    sys.exit(app.exec())