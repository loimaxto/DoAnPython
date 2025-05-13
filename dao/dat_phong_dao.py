import sys
import os

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.append(project_path)

from dto.dto import DatPhongDTO
from utils.database import SQLiteDB
from dao.hoa_don_dao import HoaDonDAO
class DatPhongDAO:
    def __init__(self):
        self.db = SQLiteDB()

    def get_all_dat_phong(self):
        query = """
        SELECT booking_id, ngay_bd, ngay_kt, phi_dat_coc, note, phong_id, tien_luc_dat, kh_id 
        FROM dat_phong
        """
        rows = self.db.execute_query(query)
        if rows:
            return [DatPhongDTO(
                booking_id=row[0],
                ngay_bd=row[1],
                ngay_kt=row[2],
                phi_dat_coc=row[3],
                note=row[4],
                phong_id=row[5],
                tien_luc_dat=row[6],
                kh_id=row[7]
            ) for row in rows]
        else:
            return []

    def get_dat_phong_by_id(self, booking_id):
        query = """
        SELECT booking_id, ngay_bd, ngay_kt, phi_dat_coc, note, phong_id, tien_luc_dat, kh_id 
        FROM dat_phong 
        WHERE booking_id = ?
        """
        row = self.db.execute_query(query, (booking_id,))
        if row:
            row = row[0]
            return DatPhongDTO(
                booking_id=row[0],
                ngay_bd=row[1],
                ngay_kt=row[2],
                phi_dat_coc=row[3],
                note=row[4],
                phong_id=row[5],
                tien_luc_dat=row[6],
                kh_id=row[7]
            )
        else:
            return None

    def get_dat_phong_next_id(self):
        query = "SELECT booking_id FROM dat_phong ORDER BY booking_id"
        rows = self.db.execute_query(query)
        existing_ids = [row[0] for row in rows]

        next_id = 1
        for booking_id in existing_ids:
            if booking_id != next_id:
                break
            next_id += 1
        return next_id


    def insert_dat_phong(self, dat_phong):
        try :
            query = "INSERT INTO dat_phong \
            (booking_id,ngay_bd, ngay_kt, phi_dat_coc, note, phong_id, tien_luc_dat, kh_id,hd_id) \
            VALUES (?,?,?,?, ?, ?, ?, ?, ?)\
            "
            hoadon = HoaDonDAO()
            params = (
                self.get_dat_phong_next_id(),
                dat_phong.ngay_bd,
                dat_phong.ngay_kt,
                dat_phong.phi_dat_coc,
                dat_phong.note,
                dat_phong.phong_id,
                dat_phong.tien_luc_dat,
                dat_phong.kh_id,
                hoadon.get_hoa_don_by_next_id()
            )
            insert_row_data = self.db.execute_query(query, params, return_last_row=True)
            return insert_row_data[0]
        except Exception as e:
            print(str(e))

    def update_dat_phong(self, dat_phong):
        query = """
        UPDATE dat_phong 
        SET ngay_bd = ?, ngay_kt = ?, phi_dat_coc = ?, note = ?, 
            phong_id = ?, tien_luc_dat = ?, kh_id = ? 
        WHERE booking_id = ?
        """
        params = (
            dat_phong.ngay_bd,
            dat_phong.ngay_kt,
            dat_phong.phi_dat_coc,
            dat_phong.note,
            dat_phong.phong_id,
            dat_phong.tien_luc_dat,
            dat_phong.kh_id,
            dat_phong.booking_id
        )
        return self.db.execute_query(query, params) is not None

    def delete_dat_phong(self, booking_id):
        query = "DELETE FROM dat_phong WHERE booking_id = ?"
        return self.db.execute_query(query, (booking_id,)) is not None

    def search_dat_phong(self, search_term):
        query = """
        SELECT booking_id, ngay_bd, ngay_kt, phi_dat_coc, note, phong_id, tien_luc_dat, kh_id 
        FROM dat_phong 
        WHERE booking_id LIKE ? OR note LIKE ? OR phong_id LIKE ?
        """
        search_param = f"%{search_term}%"
        rows = self.db.execute_query(query, (search_param, search_param, search_param))
        if rows:
            return [DatPhongDTO(
                booking_id=row[0],
                ngay_bd=row[1],
                ngay_kt=row[2],
                phi_dat_coc=row[3],
                note=row[4],
                phong_id=row[5],
                tien_luc_dat=row[6],
                kh_id=row[7]
            ) for row in rows]
        else:
            return []

    def get_dat_phong_by_khach_hang(self, kh_id):
        query = """
        SELECT booking_id, ngay_bd, ngay_kt, phi_dat_coc, note, phong_id, tien_luc_dat, kh_id 
        FROM dat_phong 
        WHERE kh_id = ?
        """
        rows = self.db.execute_query(query, (kh_id,))
        if rows:
            return [DatPhongDTO(
                booking_id=row[0],
                ngay_bd=row[1],
                ngay_kt=row[2],
                phi_dat_coc=row[3],
                note=row[4],
                phong_id=row[5],
                tien_luc_dat=row[6],
                kh_id=row[7]
            ) for row in rows]
        else:
            return []


# Example usage
if __name__ == "__main__":
    dao = DatPhongDAO()
    print("Next ID:", dao.get_dat_phong_next_id())
    for i in range(1,8):
        dao.delete_dat_phong(i)