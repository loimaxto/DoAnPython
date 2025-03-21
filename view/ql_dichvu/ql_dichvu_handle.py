import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
print(project_path) #vi tri tu file hien tai toi root !! phai toi root moi dung duoc
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from view.ql_dichvu.ql_dichvu import Ui_Form
import sqlite3
from utils.database import SQLiteDB
from dao.dich_vu_dao import DichVuDAO
from dto.dto import DichVuDTO
"""
còn tìm kiếm, sửa, xóa đang bị lỗi
"""

class ql_dichvu_ui(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dv_dao = DichVuDAO()

        # sơ chế giao diện
        self.dis_pla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        # kết nối db
        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cursor = self.conn.cursor()

        self.show_all()

        self.sea_btn.clicked.connect(self.search_item)
        self.sho_btn.clicked.connect(self.show_all)
        self.ins_btn.clicked.connect(self.insert_item)
        self.edi_btn.clicked.connect(self.update_item)
        self.del_btn.clicked.connect(self.delete_item)
    
    def show_err(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Lỗi")
        msg.setText("Dữ liệu nhập vào không hợp lệ")
        msg.exec()
    def show_all(self):
        data = self.dv_dao.get_all_DichVu()
        self.dis_pla.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.dis_pla.insertRow(row_index)
            self.dis_pla.setItem(row_index, 0, QTableWidgetItem(str(row_data.dv_id)))
            self.dis_pla.setItem(row_index, 1, QTableWidgetItem(str(row_data.ten)))
            self.dis_pla.setItem(row_index, 2, QTableWidgetItem(str(row_data.gia)))
        print(data)
        print("Hien thi")
    
    def insert_item(self):
        id = self.in_id.text()
        ten = self.in_ten.text()
        gia = self.in_price.text()
        
        try:
            self.cursor.execute("insert into dich_vu values(?, ?, ?)", (id, ten, gia))
            self.conn.commit()
            print("OK")
        except:
            print("no ok")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Lỗi")
            msg.setText("Dữ liệu nhập vào không hợp lệ")
            msg.exec()
        self.show_all()
    
    def update_item(self):
        id = self.in_id.text()
        name = self.in_ten.text()
        gia = self.in_price.text()
        
        self.cursor.execute("update dich_vu set ten_dv=?, gia=? where dv_id=?", (name, gia, id))
        self.conn.commit()

        self.show_all()
    def delete_item(self):
        id = self.in_id.text()
        self.cursor.execute("delete from dich_vu where dv_id=?", (id,))
        self.conn.commit()
        print("xoa thanh cong")
        self.show_all()
    def search_item(self):
        id = self.in_sea.text()
        if id=="":
            print("du lieu khong hop le")
            self.show_err()
            return
        data = self.dv_dao.search_dich_vu(id)
        print(data)
        self.dis_pla.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.dis_pla.insertRow(row_index)
            self.dis_pla.setItem(row_index, 0, QTableWidgetItem(str(row_data.dv_id)))
            self.dis_pla.setItem(row_index, 1, QTableWidgetItem(str(row_data.ten)))
            self.dis_pla.setItem(row_index,2, QTableWidgetItem(str(row_data.gia)))

        print("Tim kiem thanh cong")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = ql_dichvu_handle()
    ui.show()
    sys.exit(app.exec())