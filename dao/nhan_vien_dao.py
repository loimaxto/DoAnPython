import sys
import os

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

sys.path.append(project_path)
print(project_path) #print relative path c:\Code\DoAnPython

from dto.dto import NhanVienDTO
from utils.database import SQLiteDB

class NhanVienDAO:
    def __init__(self): 
        self.db = SQLiteDB()

    def get_all_nhan_vien(self):
        query = "SELECT * FROM nhan_vien"
        rows = self.db.execute_query(query)
        if rows:
            return [NhanVienDTO(nv_id=row[0], ten_nv=row[1], email=row[2], sdt=row[3], dia_chi=row[4], chuc_vu=row[5]) for row in rows]
        else:
            return []

    def get_nhan_vien_by_id(self, nv_id):
        query = "SELECT * FROM nhan_vien WHERE nv_id = ?"
        row = self.db.execute_query(query, (nv_id,))
        if row:
            row = row[0] #Unpack the single result list.
            return NhanVienDTO(nv_id=row[0], ten_nv=row[1], email=row[2], sdt=row[3], dia_chi=row[4], chuc_vu=row[5])
        else:
            return None
    def get_nhan_vien_next_id(self):
        query = "SELECT COALESCE(MAX(nv_id), 0) + 1 FROM nhan_vien;"
        rs = self.db.execute_query(query)
        id = rs[0][0]
        return id
    def insert_nhan_vien(self, nhan_vien):
        query = "INSERT INTO nhan_vien (ten_nv, email, sdt, dia_chi, chuc_vu) VALUES (?, ?, ?, ?, ?)"
        insert_row_data = self.db.execute_query(query, (nhan_vien.ten_nv , nhan_vien.email, nhan_vien.sdt, nhan_vien.dia_chi ,nhan_vien.chuc_vu), return_last_row=True)
        return insert_row_data[0] #return the last inserted ID.


    def update_nhan_vien(self, nhan_vien):
        query = "UPDATE nhan_vien SET ten_nv = ?, email = ?, sdt = ?, dia_chi = ?, chuc_vu = ? WHERE nv_id = ?"
        return self.db.execute_query(query, (nhan_vien.ten_nv , nhan_vien.email, nhan_vien.sdt, nhan_vien.dia_chi ,nhan_vien.chuc_vu, nhan_vien.nv_id)) is not None

    def delete_nhan_vien(self, nv_id):
        query = "DELETE FROM nhan_vien WHERE nv_id = ?"
        return self.db.execute_query(query, (nv_id,)) is not None

    def search_nhan_vien(self, search_term):
        query = "SELECT * FROM nhan_vien WHERE ten_nv LIKE ? OR sdt LIKE ?"
        rows = self.db.execute_query(query, ('%' + search_term + '%', '%' + search_term + '%'))
        if rows:
            return [NhanVienDTO(nv_id=row[0], ten_nv=row[1], email=row[2], sdt=row[3], dia_chi=row[4], chuc_vu=row[5]) for row in rows]
        else:
            return []

# Example usage (in a separate main.py or similar):
if __name__ == "__main__":
    dao = NhanVienDAO()
    print('ass')
    # a= dao.get_nhan_vien_next_id()
    print(a)
"""
    # Example insert
    new_customer = NhanVienDTO(ten="Doe a", sdt="123-456-7890", image="john.jpg")
    new_id = dao.insert_nhan_vien(new_customer)
    print(f"Inserted customer with ID: {new_id}")

    # Example get all
    customers = dao.get_all_nhan_vien()
    for customer in customers:
        print(customer)

    # Example search
    results = dao.search_nhan_vien("John")
    for result in results:
        print(result)
"""