from view.login.quen_pass import Ui_MainWindow
from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3
import random

class quen_pass(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # kết nối db
        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cur = self.conn.cursor()

        # sự kiện
        self.change_pass.clicked.connect(self.change_pass_fn)

        # tạo mã xác nhận
        self.xac_nhan = str("")
        for i in range(0, 6):
            self.xac_nhan += str(random.randint(0, 9))
        print("Ma xac nhan la: ", self.xac_nhan)

    def check_username(self, s):
        data = self.cur.execute("select username \
                                from user \
                                where username=?", (s, ))
        data = data.fetchone()
        if data == None:
            return False
        return True
    def change_pass_fn(self):
        # lấy dữ liệu
        username = self.inp_username.text()
        pass1 = self.inp_pass1.text()
        pass2 = self.inp_pass2.text()
        xn = self.OK_pass.text()

        # thiếu dữ liệu
        if username=="" or pass1=="" or pass2=="" or xn=="":
            msg=QtWidgets.QMessageBox();msg.setWindowTitle("Cảnh báo");msg.setText("Vui lòng điền đây đủ thông tin!");msg.setIcon(QtWidgets.QMessageBox.Icon.Warning);msg.exec()
            return
        
        #kiểm tra dữ liệu
        if self.check_username(username) == False:
            msg=QtWidgets.QMessageBox();msg.setWindowTitle("Cảnh báo");msg.setText("Tên đăng nhập không tồn tại!");msg.setIcon(QtWidgets.QMessageBox.Icon.Warning);msg.exec()
            return
        if pass1 != pass2:
            msg=QtWidgets.QMessageBox();msg.setWindowTitle("Cảnh báo");msg.setText("Mật khẩu xác nhận không trùng khớp.\nVui lòng xác nhận đúng mật khẩu!");msg.setIcon(QtWidgets.QMessageBox.Icon.Warning);msg.exec()
            return
        if xn != self.xac_nhan:
            msg=QtWidgets.QMessageBox();msg.setWindowTitle("Cảnh báo");msg.setText("Mã xác nhận chưa chính xác!");msg.setIcon(QtWidgets.QMessageBox.Icon.Warning);msg.exec()
            return

        # đổi mật khẩu
        try:
            self.cur.execute("update user set \
                            password=? \
                            where username=?", (pass1, username))
            self.conn.commit()
            msg=QtWidgets.QMessageBox();msg.setWindowTitle("Thành công");msg.setText("Cập nhật mật khẩu thành công");msg.setIcon(QtWidgets.QMessageBox.Icon.Information);msg.exec()
        except:
            msg=QtWidgets.QMessageBox();msg.setWindowTitle("Lỗi");msg.setText("Không thể đổi mật khẩukhẩu!");msg.setIcon(QtWidgets.QMessageBox.Icon.Critical);msg.exec()