from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
import sqlite3
# from ql_phong import Ui_Form
from view.phong_va_giaphong.ql_phong import Ui_Form

class ql_phong(QtWidgets.QWidget, Ui_Form):
    def __init__(self, mainwindow):
        super().__init__()
        self.setupUi(self)

        # loại quyền
        self.par = mainwindow

        # sơ chế giao diện
        self.dis_pla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.dis_pla.verticalHeader().setVisible(False)


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
        self.dis_pla.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.dis_pla.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self.dis_pla.itemSelectionChanged.connect(self.select_row)


    def show_all(self):
        self.cursor.execute("select id, ten_phong, so_giuong, tinh_trang_dat_phong, id_gia, ten_loai, gia_gio, gia_ngay, gia_dem\
                            from phong join gia_phong on id_gia=gia_id\
                            where tinh_trang_su_dung=1")
        data = self.cursor.fetchall()
        self.dis_pla.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.dis_pla.insertRow(row_index)
            for column_index, item_data in enumerate(row_data):
                self.dis_pla.setItem(row_index, column_index, QTableWidgetItem(str(item_data)))
                if column_index==3:# hiện tình trạng phòng bằng chữ
                    if item_data==0:
                        self.dis_pla.setItem(row_index, column_index, QTableWidgetItem("Trống"))
                        self.dis_pla.item(row_index, column_index).setBackground(QtGui.QColor("lightgreen"))
                    if item_data==1:
                        self.dis_pla.setItem(row_index, column_index, QTableWidgetItem("Bận"))
                        self.dis_pla.item(row_index, column_index).setBackground(QtGui.QColor("orange"))

        
        print(data)
        print("Da hien thi")
    def insert_item(self):
        # giới hạn quyền
        if self.par.acc == 1:
            self.par.gioi_han_quyen()
            return

        # dữ liệu đầu vào
        id = self.in_id.text()
        name = self.in_ten.text()
        sogiuong = self.in_sg.text()
        id_gia = self.in_price_id.text()


        try:
            self.cursor.execute("insert into phong (id, ten_phong, so_giuong, id_gia, tinh_trang_dat_phong, tinh_trang_su_dung) \
                                values(?, ?, ?, ?, ?, ?)", (id, name, sogiuong, id_gia, 0, 1))
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
        # giới hạn quyền
        if self.par.acc == 1:
            self.par.gioi_han_quyen()
            return
        # lấy dữ liệu
        id = self.select_row()
        name = self.in_ten.text()
        sogiuong = self.in_sg.text()
        id_gia = self.in_price_id.text()
        # kiểm tra dữ liệu
        if id==None:
            msg = QMessageBox()
            msg.setWindowTitle("Chưa chọn phòng")
            msg.setText("Bạn chưa chọn phòng muốn sửa\nHãy chọn một phòng muốn sửa và thử lại")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()
            return
        if name=="" or sogiuong=="" or id_gia=="":
            msg = QMessageBox()
            msg.setWindowTitle("Không thể cập nhật thông tin")
            msg.setText("Thiếu thông tin. Vui lòng kiểm tra lại thông tin và thử lại!")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.exec()
            return
        try:
            self.cursor.execute("update phong\
                                set ten_phong=?, so_giuong=?, id_gia=?\
                                where id=?\
                                ", (name, sogiuong, id_gia, id))
            self.conn.commit()
            self.show_all()
            msg = QMessageBox()
            msg.setWindowTitle("Thành công")
            msg.setText("Thông tin phòng đã được cập nhật")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
        except:
            print("no ok")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Lỗi")
            msg.setText("Dữ liệu nhập vào không hợp lệ")
            msg.exec()
        
    def search_item(self):
        id = self.in_sea.text()
        self.cursor.execute("select * from phong where id=?", (id,))
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
    ui = ql_phong()
    ui.show()
    sys.exit(app.exec())