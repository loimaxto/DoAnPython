import sys
import os

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

sys.path.append(project_path)
print(project_path) #print relative path c:\Code\DoAnPython

from dto.dto import KhachHangDTO
from utils.database import SQLiteDB

class KhachHangDAO:
    def __init__(self): 
        self.db = SQLiteDB()

    def get_all_khach_hang(self):
        query = "SELECT kh_id, ten, sdt, image FROM khach_hang"
        rows = self.db.execute_query(query)
        if rows:
            return [KhachHangDTO(kh_id=row[0], ten=row[1], sdt=row[2], image=row[3]) for row in rows]
        else:
            return []
    
    
    def get_khach_hang_by_id(self, kh_id):
        query = "SELECT kh_id, ten, sdt, image FROM khach_hang WHERE kh_id = ?"
        row = self.db.execute_query(query, (kh_id,))
        if row:
            row = row[0] #Unpack the single result list.
            return KhachHangDTO(kh_id=row[0], ten=row[1], sdt=row[2], image=row[3])
        else:
            return None
    def get_khach_hang_next_id(self):
        
        query = "SELECT kh_id FROM khach_hang ORDER BY kh_id"
        rows = self.db.execute_query(query)
        existing_ids = [row[0] for row in rows]

        next_id = 1
        for booking_id in existing_ids:
            if booking_id != next_id:
                break
            next_id += 1
        return next_id
    def insert_khach_hang(self, khach_hang):
        query = "INSERT INTO khach_hang (kh_id,ten, sdt, image) VALUES (?,?, ?, ?)"
        insert_row_data = self.db.execute_query(query, 
                                                
        (self.get_khach_hang_next_id(),khach_hang.ten, khach_hang.sdt, khach_hang.image), return_last_row=True)
        return insert_row_data[0] #return the last inserted ID.


    def update_khach_hang(self, khach_hang):
        query = "UPDATE khach_hang SET ten = ?, sdt = ? WHERE kh_id = ?"
        return self.db.execute_query(query, (khach_hang.ten, khach_hang.sdt, khach_hang.kh_id)) is not None
    def update_khach_hang_image(self, id):
        query = "UPDATE khach_hang SET image=? WHERE kh_id = ?"
        return self.db.execute_query(query, (f"face_{id}.pth",id)) is not None

    def delete_khach_hang(self, kh_id):
        query = "DELETE FROM khach_hang WHERE kh_id = ?"
        return self.db.execute_query(query, (kh_id,)) is not None

    def search_khach_hang(self, search_term):
        query = "SELECT kh_id, ten, sdt, image FROM khach_hang WHERE ten LIKE ? OR sdt LIKE ?"
        rows = self.db.execute_query(query, ('%' + search_term + '%', '%' + search_term + '%'))
        if rows:
            return [KhachHangDTO(kh_id=row[0], ten=row[1], sdt=row[2], image=row[3]) for row in rows]
        else:
            return []
    

# Example usage (in a separate main.py or similar):
if __name__ == "__main__":
    dao = KhachHangDAO()
    print('ass')
    a= dao.get_khach_hang_next_id()
    print(a)
"""
    # Example insert
    new_customer = KhachHangDTO(ten="Doe a", sdt="123-456-7890", image="john.jpg")
    new_id = dao.insert_khach_hang(new_customer)
    print(f"Inserted customer with ID: {new_id}")

    # Example get all
    customers = dao.get_all_khach_hang()
    for customer in customers:
        print(customer)

    # Example search
    results = dao.search_khach_hang("John")
    for result in results:
        print(result)
"""