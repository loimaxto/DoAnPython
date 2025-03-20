from PyQt6 import QtCore, QtGui, QtWidgets
from view.login.dangnhap import Ui_MainWindow
# from dangnhap import Ui_MainWindow
import sqlite3

class dangnhap(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, mainwindow):
        super().__init__()
        self.setupUi(self)

        # kết nối db
        self.conn = sqlite3.connect("db/hotel7-3.db")
        self.cursor = self.conn.cursor()

        # điều khiển sự kiện
        self.login_btn.clicked.connect(lambda: self.xuatInfo(mainwindow))

        self.show()
        
    def xuatInfo(self, mainwindow):
        mainwindow.username = self.username.text()
        mainwindow.password = self.password.text()
        print(mainwindow.username, mainwindow.password)
        mainwindow.tk_page.user_name.setText(mainwindow.username)
        self.hide()


        self.cursor.execute("select * from user join nhan_vien on user.nv_id=nhan_vien.nv_id\
                            where user.username=? and user.password=?", (mainwindow.username, mainwindow.password))
        data = self.cursor.fetchone()
        print(data)
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = dangnhap()
    ui.show()
    sys.exit(app.exec())