import sys
import os
from dto.dto import PhongDTO

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

sys.path.append(project_path)
print(project_path) #print relative path c:\Code\DoAnPython

from utils.database import SQLiteDB

class PhongDAO:
    def __init__(self): 
        self.db = SQLiteDB()

    def get_all_available_phong(self) -> int:
        query = "SELECT COUNT(*) FROM phong WHERE tinh_trang_dat_phong = 0 AND tinh_trang_su_dung = 1"
        result = self.db.execute_query(query)
        if result and isinstance(result, list) and len(result) > 0 and len(result[0]) > 0:
            return result[0][0]
        return 0
    
    def get_all_occupied_phong(self) -> int:
        query = "SELECT COUNT(*) FROM phong WHERE tinh_trang_dat_phong = 1 AND tinh_trang_su_dung = 1"
        result = self.db.execute_query(query)
        if result and isinstance(result, list) and len(result) > 0 and len(result[0]) > 0:
            return result[0][0]
        return 0
    def get_phong_by_name(self,name):
        query = "SELECT id, ten_phong, so_giuong, id_gia, tinh_trang_dat_phong, tinh_trang_su_dung FROM phong WHERE ten_phong LIKE ?"
        rows = self.db.execute_query(query,("%"+name+"%",))
        if rows:
            return [PhongDTO(id=row[0], ten_phong=row[1], so_giuong=row[2], id_gia=row[3], tinh_trang_dat_phong=row[4], tinh_trang_su_dung=row[5]) for row in rows]
        else:
            return []

    def get_all_phong(self):
        query = "SELECT id, ten_phong, so_giuong, id_gia, tinh_trang_dat_phong, tinh_trang_su_dung FROM phong"
        rows = self.db.execute_query(query)
        if rows:
            return [PhongDTO(id=row[0], ten_phong=row[1], so_giuong=row[2], id_gia=row[3], tinh_trang_dat_phong=row[4], tinh_trang_su_dung=row[5]) for row in rows]
        else:
            return []
    def get_all_phong_for_order(self):
        query = "SELECT phong.id,phong.ten_phong, gia_phong.ten_loai,phong.tinh_trang_dat_phong FROM phong INNER JOIN gia_phong ON phong.id_gia = gia_phong.gia_id;"
        rows = self.db.execute_query(query)
        if rows:
            return rows # 0 id ;1 ten phong, 2 ten loai, 3 tinh trang
        else:
            return []
    def get_phong_by_id(self, id):
        query = "SELECT id, ten_phong, so_giuong, id_gia, tinh_trang_dat_phong, tinh_trang_su_dung,curren_hoadon_id FROM phong WHERE id = ?"
        row = self.db.execute_query(query, (id,))
        if row:
            row = row[0]  # Unpack the single result list.
            return PhongDTO(id=row[0], ten_phong=row[1], so_giuong=row[2], id_gia=row[3], tinh_trang_dat_phong=row[4], tinh_trang_su_dung=row[5],current_hoadon_id=row[6])
        else:
            return None
    def get_phong_by_id2(self, id):
        query = "SELECT id, ten_phong, so_giuong, id_gia, tinh_trang_dat_phong, tinh_trang_su_dung FROM phong WHERE id = ?"
        row = self.db.execute_query(query, (id,))
        if row:
            row = row[0]  # Unpack the single result list.
            return PhongDTO(id=row[0], ten_phong=row[1], so_giuong=row[2], id_gia=row[3], tinh_trang_dat_phong=row[4], tinh_trang_su_dung=row[5])
        else:
            return None
    def get_phong_next_id(self):
        query = "SELECT COALESCE(MAX(id), 0) + 1 FROM phong;"
        rs = self.db.execute_query(query)
        id = rs[0][0]
        return id

    def insert_phong(self, phong):
        query = "INSERT INTO phong (ten_phong, so_giuong, id_gia, tinh_trang_dat_phong, tinh_trang_su_dung) VALUES (?, ?, ?, ?, ?)"
        insert_row_data = self.db.execute_query(query, (phong.ten_phong, phong.so_giuong, phong.id_gia, phong.tinh_trang_dat_phong, phong.tinh_trang_su_dung), return_last_row=True)
        return insert_row_data[0]  # Return the last inserted ID.

    def update_phong(self, phong):
        query = "UPDATE phong SET ten_phong = ?, so_giuong = ?, id_gia = ?, tinh_trang_dat_phong = ?, tinh_trang_su_dung = ?, curren_hoadon_id =? WHERE id = ?"
        return self.db.execute_query(query, (phong.ten_phong, phong.so_giuong, phong.id_gia, phong.tinh_trang_dat_phong, phong.tinh_trang_su_dung,phong.current_hoadon_id, phong.id), ) is not None
    def update_tinh_trang_su_dung(self, id, tinh_trang_su_dung):
        query = "UPDATE phong SET tinh_trang_su_dung = ? WHERE id = ?"
        return self.db.execute_query(query, (tinh_trang_su_dung, id)) 
    def update_tinh_trang_dat_phong(self, id, tinh_trang_dat_phong, hoadon_id):
        query = "UPDATE phong SET tinh_trang_dat_phong = ?,curren_hoadon_id =? WHERE id = ?"
        return self.db.execute_query(query, (tinh_trang_dat_phong,hoadon_id, id)) 
    def delete_phong(self, id):
        query = "DELETE FROM phong WHERE id = ?"
        return self.db.execute_query(query, (id,))
    def get_all_available_obj_phong(self):
        query = "select id, ten_phong, so_giuong, loai \
                from phong \
                    where tinh_trang_dat_phong=0"
        tmp = self.db.execute_query(query)
        data = []
        for row in tmp:
            row_data = PhongDTO(row[0], row[1], row[2], row[3])
            data.append(row_data)
        print(data)
        return data


if __name__ == "__main__":
    dao = PhongDAO()
    print("bg")
    print(dao.get_phong_by_id(201))
    print(dao.update_tinh_trang_dat_phong(201,1))
    print(dao.get_phong_by_id(201))

