from PyQt6 import QtCore, QtGui, QtWidgets
from dangky import Ui_MainWindow
import sqlite3;

class dangky(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cursor = self.conn.cursor()

        # điều khiển sự kiện
        self.finishBtn.clicked.connect(self.dk)

    def dk(self):
        # lấy dữ liệu từ form đăng ký
        usname = self.username.text()
        pass1 = self.password.text()
        pass2 = self.password2.text()
        name = self.name.text()
        diachi = self.diachi.text()
        email = self.email.text()
        chucvu = self.chucvu.text()
        sdt = self.sdt.text()
        print(usname)

        # kiểm tra dữ liệu
        if pass1 != pass2:
            print("mat khau chua dung")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.setWindowTitle("Không thể đăng ký")
            msg.setText("Mật khẩu chưa chính xác!\nVui lòng nhập lại mật khẩu")
            return
        try:
            self.cursor.execute("insert into nhan_vien values(?, ?, ?, ?, ?)", (name, email, sdt, diachi, chucvu))
            self.cursor.execute("insert into user values(?, ?)", (usname, pass1))
            self.conn.commit()
            print("thanh cong")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setWindowTitle("Đăng ký thành công")
            msg.setText("Tài khoản của bạn đã được đăng ký!\n\
                        Vui lòng đăng nhập để sử dụng tài khoản.")
            return
        except:
            print("du lieu co roi")
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.setWindowTitle("Không thể đăng ký")
            msg.setText("Nhân viên này đã có tài khoản")
            return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = dangky()
    ui.setupUi(ui)
    ui.show()
    sys.exit(app.exec())