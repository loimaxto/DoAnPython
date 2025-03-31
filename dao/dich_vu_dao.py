import sys
import os

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

sys.path.append(project_path)
print(project_path) #print relative path c:\Code\DoAnPython

from dto.dto import DichVuDTO
from utils.database import SQLiteDB

class DichVuDAO:
    def __init__(self): 
        self.db = SQLiteDB()

    def get_all_DichVu(self):
        query = "SELECT * from dich_vu"
        rows = self.db.execute_query(query)
        if rows:
            return [DichVuDTO(dv_id=row[0], ten=row[1], gia=row[2]) for row in rows]
        else:
            return []

    def get_dich_vu_by_id(self, dv_id):
        query = "SELECT dv_id, ten_dv, gia FROM dich_vu WHERE dv_id = ?"
        row = self.db.execute_query(query, (dv_id,))
        if row:
            row = row[0] #Unpack the single result list.
            return DichVuDTO(dv_id=row[0], ten=row[1], gia=row[2])
        else:
            return None

    def insert_dich_vu(self, dich_vu):
        query = "INSERT INTO dich_vu (dv_id, ten_dv, gia) VALUES (?, ?. ?)"
        insert_row_data = self.db.execute_query(query, (dich_vu.dv_id, dich_vu.ten, dich_vu.gia), return_last_row=True)
        return insert_row_data[0] #return the last inserted ID.

    def update_dich_vu(self, dich_vu):
        query = "UPDATE dich_vu SET ten_dv = ?, gia = ? WHERE kh_id = ?"
        return self.db.execute_query(query, (dich_vu.ten, dich_vu.gia, dich_vu.dv_id)) is not None

    def delete_dich_vu(self, dv_id):
        query = "DELETE FROM dich_vu WHERE dv_id = ?"
        return self.db.execute_query(query, (dv_id,)) is not None

    def search_dich_vu(self, search_term):
        query = "SELECT * FROM dich_vu WHERE dv_id = ?"
        rows = self.db.execute_query(query, (search_term, ))
        if rows:
            return [DichVuDTO(dv_id=row[0], ten=row[1], gia=row[2]) for row in rows]
        else:
            return []
    def search_dich_vu_by_name (self, search_term):
        query = "SELECT * FROM dich_vu WHERE ten_dv LIKE ?" # Modify the query
        rows = self.db.execute_query(query, ('%' + search_term + '%', )) # Modify the argument
        if rows:
            return [DichVuDTO(dv_id=row[0], ten=row[1], gia=row[2]) for row in rows]
        else:
            return []
        
if __name__ == "__main__":
    dv_dao = DichVuDAO()
    print(dv_dao.get_dich_vu_by_id(1))
    print(dv_dao.search_dich_vu_by_name("a")[0])
