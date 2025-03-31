import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from view.statistics.statistics_ui import Ui_StatisticsMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np
from dao.nhan_vien_dao import NhanVienDAO
from dao.hoa_don_dao import HoaDonDAO
from dao.statistics_dao import ThongKeDAO
from dao.phong_dao import PhongDAO
from dto.dto import ThongKeTheoThangDTO, ThongKeDoanhThuDTO

import datetime
import locale
class StatisticsMainWindow(QtWidgets.QWidget, Ui_StatisticsMainWindow):
    def __init__(self):      
        super().__init__()
        self.diagram_shown = False
        self.setupUi(self)  # Gọi setupUi đúng cách để khởi tạo UI
        self.dao_phong = PhongDAO()
        self.dao_staff = NhanVienDAO() 
        self.dao_hoa_don = HoaDonDAO()
        self.dao_thong_ke = ThongKeDAO() 

        # Đảm bảo các widget được gọi đúng tên
        self.stackedWidget.setCurrentWidget(self.overViewPage)
        self.load_data()
        # Gán sự kiện cho các nút
        # self.show_chart.clicked.connect(self.show_diagram)
        self.overview_screen.addWidget(show_chart())
        self.TongQuanBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.overViewPage))
        self.DoanhThuBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.doanhThuPage))

        self.modelTongQuan = QtGui.QStandardItemModel(0, 2)  # rows, columns
        self.modelTongQuan.setHorizontalHeaderLabels(["Thời gian", "Doanh thu"])
        self.tableOverView.setModel(self.modelTongQuan)
        # Resize columns
        self.tableOverView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableOverView.verticalHeader().setVisible(False) 
        self.tableOverView.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.tableOverView.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        
        # Load data table
        locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')

        # Định dạng số tiền
        self.load_data_table_tong_quan()

        
    def load_data_table_tong_quan(self, search_term=None):
        info_data = self.dao_thong_ke.getDoanhThu7NgayGanNhat()
        print(info_data)
        if not info_data:
            print("Lỗi: Không có dữ liệu để hiển thị trong bảng.")
            return

        table_data = [(item.date,locale.currency(item.doanh_thu, grouping=True)) for item in info_data]
        
        self.modelTongQuan.setRowCount(0)
        for row in table_data:
            if search_term:
                if search_term.lower() not in str(row[0]).lower() and search_term.lower() not in str(row[1]).lower():
                    continue
            items = []
            for item in row:
                item_obj = QtGui.QStandardItem(str(item))
                item_obj.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item_obj.setFlags(item_obj.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                items.append(item_obj)
            self.modelTongQuan.appendRow(items)

    # def show_diagram(self):
    #     if not self.diagram_shown:  # Chỉ chạy nếu chưa chạy trước đó
    #         self.overview_screen.addWidget(show_chart())
    #         self.diagram_shown = True  # Đánh dấu là đã chạy

    def load_data(self):
        if not self.dao_staff:
            print("Lỗi: Không thể tải dữ liệu vì DAO chưa được khởi tạo!")
            return
        
        try:
            # Lấy số lượng nhân viên từ database
            number_of_staff = self.dao_staff.get_number_of_staff()
            
            # Kiểm tra và cập nhật QLabel
            if hasattr(self, 'occupied_rooms') and isinstance(self.staffs, QtWidgets.QLabel):
                self.staffs.setText(str(number_of_staff))
            else:
                print("Lỗi: 'occupied_rooms' không tồn tại hoặc không phải QLabel.")
        
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu nhân viên: {e}")

        if not self.dao_phong:
            print("Lỗi: Không thể tải dữ liệu vì DAO chưa được khởi tạo!")
            return
        
        try:
            # Lấy số lượng phòng từ database
            number_of_rooms = self.dao_phong.get_all_available_phong()
            
            # Kiểm tra và cập nhật QLabel
            if hasattr(self, 'available_rooms') and isinstance(self.available_rooms, QtWidgets.QLabel):
                self.available_rooms.setText(str(number_of_rooms))
            else:
                print("Lỗi: 'available_rooms' không tồn tại hoặc không phải QLabel.")
        
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu nhân viên: {e}")

        if not self.dao_phong:
            print("Lỗi: Không thể tải dữ liệu vì DAO chưa được khởi tạo!")
            return
        
        try:
            # Lấy số lượng phòng từ database
            number_of_rooms = self.dao_phong.get_all_occupied_phong()
            
            # Kiểm tra và cập nhật QLabel
            if hasattr(self, 'occupied_rooms') and isinstance(self.occupied_rooms, QtWidgets.QLabel):
                self.occupied_rooms.setText(str(number_of_rooms))
            else:
                print("Lỗi: 'occupied_rooms' không tồn tại hoặc không phải QLabel.")
        
        except Exception as e:
            print(f"Lỗi khi tải dữ liệu nhân viên: {e}")

class show_chart(FigureCanvasQTAgg):
    def __init__(self):
        self.dao_thong_ke = ThongKeDAO() 
        self.dao_hoa_don = HoaDonDAO()
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)

        today = datetime.date.today()
        dates = [today - datetime.timedelta(days=i) for i in range(6, -1, -1)]

        data_doanh_thu = self.dao_thong_ke.getDoanhThu7NgayGanNhat()      
        # doanh_thu = self.dao_hoa_don.get_doanh_thu_8_ngay_gan_nhat() or [1000000, 500000, 2000000, 1500000, 6000000, 2700000, 1500000, 900000]
        doanh_thu = [(item.doanh_thu) for item in data_doanh_thu]
        # Convert dates to string format
        date_labels = [date.strftime("%Y-%m-%d") for date in dates]

        x = np.arange(len(date_labels))  # X-axis positions
        width = 0.2  # Bar width

        # Plot Bars
       
        rects = self.ax.bar(x, doanh_thu, width, label="Doanh thu", color="purple")
        

        # Add labels on top of bars
        

        # Title and Labels
        self.fig.suptitle("Thống kê doanh thu 7 ngày gần nhất", fontsize=15)
        self.ax.set_ylabel("Giá trị (Triệu VNĐ)")
        self.ax.set_xlabel("Ngày")

        # Set X-axis labels
        # self.ax.set_xticks(x)
        # self.ax.set_xticklabels(date_labels, rotation=30, ha="right")

        step = max(1, len(x) // 10)  # Hiển thị khoảng 10 nhãn, điều chỉnh tùy dữ liệu
        self.ax.set_xticks(x[::step])
        self.ax.set_xticklabels(date_labels[::step], rotation=0, ha="right")

        # Grid and Legend
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.ax.legend()
         
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = StatisticsMainWindow()
    mainwindow.show()
    sys.exit(app.exec())
