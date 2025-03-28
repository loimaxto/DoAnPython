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

    def get_all_HoaDon(self):
        query = "SELECT * FROM hoa_don"
        rows = self.db.execute_query(query)
        if rows:
            return [HoaDonDTO(hd_id=row[0], tong_tien=row[1], thoi_gian=row[2], nv_id=row[3], thanh_toan_status=row[4]) for row in rows]
        else:
            return []

    def get_hoa_don_by_id(self, kh_id):
        query = "SELECT * FROM hoa_don WHERE hd_id = ?"
        row = self.db.execute_query(query, (kh_id,))
        if row:
            row = row[0] #Unpack the single result list.
            return HoaDonDTO(hd_id=row[0], tong_tien=row[1], thoi_gian=row[2], nv_id=row[3], thanh_toan_status=row[4])
        else:
            return None
    
    def insert_hoa_don(self, hoa_don):
        query = "INSERT INTO hoa_don (tong_tien, thoi_gian, nv_id, thanh_toan_status) VALUES (?, ?, ?,?)"
        insert_row_data = self.db.execute_query(query, (hoa_don.tong_tien , hoa_don.thoi_gian , hoa_don.nv_id , hoa_don.thanh_toan_status), return_last_row=True)
        return insert_row_data[0] #return the last inserted ID.

    def delete_hoa_don(self, hd_id):
        query = "DELETE FROM hoa_don WHERE hd_id = ?"
        return self.db.execute_query(query, (hd_id,)) is not None

    def search_hoa_don(self, search_term):
        query = "SELECT * FROM hoa_don WHERE hd_id LIKE ? OR nv_id LIKE ?"
        rows = self.db.execute_query(query, ('%' + search_term + '%', '%' + search_term + '%'))
        if rows:
            return [HoaDonDTO(hd_id=row[0], tong_tien=row[1], thoi_gian=row[2], nv_id=row[3], thanh_toan_status=row[4]) for row in rows]
        else:
            return []

    def TongDoanhThu(self) -> int:
        query = "SELECT SUM(tong_tien) FROM hoa_don"
        result = self.db.execute_query(query)
        if result and result[0][0] is not None:
            return int(result[0][0])
        return 0 
    
    def TongDoanhThuTheoNam(self, YearToStart: int, YearToEnd: int) -> int:
        query = "SELECT SUM(tong_tien) FROM hoa_don WHERE strftime('%Y', thoi_gian) BETWEEN ? AND ?"
        result = self.db.execute_query(query, (str(YearToStart), str(YearToEnd)))

        if result and result[0][0] is not None:
            return int(result[0][0])

        return 0 

    
    def TongDoanhThuTheoThangTrongNam(self, Year: int, Month: int) -> int:
        query = """
        SELECT SUM(tong_tien) 
        FROM hoa_don 
        WHERE strftime('%Y', thoi_gian) = ? AND strftime('%m', thoi_gian) = ?
        """
        result = self.db.execute_query(query, (str(Year), f"{Month:02d}")) 

        if result and result[0][0] is not None:
            return int(result[0][0])

        return 0  

    def TongDoanhThuTheoKhoangNgay(self, StartDate: str, EndDate: str) -> int:
        query = """
        SELECT SUM(tong_tien) 
        FROM hoa_don 
        WHERE strftime('%Y-%m-%d', thoi_gian) BETWEEN ? AND ?
        """
        
        result = self.db.execute_query(query, (StartDate, EndDate))

        if result and result[0][0] is not None:
            return int(result[0][0])

        return 0 



# Example usage (in a separate main.py or similar):
if __name__ == "__main__":
    dao = HoaDonDAO()
