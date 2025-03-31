from PyQt6 import QtCore, QtGui, QtWidgets
from view.hoadon.hoadon import Ui_Form
from view.hoadon.chitiet_hoadon_handle import chitiet_hoadon
import sqlite3

class hoadon(Ui_Form, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.chitiet = chitiet_hoadon()

        # kết nối db
        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cur = self.conn.cursor()

        # sơ chế giao diện
        self.dis_pla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.dis_pla.verticalHeader().setVisible(False)
        self.dis_pla.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.dis_pla.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)

        # sự kiện
        self.show_all()
        self.all_btn.clicked.connect(self.show_all)
        self.sea_btn.clicked.connect(self.search_hoadon)

    
    def show_all(self):
        # lấy dữ liệu
        data = self.cur.execute("select * from hoa_don")
        data = data.fetchall()

        # hiển thị ra ui
        self.dis_pla.setRowCount(0)
        for irow, row_data in enumerate(data):
            self.dis_pla.insertRow(irow)
            for icolumn, item_data in enumerate(row_data):
                self.dis_pla.setItem(irow, icolumn, QtWidgets.QTableWidgetItem(str(item_data)))
            # thêm nút xem chi tiết cuối hóa đơn
            btn = QtWidgets.QPushButton("Chi tiết")
            self.dis_pla.setCellWidget(irow, 5, btn)
            btn.clicked.connect(self.xem_chitiet)
    def xem_chitiet(self):
        row = self.dis_pla.currentRow()
        id = self.dis_pla.item(row, 0).text()
        self.chitiet.show_all(id)
        self.chitiet.show()
    def search_hoadon(self):
        inp = self.inp_sea.text()
        inp = f"%{inp}%"
        # lấy dữ liệu
        data = self.cur.execute("select * from hoa_don where thoi_gian like ?", (inp, ))
        data = data.fetchall()
        # hiển thị ra ui
        self.dis_pla.setRowCount(0)
        for irow, row_data in enumerate(data):
            self.dis_pla.insertRow(irow)
            for icolumn, item_data in enumerate(row_data):
                self.dis_pla.setItem(irow, icolumn, QtWidgets.QTableWidgetItem(str(item_data)))
            # thêm nút xem chi tiết cuối hóa đơn
            btn = QtWidgets.QPushButton("Chi tiết")
            self.dis_pla.setCellWidget(irow, 5, btn)
            btn.clicked.connect(self.xem_chitiet)

