import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_path)
print(project_path)
from dto.dto import (
    PhongDTO, DichVuDTO, ChiTietDVDTO,HoaDonDTO
)
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit,QListWidgetItem,
    QListWidget, QMessageBox, QLabel,QScrollArea
)
from PyQt6.QtCore import pyqtSignal

from view.datphong2.listPhieuDatPhong import Ui_Form
from dao.datphong_dao import DatPhongDAO

class ListPhieuDatPhongWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.model = QtGui.QStandardItemModel(0, 5)
        self.model.setHorizontalHeaderLabels(["ID Phiếu", "Ngày bắt đầu", "Ngày kết thúc", "Tiền cọc", "Tên khách hàng", "Điện thoại"])
        self.tableViewListPhieu.setModel(self.model)
        self.tableViewListPhieu.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableViewListPhieu.verticalHeader().setVisible(False)
        self.dat_phong_dao = DatPhongDAO()  # Create an instance of DatPhongDAO
        self.load_phieu_dat_phong_data()
        
        self.btnReset.clicked.connect(self.load_phieu_dat_phong_data)

    def load_phieu_dat_phong_data(self):
        print("load_phieu_dat_phong_data")
        list_of_phieu = self.dat_phong_dao.get_all_phieu_dat_phong() # Call the method on the instance
        self.model.setRowCount(0)

        if not list_of_phieu:
            print("Không có dữ liệu phiếu đặt phòng để hiển thị.")
            return

        for phieu_dto in list_of_phieu:
            row_data = [
                str(phieu_dto.booking_id),
                str(phieu_dto.ngay_bd),
                str(phieu_dto.ngay_kt),
                str(phieu_dto.phi_dat_coc),
                str(phieu_dto.ten_kh),
                str(phieu_dto.sdt)
            ]
            items = [QtGui.QStandardItem(data) for data in row_data]
            for item in items:
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.model.appendRow(items)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ListPhieuDatPhongWindow()
    window.show()
    sys.exit(app.exec())