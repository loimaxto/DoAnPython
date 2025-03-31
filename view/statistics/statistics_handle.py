import sys
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt
from view.statistics.statistics_ui import Ui_StatisticsMainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import numpy as np
from dao.nhan_vien_dao import NhanVienDAO
from dao.hoa_don_dao import HoaDonDAO
from dao.statistics_dao import ThongKeDAO
from dao.phong_dao import PhongDAO
import pandas as pd
from dto.dto import ThongKeTheoThangDTO, ThongKeDoanhThuDTO, ThongKeTheoTungNgayTrongThangDTO

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
        self.stackedWidget_2.setCurrentWidget(self.thongKeTheoNamPage)
        self.load_data()
        # Gán sự kiện cho các nút
        # self.show_chart.clicked.connect(self.show_diagram)
        self.overview_screen.addWidget(show_chart())
        self.yearScreenChart.addWidget(show_year_chart(2020, 2025))
        self.monthScreenChart.addWidget(show_month_chart(2025))
        self.TongQuanBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.overViewPage))
        self.DoanhThuBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.doanhThuPage))

        self.StaYearBtn.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.thongKeTheoNamPage))
        self.StaMonthBtn.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.thongKeTheoTNTTPage))
        self.StaDayToDayBtn.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.thongKeTheoTTTNPage))

        self.statistisBtn.clicked.connect(self.search_data)
        self.refreshBtn.clicked.connect(self.refresh_data)

         # Gán sự kiện cho các nút xuất excel
        self.exportExcelBtn.clicked.connect(lambda: self.export_qtableview_to_excel(self.tableYearStatisticView))
        self.exportExcelBtn_2.clicked.connect(lambda: self.export_qtableview_to_excel(self.tableMonthStatisticView))
        self.exportExcelBtn_3.clicked.connect(lambda: self.export_qtableview_to_excel(self.tableDateStatisticView))

        self.yearOfMonths.setMinimum(0)
        self.yearOfMonths.setMaximum(10000)
        self.yearOfMonths.setValue(2025)  # Set default value to 2025
        self.yearOfMonths.setSingleStep(1)  # Set step to 1 year
        self.yearOfMonths.valueChanged.connect(self.update_month_chart)
        self.dateStartTXT.setDisplayFormat("yyyy-MM-dd")
        self.dateEndTXT.setDisplayFormat("yyyy-MM-dd")
        self.statisticDateBtn.clicked.connect(lambda: self.load_data_table_theo_ngay(self.dateStartTXT.text(), self.dateEndTXT.text()))
        self.refreshDateBtn.clicked.connect(self.refresh_date_data)

        self.modelTongQuan = QtGui.QStandardItemModel(0, 2)  # rows, columns
        self.modelTongQuan.setHorizontalHeaderLabels(["Thời gian", "Doanh thu"])
        self.tableOverView.setModel(self.modelTongQuan)
        # Resize columns
        self.tableOverView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableOverView.verticalHeader().setVisible(False) 
        self.tableOverView.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.tableOverView.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)
        
        # trang thong ke doanh thu
        self.modelYearStatistics = QtGui.QStandardItemModel(0, 2)  # rows, columns
        self.modelYearStatistics.setHorizontalHeaderLabels(["Năm", "Doanh thu"])
        self.tableYearStatisticView.setModel(self.modelYearStatistics)
        # Resize columns
        self.tableYearStatisticView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableYearStatisticView.verticalHeader().setVisible(False) 
        self.tableYearStatisticView.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.tableYearStatisticView.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)

        
        self.modelMonthStatistics = QtGui.QStandardItemModel(0, 2)  # rows, columns
        self.modelMonthStatistics.setHorizontalHeaderLabels(["Tháng", "Doanh thu"])
        self.tableMonthStatisticView.setModel(self.modelMonthStatistics)
        # Resize columns
        self.tableMonthStatisticView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableMonthStatisticView.verticalHeader().setVisible(False) 
        self.tableMonthStatisticView.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.tableMonthStatisticView.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)

        self.modelDateStatistics = QtGui.QStandardItemModel(0, 2)  # rows, columns
        self.modelDateStatistics.setHorizontalHeaderLabels(["Tháng", "Doanh thu"])
        self.tableDateStatisticView.setModel(self.modelDateStatistics)
        # Resize columns
        self.tableDateStatisticView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableDateStatisticView.verticalHeader().setVisible(False) 
        self.tableDateStatisticView.setSelectionMode(QtWidgets.QTableView.SelectionMode.SingleSelection)
        self.tableDateStatisticView.setSelectionBehavior(QtWidgets.QTableView.SelectionBehavior.SelectRows)

        # Load data table
        locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')

        self.load_data_table_tong_quan()
        self.load_data_table_doanh_thu()
        self.load_data_table_theo_thang()
        self.load_data_table_theo_ngay()

    def load_data_table_tong_quan(self, search_term=None):
        info_data = self.dao_thong_ke.getDoanhThu7NgayGanNhat()
        
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
    
    def load_data_table_doanh_thu(self,year_start=None, year_end=None):
        info_data = self.dao_thong_ke.getDoanhThuTheoNam(year_start, year_end) if year_start and year_end else self.dao_thong_ke.getDoanhThuTheoNam(2020, 2025)
        if not info_data:
            print("Lỗi: Không có dữ liệu để hiển thị trong bảng.")
            return

        table_data = [(item.date,locale.currency(item.doanh_thu, grouping=True)) for item in info_data]
        
        self.modelYearStatistics.setRowCount(0)
        for row in table_data:
            items = []
            for item in row:
                item_obj = QtGui.QStandardItem(str(item))
                item_obj.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item_obj.setFlags(item_obj.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                items.append(item_obj)
            self.modelYearStatistics.appendRow(items)

    def load_data_table_theo_thang(self,year=None):
        info_data = self.dao_thong_ke.getDoanhThuTheoThang(year) if year else self.dao_thong_ke.getDoanhThuTheoThang(2025)
        if not info_data:
            print("Lỗi: Không có dữ liệu để hiển thị trong bảng.")
            return

        table_data = [(item.thang,locale.currency(item.doanh_thu, grouping=True)) for item in info_data]
        
        self.modelMonthStatistics.setRowCount(0)
        for row in table_data:
            items = []
            for item in row:
                item_obj = QtGui.QStandardItem(str(item))
                item_obj.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item_obj.setFlags(item_obj.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                items.append(item_obj)
            self.modelMonthStatistics.appendRow(items)
    
    def load_data_table_theo_ngay(self,dateStart=None , dateEnd=None):
        info_data = self.dao_thong_ke.getDoanhThuTuNgayDenNgay(dateStart, dateEnd)
        if not info_data:
            print("Lỗi: Không có dữ liệu để hiển thị trong bảng.")
            return

        table_data = [(item.ngay,locale.currency(item.doanh_thu, grouping=True)) for item in info_data]
        
        self.modelDateStatistics.setRowCount(0)
        for row in table_data:
            items = []
            for item in row:
                item_obj = QtGui.QStandardItem(str(item))
                item_obj.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item_obj.setFlags(item_obj.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                items.append(item_obj)
            self.modelDateStatistics.appendRow(items)

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

    def search_data(self):
        year_start = self.startYearTXT.text()
        year_end = self.endYearTXT.text()

        if not year_start or not year_end:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập năm bắt đầu và kết thúc.")
            return

        try:
            year_start = int(year_start)
            year_end = int(year_end)
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Năm phải là số nguyên.")
            return

        if year_start > year_end:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Năm bắt đầu không thể lớn hơn năm kết thúc.")
            return
        if year_start < 2020 or year_end > 2025:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Năm phải nằm trong khoảng từ 2020 đến 2025.")
            return

        self.load_data_table_doanh_thu(year_start, year_end)
        # Tạo và thêm biểu đồ mới vào yearScreenChart
        # Clear the layout and add the new chart
        for i in reversed(range(self.yearScreenChart.count())):
            widget_to_remove = self.yearScreenChart.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        self.yearScreenChart.addWidget(show_year_chart(year_start, year_end))

    def refresh_data(self):
        self.startYearTXT.clear()
        self.endYearTXT.clear()
        self.load_data_table_doanh_thu()
        # Tạo và thêm biểu đồ mới vào yearScreenChart
        for i in reversed(range(self.yearScreenChart.count())):
            widget_to_remove = self.yearScreenChart.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        self.yearScreenChart.addWidget(show_year_chart(2020, 2025))

    def update_month_chart(self):
        year = self.yearOfMonths.value()
        self.load_data_table_theo_thang(year)
        # Tạo và thêm biểu đồ mới vào monthScreenChart  
        for i in reversed(range(self.monthScreenChart.count())):
            widget_to_remove = self.monthScreenChart.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)
        self.monthScreenChart.addWidget(show_month_chart(year))

    def refresh_date_data(self):
        self.dateStartTXT.setDate(QtCore.QDate.fromString("2020-01-01", "yyyy-MM-dd"))
        self.dateEndTXT.setDate(QtCore.QDate.fromString("2020-01-01", "yyyy-MM-dd"))
        self.modelDateStatistics.setRowCount(0)

    def export_qtableview_to_excel(self, table_view):
            # Open file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Excel File", "", "Excel Files (*.xlsx);;All Files (*)"
        )

        if not file_path:
            return  # User canceled the save dialog

        # Ensure file has a .xlsx extension
        if not file_path.endswith(".xlsx"):
            file_path += ".xlsx"

        # Get the model from QTableView
        model = table_view.model()
        if not model:
            print("❌ No model found in QTableView!")
            return

        # Extract data from the model
        rows = model.rowCount()
        cols = model.columnCount()

        # Get column headers
        headers = [model.headerData(col, Qt.Orientation.Horizontal) for col in range(cols)]

        # Get table data
        data = []
        for row in range(rows):
            row_data = []
            for col in range(cols):
                index = model.index(row, col)
                value = model.data(index)
                row_data.append(value if value is not None else "")  # Handle empty cells
            data.append(row_data)

        # Convert to DataFrame
        df = pd.DataFrame(data, columns=headers)

        # Try to export to Excel
        try:
            df.to_excel(file_path, index=False, engine='xlsxwriter')
            print(f"✅ Exported table data to {file_path} successfully!")
        except Exception as e:
            print(f"❌ Error exporting to Excel: {e}")

    
           
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

class show_year_chart(FigureCanvasQTAgg):
    def __init__(self ,yearStart ,yearEnd):
        self.yearStart = yearStart
        self.yearEnd = yearEnd
        self.dao_thong_ke = ThongKeDAO() 
        self.dao_hoa_don = HoaDonDAO()
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)

        
        years = [year for year in range(yearStart, yearEnd + 1)]


        data_doanh_thu = self.dao_thong_ke.getDoanhThuTheoNam(year_start=yearStart, year_end=yearEnd)      
        # doanh_thu = self.dao_hoa_don.get_doanh_thu_8_ngay_gan_nhat() or [1000000, 500000, 2000000, 1500000, 6000000, 2700000, 1500000, 900000]
        doanh_thu = [(item.doanh_thu) for item in data_doanh_thu]
        

        x = np.arange(len(years))  # X-axis positions
        width = 0.2  # Bar width

        # Plot Bars
       
        rects = self.ax.bar(x, doanh_thu, width, label="Doanh thu", color="purple")
        

        # Add labels on top of bars
        

        # Title and Labels
        self.ax.set_ylabel("Giá trị (Triệu VNĐ)")
        self.ax.set_xlabel("Năm")

        # Set X-axis labels
        # self.ax.set_xticks(x)
        # self.ax.set_xticklabels(date_labels, rotation=30, ha="right")

        step = max(1, len(x) // 10)  # Hiển thị khoảng 10 nhãn, điều chỉnh tùy dữ liệu
        self.ax.set_xticks(x[::step])
        self.ax.set_xticklabels(years[::step], rotation=0, ha="right")

        # Grid and Legend
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.ax.legend()

class show_month_chart(FigureCanvasQTAgg):
    def __init__(self ,year):
        self.year = year
        self.dao_thong_ke = ThongKeDAO() 
        self.dao_hoa_don = HoaDonDAO()
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)

        months = [month for month in range(1, 13)]
        
        data_doanh_thu = self.dao_thong_ke.getDoanhThuTheoThang(nam=year)      
        
        doanh_thu = [(item.doanh_thu) for item in data_doanh_thu]
        

        x = np.arange(len(months))  # X-axis positions
        width = 0.2  # Bar width

        # Plot Bars
       
        rects = self.ax.bar(x, doanh_thu, width, label="Doanh thu", color="purple")
        

        # Add labels on top of bars
        

        # Title and Labels
        self.ax.set_ylabel("Giá trị (Triệu VNĐ)")
        self.ax.set_xlabel("Tháng")

        # Set X-axis labels
        # self.ax.set_xticks(x)
        # self.ax.set_xticklabels(date_labels, rotation=30, ha="right")

        step = max(1, len(x) // 10)  # Hiển thị khoảng 10 nhãn, điều chỉnh tùy dữ liệu
        self.ax.set_xticks(x[::step])
        self.ax.set_xticklabels(months[::step], rotation=0, ha="right")

        # Grid and Legend
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.ax.legend()
        
 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = StatisticsMainWindow()
    mainwindow.show()
    sys.exit(app.exec())
