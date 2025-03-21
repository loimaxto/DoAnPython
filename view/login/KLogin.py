from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt6 import QtWidgets
from PyQt6 import uic
import sqlite3


# kết nối database
# try:
#     conn = sqlite3.connect("db/qlKhachSan.db")
#     cursor = conn.cursor()
#     print("OK")
# except:
#     print("No OK")


# def querry_all_user():
#     cursor.execute("select * from user")
#     data = cursor.fetchall()
#     print(data)

# querry_all_user()

# khi đăng nhập mình sẽ lấy được nv_id từ db
class Login(QMainWindow):
    us_id = ""
    us_name = ""
    nv_id = ""
    nv_name = ""
    nv_email = ""
    nv_sdt = ""
    nv_diachi = ""
    nv_chucvu = ""

    checkOk = False
    def __init__(self):
        # kết nối database
        try:
            self.conn = sqlite3.connect("db/hotel7-3.db")
            self.cursor = self.conn.cursor()
            print("OK")
        except:
            print("No OK")


        def querry_all_user():
            self.cursor.execute("select * from user")
            data = self.cursor.fetchall()
            print(data)

        querry_all_user()

        super().__init__()
        uic.loadUi("view/login/KLogin.ui", self)

        #sự kiện
        self.loginBtn.clicked.connect(lambda: self.login(ui))
    
    def login(self):
        name = self.username.text()
        pwd = self.password.text()
        print(name, pwd)


    
    def show_error(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Đăng nhập thất bại")
        msg.setText("Tên đăng nhập hoặc mật khẩu không chính xác")
        msg.setInformativeText("Vui lòng đăng nhập lại")
        # msg.setStandardButtons(QMessageBox.standardButton.Ok)
        msg.exec()


    
# app = QApplication([])
# ui = Login()
# show()
# app.exec()

# cursor.close()
# conn.close()