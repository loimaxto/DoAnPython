from PyQt6 import QtCore, QtGui, QtWidgets
from view.hoadon.chitiet_hoadon import Ui_MainWindow
import sqlite3

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
    
    def show_all(self, id):
        data = self.cur.execute("select * from chi_tiet_dv\
                                where hd_id=?", (id, ))
        data = data.fetchall()

        self.dis_pla.setRowCount(0)
        for index_row, row_data in enumerate(data):
            self.dis_pla.insertRow(index_row)
            for index_column, item_data in enumerate(row_data):
                self.dis_pla.setItem(index_row, index_column, QtWidgets.QTableWidgetItem(str(item_data)))