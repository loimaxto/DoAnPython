from PyQt6.QtWidgets import QMainWindow, QMessageBox
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
    def __init__(self, ui):
        # kết nối database
        try:
            self.conn = sqlite3.connect("db/qlKhachSan.db")
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
    
    def login(self, ui):
        name = self.username.text()
        pwd = self.password.text()
        print(name, pwd)

        try:
            self.cursor.execute("select * \
                            from user join nhan_vien on user.nv_id=nhan_vien.nv_id \
                            where user.username=? and user.password=?", (name, pwd))
            data = self.cursor.fetchone()
            print(data)
            # if data.lenght==0:
            #     self.show_error()
            #     return

            # lấy thông tin
            self.us_id = data[0]
            self.us_name = data[1]
            self.nv_id = data[4]
            self.nv_name = data[5]
            self.nv_email = data[6]
            self.nv_sdt = data[7]
            self.nv_diachi = data[8]
            self.nv_chucvu = data[9]
            self.checkOK = True

            # truyền dữ liệu cho giao diện
            ui.user_id.setText(str(self.us_id))
            ui.user_name.setText(str(self.us_name))
            ui.nv_id.setText(str(self.nv_id))
            ui.nv_name.setText(str(self.nv_name))
            ui.nv_email.setText(str(self.nv_email))
            ui.nv_sdt.setText(str(self.nv_sdt))
            ui.nv_diachi.setText(str(self.nv_diachi))
            ui.nv_chucvu.setText(str(self.nv_chucvu))

            # đăng nhập thành công, tắt màn hình đăng nhập
            self.hide()
            
        except:
            print("loi dang nhap")
            self.show_error()
    
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
# ui.show()
# app.exec()

# cursor.close()
# conn.close()