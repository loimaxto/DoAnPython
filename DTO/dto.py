class KhachHangDTO:
    def __init__(self, kh_id=None, ten=None, sdt=None, image=None):
        self.kh_id = kh_id
        self.ten = ten
        self.sdt = sdt
        self.image = image

    def __str__(self):
        return f"KhachHang(kh_id={self.kh_id}, ten='{self.ten}', sdt='{self.sdt}', image='{self.image}')"
    
class UserDTO:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f"UserDTO(user_id={self.user_id}, username='{self.username}', role='{self.role}')"

class DichVuDTO:
    def __init__(self, ten, gia):
        self.ten = ten
        self.gia = gia
    def __init__(self, dv_id=None, ten=None, gia=None):
        self.dv_id = dv_id
        self.ten = ten
        self.gia = gia
    
    def __str__(self):
        return f"DichVuDTO(dv_id={self.dv_id}, ten='{self.ten}', gia={self.gia})"
    
class NhanVienDTO:
    def __init__(self, nv_id=None, ten_nv=None, email=None, sdt=None, dia_chi=None, chuc_vu=None):
        self.nv_id = nv_id
        self.ten_nv = ten_nv
        self.email = email
        self.sdt = sdt
        self.dia_chi = dia_chi
        self.chuc_vu = chuc_vu

    def __str__(self):
        return f"KhachHang(nv_id={self.nv_id}, ten_nv='{self.ten_nv}', email='{self.email}', sdt='{self.sdt}', dia_chi='{self.dia_chi}', chuc_vu='{self.chuc_vu}')"
    
class HoaDonDTO:
    def __init__(self, hd_id=None, tong_tien=None, thoi_gian=None, nv_id=None, thanh_toan_status=None):
        self.hd_id = hd_id
        self.tong_tien = tong_tien
        self.thoi_gian = thoi_gian
        self.nv_id = nv_id
        self.thanh_toan_status = thanh_toan_status

    def __str__(self):
        return f"HoaDon(hd_id={self.hd_id}, tong_tien='{self.tong_tien}', thoi_gian='{self.thoi_gian}', nv_id='{self.nv_id}', thanh_toan_status='{self.thanh_toan_status}')"