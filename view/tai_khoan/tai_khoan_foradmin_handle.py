from tai_khoan_foradmin import Ui_Form
from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3

class ql_taikhoan(Ui_Form, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        

        # kết nối db
        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cur = self.conn.cursor()
        

        # sơ chế giao diện
        # self.dis_pla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.dis_pla.verticalHeader().setVisible(False)
        self.dis_pla.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.dis_pla.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        self.show_all()

        # sự kiện
        self.hienthi_btn.clicked.connect(self.show_all)
        self.sea_btn.clicked.connect(self.search_acc)
        self.xoa_btn.clicked.connect(self.delete_acc)
        self.dis_pla.itemSelectionChanged.connect(self.select_row)
        self.show()

    # các hàm sử lý sự kiện
    def show_all(self):
        # lấy dữ liệu
        data = self.cur.execute("select user_id, username, password, user.nv_id, ten_nv, email, sdt, dia_chi, chuc_vu \
                            from user left join nhan_vien on user.nv_id = nhan_vien.nv_id")
        data = data.fetchall()

        # hiển thị dữ liệu
        # print(data)
        self.dis_pla.setRowCount(0)
        for index_row, row_data in enumerate(data):
            self.dis_pla.insertRow(index_row)
            for index_column, item_data in enumerate(row_data):
                self.dis_pla.setItem(index_row, index_column, QtWidgets.QTableWidgetItem(str(item_data)))
    
    def search_acc(self):
        inp = self.inp_sea.text()
        # lấy dữ liệu
        data = self.cur.execute("select user_id, username, password, user.nv_id, ten_nv, email, sdt, dia_chi, chuc_vu \
                            from user left join nhan_vien on user.nv_id = nhan_vien.nv_id \
                                where user_id=?", (inp, ))
        data = data.fetchall()

        # hiển thị dữ liệu
        # print(data)
        self.dis_pla.setRowCount(0)
        for index_row, row_data in enumerate(data):
            self.dis_pla.insertRow(index_row)
            for index_column, item_data in enumerate(row_data):
                self.dis_pla.setItem(index_row, index_column, QtWidgets.QTableWidgetItem(str(item_data)))
    def delete_acc(self):
        try:
            id = self.select_row()
            self.cur.execute("delete from user where user_id=?", (id, ))
            self.conn.commit()
            self.show_all()
        except:
            msg = QtWidgets.QMessageBox()
            msg.setText("Không thể xóa")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.setWindowTitle("Lỗi")
            msg.exec()

    def select_row(self):
        row = self.dis_pla.currentRow()
        if row<0:
            return
        id = self.dis_pla.item(row, 0).text()
        username = self.dis_pla.item(row, 1).text()
        password = self.dis_pla.item(row, 2).text()
        nv_id = self.dis_pla.item(row, 3).text()
        ten_nv = self.dis_pla.item(row, 4).text()
        email = self.dis_pla.item(row, 5).text()
        sdt = self.dis_pla.item(row, 6).text()
        dia_chi = self.dis_pla.item(row, 7).text()
        chuc_vu = self.dis_pla.item(row, 8).text()
        print(id)
        return id

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = ql_taikhoan()
    sys.exit(app.exec())