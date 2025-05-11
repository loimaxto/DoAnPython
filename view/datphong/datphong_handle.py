import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
print(project_path)
from PyQt6 import QtCore, QtGui, QtWidgets
from datphong import Ui_Form
from dao.khach_hang_dao import KhachHangDAO
from dao.phong_dao import PhongDAO
import sqlite3

class datphong_handle(Ui_Form, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        # lược đồ cần đọc
        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cur = self.conn.cursor()
        self.data_customer = KhachHangDAO()
        self.data_room = PhongDAO()

        # sơ chế giao diện
        self.customer_list.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.customer_list.verticalHeader().setVisible(False)
        self.customer_list.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.customer_list.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)

        self.room_list.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.room_list.verticalHeader().setVisible(False)
        self.room_list.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.room_list.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)

        # sự kiện
        self.show_all_customer()
        self.show_all_room()


    # phương thức
    def show_all_customer(self):
        self.customer_list.setRowCount(0)
        data = self.data_customer.get_all_khach_hang()
        for row_index, row_data in enumerate(data):
            self.customer_list.insertRow(row_index)
            self.customer_list.setItem(row_index, 0, QtWidgets.QTableWidgetItem(str(row_data.kh_id)))
            self.customer_list.setItem(row_index, 1, QtWidgets.QTableWidgetItem(str(row_data.ten)))
            self.customer_list.setItem(row_index, 2, QtWidgets.QTableWidgetItem(str(row_data.sdt)))
    def show_all_room(self):
        self.room_list.setRowCount(0)
        data = self.cur.execute("select id, ten_phong, so_giuong, loai \
                                from phong \
                                where tinh_trang_dat_phong=0")
        data = data.fetchall()
        for row_index, row_data in enumerate(data):
            self.room_list.insertRow(row_index)
            for column_index, item_data in enumerate(row_data):
                self.room_list.setItem(row_index, column_index, QtWidgets.QTableWidgetItem(str(item_data)))
    def booking(self):
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = datphong_handle()
    sys.exit(app.exec())