from PyQt6 import QtCore, QtGui, QtWidgets
from view.hoadon.chitiet_hoadon import Ui_MainWindow
import sqlite3
from view.css import css

class chitiet_hoadon(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # kết nối db
        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cur = self.conn.cursor()

        # sơ chế giao diện
        self.dis_pla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.dis_pla.verticalHeader().setVisible(False)
        self.dis_pla.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.dis_pla.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        # css(self)

    
    def show_all(self, id):
        # lấy dữ liệu hóa đơn
        data = self.cur.execute("select * from \
                                hoa_don left join nhan_vien on hoa_don.nv_id=nhan_vien.nv_id \
                                left join dat_phong on hoa_don.hd_id=dat_phong.hd_id \
                                left join khach_hang on dat_phong.kh_id=khach_hang.kh_id \
                                left join phong on dat_phong.phong_id=phong.id\
                                where hoa_don.hd_id=?", (id, ))
        data = data.fetchone()
        print(data)
        #hiển thị ra gui
        # thông tin hóa đơnđơn
        self.in4_hoadon.setText(f"{data[0]} - {data[2]}")
        self.thanhtien.setText(f"{data[1]}VND")
        if data[4]==0:
            self.tinhtrangthanhtoan.setText("Chưa thanh toán")
        else:
            self.tinhtrangthanhtoan.setText("Đã thanh toán")
        # thông tin nhân viên
        self.in4_nhanvien.setText(f"{data[5]} - {data[6]} - {data[8]} - {data[10]}")
        # thông tin khách hàng
        self.in4_khachhang.setText(f"{data[21]} - {data[22]}")
        # thông tin phòng
        self.ngaydatphong.setText(f"{data[12]}"); self.ngaytraphong.setText(f"{data[13]}")
        self.phicoc.setText(f"{data[14]}VND"); self.tienphong.setText(f"{data[17]}VND")
        self.maphong.setText(f"{data[24]}"); self.tenphong.setText(f"{data[25]}")
        self.sogiuong.setText(f"{data[26]}"); self.loaiphong.setText(f"{data[30]}")

        # lấy dữ liệu các dịch vụ
        data = self.cur.execute("select * from chi_tiet_dv\
                                where hd_id=?", (id, ))
        data = data.fetchall()

        self.dis_pla.setRowCount(0)
        for index_row, row_data in enumerate(data):
            self.dis_pla.insertRow(index_row)
            for index_column, item_data in enumerate(row_data):
                self.dis_pla.setItem(index_row, index_column, QtWidgets.QTableWidgetItem(str(item_data)))