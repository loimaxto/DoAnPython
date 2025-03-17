from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
import sqlite3
from view.statistics.dash_board import Ui_Form

class dash_board(Ui_Form):
    def __init__(self, Form):
        self.setupUi(Form)

        # kết nối db
        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cursor = self.conn.cursor()
        self.show_doanh_thu()
        # self.occupied_rate()
        # sự kiện
        self.check_btn.clicked.connect(self.show_doanh_thu)
        
    def show_doanh_thu(self):
        self.cursor.execute("SELECT SUM(tong_tien) FROM hoa_don")
        data = self.cursor.fetchone()  
        
        total_income = data[0] if data and data[0] is not None else 0  
        self.tong_doanh_thu.setText(str(total_income)) 
        
        print(total_income)
        print("Đã hiển thị")

    
    def show_doanh_thu_ngay(self) :
        date = self.dateEdit.date().toString("yyyy-MM-dd")
        self.cursor.execute("SELECT SUM(tong_tien) FROM hoa_don WHERE ngay=?", (date,))
        data = self.cursor.fetchone() 
        total_income = data[0] if data and data[0] is not None else 0  
        self.tong_doanh_thu.setText(str(total_income)) 
        print(total_income)
        print("Đã hiển thị")
    
    # def occupied_rate(self):
    #     self.cursor.execute("SELECT COUNT(*) FROM phong")
    #     data1 = self.cursor.fetchone()
    #     all = data1[0] if data1 and data1[0] is not None else 0  

    #     self.cursor.execute("SELECT COUNT(*) FROM phong WHERE status")
    #     data1 = self.cursor.fetchone()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = ql_nhan_vien(Form)
    Form.show()
    sys.exit(app.exec())