import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from view.phong_va_giaphong.ql_gia_phong import Ui_Form
import sqlite3


class gia_phong(QtWidgets.QWidget, Ui_Form):
    def __init__(self, mainwindow):
        super().__init__()
        self.setupUi(self)

        self.par = mainwindow

        # sơ chế lại sương sương
        self.dis_pla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.dis_pla.verticalHeader().setVisible(False)
        self.dis_pla.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.dis_pla.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)

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
        self.dis_pla.itemSelectionChanged.connect(self.select_row)
    
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
        # giới hạn quyền
        if self.par.acc == 1:
            self.par.gioi_han_quyen()
            return
        # dữ liệu đầu vào
        id = self.in_id.text()
        name = self.in_name.text()
        gio = self.in_hour.text()
        ngay = self.in_day.text()
        dem = self.in_night.text()

        try:
            self.cursor.execute("insert into gia_phong (ten_loai, gia_gio, gia_ngay, gia_dem) \
                                values(?, ?, ?, ?)", (name, gio, ngay, dem))
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
        # giới hạn quyền
        if self.par.acc == 1:
            self.par.gioi_han_quyen()
            return
        id = self.select_row()

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
        # giới hạn quyền
        if self.par.acc == 1:
            self.par.gioi_han_quyen()
            return
        id = self.select_row()
        name = self.in_name.text()
        gio = self.in_hour.text()
        ngay = self.in_day.text()
        dem = self.in_night.text()
        if id==None:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Không thể sửa")
            msg.setText("Bạn chưa chọn giá phòng muốn sửa\nHãy chọn một giá phòng và thử lại")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.exec()
            return
        if name=="" or gio=="" or ngay=="" or dem=="":
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Thiếu thông tin")
            msg.setText("Hãy điền đầy đủ thông tin và thử lại")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msg.exec()
            return

        try:
            self.cursor.execute("update gia_phong\
                                set ten_loai=?, gia_gio=?, gia_ngay=?, gia_dem=?\
                                where gia_id=?\
                                ", (name, gio, ngay, dem, id))
            self.conn.commit()
            self.show_all()
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Thành công")
            msg.setText("Thông tin dịch vụ đã được cập nhật")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.exec()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Lỗi")
            msg.setText("Dữ liệu nhập vào không hợp lệ")
            msg.exec()
    def search_item(self):
        id = self.in_sea.text()
        self.cursor.execute("select * from gia_phong where gia_id=?", (id,))
        data = self.cursor.fetchall()
        self.dis_pla.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.dis_pla.insertRow(row_index)
            for column_index, item_data in enumerate(row_data):
                self.dis_pla.setItem(row_index, column_index, QTableWidgetItem(str(item_data)))
    def select_row(self):
        row = self.dis_pla.currentRow()
        if row<0:
            return
        data = self.dis_pla.item(row, 0).text()
        print(data)
        return data    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = gia_phong()
    ui.show()
    sys.exit(app.exec())