from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        
        self.dateEdit = QtWidgets.QDateEdit(parent=Form)
        self.dateEdit.setGeometry(QtCore.QRect(20, 10, 110, 22))
        self.dateEdit.setObjectName("dateEdit")
        
        self.check_btn = QtWidgets.QPushButton(parent=Form)
        self.check_btn.setGeometry(QtCore.QRect(140, 10, 93, 28))
        self.check_btn.setObjectName("check_btn")
        
        self.groupBox_visits = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_visits.setGeometry(QtCore.QRect(20, 50, 170, 80))
        self.groupBox_visits.setObjectName("groupBox_visits")
        
        self.tong_doanh_thu = QtWidgets.QLabel(parent=self.groupBox_visits)
        self.tong_doanh_thu.setGeometry(QtCore.QRect(10, 30, 150, 30))
        self.tong_doanh_thu.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tong_doanh_thu.setObjectName("tong_doanh_thu")
        
        self.groupBox_pages = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_pages.setGeometry(QtCore.QRect(210, 50, 170, 80))
        self.groupBox_pages.setObjectName("groupBox_pages")
        
        self.ty_le_full_phong = QtWidgets.QLabel(parent=self.groupBox_pages)
        self.ty_le_full_phong.setGeometry(QtCore.QRect(10, 30, 150, 30))
        self.ty_le_full_phong.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ty_le_full_phong.setObjectName("ty_le_full_phong")
        
        self.groupBox_avg = QtWidgets.QGroupBox(parent=Form)
        self.groupBox_avg.setGeometry(QtCore.QRect(400, 50, 170, 80))
        self.groupBox_avg.setObjectName("groupBox_avg")
        
        self.thoi_diem_dong_khach = QtWidgets.QLabel(parent=self.groupBox_avg)
        self.thoi_diem_dong_khach.setGeometry(QtCore.QRect(10, 30, 150, 30))
        self.thoi_diem_dong_khach.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.thoi_diem_dong_khach.setObjectName("thoi_diem_dong_khach")
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_visits.setTitle(_translate("Form", "Tổng Doanh Thu"))
        self.tong_doanh_thu.setText(_translate("Form", "560"))
        self.groupBox_pages.setTitle(_translate("Form", "Tỷ Lệ Lấp Đầy Phòng"))
        self.ty_le_full_phong.setText(_translate("Form", "4.79"))
        self.groupBox_avg.setTitle(_translate("Form", "Thời Điểm Đông Khách"))
        self.thoi_diem_dong_khach.setText(_translate("Form", "00:04:49"))
        self.check_btn.setText(_translate("Form", "Search"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
