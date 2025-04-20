import sys
import os

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

sys.path.append(project_path)
print(project_path) #print relative path c:\Code\DoAnPython

from dto.dto import DatPhongDTO
from utils.database import SQLiteDB

class DatPhongDAO:
    def __init__(self):
        self.db = SQLiteDB()

    def insert_chi_tiet_dv(self, chi_tiet_dv):
        query = "INSERT INTO chi_tiet_dv (hd_id, dv_id, so_luong, gia_luc_dat, tong) VALUES (?, ?, ?, ?, ?)"
        return self.db.execute_query(query, (chi_tiet_dv.hd_id, chi_tiet_dv.dv_id, chi_tiet_dv.so_luong, chi_tiet_dv.gia_luc_dat, chi_tiet_dv.so_luong * chi_tiet_dv.gia_luc_dat)) is not None
   
    def get_phieuDatPhongById(self, booking_id):
        if booking_id == None:
            return 
        print("phiếu đặt phòng dao id: ",booking_id)
        query = "Select \
                booking_id,\
                ngay_bd,\
                ngay_kt,\
                phi_dat_coc,\
                note,\
                phong_id,\
                tien_luc_dat,\
                khach_hang.kh_id ,\
                khach_hang.ten \
                from dat_phong, khach_hang WHERE dat_phong.hd_id = ? and khach_hang.kh_id = dat_phong.kh_id"
        row = self.db.execute_query(query, (booking_id))
        if row:
            row = row[0]
            return DatPhongDTO(booking_id=row[0], ngay_bd=row[1], ngay_kt=row[2], phi_dat_coc=row[3], note=row[4], phong_id=row[5], tien_luc_dat=row[6], kh_id=row[7],ten_kh=row[8])
        else:
            print("phiếu đặt phòng dao: khong tim thấy phieu dat phòng")
            return None
if __name__ == "__main__":
    dv_dao = DatPhongDAO()
    print(dv_dao.get_phieuDatPhongById("1"))

# def __init__(self, booking_id=None, ngay_bd=None, ngay_kt=None, phi_dat_coc=None, note=None, phong_id=None, tien_luc_dat=None, kh_id=None):
#         self.booking_id = booking_id
#         self.ngay_bd = ngay_bd
#         self.ngay_kt = ngay_kt
#         self.phi_dat_coc = phi_dat_coc
#         self.note = note
#         self.phong_id = phong_id
#         self.tien_luc_dat = tien_luc_dat
#         self.kh_id = kh_id