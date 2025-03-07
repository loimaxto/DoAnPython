import mysql.connector

class NhanVien:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def them_nhan_vien(self, ten_nv, email, sdt, dia_chi, chuc_vu):
        sql = "INSERT INTO nhan_vien (ten_nv, email, sdt, dia_chi, chuc_vu) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (ten_nv, email, sdt, dia_chi, chuc_vu))
        self.conn.commit()
        print("✔ Nhân viên đã được thêm thành công!")


    def lay_danh_sach_nhan_vien(self):
        self.cursor.execute("SELECT * FROM nhan_vien")
        columns = [column[0] for column in self.cursor.description]  # Lấy tên cột
        result = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        return result


    def cap_nhat_nhan_vien(self, nv_id, ten_nv=None, email=None, sdt=None, dia_chi=None, chuc_vu=None):
        fields = []
        values = []
        if ten_nv:
            fields.append("ten_nv = %s")
            values.append(ten_nv)
        if email:
            fields.append("email = %s")
            values.append(email)
        if sdt:
            fields.append("sdt = %s")
            values.append(sdt)
        if dia_chi:
            fields.append("dia_chi = %s")
            values.append(dia_chi)
        if chuc_vu:
            fields.append("chuc_vu = %s")
            values.append(chuc_vu)
        
        values.append(nv_id)
        sql = f"UPDATE nhan_vien SET {', '.join(fields)} WHERE nv_id = %s"
        self.cursor.execute(sql, values)
        self.conn.commit()
        print("✔ Cập nhật thông tin nhân viên thành công!")

    def xoa_nhan_vien(self, nv_id):
        sql = "DELETE FROM nhan_vien WHERE nv_id = %s"
        self.cursor.execute(sql, (nv_id,))
        self.conn.commit()
        print("✔ Nhân viên đã được xóa thành công!")

    def dong_ket_noi(self):
        self.cursor.close()
        self.conn.close()



# # Kết nối đến MySQL
# nv_manager = NhanVien(host="localhost", user="root", password="password", database="hotel_db")

# # 1. Thêm nhân viên mới
# nv_manager.them_nhan_vien("Nguyễn Văn A", "vana@gmail.com", "0123456789", "Hà Nội", "Quản lý")

# # 2. Lấy danh sách nhân viên
# print("\nDanh sách nhân viên:")
# nv_manager.lay_danh_sach_nhan_vien()

# # 3. Cập nhật thông tin nhân viên
# nv_manager.cap_nhat_nhan_vien(nv_id=1, sdt="0987654321", chuc_vu="Giám đốc")

# # 4. Xóa nhân viên
# nv_manager.xoa_nhan_vien(nv_id=1)

# # Đóng kết nối
# nv_manager.dong_ket_noi()
