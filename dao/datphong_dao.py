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
    def update_hoaDonId_for_phieuDatPhong(self, hd_id, booking_id):
        query = "UPDATE dat_phong SET hd_id = ? WHERE booking_id = ?"
        return self.db.execute_query(query, (hd_id, booking_id)) is not None

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
                from dat_phong, khach_hang WHERE dat_phong.booking_id = ? and khach_hang.kh_id = dat_phong.kh_id"
        row = self.db.execute_query(query, (booking_id))
        if row:
            row = row[0]
            return DatPhongDTO(booking_id=row[0], ngay_bd=row[1], ngay_kt=row[2], phi_dat_coc=row[3], note=row[4], phong_id=row[5], tien_luc_dat=row[6], kh_id=row[7],ten_kh=row[8])
        else:
            print("phiếu đặt phòng dao: khong tim thấy phieu dat phòng")
            return None
    
    def get_all_phieu_dat_phong(self): # Corrected function name and signature
        query = """SELECT
                dp.booking_id,
                dp.ngay_bd,
                dp.ngay_kt,
                dp.phi_dat_coc,
                dp.note,
                dp.phong_id,
                dp.tien_luc_dat,
                kh.kh_id,
                kh.ten,
                kh.sdt        
            FROM
                dat_phong dp
            JOIN
                khach_hang kh ON kh.kh_id = dp.kh_id
            ORDER BY dp.booking_id desc
        """
        rows = self.db.execute_query(query)
        print(rows)
        if rows:
            phieu_dat_phong_list = []
            for row_data in rows: # Iterate through each row returned
                dto = DatPhongDTO(
                    booking_id=row_data[0], 
                    ngay_bd=row_data[1], 
                    ngay_kt=row_data[2], 
                    phi_dat_coc=row_data[3], 
                    note=row_data[4], 
                    phong_id=row_data[5], 
                    tien_luc_dat=row_data[6], 
                    kh_id=row_data[7],
                    ten_kh=row_data[8],
                    sdt=row_data[9],              
                )
                phieu_dat_phong_list.append(dto)
            return phieu_dat_phong_list 
        else:
            print("Phiếu đặt phòng DAO: Không tìm thấy phiếu đặt phòng nào.") 
            return []
        
if __name__ == "__main__":
    dv_dao = DatPhongDAO()
    print(dv_dao.get_all_phieu_dat_phong())
    print(dv_dao.get_phieuDatPhongById("1"))

