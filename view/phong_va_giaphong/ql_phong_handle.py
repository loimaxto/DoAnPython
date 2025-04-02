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
        self.cur = self.conn.cursor()
        self.show_all()
        self.setUpInput()

        # sự kiện
        self.sho_btn.clicked.connect(self.show_all)
        self.ins_btn.clicked.connect(self.insert_item)
        self.del_btn.clicked.connect(self.delete_item)
        self.edi_btn.clicked.connect(self.update_item)
        self.sea_btn.clicked.connect(self.search_item)
        self.dis_pla.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.dis_pla.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self.dis_pla.itemSelectionChanged.connect(self.select_row)

    def setUpInput(self):
        self.inp_loai.clear()
        data = self.cur.execute("select gia_id, ten_loai from gia_phong")
        data = data.fetchall()
        print(data)
        for i in range(0, data.__len__()):
            self.inp_loai.addItem(data[i][1], data[i][0])
    def show_all(self):
        self.cur.execute("select id, ten_phong, loai, so_giuong, tinh_trang_dat_phong, id_gia, ten_loai, gia_gio, gia_ngay, gia_dem\
                            from phong join gia_phong on id_gia=gia_id\
                            where tinh_trang_su_dung=1")
        data = self.cur.fetchall()
        self.dis_pla.setRowCount(0)
        for row_index, row_data in enumerate(data):
            self.dis_pla.insertRow(row_index)
            for column_index, item_data in enumerate(row_data):
                self.dis_pla.setItem(row_index, column_index, QTableWidgetItem(str(item_data)))
                if column_index==4:# hiện tình trạng phòng bằng chữ
                    if item_data==0:
                        self.dis_pla.setItem(row_index, column_index, QTableWidgetItem("Trống"))
                        self.dis_pla.item(row_index, column_index).setBackground(QtGui.QColor("lightgreen"))
                    if item_data==1:
                        self.dis_pla.setItem(row_index, column_index, QTableWidgetItem("Bận"))
                        self.dis_pla.item(row_index, column_index).setBackground(QtGui.QColor("orange"))
    def insert_item(self):
        # giới hạn quyền
        if self.par.acc == 1:
            self.par.gioi_han_quyen()
            return

        # dữ liệu đầu vào và xữ lý dữ liệu
        id = self.in_id.text()
        name = self.in_ten.text()
        sogiuong = self.in_sg.text()
        loai = self.inp_loai.currentText()
        id_gia = self.cur.execute("select gia_id from gia_phong where ten_loai=?", (loai, ))
        id_gia = id_gia.fetchone()
        id_gia = id_gia[0]


        try:
            self.cur.execute("insert into phong (id, ten_phong, loai, so_giuong, tinh_trang_dat_phong, tinh_trang_su_dung, id_gia) \
                                values(?, ?, ?, ?, ?, ?, ?)", (id, name, loai, sogiuong, 0, 1, id_gia))
            self.conn.commit()
        except:
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
            self.cur.execute("delete from phong where id=?", (id,))
            self.conn.commit()
        except:
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
        loai = self.inp_loai.currentText()
        id_gia = self.cur.execute("select gia_id from gia_phong where ten_loai=?", (loai, ))
        id_gia = id_gia.fetchone()
        id_gia = id_gia[0]
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
            self.cur.execute("update phong\
                                set ten_phong=?, so_giuong=?, id_gia=?, loai=?\
                                where id=?\
                                ", (name, sogiuong, id_gia, loai, id))
            self.conn.commit()
            self.show_all()
            msg = QMessageBox()
            msg.setWindowTitle("Thành công")
            msg.setText("Thông tin phòng đã được cập nhật")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Lỗi")
            msg.setText("Dữ liệu nhập vào không hợp lệ")
            msg.exec()
        
    def search_item(self):
        id = self.in_sea.text()
        self.cur.execute("select * from phong where id=?", (id,))
        data = self.cur.fetchall()
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
        return data

if __name__ == "__main__": 
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = ql_phong()
    ui.show()
    sys.exit(app.exec())