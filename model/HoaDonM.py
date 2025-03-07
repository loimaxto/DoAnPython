import mysql.connector

class HoaDonM:
    def __init__(self, host, user, password, database):
        """Kết nối tới MySQL"""
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    
    def lay_danh_sach_hoa_don(self):
        """Lấy danh sách tất cả hóa đơn dưới dạng danh sách từ điển"""
        self.cursor.execute("SELECT * FROM hoa_don")
        columns = [column[0] for column in self.cursor.description]  # Lấy tên cột
        result = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
        return result

    def them_hoa_don(self, hd_id, dv_id, so_luong, gia_luc_dat, tong):
        """Thêm hóa đơn"""
        sql = """
        INSERT INTO chi_tiet_dv (hd_id, dv_id, so_luong, gia_luc_dat, tong) 
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(sql, (hd_id, dv_id, so_luong, gia_luc_dat, tong))
        self.conn.commit()
        print("✔ Thêm hóa đơn thành công!")

    def lay_hoa_don(self, hd_id):
        """Lấy danh sách hóa đơn theo ID hóa đơn"""
        sql = "SELECT * FROM chi_tiet_dv WHERE hd_id = %s"
        self.cursor.execute(sql, (hd_id,))
        result = self.cursor.fetchall()
        print(f"\nhóa đơn {hd_id}:")
        for row in result:
            print(row)

    def cap_nhat_hoa_don(self, hd_id, dv_id, so_luong=None, gia_luc_dat=None, tong=None):
        """Cập nhật thông tin hóa đơn"""
        fields = []
        values = []
        if so_luong is not None:
            fields.append("so_luong = %s")
            values.append(so_luong)
        if gia_luc_dat is not None:
            fields.append("gia_luc_dat = %s")
            values.append(gia_luc_dat)
        if tong is not None:
            fields.append("tong = %s")
            values.append(tong)

        values.append(hd_id)
        values.append(dv_id)

        sql = f"UPDATE chi_tiet_dv SET {', '.join(fields)} WHERE hd_id = %s AND dv_id = %s"
        self.cursor.execute(sql, values)
        self.conn.commit()
        print("✔ Cập nhật hóa đơn thành công!")

    def xoa_hoa_don(self, hd_id, dv_id):
        """Xóa hóa đơn"""
        sql = "DELETE FROM chi_tiet_dv WHERE hd_id = %s AND dv_id = %s"
        self.cursor.execute(sql, (hd_id, dv_id))
        self.conn.commit()
        print("✔ Xóa hóa đơn thành công!")

    def dong_ket_noi(self):
        """Đóng kết nối MySQL"""
        self.cursor.close()
        self.conn.close()
