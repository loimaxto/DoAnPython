from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from view.phong_va_giaphong.ql_gia_phong import Ui_Form
import sqlite3

class gia_phong(Ui_Form):
    def __init__(self, Form):
        self.setupUi(Form)

        # kết nối db
        self.conn = sqlite3.connect("db/qlKhachSan.db")
        self.cursor = self.conn.cursor()
        self.show_all()

        # sự kiện
        self.sho_btn.clicked.connect(self.show_all)
        self.ins_btn.clicked.connect(self.insert_item)
        self.del_btn.clicked.connect(self.delete_item)
        self.edi_btn.clicked.connect(self.update_item)
        self.sea_btn.clicked.connect(self.search_item)
    
    def show_all(self):
        self.cursor.execute("select * from gia_phong")
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
        id = self.in_id.text()
        name = self.in_name.text()
        gio = self.in_hour.text()
        ngay = self.in_day.text()
        dem = self.in_night.text()

        try:
            self.cursor.execute("insert into gia_phong values(?, ?, ?, ?, ?)", (id, name, gio, ngay, dem))
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
        id = self.in_id.text()

        try:
            self.cursor.execute("delete from gia_phong where gia_id=?", (id,))
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
        id = self.in_id.text()
        name = self.in_name.text()
        gio = self.in_hour.text()
        ngay = self.in_day.text()
        dem = self.in_night.text()

        try:
            self.cursor.execute("update gia_phong\
                                set ten_loai=?, gia_gio=?, gia_ngay=?, gia_dem=?\
                                where gia_id=?\
                                ", (name, gio, ngay, dem, id))
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
        self.cursor.execute("select * from gia_phong where gia_id=?", (id,))
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
    ui = gia_phong(Form)
    Form.show()
    sys.exit(app.exec())