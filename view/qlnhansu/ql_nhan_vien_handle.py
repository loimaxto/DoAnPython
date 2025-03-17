from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
import sqlite3
from view.qlnhansu.ql_nhan_vien import Ui_Form

class ql_nhan_vien(Ui_Form):
    def __init__(self, Form):
        self.setupUi(Form)

        # kết nối db
        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cursor = self.conn.cursor()
        self.show_all()

        # sự kiện
        self.sho_btn.clicked.connect(self.show_all)
        self.ins_btn.clicked.connect(self.insert_item)
        self.del_btn.clicked.connect(self.delete_item)
        self.edi_btn.clicked.connect(self.update_item)
        self.sea_btn.clicked.connect(self.search_item)

    def show_all(self):
        self.cursor.execute("select * from nhan_vien")
        data = self.cursor.fetchall()
        self.dis_pla.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.dis_pla.insertRow(row_index)
            for column_index, item_data in enumerate(row_data):
                self.dis_pla.setItem(row_index, column_index, QTableWidgetItem(str(item_data)))
        
        print(data)
        print("Da hien thi")
    def insert_item(self):
        # dữ liệu đầu vào
        id = self.grid_widgets["ID"].text()
        name = self.grid_widgets["Tên"].text()
        email = self.grid_widgets["Email"].text()
        sodienthoai = self.grid_widgets["Số ĐT"].text()
        diachi = self.grid_widgets["Địa chỉ"].text()
        chucvu = self.grid_widgets["Chức Vụ"].text()
        try:
            self.cursor.execute("insert into nhan_vien values(? , ?, ?, ?, ?, ?)", (id, name, email, sodienthoai, diachi, chucvu))
            self.conn.commit()
            print("Da them")
        except:
            print("khong the them")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Lỗi")
            msg.setText("Dữ liệu chèn vào không hợp lệ")
            msg.exec()
        self.show_all()
    def delete_item(self):
        id = self.grid_widgets["ID"].text()

        try:
            self.cursor.execute("delete from nhan_vien where id=?", (id,))
            self.conn.commit()
            print("da xoa")
        except:
            print("xoa khong thanh cong")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Lỗi")
            msg.setText("ID không hợp lệ")
            msg.exec()
        self.show_all()
    def update_item(self):
        id = self.grid_widgets["ID"].text()
        name = self.grid_widgets["Tên"].text()
        email = self.grid_widgets["Email"].text()
        sodienthoai = self.grid_widgets["Số ĐT"].text()
        diachi = self.grid_widgets["Địa chỉ"].text()
        chucvu = self.grid_widgets["Chức Vụ"].text()
        try:
            self.cursor.execute("update nhan_vien\
                                set ten_nv=?, email=?, sdt=?, dia_chi=?, chuc_vu=? \
                                where id=?\
                                ", (name, email, sodienthoai, diachi, chucvu , id))
            self.conn.commit()
            print("ok")
        except:
            print("no ok")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Lỗi")
            msg.setText("Dữ liệu nhập vào không hợp lệ")
            msg.exec()
        self.show_all()
    def search_item(self):
        id = self.in_sea.text()
        self.cursor.execute("select * from nhan_vien where id=?", (id,))
        data = self.cursor.fetchall()
        self.dis_pla.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.dis_pla.insertRow(row_index)
            for column_index, item_data in enumerate(row_data):
                self.dis_pla.setItem(row_index, column_index, QTableWidgetItem(str(item_data)))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = ql_nhan_vien(Form)
    Form.show()
    sys.exit(app.exec())