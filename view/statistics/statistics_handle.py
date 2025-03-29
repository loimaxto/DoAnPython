import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from view.statistics.statistics_ui import Ui_StatisticsMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np
from dao.nhan_vien_dao import NhanVienDAO
from dao.hoa_don_dao import HoaDonDAO
from dao.statistics_dao import ThongKeDAO
import datetime
class StatisticsMainWindow(QtWidgets.QWidget, Ui_StatisticsMainWindow):
    def __init__(self):      
        super().__init__()
        self.setupUi(self)  # Gọi setupUi đúng cách để khởi tạo UI
        self.dao_staff = NhanVienDAO() 
        self.dao_hoa_don = HoaDonDAO()
        self.dao_thong_ke = ThongKeDAO() 
        # Đảm bảo các widget được gọi đúng tên
        self.stackedWidget.setCurrentWidget(self.overViewPage)
        self.load_data()
        # Gán sự kiện cho các nút
        self.show_chart.clicked.connect(self.show_diagram)
        self.TongQuanBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.overViewPage))
        self.DoanhThuBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.doanhThuPage))

        self.model = QtGui.QStandardItemModel(0, 4)  # rows, columns
        self.model.setHorizontalHeaderLabels(["Thời gian", "Vốn", "Doanh thu", "Lợi nhuận"])
        self.tableOverView.setModel(self.model)
        # Resize columns
        self.tableOverView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableOverView.verticalHeader().setVisible(False) 
        self.tableOverView.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.tableOverView.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        
        # Load fake data
        self.load_fake_data()

        
    def load_fake_data(self, search_term=None):
        info_data = self.dao_thong_ke.get_thong_ke_7_ngay_gan_nhat()
        table_data = [(item.ngay , item.chiphi , item.doanhthu , item.loinhuan) for item in info_data]
        
        self.model.setRowCount(0)
        for row in table_data:
            if search_term:
                if search_term.lower() not in str(row[1]).lower() and search_term not in str(row[2]):
                    continue
            items = []
            for item in row:
                item_obj = QtGui.QStandardItem(str(item))
                item_obj.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item_obj.setFlags(item_obj.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                items.append(item_obj)
            self.model.appendRow(items)

    def show_diagram(self):
        self.overview_screen.addWidget(show_chart())
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
class show_chart(FigureCanvasQTAgg):
    def __init__(self):
        self.dao_hoa_don = HoaDonDAO()
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)

        today = datetime.date.today()
        dates = [today - datetime.timedelta(days=i) for i in range(7, -1, -1)]

        von = [0, 0, 0, 0, 0, 0, 0, 0]  # Replace with real data       
        doanh_thu = self.dao_hoa_don.get_doanh_thu_8_ngay_gan_nhat() or [1000000, 500000, 2000000, 1500000, 6000000, 2700000, 1500000, 900000]
        loi_nhuan = [doanh_thu[i] - von[i] for i in range(len(doanh_thu))]

        # Convert dates to string format
        date_labels = [date.strftime("%Y-%m-%d") for date in dates]

        x = np.arange(len(date_labels))  # X-axis positions
        width = 0.2  # Bar width

        # Plot Bars
        rects1 = self.ax.bar(x - width, von, width, label="Vốn", color="blue")
        rects2 = self.ax.bar(x, doanh_thu, width, label="Doanh thu", color="purple")
        rects3 = self.ax.bar(x + width, loi_nhuan, width, label="Lợi nhuận", color="brown")

        # Add labels on top of bars
        

        # Title and Labels
        self.fig.suptitle("Thống kê doanh thu 8 ngày gần nhất", fontsize=15)
        self.ax.set_ylabel("Giá trị (VNĐ)")
        self.ax.set_xlabel("Ngày")

        # Set X-axis labels
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(date_labels, rotation=30, ha="right")

        # Grid and Legend
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.ax.legend()
         
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = StatisticsMainWindow()
    mainwindow.show()
    sys.exit(app.exec())
