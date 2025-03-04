from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem
from ql_dichvu import Ui_Form
import sqlite3

class ql_dichvu_handle(Ui_Form):
    def __init__(self, uiform):

        # kết nối db
        self.conn = sqlite3.connect("db/qlKhachSan.db")
        self.cursor = self.conn.cursor()
        self.setupUi(uiform)

        self.sho_btn.clicked.connect(self.show_all)
        self.ins_btn.clicked.connect(self.insert_item)
    
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
        id = int(self.in_id.text())
        ten = self.in_ten.text()
        gia = int(self.in_price.text())

        self.cursor.execute("insert into dich_vu values(?, ?, ?)", (id, ten, gia))
        print("da them thanh cong")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = ql_dichvu_handle(Form)
    Form.show()
    sys.exit(app.exec())