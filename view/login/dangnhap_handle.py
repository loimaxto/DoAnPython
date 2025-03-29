from PyQt6 import QtCore, QtGui, QtWidgets
from view.login.dangnhap import Ui_MainWindow
# from dangnhap import Ui_MainWindow
from view.login.dangky_handle import dangky
from view.tai_khoan.tai_khoan_foradmin_handle import ql_taikhoan
from view.tai_khoan.tai_khoan_handle import tai_khoan
import sqlite3

class dangnhap(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, mainwindow):
        super().__init__()
        self.setupUi(self)
        self.dk = dangky()

        # kết nối db
        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cursor = self.conn.cursor()

        # điều khiển sự kiện
        self.login_btn.clicked.connect(lambda: self.chonTK(mainwindow))
        self.newTk_btn.clicked.connect(lambda: self.dk.show())

        self.show()

    def chonTK(self, mainwindow):
        # lấy dữ liệu để xác định loại tài khoản
        data = self.cursor.execute("select * from user where username=? and password=?", (self.username.text(), self.password.text()))
        data = data.fetchone()
        if data==None:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi đăng nhập")
            msg.setText("Tên đăng nhập hoặc mật khẩu chưa chính xác!\n\
                        Vui lòng đăng nhập lại")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.exec()
            return
        if(data[3]==None):
            mainwindow.tk_page = ql_taikhoan()
        else:
            mainwindow.tk_page = tai_khoan()
            self.xuatInfo(mainwindow)
        
        # thêm màn hình vào main
        mainwindow.ui.stackedWidget.addWidget(mainwindow.tk_page)

        self.hide()
        
    def xuatInfo(self, mainwindow):
        # lấy dữ liệu từ cửa sổ đăng nhập
        self.cursor.execute("select * from user join nhan_vien on user.nv_id=nhan_vien.nv_id\
                            where user.username=? and user.password=?", (self.username.text(), self.password.text()))
        data = self.cursor.fetchone()
        print("du lieu dang nhap", data)

        if data==None:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Lỗi đăng nhập")
            msg.setText("Tên đăng nhập hoặc mật khẩu chưa chính xác!\n\
                        Vui lòng đăng nhập lại")
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.exec()
            return

        # chuyển dữ liệu vào menu
        mainwindow.tk_page.user_id.setText(str(data[0]))
        mainwindow.tk_page.user_name.setText(data[1])
        mainwindow.tk_page.nv_id.setText(str(data[3]))
        mainwindow.tk_page.nv_name.setText(data[5])
        mainwindow.tk_page.nv_email.setText(data[6])
        mainwindow.tk_page.nv_sdt.setText(data[7])
        mainwindow.tk_page.nv_diachi.setText(data[8])
        mainwindow.tk_page.nv_chucvu.setText(data[9])

        mainwindow.show()
        self.hide()


        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = dangnhap()
    ui.show()
    sys.exit(app.exec())