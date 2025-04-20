
import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_path)
print(project_path)
from dto.dto import (
    PhongDTO, DichVuDTO, ChiTietDVDTO,HoaDonDTO
)
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (
    QPushButton,QHBoxLayout, QWidget,QSizePolicy,
    QWidget, QVBoxLayout, QLineEdit,QListWidgetItem,
    QListWidget, QMessageBox, QLabel,QScrollArea,QRadioButton,
    QTableWidgetItem
)
from dao.gia_phong_dao import GiaPhongDAO
from dao.dat_phong_dao import DatPhongDAO
from PyQt6.QtCore import pyqtSignal
from datphong2_ui import Ui_datphong2
from dao.khach_hang_dao import KhachHangDAO
from dao.phong_dao import PhongDAO
class DatPhong2(QtWidgets.QWidget,Ui_datphong2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # chỉnh sửa table đẹp hơn
        self.tableviewcustomer.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableviewcustomer.verticalHeader().setVisible(False)
        self.tableviewroom.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableviewroom.verticalHeader().setVisible(False)

        # lập trình nút
        
        self.table_khachhang = KhachHangDAO()
        self.table_phong = PhongDAO()
        self.khachhangs = self.table_khachhang.get_all_khach_hang()
        self.phongs = self.table_phong.get_all_phong()
        self.show_customer()
        self.show_room()
        self.btn_khachhang.clicked.connect(self.find_customer)
        self.btn_phong.clicked.connect(self.find_room)
        self.btn_submit.clicked.connect(self.submit_datphong)
        self.start_date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.end_date.setDateTime(QtCore.QDateTime.currentDateTime())
    def show_customer(self):
        self.tableviewcustomer.clear()
        print(self.khachhangs)
        try:
            # xóa tất cả các nut radio cũ
            for button in self.radio_group_customer.buttons():
                self.radio_group_customer.removeButton(button)
            
            
            self.tableviewcustomer.setColumnCount(5)
            self.tableviewcustomer.setHorizontalHeaderLabels(["Chọn","ID","Họ tên"
                                                              ,"Số Điện Thoại","Image"])
            for row_index,row_data in enumerate(self.khachhangs):
                self.tableviewcustomer.insertRow(row_index)
                radio_temp = QRadioButton()
                radio_temp.clicked.connect(lambda check,row=row_index: self.on_radio_customer_clicked(row))
                self.radio_group_customer.addButton(radio_temp,row_index)
                
                radio_widget = QWidget()
                layout = QHBoxLayout(radio_widget)
                layout.addWidget(radio_temp)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                radio_widget.setLayout(layout)
                self.tableviewcustomer.setCellWidget(row_index,0,radio_widget)
                
                item = QTableWidgetItem(str(row_data.kh_id))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewcustomer.setItem(row_index, 1, item)  # +1 vì cột đầu là radio
                item = QTableWidgetItem(str(row_data.ten))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewcustomer.setItem(row_index, 2, item)  # +1 vì cột đầu là radio
                item = QTableWidgetItem(str(row_data.sdt))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewcustomer.setItem(row_index, 3, item)  # +1 vì cột đầu là radio
                item = QTableWidgetItem(str(row_data.image))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewcustomer.setItem(row_index, 4, item)  # +1 vì cột đầu là radio
        except Exception as e:
            QMessageBox.critical(self,"lỗi",f"lỗi khi tải dữ liệu khách hàng: {str(e)}")
    def find_customer(self):
        name = self.name_khachhang.text()
        id = self.id_khachhang.text()
        sdt = self.phone_khachhang.text()
        name = name.strip()
        id = id.strip().replace(" ","")
        sdt = sdt.strip().replace(" ","")
        # Kiểm tra định dạng ID nếu được cung cấp
        if id != "":
            try:
                id = int(id)
                print(id)
                self.khachhangs = [self.table_khachhang.get_khach_hang_by_id(id)] 
                self.show_customer()
            except Exception as e:
                QMessageBox.critical(self,"lỗi",f"lỗi khi id không phải là số {str(e)}")
        
        # Kiểm tra định dạng tên nếu được cung cấp
        elif name != "":
            name = name.strip().lower()  # Chuẩn hóa tên
            self.khachhangs=self.table_khachhang.search_khach_hang(name)
            self.show_customer()
        
        # Kiểm tra định dạng số điện thoại nếu được cung cấp
        elif sdt != "":
            self.khachhangs = self.table_khachhang.search_khach_hang(sdt)
            self.show_customer()
        elif (id and name and sdt) == "":
            self.khachhangs = self.table_khachhang.get_all_khach_hang()
            self.show_customer()
        
    # Tìm kiếm khách hàng trong danh sách
        
        
        

    def show_room(self):
        self.tableviewroom.clear()
        try:
            # xóa tất cả các nut radio cũ
            for button in self.radio_group_room.buttons():
                self.radio_group_room.removeButton(button)
            
            
            self.tableviewroom.setColumnCount(7)
            self.tableviewroom.setHorizontalHeaderLabels(["Chọn","ID","Tên Phòng"
                                                              ,"Số Giường","Giá Phòng",
                                                              "Tình Trạng Phòng","Tình Trạng SD"])
            table_giaphong = GiaPhongDAO()
            
            for row_index,row_data in enumerate(self.phongs):
                self.tableviewroom.insertRow(row_index)
                radio_temp = QRadioButton()
                # Kết nối sự kiện clicked
                radio_temp.clicked.connect(lambda check,row=row_index: self.on_radio_room_clicked(row))
                self.radio_group_room.addButton(radio_temp,row_index)
                radio_widget = QWidget()
                layout = QHBoxLayout(radio_widget)
                layout.addWidget(radio_temp)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                radio_widget.setLayout(layout)
                self.tableviewroom.setCellWidget(row_index,0,radio_widget)
                
                item = QTableWidgetItem(str(row_data.id))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewroom.setItem(row_index, 1, item)  # +1 vì cột đầu là radio
                item = QTableWidgetItem(str(row_data.ten_phong))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewroom.setItem(row_index, 2, item)  # +1 vì cột đầu là radio
                item = QTableWidgetItem(str(row_data.so_giuong))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewroom.setItem(row_index, 3, item)  # +1 vì cột đầu là radio
                giaphongDTO = table_giaphong.get_gia_phong_by_id(row_data.id_gia)
                item = QTableWidgetItem(f"{giaphongDTO.gia_ngay}đ/Ngày {giaphongDTO.gia_dem}đ/Đêm {giaphongDTO.gia_gio}đ/Giờ")
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewroom.setItem(row_index, 4, item)  # +1 vì cột đầu là radio
                item = QTableWidgetItem(str(row_data.tinh_trang_dat_phong))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewroom.setItem(row_index, 5, item)  # +1 vì cột đầu là radio
                item = QTableWidgetItem(str(row_data.tinh_trang_su_dung))
                
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewroom.setItem(row_index, 6, item)  # +1 vì cột đầu là radio
        except Exception as e:
            QMessageBox.critical(self,"lỗi",f"lỗi khi tải dữ liệu phòng: {str(e)}")
    def on_radio_customer_clicked(self,row):
        name_customer = self.tableviewcustomer.item(row,2).text()
        print(name_customer)
        
        self.show_khachhang.setText(name_customer)
    def on_radio_room_clicked(self,row):
        name_room = self.tableviewroom.item(row,2).text()
        self.show_phong.setText(name_room)
        print(name_room)
    def find_room(self):
        id = self.id_phong.text()
        name = self.ten_phong.text()
        name = name.strip()
        id = id.strip().replace(" ","")
        # Kiểm tra định dạng ID nếu được cung cấp
        if id != "":
            try:
                id = int(id)
                print(id)
                self.phongs = [self.table_phong.get_phong_by_id2(id)] 
                self.show_room()
            except Exception as e:
                QMessageBox.critical(self,"lỗi",f"lỗi khi id không phải là số {str(e)}")
        
        # Kiểm tra định dạng tên nếu được cung cấp
        elif name != "":
            name = name.strip().lower()  # Chuẩn hóa tên
            self.phongs=self.table_phong.get_phong_by_name(name)
            self.show_room()
        
        # Kiểm tra định dạng số điện thoại nếu được cung cấp
        elif (id and name) == "":
            self.phongs = self.table_phong.get_all_phong()
            self.show_room()
    def submit_datphong(self):
        index_customer = self.radio_group_customer.checkedId()
        index_room = self.radio_group_room.checkedId()
        if index_customer == -1:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một khách hàng")
            return
        if index_room == -1:
            QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một phòng")
            return
        id_customer = self.tableviewcustomer.item(index_customer,1).text()
        id_room = self.tableviewroom.item(index_room,1).text()
        print(id_customer)
        #print(self.start_date.dateTime(),self.end_date.dateTime())
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = DatPhong2()
    ui.show()
    sys.exit(app.exec())