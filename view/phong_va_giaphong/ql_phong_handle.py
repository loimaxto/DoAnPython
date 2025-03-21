from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
import sqlite3
# from ql_phong import Ui_Form
from view.phong_va_giaphong.ql_phong import Ui_Form

class ql_phong(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # sơ chế giao diện
        self.dis_pla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

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
        self.cursor.execute("select * from phong")
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
        name = self.in_ten.text()
        sogiuong = self.in_sg.text()
        id_gia = self.in_price_id.text()

        try:
            self.cursor.execute("insert into phong values(?, ?, ?, ?)", (id, name, sogiuong, id_gia))
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
            self.cursor.execute("delete from phong where id=?", (id,))
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
        name = self.in_ten.text()
        sogiuong = self.in_sg.text()
        id_gia = self.in_price_id.text()

        try:
            self.cursor.execute("update phong\
                                set ten_phong=?, so_giuong=?, id_gia=?\
                                where id=?\
                                ", (name, sogiuong, id_gia, id))
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
        self.cursor.execute("select * from phong where id=?", (id,))
        data = self.cursor.fetchall()
        self.dis_pla.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.dis_pla.insertRow(row_index)
            for column_index, item_data in enumerate(row_data):
                self.dis_pla.setItem(row_index, column_index, QTableWidgetItem(str(item_data)))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = ql_phong()
    ui.show()
    sys.exit(app.exec())