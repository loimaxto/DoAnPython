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
    QListWidget, QMessageBox, QLabel,QScrollArea
)
from PyQt6.QtCore import pyqtSignal

from view.DatPhong.dat_phong_ui import Ui_DatPhong_UI

from dao.khach_hang_dao import KhachHangDAO
from dao.phong_dao import PhongDAO
from dao.dich_vu_dao import DichVuDAO
from dao.ct_dv_dao import ChiTietDVDAO
from dao.hoadon_dao import HoaDonDAO
from dao.datphong_dao import DatPhongDAO
from view.hoadon.chitiet_hoadon_handle import chitiet_hoadon
class DatPhongWindow(QtWidgets.QWidget, Ui_DatPhong_UI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dao_phong = PhongDAO()
        self.dao_customer = KhachHangDAO()
        self.dao_hoaDon = HoaDonDAO()
        self.dao_ct_dv = ChiTietDVDAO()
        self.dao_datphong = DatPhongDAO()
        self.nv_id = 1
        self.cthd = chitiet_hoadon()
        
        self.listDvHdWidget = ListDichVuHoaDon(self)
        self.searchWindowWidget = SearchWindow(self)
        self.current_hoadon_dto = None
        self.current_phong_dto = None

        #  widget.setStyleSheet(f"background-color: {color};")       
        self.bodyW_layout = QVBoxLayout()
        self.bodyW.setLayout(self.bodyW_layout)
        self.bodyW_layout.addWidget(self.listDvHdWidget)
        
        self.verticalLayout_3.addWidget(self.searchWindowWidget)
        
        self.model = QtGui.QStandardItemModel(0, 5)  # rows, columns, added one for buttons
        self.model.setHorizontalHeaderLabels(["ID", "Tên phòng", "Loại phòng", "Tình trạng", "Hành động"])
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tableView.verticalHeader().setVisible(False)
        self.load_table_data()
        
        self.btnUpdateDatPhong.clicked.connect(self.insert_datPhongIdForCurrentHoaDon)
        self.btnCompletePayment.clicked.connect(self.completePaymentActionEvent)

    def completePaymentActionEvent(self):
        # xuất chi tiết hóa đơn
        self.cthd.show_all(self.current_hoadon_dto.hd_id)# thử nghiệm

        print("thanh toán")
        print("Hoa don dang chon: ", self.current_hoadon_dto.hd_id)
        self.cthd.show()
        
    def insert_datPhongIdForCurrentHoaDon(self):
        phieuDatPhongId = self.textEditIdPhieuDatPhong.toPlainText()
        # nếu phong hiện tại đã có hóa đơn thì cập nhật mã phiếu đặt phòng
        if self.current_hoadon_dto != None :
            phieuDatPhongDTO = self.dao_datphong.get_phieuDatPhongById(phieuDatPhongId)
            if phieuDatPhongDTO == None:
                QMessageBox.information(self, "", "Không tìm thấy mã phiếu đặt phòng này !")
                return
            else:
                self.current_hoadon_dto.dat_phong_id = phieuDatPhongId
                self.dao_hoaDon.update_hoa_don(self.current_hoadon_dto)
                self.lbCustomerName.setText(phieuDatPhongDTO.ten_kh)
                return
        else:
            QMessageBox.information(self, "", "Chọn phòng đang sử dụng để thêm phiếu đặt phòng !")
            return
        
    def convertStatus(self, numb):
        if numb == 0:
            return "Trống"
        else:
            return "Đang sử dụng"

    def load_table_data(self):
        phong_data = self.dao_phong.get_all_phong_for_order()
        table_data = []
        for row in phong_data:
            table_data.append([row[0], row[1], row[2], self.convertStatus(row[3])])

        self.model.setRowCount(0) #remove old data
        for row_index, row in enumerate(table_data):
            items = []
            for item in row:
                item_obj = QtGui.QStandardItem(str(item))
                item_obj.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                item_obj.setFlags(item_obj.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                items.append(item_obj)
            self.model.appendRow(items + [QtGui.QStandardItem("")]) # Add empty cell for button widget
            widget = CellButtonWidget(row,self)
            self.tableView.setIndexWidget(self.model.index(row_index, 4), widget) # Set the widget
    def render_dv_hoadon(self):
        self.listDvHdWidget.update_ct_dv()
    
    def resetHoaDon(self):
        self.current_hoadon_dto = None
        self.labelTableName.setText("Chưa chọn phòng !")
        self.listDvHdWidget.reset_ct_dv_layout()

    def handle_datphong(self, row_data):
        # print(row_data)
        # [101, 'Phòng 101', 'Phòng Đơn', 'Đang sử dụng']
        
        print("datphong -")
        print(row_data)
        self.current_hoadon_dto =  self.dao_hoaDon.insert_hoa_don(HoaDonDTO(nv_id=self.nv_id))
        print("datphong",self.current_hoadon_dto)
       
        #update trang that dat phong va hoa don hien tai
        self.dao_phong.update_tinh_trang_dat_phong(row_data[0], 1, self.current_hoadon_dto.hd_id) 
        update_phong_dto = self.dao_phong.get_phong_by_id(row_data[0])
        print("phong da dat: ",update_phong_dto)
        update_phong_dto.current_hoadon_id = self.current_hoadon_dto.hd_id
        
        self.current_phong_dto = update_phong_dto
        self.labelTableName.setText(update_phong_dto.ten_phong)
        
        self.load_table_data()
        print("dat phong thanh cong",row_data)
    def handle_delete(self, row_data):
        self.dao_phong.update_tinh_trang_dat_phong(row_data[0], 0,None) 
        self.load_table_data()
        self.resetHoaDon()
    def handle_view(self, row_data):
        self.current_phong_dto = self.dao_phong.get_phong_by_id(row_data[0])
        self.current_hoadon_dto = self.dao_hoaDon.get_hoa_don_by_id(self.current_phong_dto.current_hoadon_id)
        self.render_dv_hoadon()
        self.labelTableName.setText(self.current_phong_dto.ten_phong)
        # neu co phieu dat phong trong hoa đơn thì thực hiện
        if self.current_hoadon_dto.dat_phong_id != None :
            datphongDto = self.dao_datphong.get_phieuDatPhongById(str(self.current_hoadon_dto.dat_phong_id))
            if datphongDto != None:
                self.lbCustomerName.setText(datphongDto.ten_kh)
        else:
            print("chua co phieu dat phong")
            self.lbCustomerName.setText("Chưa thêm phiếu đặt phòng")
            return
        
        
class CellButtonWidget(QWidget):
    """Custom widget that contains three buttons in a table cell, with row data."""

    buttonClicked = pyqtSignal(int, str)  # Signal to emit row and button name
    
    def __init__(self, row_data, parent=None):
        super().__init__(parent)
        self.row_data = row_data
        self.datphong_class = parent
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.btn_dat_phong = QPushButton("Đặt phòng")
        self.btn_dat_phong.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_delete = QPushButton("Hủy")
        self.btn_delete.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_view = QPushButton("Chi tiết")
        self.btn_view.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.btn_dat_phong.setVisible(row_data[3] == "Trống")
        self.btn_delete.setVisible(row_data[3] == "Đang sử dụng")
        self.btn_view.setVisible(row_data[3] == "Đang sử dụng")

        layout.addWidget(self.btn_dat_phong)
        layout.addWidget(self.btn_view)
        layout.addWidget(self.btn_delete)

        self.btn_dat_phong.clicked.connect(lambda: self.datphong_class.handle_datphong(row_data))
        self.btn_delete.clicked.connect( lambda: self.datphong_class.handle_delete(row_data))
        self.btn_view.clicked.connect( lambda: self.datphong_class.handle_view(row_data))

        self.setLayout(layout)
    

class SearchWindow(QWidget):
    def __init__(self,datPhongWindow=None):
        super().__init__()
        self.dich_vu_dao = DichVuDAO()
        self.setWindowTitle("Tìm kiếm dịch Vụ")
        self.popup = None  # Add an instance variable for the popup
        self.DatPhongWindow = datPhongWindow
        
        layout = QVBoxLayout()
        self.label = QLabel("Nhập từ khóa:")
        self.search_input = QLineEdit()
        layout.addWidget(self.label)
        layout.addWidget(self.search_input)

        self.search_input.returnPressed.connect(self.perform_search)

        self.setLayout(layout)

    def perform_search(self):
        search_term = self.search_input.text()
        results = self.dich_vu_dao.search_dich_vu_by_name(search_term)

        if results:
            self.show_results_popup(results)
        else:
            QMessageBox.information(self, "", "Khong tìm thấy dịch vụ.")

    def show_results_popup(self, results):
        self.popup = QWidget()  # Assign the popup to the instance variable
        popup_layout = QVBoxLayout()
        result_list = QListWidget()
        popup_layout.addWidget(result_list)
        self.popup.setLayout(popup_layout)

        for result in results:
            item =  QListWidgetItem()
            item.dv_dto = result
            item.setText(result.ten)
            result_list.addItem(item)
            
           
        result_list.itemClicked.connect(self.handle_item_click) # Modified here
        self.popup.show()

    def handle_item_click(self, item): # Modified here
        picked_dv=self.DatPhongWindow.dao_ct_dv.get_chi_tiet_dv_by_hd_id(self.DatPhongWindow.current_hoadon_dto.hd_id)
        for ct_dv in picked_dv:
            if ct_dv.dv_id == item.dv_dto.dv_id:
                QMessageBox.information(self, "", "Dịch vụ đã được chọn !")
                return
        dto_ct_dv = ChiTietDVDTO(
            hd_id=self.DatPhongWindow.current_hoadon_dto.hd_id,
            dv_id=item.dv_dto.dv_id,
            so_luong=1,
            ten_dv=item.dv_dto.ten,
            gia_luc_dat=item.dv_dto.gia
        )
        self.DatPhongWindow.dao_ct_dv.insert_chi_tiet_dv(dto_ct_dv)
        self.DatPhongWindow.render_dv_hoadon()
        self.popup.close()

class ItemDichVuHoaDon(QWidget):
    def __init__(self, ct_dv_dto = ChiTietDVDTO(), parent=None):
        super().__init__(parent)
        self.ct_dv_dto = ct_dv_dto
        self.name = ct_dv_dto.ten_dv
        self.quantity = ct_dv_dto.so_luong
        self.datPhongWindow = parent
        self.ct_dv_dao = ChiTietDVDAO()
        
        #layout declare 
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        self.name_label = QLabel(self.name)
        self.name_label.setFixedWidth(150)
        main_layout.addWidget(self.name_label)

        quantity_layout = QHBoxLayout()
        main_layout.addLayout(quantity_layout)

        self.decrease_button = QPushButton("-")
        self.decrease_button.clicked.connect(self.decrease_quantity)
        self.decrease_button.setFixedWidth(50)
        quantity_layout.addWidget(self.decrease_button)
        self.decrease_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.quantity_input = QLineEdit(str(self.quantity))
        self.quantity_input.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.quantity_input.setFixedWidth(50)
        quantity_layout.addWidget(self.quantity_input)
        self.quantity_input.textChanged.connect(self.quantity_changed)
        self.quantity_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.increase_button = QPushButton("+")
        self.increase_button.clicked.connect(self.increase_quantity)
        self.increase_button.setFixedWidth(50)
        quantity_layout.addWidget(self.increase_button)
        self.increase_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def increase_quantity(self):
        self.quantity += 1
        self.quantity_input.setText(str(self.quantity))
        self.ct_dv_dto.so_luong = self.quantity
        self.ct_dv_dao.update_chi_tiet_dv(self.ct_dv_dto)
    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.quantity_input.setText(str(self.quantity))
            self.ct_dv_dao.update_chi_tiet_dv(self.ct_dv_dto)
        else:
            self.ct_dv_dao.delete_chi_tiet_dv(self.ct_dv_dto.hd_id, self.ct_dv_dto.dv_id)
            self.datPhongWindow.render_dv_hoadon()
            
            
    def quantity_changed(self, text):
        try:
            self.quantity = int(text)
            if self.quantity < 1:
                self.quantity = 1
                self.quantity_input.setText("1")
        except ValueError:
            self.quantity_input.setText(str(self.quantity))
       
class ListDichVuHoaDon(QWidget):
    def __init__(self,parent = None):
        super().__init__()
        self.datPhongWindow = parent
        self.ct_dv_dao = ChiTietDVDAO() 
        
        
        #layout declare
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.items_layout = QVBoxLayout()
        self.scroll_content = QWidget() #add this line.
        self.scroll_content.setLayout(self.items_layout) #add this line.
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.scroll_content)
        scroll_area.setWidgetResizable(True)

        main_layout.addWidget(scroll_area)

    

    def update_ct_dv(self):
        self.hoa_don_dto = self.datPhongWindow.current_hoadon_dto
        self.items = self.ct_dv_dao.get_chi_tiet_dv_by_hd_id(self.hoa_don_dto.hd_id)
        self.reset_ct_dv_layout()
        
        # Add items to the layout
        for ct_dv_dto in self.items:
            self.items_layout.addWidget(ItemDichVuHoaDon(ct_dv_dto,self.datPhongWindow))
    def reset_ct_dv_layout(self):
        # Clear the layout
        while self.items_layout.count():
            item = self.items_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def add_ct_dv(self,ct_dv_dto = ChiTietDVDTO()):
        # Add a new item to the list
        self.ct_dv_dao.insert_chi_tiet_dv(ct_dv_dto)
        self.update_items()
    def set_hoa_don_dto(self,hoa_don_dto):
        self.hoa_don_dto = hoa_don_dto
    def set_phong_dto(self,phong_dto):
        self.phong_dto = phong_dto
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DatPhongWindow()
    window.show()
    sys.exit(app.exec())