from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from ql_dichvu import Ui_Form
import sqlite3

class ql_dichvu_handle(Ui_Form):
    def __init__(self, uiform):

        # kết nối db
        self.conn = sqlite3.connect("db/qlKhachSan.db")
        self.cursor = self.conn.cursor()
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
        self.cursor.execute("select * from dich_vu")
        data = self.cursor.fetchall()
        self.dis_pla.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.dis_pla.insertRow(row_index)
            for column_index, item_data in enumerate(row_data):
                self.dis_pla.setItem(row_index, column_index, QTableWidgetItem(str(item_data)))
        print(data)
        print("Hien thi")
    
    def insert_item(self):
        id = self.in_id.text()
        ten = self.in_ten.text()
        gia = self.in_price.text()
        try:
            self.cursor.execute("insert into dich_vu values(?, ?, ?)", (id, ten, gia))
            print("da them thanh cong")
            self.conn.commit()
        except:
            print("them khong thanh cong")
            self.show_err()
        self.show_all()
    
    def update_item(self):
        id = self.in_id.text()
        name = self.in_ten.text()
        gia = self.in_price.text()
        if id=="" or name=="" or gia=="":
            print("du lieu khong hop le")
            return
        self.cursor.execute("update dich_vu\
            set ten_dv=?, gia=?\
                where dv_id=?", (name, gia, id))
        self.conn.commit()
        self.show_all()
    def delete_item(self):
        id = self.in_id.text()
        if id=="":
            print("du lieu khong hop le")
            self.show_err()
            return
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
        self.cursor.execute("select * from dich_vu where dv_id=?", (id,))
        data = self.cursor.fetchall()
        self.dis_pla.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.dis_pla.insertRow(row_index)
            for column_index, item_data in enumerate(row_data):
                self.dis_pla.setItem(row_index, column_index, QTableWidgetItem(str(item_data)))
        print("Tim kiem thanh cong")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = ql_dichvu_handle(Form)
    Form.show()
    sys.exit(app.exec())