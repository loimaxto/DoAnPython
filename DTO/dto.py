class KhachHangDTO:
    def __init__(self, kh_id=None, ten=None, sdt=None, image="None"):
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
class DatPhongDTO:
    def __init__(self, booking_id=None, ngay_bd=None, ngay_kt=None, phi_dat_coc=None, note=None, phong_id=None, tien_luc_dat=None, kh_id=None, ten_kh = None):
        self.booking_id = booking_id
        self.ngay_bd = ngay_bd
        self.ngay_kt = ngay_kt
        self.phi_dat_coc = phi_dat_coc
        self.note = note
        self.phong_id = phong_id
        self.tien_luc_dat = tien_luc_dat
        self.kh_id = kh_id
        self.ten_kh = ten_kh

    def __repr__(self):
        return f"DatPhongDTO(booking_id={self.booking_id}, ngay_bd='{self.ngay_bd}', ngay_kt='{self.ngay_kt}', phi_dat_coc={self.phi_dat_coc}, note='{self.note}', phong_id={self.phong_id}, tien_luc_dat={self.tien_luc_dat}, kh_id={self.kh_id}), kh_ten={self.ten_kh})"

class PhongDTO:
    def __init__(self, id=None, ten_phong=None, so_giuong=None, id_gia=None, tinh_trang_dat_phong=0, tinh_trang_su_dung=None,current_hoadon_id=None):
        self.id = id
        self.ten_phong = ten_phong
        self.so_giuong = so_giuong
        self.id_gia = id_gia
        self.tinh_trang_dat_phong = tinh_trang_dat_phong
        self.tinh_trang_su_dung = tinh_trang_su_dung
        self.current_hoadon_id=current_hoadon_id
    def __init__(self, id, ten, sogiuong, loai):
        self.id = id
        self.ten_phong = ten
        self.so_giuong = sogiuong
        self.loai = loai
    def __repr__(self):
        try:
            return f"PhongDTO(id={self.id}, ten_phong='{self.ten_phong}', so_giuong={self.so_giuong}, id_gia={self.id_gia}, tinh_trang_dat_phong={self.tinh_trang_dat_phong}, tinh_trang_su_dung={self.tinh_trang_su_dung}, hoadon_id={ self.current_hoadon_id})"
        except:
            pass
class GiaPhongDTO:
    def __init__(self,id=None,ten_loai=None,gia_gio=None,gia_ngay=None,gia_dem=None):
        self.id = id
        self.ten_loai = ten_loai
        self.gia_gio = gia_gio
        self.gia_ngay = gia_ngay
        self.gia_dem = gia_dem
    def __repr__(self):
        return f"GiaPhongDTO(id={self.id},ten_loai={self.ten_loai},gia_gio={self.gia_gio},gia_ngay={self.gia_ngay},gia_dem={self.gia_dem})"
class ChiTietDVDTO:
    def __init__(self, hd_id=None, dv_id=None, so_luong=None, gia_luc_dat=None, tong=None, ten_dv=None, gia_dv=None):
        self.hd_id = hd_id
        self.dv_id = dv_id
        self.so_luong = so_luong
        self.gia_luc_dat = gia_luc_dat
        self.tong = tong
        self.ten_dv = ten_dv
        self.gia_dv = gia_dv

    def __repr__(self):
        return f"ChiTietDichVuDTO(hd_id={self.hd_id}, dv_id={self.dv_id}, so_luong={self.so_luong}, gia_luc_dat={self.gia_luc_dat}, tong={self.tong}, ten_dv={self.ten_dv}, gia_dv={self.gia_dv})"
class HoaDonDTO:
    def __init__(self, hd_id=None, tong_tien=None, thoi_gian=None, nv_id=None, thanh_toan_status=None,dat_phong_id=None):
        self.hd_id = hd_id
        self.tong_tien = tong_tien
        self.thoi_gian = thoi_gian
        self.nv_id = nv_id
        self.thanh_toan_status = thanh_toan_status
        self.dat_phong_id = dat_phong_id
    def __repr__(self):
        return f"HoaDonDTO(hd_id={self.hd_id}, tong_tien={self.tong_tien}, thoi_gian='{self.thoi_gian}', nv_id={self.nv_id}, thanh_toan_status={self.thanh_toan_status}), dat_phong_id={self.dat_phong_id})"

# DTO THONG KE
class ThongKeDoanhThuDTO:
    def __init__(self, date,doanh_thu):
        self.date = date
        self.doanh_thu = doanh_thu
    def __str__(self):
        return f"ThongKe(date='{self.date}', doanh_thu={self.doanh_thu})"
    
class ThongKeTheoThangDTO:
    def __init__(self, thang,doanh_thu):
        self.thang = thang
        self.doanh_thu = doanh_thu
    def __str__(self):
        return f"ThongKe(thang='{self.thang}', doanh_thu={self.doanh_thu})"
    
class ThongKeTheoTungNgayTrongThangDTO:
    def __init__(self, ngay,doanh_thu):
        self.ngay = ngay
        self.doanh_thu = doanh_thu
    def __str__(self):
        return f"ThongKe(ngay='{self.ngay}', doanh_thu={self.doanh_thu})"
    
