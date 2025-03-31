import sys
import os
import sqlite3
from typing import List

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

sys.path.append(project_path)
print(project_path)

from dto.dto import ThongKeDoanhThuDTO, ThongKeTheoThangDTO, ThongKeTheoTungNgayTrongThangDTO
from utils.database import SQLiteDB

class ThongKeDAO:
    def __init__(self): 
        self.db = SQLiteDB()
    def getDoanhThu7NgayGanNhat(self, db_path: str = "db/hotel7-3.db") -> List[ThongKeDoanhThuDTO]:
        result = []
        try:
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            
            sql = """
                WITH RECURSIVE dates(date) AS (
                    SELECT DATE('now', '-6 days')  -- Lấy 7 ngày gần nhất (từ 6 ngày trước đến hôm nay)
                    UNION ALL
                    SELECT DATE(date, '+1 day')
                    FROM dates
                    WHERE date < DATE('now')
                )
                SELECT 
                    dates.date AS ngay,
                    COALESCE(SUM(hoa_don.tong_tien), 0) AS doanhthu
                FROM dates
                LEFT JOIN hoa_don ON strftime('%Y-%m-%d', hoa_don.thoi_gian) = dates.date
                GROUP BY dates.date
                ORDER BY dates.date;
            """
            
            cur.execute(sql)
            for row in cur.fetchall():
                ngay, doanhthu = row
                result.append(ThongKeDoanhThuDTO(ngay, doanhthu))  # Không có cột chi phí nên để 0
            
        except sqlite3.Error as e:
            print("Lỗi SQLite:", e)
        finally:
            con.close()
        
        return result

        
    
    def getDoanhThuTheoNam(self,year_start: int, year_end: int,db_path: str = "db/hotel7-3.db") -> List[ThongKeDoanhThuDTO]:
        result = []
        try:
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            
            # Tạo danh sách năm
            years = [(year,) for year in range(year_start, year_end + 1)]
            cur.execute("CREATE TEMP TABLE IF NOT EXISTS years(year INTEGER)")
            cur.execute("DELETE FROM years")
            cur.executemany("INSERT INTO years(year) VALUES (?)", years)

            # Truy vấn doanh thu và chi phí theo năm
            sql = """
                SELECT 
                    years.year AS nam,
                    COALESCE(SUM(hoa_don.tong_tien), 0) AS doanhthu
                FROM years
                LEFT JOIN hoa_don ON strftime('%Y', hoa_don.thoi_gian) = years.year
                GROUP BY years.year
                ORDER BY years.year;
            """
            cur.execute(sql)
            
            for row in cur.fetchall():
                nam, doanhthu = row
                result.append(ThongKeDoanhThuDTO(nam, doanhthu))
            
        except sqlite3.Error as e:
            print("Lỗi SQLite:", e)
        finally:
            con.close()
        
        return result
        
    def getDoanhThuTheoThang(self,nam: int,db_path: str = "db/hotel7-3.db") -> List[ThongKeTheoThangDTO]:
        result = []
        try:
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            
            # Truy vấn doanh thu theo từng tháng trong năm
            sql = """
                WITH months AS (
                    SELECT 1 AS month UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4
                    UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8
                    UNION ALL SELECT 9 UNION ALL SELECT 10 UNION ALL SELECT 11 UNION ALL SELECT 12
                )
                SELECT 
                    months.month AS thang,
                    COALESCE(SUM(hoa_don.tong_tien), 0) AS doanhthu
                FROM months
                LEFT JOIN hoa_don 
                    ON strftime('%m', hoa_don.thoi_gian) = printf('%02d', months.month)  -- Chuyển tháng về dạng 2 chữ số
                    AND strftime('%Y', hoa_don.thoi_gian) = ?  -- Lọc theo năm
                GROUP BY months.month
                ORDER BY months.month;

            """
            
            cur.execute(sql, (str(nam),))
            for row in cur.fetchall():
                thang,doanhthu = row
                result.append(ThongKeTheoThangDTO(thang, doanhthu))
            
        except sqlite3.Error as e:
            print("Lỗi SQLite:", e)
        finally:
            con.close()
        
        return result

    def getDoanhThuTungNgayTrongThang(self,thang: int, nam: int, db_path: str = "db/hotel7-3.db") -> List[ThongKeTheoTungNgayTrongThangDTO]:
        result = []
        try:
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            
            sql = """
                WITH RECURSIVE dates(date) AS (
                    SELECT DATE(?, 'start of month')
                    UNION ALL
                    SELECT DATE(date, '+1 day')
                    FROM dates
                    WHERE date < DATE(?, 'start of month', '+1 month', '-1 day')
                )
                SELECT 
                    dates.date AS ngay,
                    COALESCE(SUM(hoa_don.tong_tien), 0) AS doanhthu
                FROM dates
                LEFT JOIN hoa_don ON DATE(hoa_don.thoi_gian) = dates.date
                GROUP BY dates.date
                ORDER BY dates.date;
            """
            
            cur.execute(sql, (f"{nam}-{thang:02d}-01", f"{nam}-{thang:02d}-01"))
            for row in cur.fetchall():
                ngay, doanhthu = row
                result.append(ThongKeTheoTungNgayTrongThangDTO(ngay,doanhthu))
            
        except sqlite3.Error as e:
            print("Lỗi SQLite:", e)
        finally:
            con.close()
        
        return result

    def getDoanhThuTuNgayDenNgay(self,dateStart: str, dateEnd: str,db_path: str = "db/hotel7-3.db" ) -> List[ThongKeTheoTungNgayTrongThangDTO]:
        result = []
        try:
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            
            sql = """
                SELECT 
                    hoa_don.thoi_gian AS ngay,
                    SUM(hoa_don.tong_tien) AS doanhthu
                FROM hoa_don
                WHERE hoa_don.thoi_gian BETWEEN ? AND ?
                GROUP BY hoa_don.thoi_gian
                ORDER BY hoa_don.thoi_gian;
            """
            
            cur.execute(sql, (dateStart, dateEnd))
            for row in cur.fetchall():
                ngay,doanhthu = row
                result.append(ThongKeTheoTungNgayTrongThangDTO(ngay,doanhthu))
            
        except sqlite3.Error as e:
            print("Lỗi SQLite:", e)
        finally:
            con.close()
        
        return result
# Example usage (in a separate main.py or similar):
if __name__ == "__main__":
    dao = ThongKeDAO()
 