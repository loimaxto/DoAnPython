import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(project_path)
print(project_path) #print relative path c:\Code\DoAnPython
from dto.dto import ChiTietDVDTO
from utils.database import SQLiteDB

class ChiTietDVDAO:
    def __init__(self):
        self.db = SQLiteDB()

    def insert_chi_tiet_dv(self, chi_tiet_dv):
        query = "INSERT INTO chi_tiet_dv (hd_id, dv_id, so_luong, gia_luc_dat, tong) VALUES (?, ?, ?, ?, ?)"
        return self.db.execute_query(query, 
        (chi_tiet_dv.hd_id, chi_tiet_dv.dv_id, 
         chi_tiet_dv.so_luong, 
         chi_tiet_dv.gia_luc_dat, 
         chi_tiet_dv.so_luong * chi_tiet_dv.gia_luc_dat)) is not None

    def update_chi_tiet_dv(self, chi_tiet_dv):
        query = "UPDATE chi_tiet_dv SET so_luong = ?, gia_luc_dat = ?, tong = ? WHERE hd_id = ? AND dv_id = ?"
        return self.db.execute_query(query, (chi_tiet_dv.so_luong, chi_tiet_dv.gia_luc_dat, chi_tiet_dv.so_luong * chi_tiet_dv.gia_luc_dat, chi_tiet_dv.hd_id, chi_tiet_dv.dv_id)) is not None

    def delete_chi_tiet_dv(self, hd_id, dv_id):
        query = "DELETE FROM chi_tiet_dv WHERE hd_id = ? AND dv_id = ?"
        return self.db.execute_query(query, (hd_id, dv_id)) is not None
    def insert_ctdv_by_hdid(self,hd_id):
        from dao.dich_vu_dao import DichVuDAO
        hoadon = DichVuDAO()
        table_dichvu = hoadon.get_all_DichVu()
        
        for i in table_dichvu:
            query = "INSERT INTO chi_tiet_dv (hd_id, dv_id, so_luong, gia_luc_dat, tong) VALUES (?, ?, ?, ?, ?)"
            self.db.execute_query(query, 
            (hd_id, i.dv_id, 
            0, 
            i.gia, 
            0))

    def get_all_chi_tiet_dv(self):
        """Gets all chi_tiet_dv data, including ten_dv and gia_dv from dich_vu."""
        query ="SELECT chi_tiet_dv.hd_id, chi_tiet_dv.dv_id, chi_tiet_dv.so_luong, chi_tiet_dv.gia_luc_dat, chi_tiet_dv.tong, dich_vu.ten_dv, dich_vu.gia FROM chi_tiet_dv INNER JOIN dich_vu ON chi_tiet_dv.dv_id = dich_vu.dv_id"
        rows = self.db.execute_query(query)
        if rows:
            return [ChiTietDVDTO(hd_id=row[0], dv_id=row[1], so_luong=row[2], gia_luc_dat=row[3], tong=row[4], ten_dv=row[5], gia_dv=row[6]) for row in rows]
        else:
            return []

    def get_chi_tiet_dv_by_ids(self, hd_id, dv_id):

        query = "SELECT chi_tiet_dv.hd_id, chi_tiet_dv.dv_id, chi_tiet_dv.so_luong, chi_tiet_dv.gia_luc_dat, chi_tiet_dv.tong, dich_vu.ten_dv, dich_vu.gia FROM chi_tiet_dv INNER JOIN dich_vu ON chi_tiet_dv.dv_id = dich_vu.dv_id WHERE chi_tiet_dv.hd_id = ? AND chi_tiet_dv.dv_id = ?"
        row = self.db.execute_query(query, (hd_id, dv_id))
        if row:
            row = row[0]
            return ChiTietDVDTO(hd_id=row[0], dv_id=row[1], so_luong=row[2], gia_luc_dat=row[3], tong=row[4], ten_dv=row[5], gia_dv=row[6])
        else:
            return None

    def get_chi_tiet_dv_by_hd_id(self, hd_id):
        """Gets chi_tiet_dv data by hd_id, including ten_dv and gia_dv from dich_vu."""
        query = "SELECT chi_tiet_dv.hd_id, chi_tiet_dv.dv_id, chi_tiet_dv.so_luong, chi_tiet_dv.gia_luc_dat, chi_tiet_dv.tong, dich_vu.ten_dv, dich_vu.gia FROM chi_tiet_dv INNER JOIN dich_vu ON chi_tiet_dv.dv_id = dich_vu.dv_id WHERE chi_tiet_dv.hd_id = ?"
        
        rows = self.db.execute_query(query, (hd_id,))
        if rows:
            return [ChiTietDVDTO(hd_id=row[0], dv_id=row[1], so_luong=row[2], gia_luc_dat=row[3], tong=row[4], ten_dv=row[5], gia_dv=row[6]) for row in rows]
        else:
            return []
        
if __name__ == "__main__":
    dv_dao = ChiTietDVDAO()
    for i in range(1,17):
        for j in range(1,5):
            dv_dao.delete_chi_tiet_dv(i,j)