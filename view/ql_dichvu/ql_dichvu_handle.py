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

class ql_dichvu_handle(Ui_Form):
    def __init__(self, uiform):
        self.dv_dao = DichVuDAO()
        # kết nối db
        self.setupUi(uiform)

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
        my_dv = DichVuDTO(id, ten, gia)
        DichVuDAO.insert_dich_vu(my_dv)
        # print(data)
        self.show_all()
    
    def update_item(self):
        id = self.in_id.text()
        name = self.in_ten.text()
        gia = self.in_price.text()
        if id=="" or name=="" or gia=="":
            print("du lieu khong hop le")
            return
        dicVu =  DichVuDTO(id,name,gia)
        DichVuDAO.update_dich_vu(dicVu)
        self.show_all()
    def delete_item(self):
        id = self.in_id.text()
        if id=="":
            print("du lieu khong hop le")
            self.show_err()
            return
        self.dv_dao.delete_dich_vu(id)
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
    Form = QtWidgets.QWidget()
    ui = ql_dichvu_handle(Form)
    Form.show()
    sys.exit(app.exec())