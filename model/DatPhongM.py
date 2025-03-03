from datetime import datetime
class DatPhong:
    def __init__(self, booking_id: int, ngay_bd: datetime, ngay_kt: datetime, 
                 phi_dat_coc: float, note: str, phong_id: int, kh_id: int, tien_luc_dat: float):
        """
        Khởi tạo đối tượng đặt phòng
        
        :param booking_id: Mã đặt phòng
        :param ngay_bd: Ngày bắt đầu
        :param ngay_kt: Ngày kết thúc
        :param phi_dat_coc: Phí đặt cọc
        :param note: Ghi chú đặt phòng
        :param phong_id: ID phòng đặt
        :param kh_id: ID khách hàng
        :param tien_luc_dat: Số tiền phải trả tại thời điểm đặt
        """
        self.booking_id = booking_id
        self.ngay_bd = ngay_bd
        self.ngay_kt = ngay_kt
        self.phi_dat_coc = phi_dat_coc
        self.note = note
        self.phong_id = phong_id
        self.kh_id = kh_id
        self.tien_luc_dat = tien_luc_dat

    def update_booking(self, ngay_bd=None, ngay_kt=None, phi_dat_coc=None, note=None, phong_id=None, kh_id=None, tien_luc_dat=None):
        """
        Cập nhật thông tin đặt phòng
        
        :param ngay_bd: Ngày bắt đầu mới (nếu có)
        :param ngay_kt: Ngày kết thúc mới (nếu có)
        :param phi_dat_coc: Phí đặt cọc mới (nếu có)
        :param note: Ghi chú mới (nếu có)
        :param phong_id: ID phòng mới (nếu có)
        :param kh_id: ID khách hàng mới (nếu có)
        :param tien_luc_dat: Tiền lúc đặt mới (nếu có)
        """
        if ngay_bd:
            self.ngay_bd = ngay_bd
        if ngay_kt:
            self.ngay_kt = ngay_kt
        if phi_dat_coc:
            self.phi_dat_coc = phi_dat_coc
        if note:
            self.note = note
        if phong_id:
            self.phong_id = phong_id
        if kh_id:
            self.kh_id = kh_id
        if tien_luc_dat:
            self.tien_luc_dat = tien_luc_dat

    def calculate_total_days(self):
        """Tính số ngày đặt phòng"""
        return (self.ngay_kt - self.ngay_bd).days

    def __str__(self):
        return (f"DatPhong(booking_id={self.booking_id}, ngay_bd={self.ngay_bd}, ngay_kt={self.ngay_kt}, "
                f"phi_dat_coc={self.phi_dat_coc}, note='{self.note}', phong_id={self.phong_id}, "
                f"kh_id={self.kh_id}, tien_luc_dat={self.tien_luc_dat})")
