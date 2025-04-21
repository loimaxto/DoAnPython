import sys
import os

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(project_path)
print(project_path)  # print relative path c:\Code\DoAnPython

from dto.dto import GiaPhongDTO
from utils.database import SQLiteDB

class GiaPhongDAO:
    def __init__(self):
        self.db = SQLiteDB()

    def get_all_gia_phong(self):
        query = "SELECT id, ten_loai, gia_gio, gia_ngay, gia_dem FROM gia_phong"
        rows = self.db.execute_query(query)
        if rows:
            return [GiaPhongDTO(
                id=row[0],
                ten_loai=row[1],
                gia_gio=row[2],
                gia_ngay=row[3],
                gia_dem=row[4]
            ) for row in rows]
        else:
            return []

    def get_gia_phong_by_id(self, id):
        query = "SELECT gia_id, ten_loai, gia_gio, gia_ngay, gia_dem FROM gia_phong WHERE gia_id = ?"
        row = self.db.execute_query(query, (id,))
        if row:
            row = row[0]
            return GiaPhongDTO(
                id=row[0],
                ten_loai=row[1],
                gia_gio=row[2],
                gia_ngay=row[3],
                gia_dem=row[4]
            )
        else:
            return None

    def insert_gia_phong(self, gia_phong):
        query = "INSERT INTO gia_phong (ten_loai, gia_gio, gia_ngay, gia_dem) VALUES (?, ?, ?, ?)"
        result = self.db.execute_query(
            query, 
            (gia_phong.ten_loai, gia_phong.gia_gio, gia_phong.gia_ngay, gia_phong.gia_dem),
            return_last_row=True
        )

        if result:
            return GiaPhongDTO(
                id=result[0],
                ten_loai=result[1],
                gia_gio=result[2],
                gia_ngay=result[3],
                gia_dem=result[4]
            )
        else:
            return None
        
    def update_gia_phong(self, gia_phong):
        query = "UPDATE gia_phong SET ten_loai = ?, gia_gio = ?, gia_ngay = ?, gia_dem = ? WHERE id = ?"
        return self.db.execute_query(
            query, 
            (gia_phong.ten_loai, gia_phong.gia_gio, gia_phong.gia_ngay, gia_phong.gia_dem, gia_phong.id)
        ) is not None

    def delete_gia_phong(self, id):
        query = "DELETE FROM gia_phong WHERE id = ?"
        return self.db.execute_query(query, (id,)) is not None

    def search_gia_phong(self, search_term):
        query = "SELECT id, ten_loai, gia_gio, gia_ngay, gia_dem FROM gia_phong WHERE id = ?"
        rows = self.db.execute_query(query, (search_term,))
        if rows:
            return [GiaPhongDTO(
                id=row[0],
                ten_loai=row[1],
                gia_gio=row[2],
                gia_ngay=row[3],
                gia_dem=row[4]
            ) for row in rows]
        else:
            return []

    def search_gia_phong_by_name(self, search_term):
        query = "SELECT id, ten_loai, gia_gio, gia_ngay, gia_dem FROM gia_phong WHERE ten_loai LIKE ?"
        rows = self.db.execute_query(query, ('%' + search_term + '%',))
        if rows:
            return [GiaPhongDTO(
                id=row[0],
                ten_loai=row[1],
                gia_gio=row[2],
                gia_ngay=row[3],
                gia_dem=row[4]
            ) for row in rows]
        else:
            return []

if __name__ == "__main__":
    gia_phong_dao = GiaPhongDAO()
    #test = GiaPhongDTO(
    #    id=None,
    #    ten_loai="Phòng VIP",
    #    gia_gio=100000,
    #    gia_ngay=500000,
    #    gia_dem=300000
    #)
    test =gia_phong_dao.get_gia_phong_by_id(3)
    print(test)