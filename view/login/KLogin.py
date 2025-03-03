from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic
import sqlite3


# kết nối database
try:
    conn = sqlite3.connect("db/qlKhachSan.db")
    cursor = conn.cursor()
    print("OK")
except:
    print("No OK")


def querry_all_user():
    cursor.execute("select * from user")
    data = cursor.fetchall()
    print(data)

querry_all_user()

# khi đăng nhập mình sẽ lấy được nv_id từ db
class Login(QMainWindow):
    nv_id = ""
    def __init__(self):
        super().__init__()
        uic.loadUi("view/login/KLogin.ui", self)

        #sự kiện
        self.loginBtn.clicked.connect(self.login)
    
    def login(self):
        name = self.username.text()
        pwd = self.password.text()
        print(name, pwd)

        self.nv_id = cursor.execute("select nv_id from user where username=? and password=?", (name, pwd)).fetchone()
        # print(cursor.fetchone())
        self.nv_id = self.nv_id[0]
        print(self.nv_id)


    
app = QApplication([])
ui = Login()
ui.show()
app.exec()

cursor.close()
conn.close()