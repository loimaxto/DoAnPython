
import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_path)
print(project_path)
import time
from dto.dto import (
    PhongDTO, DichVuDTO, ChiTietDVDTO,HoaDonDTO
)
from dao.hoadon_dao import HoaDonDAO
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (
    QPushButton,QHBoxLayout, QWidget,QSizePolicy,
    QWidget, QVBoxLayout, QLineEdit,QListWidgetItem,
    QListWidget, QMessageBox, QLabel,QScrollArea,QRadioButton,
    QTableWidgetItem,QTableWidget
)
from dao.gia_phong_dao import GiaPhongDAO,GiaPhongDTO
from dao.dat_phong_dao import DatPhongDAO,DatPhongDTO
from PyQt6.QtCore import pyqtSignal
from view.datphong2.datphong2_uitest import Ui_datphong2
from dao.khach_hang_dao import KhachHangDAO
from dao.phong_dao import PhongDAO

class DatPhong2(QtWidgets.QWidget,Ui_datphong2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.nv_id=2
        # chỉnh sửa table đẹp hơn
        self.tableviewcustomer.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableviewcustomer.verticalHeader().setVisible(False)
        self.tableviewroom.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableviewroom.verticalHeader().setVisible(False)
        
        #hiển thị lịch khi bấm vào
        self.start_date.setCalendarPopup(True)
        self.end_date.setCalendarPopup(True)
        # Thiết lập chỉ đọc
        self.tableviewcustomer.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tableviewroom.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        #tạo dói tượng trước khi xử lí
        self.table_khachhang = KhachHangDAO()
        self.table_phong = PhongDAO()
        self.table_datphong = DatPhongDAO()
        self.khachhangs = self.table_khachhang.get_all_khach_hang()
        self.phongs = self.table_phong.get_all_phong()
        self.show_customer()
        self.show_room()
        self.__gia = {"ngày": 0,"đêm": 0,"giờ": 0}
        # lập trình nút
        self.khachhang_btn.clicked.connect(lambda: self.showlayout_roomcustomer("khách hàng"))
        self.phong_btn.clicked.connect(lambda: self.showlayout_roomcustomer("phòng"))
        self.btn_khachhang.clicked.connect(self.find_customer)
        self.btn_phong.clicked.connect(self.find_room)
        self.btn_submit.clicked.connect(self.submit_datphong)
        self.start_date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.end_date.setDateTime(QtCore.QDateTime.currentDateTime())
        # thêm sự kiện cập nhật tiền ước tính khi bấm vào combobox
        self.comboBox.activated.connect(self.setcombobox)
        # cập nhật lại thời gian khi thay đổi lịch
        self.start_date.dateTimeChanged.connect(lambda :self.setupdate("start"))
        self.end_date.dateTimeChanged.connect(lambda :self.setupdate("end"))
    def resetForm(self):
        self.settienlucdat(0)
        self.settienuoctinh(0)
        self.start_date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.end_date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.khachhangs = self.table_khachhang.get_all_khach_hang()
        self.phongs = self.table_phong.get_all_phong()
        self.show_customer()
        self.show_room()
        self.set_default()
        self.note.clear()
        self.show_phong.setText("Chưa Chọn")
        self.show_khachhang.setText("Chưa chọn")
    def showlayout_roomcustomer(self,choose):
        if(choose=='phòng'):
            self.btn_khachhang.hide()
            self.name_khachhang.hide()
            self.id_khachhang.hide()
            self.tableviewcustomer.hide()
            self.phone_khachhang.hide()
            self.tableviewroom.show()
            self.btn_phong.show()
            self.id_phong.show()
            self.ten_phong.show()
            self.label_12.hide()
            self.label_13.hide()
            self.label_14.hide()
            self.label_15.show()
            self.label_16.show()
            self.phong_btn.setStyleSheet("""QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                background-color: #4CAF50; color: white;
            }
            """)
            self.khachhang_btn.setStyleSheet("""QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                background-color:#4f4a4f;
            }
            QPushButton:hover {
                background-color: #45a049;
            }""")
            self.phongs = self.table_phong.get_all_phong()

            self.show_room()
        else:
            self.btn_khachhang.show()
            self.name_khachhang.show()
            self.id_khachhang.show()
            self.tableviewcustomer.show()
            self.phone_khachhang.show()
            self.tableviewroom.hide()
            self.btn_phong.hide()
            self.id_phong.hide()
            self.ten_phong.hide()
            self.label_12.show()
            self.label_13.show()
            self.label_14.show()
            self.label_15.hide()
            self.label_16.hide()
            self.khachhang_btn.setStyleSheet("""QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                background-color: #4CAF50; color: white;
            }
            """)
            self.phong_btn.setStyleSheet("""QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                background-color:#4f4a4f;
            }
            QPushButton:hover {
                background-color: #45a049;
            }""")
            self.khachhangs = self.table_khachhang.get_all_khach_hang()
            self.show_customer()
            
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
            self.tableviewcustomer.setRowCount(0)
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
        
        
    def confirm_action(self, callback):
        """Hiển thị hộp thoại xác nhận trước khi thực hiện hành động"""
        # Lấy text từ nút được nhấn
        
        reply = QMessageBox.question(
            self,
            'Xác nhận hành động',
            f'Bạn có chắc chắn muốn lưu dữ liệu khách hàng?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            callback()  # Gọi hàm xử lý tương ứng

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
            self.tableviewroom.setRowCount(0)
            table_giaphong = GiaPhongDAO()
            
            for row_index,row_data in enumerate(self.phongs):
                self.tableviewroom.insertRow(row_index)
                radio_temp = QRadioButton()
                # Kết nối sự kiện clicked
                
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
                # thêm nhận diện cho radio khi bấm vào nút đó
                radio_temp.clicked.connect(lambda check,row=row_index,giaphong=giaphongDTO: self.on_radio_room_clicked(row,giaphong))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewroom.setItem(row_index, 4, item)  # +1 vì cột đầu là radio
                item = QTableWidgetItem(str("Bận" if row_data.tinh_trang_dat_phong else "Trống"))
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewroom.setItem(row_index, 5, item)  # +1 vì cột đầu là radio
                item = QTableWidgetItem(str(row_data.tinh_trang_su_dung))
                
                item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tableviewroom.setItem(row_index, 6, item)  # +1 vì cột đầu là radio
        except Exception as e:
            QMessageBox.critical(self,"lỗi",f"lỗi khi tải dữ liệu phòng: {str(e)}")
    def setcombobox(self):
        money = self.gettienlucdat()
        self.settienuoctinh(money)
    def on_radio_customer_clicked(self,row):
        name_customer = self.tableviewcustomer.item(row,2).text()
        print(name_customer)
        
        self.show_khachhang.setText(name_customer)
    def on_radio_room_clicked(self,row,giaphong):
        name_room = self.tableviewroom.item(row,2).text()
        self.show_phong.setText(name_room)
        self.__gia.update({"ngày":giaphong.gia_ngay,
                           "giờ":giaphong.gia_gio,"đêm":giaphong.gia_dem})
        print (self.__gia)
        ngay,dem,gio = self.__calculate_time()
        total_cash = self.__calculate_monney()
        self.settienlucdat(total_cash)
        data = [f"Ngày: {ngay} x {self.__gia.get("ngày")} = {ngay*self.__gia.get("ngày")}Đ",
                f"Đêm: {dem} x {self.__gia.get("đêm")} = {dem*self.__gia.get("đêm")}Đ", 
                f"Giờ: {gio} x {self.__gia.get("giờ")} = {gio*self.__gia.get("giờ")}Đ"]
        model = QtCore.QStringListModel(data)
        self.listView.setModel(model)
        self.listView.show()
        
        self.settienuoctinh(total_cash)
    def getratio(self):
        return int(self.comboBox.currentText().split("%")[0])
    def gettienlucdat(self):
        print(self.tienlucdat.text())
        return int(float(self.tienlucdat.text().split(" Đ")[0]))
    def settienlucdat(self,number):
        self.tienlucdat.setText(f"{number} Đ")
    def settienuoctinh(self,number):
        print(number,self.getratio())
        self.tienuoctinh.setText(f"{number*self.getratio()/100.0} Đ")
    def getphidatcoc(self):
        return int(float(self.tienuoctinh.text().split(" Đ")[0]))
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
    def __calculate_time(self):
        start_dt = self.start_date.dateTime()
        end_dt = self.end_date.dateTime()
        total_seconds = start_dt.secsTo(end_dt)
        
        # 2. Chuyển đổi sang ngày, giờ, phút, giây
        days = total_seconds // (24 * 3600)
        remaining_seconds = total_seconds % (24 * 3600)
        
        hours = remaining_seconds // 3600
        remaining_seconds %= 3600
        nights = 0
        if hours >=12:
            nights = 1
            hours-=12
        return days,nights,hours
    def __calculate_monney(self):
        days,nights,hours = self.__calculate_time()
        return days*self.__gia.get("ngày")+nights*self.__gia.get("đêm")+hours*self.__gia.get("giờ")
    def submit_datphong(self):
        try:
            index_customer = self.radio_group_customer.checkedId()
            index_room = self.radio_group_room.checkedId()
            

            tinhtrangphong = 1 if self.tableviewroom.item(index_room,5).text().lower()=="bận" else 0
            if tinhtrangphong!=0:
                QMessageBox.warning(self,"cảnh báo",f"Phòng này đã được sử dụng!")
                return 
            if self.start_date.dateTime()>self.end_date.dateTime():
                QMessageBox.warning(self,"cảnh báo",f"thời gian bắt đầu không được lớn hơn thời gian kết thúc")
                return
            if self.start_date.dateTime()<QtCore.QDateTime.currentDateTime():
                QMessageBox.warning(self,"cảnh báo",f"thời gian bắt đầu phải lớn hơn thòi gian hiện tại")
                return
            if index_customer == -1:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một khách hàng")
                return
            if index_room == -1:
                QMessageBox.warning(self, "Cảnh báo", "Vui lòng chọn một phòng")
                return
            reply = QMessageBox.question(
                self,
                'Xác nhận',
                f'Bạn có chắc chắn muốn lưu dữ liệu khách hàng?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.No:
                return
            id_customer = self.tableviewcustomer.item(index_customer,1).text()
            id_room = self.tableviewroom.item(index_room,1).text()
            print(id_customer)
            from dao.hoa_don_dao import HoaDonDAO
            from dao.ct_dv_dao import ChiTietDVDAO
            hoadon=HoaDonDAO()
            ctdv = ChiTietDVDAO()
            self.table_phong.update_tinh_trang_dat_phong(id_room,1,hoadon.get_hoa_don_by_next_id())
        
        #print(self.start_date.dateTime(),self.end_date.dateTime())
        
            note = self.note.toPlainText()
            ngay_bd = self.start_date.dateTime().toString()
            ngay_kt = self.end_date.dateTime().toString()
            phi_dat_coc = self.getphidatcoc()
            tien_luc_dat = self.gettienlucdat()
            datphongtemp = DatPhongDTO(ngay_bd=ngay_bd,
                        ngay_kt=ngay_kt,
                        phi_dat_coc=phi_dat_coc,
                        note=note,
                        tien_luc_dat=tien_luc_dat,
                        phong_id=id_room,
                        kh_id=id_customer)
            print(datphongtemp)
            table_ctdv= ChiTietDVDAO()
            id_hdnext = hoadon.get_hoa_don_by_next_id()
            id_datphong=self.table_datphong.get_dat_phong_next_id()
            self.table_datphong.insert_dat_phong(dat_phong=datphongtemp)
            hoadon.insert_hoa_don(HoaDonDTO(hd_id=self.nv_id,dat_phong_id=id_datphong))
            self.resetForm()
            self.on_success("Bạn đã đặt phòng thành công!")

            ctdv.insert_ctdv_by_hdid(id_hdnext)
        except Exception as e:
            print(str(e))
            QMessageBox.critical(self,"lỗi",f"lỗi khi thêm datphong{str(e)}")
    def setupdate(self,action):
        print(action)
        checkID = self.radio_group_room.checkedId()
        if checkID!=-1:
            self.on_radio_room_clicked(checkID,GiaPhongDTO(gia_ngay=self.__gia.get("ngày"),
                                                gia_dem=self.__gia.get("đêm"),
                                                gia_gio=self.__gia.get("giờ")))
            
        else:
            QMessageBox.critical(self,"lỗi",f"bạn phải chọn phòng trước khi chọn thời gian")
            return
    def on_success(self,content):
        QMessageBox.information(
            self,  # parent window
            "Thành công",  # tiêu đề
            f"{content}"  # nội dung
        )
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = DatPhong2()
    ui.show()
    sys.exit(app.exec())