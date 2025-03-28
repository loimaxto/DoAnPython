import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from view.check_in.checkin_ui import Ui_Checkin
import sqlite3
class Checkin(QtWidgets.QWidget, Ui_Checkin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.id = []
        # chỉnh sửa table đẹp hơn
        self.view_customer.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.view_customer.verticalHeader().setVisible(False)
        self.view_room.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.view_room.verticalHeader().setVisible(False)

        # kết nối db
        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cursor = self.conn.cursor()
        #hiển thị tất cả khách hàng và phòng
        self.show_customer()
        self.show_room()
        # Sự kiện
        self.pushButton.clicked.connect(self.getID)
    def getID(self):
        if self.search_customer.text()=="" and self.search_room.text()=="":
            print("mời bạn nhập lại")
        else: self.id.append([self.search_customer.text(),self.search_room.text()])
        print(self.id)
    def show_customer(self):
        self.cursor.execute("select * from khach_hang")
        data = self.cursor.fetchall()
        self.view_customer.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.view_customer.insertRow(row_index)
            for column_index, item_data in enumerate(row_data):
                self.view_customer.setItem(row_index, column_index, QTableWidgetItem(str(item_data)))
    def show_room(self):
        self.cursor.execute("select * from phong")
        data = self.cursor.fetchall()
        self.view_room.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.view_room.insertRow(row_index)
            for column_index, item_data in enumerate(row_data):
                self.view_room.setItem(row_index, column_index, QTableWidgetItem(str(item_data)))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Checkin()
    ui.show()
    sys.exit(app.exec())