import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(project_path)
print(project_path) #print relative path c:\Code\DoAnPython
from dto.dto import HoaDonDTO
from utils.database import SQLiteDB

class HoaDonDAO:
    def __init__(self):
        self.db = SQLiteDB()

    def get_all_hoa_don(self):
        query = "SELECT hd_id, tong_tien, thoi_gian, nv_id, thanh_toan_status FROM hoa_don"
        rows = self.db.execute_query(query)
        if rows:
            return [HoaDonDTO(hd_id=row[0], tong_tien=row[1], thoi_gian=row[2], nv_id=row[3], thanh_toan_status=row[4]) for row in rows]
        else:
            return []

    def get_hoa_don_by_id(self, hd_id):
        query = "SELECT hd_id, tong_tien, thoi_gian, nv_id, thanh_toan_status,dat_phong_id FROM hoa_don WHERE hd_id = ?"
        row = self.db.execute_query(query, (hd_id,))
        if row:
            row = row[0]
            return HoaDonDTO(hd_id=row[0], tong_tien=row[1], thoi_gian=row[2], nv_id=row[3], thanh_toan_status=row[4],dat_phong_id=row[5])
        else:
            return None

    def insert_hoa_don(self, hoa_don):
        query = "INSERT INTO hoa_don (tong_tien, thoi_gian, nv_id, thanh_toan_status) VALUES (?, ?, ?, ?)"
        result = self.db.execute_query(query, (hoa_don.tong_tien, hoa_don.thoi_gian, hoa_don.nv_id, hoa_don.thanh_toan_status), return_last_row=True)

        if result:
            return HoaDonDTO(
                hd_id=result[0],
                tong_tien=result[1],
                thoi_gian=result[2],
                nv_id=result[3],
                thanh_toan_status=result[4]
            )
        else:
            return None
        
    def update_hoa_don(self, hoa_don):
        query = "UPDATE hoa_don SET tong_tien = ?, thoi_gian = ?, nv_id = ?, thanh_toan_status = ?,dat_phong_id = ? WHERE hd_id = ?"
        return self.db.execute_query(query, (hoa_don.tong_tien, hoa_don.thoi_gian, hoa_don.nv_id, hoa_don.thanh_toan_status,hoa_don.dat_phong_id, hoa_don.hd_id)) is not None
    def update_tong_tien(self, hd_id, tong_tien):
        query = "UPDATE hoa_don SET tong_tien = ?,thoi_gian = datetime('now'),thanh_toan_status = 1 WHERE hd_id = ?"
        return self.db.execute_query(query, (tong_tien, hd_id)) is not None

    def delete_hoa_don(self, hd_id):
        query = "DELETE FROM hoa_don WHERE hd_id = ?"
        return self.db.execute_query(query, (hd_id,)) is not None

    def search_hoa_don(self, search_term):
        query = "SELECT hd_id, tong_tien, thoi_gian, nv_id, thanh_toan_status FROM hoa_don WHERE hd_id = ?"
        rows = self.db.execute_query(query, (search_term,))
        if rows:
            return [HoaDonDTO(hd_id=row[0], tong_tien=row[1], thoi_gian=row[2], nv_id=row[3], thanh_toan_status=row[4]) for row in rows]
        else:
            return []

    def search_hoa_don_by_time(self, search_term):
        query = "SELECT hd_id, tong_tien, thoi_gian, nv_id, thanh_toan_status FROM hoa_don WHERE thoi_gian LIKE ?"
        rows = self.db.execute_query(query, ('%' + search_term + '%',))
        if rows:
            return [HoaDonDTO(hd_id=row[0], tong_tien=row[1], thoi_gian=row[2], nv_id=row[3], thanh_toan_status=row[4]) for row in rows]
        else:
            return []

if __name__ == "__main__":
    dv_dao = HoaDonDAO()
    test = HoaDonDTO()
    test.nv_id =1
    
    print(dv_dao.insert_hoa_don(HoaDonDTO(nv_id=1)))