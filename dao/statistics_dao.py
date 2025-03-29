import sys
import os
import sqlite3

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

sys.path.append(project_path)
print(project_path)

from dto.dto import ThongKeDTO
from utils.database import SQLiteDB

class ThongKeDAO:
    def __init__(self): 
        self.db = SQLiteDB()
    def get_thong_ke_7_ngay_gan_nhat(self):
        sql = """
            WITH RECURSIVE dates(date) AS (
                SELECT DATE('now', '-7 days')
                UNION ALL
                SELECT DATE(date, '+1 day')
                FROM dates
                WHERE date < DATE('now')
            )
            SELECT 
                dates.date AS ngay,
                COALESCE(SUM(hoa_don.TongTien), 0) AS doanhthu,
                COALESCE(SUM(chi_phi.amount), 0) AS chiphi
            FROM dates
            LEFT JOIN hoa_don ON DATE(hoa_don.thoi_gian) = dates.date
            LEFT JOIN chi_phi ON DATE(chi_phi.thoi_gian) = dates.date
            GROUP BY dates.date
            ORDER BY dates.date;
        """
        result = self.db.execute_query(sql)
        if result:
            return [ThongKeDTO(ngay=row[0], doanhthu=row[1], chiphi=row[2]) for row in result]
        else:
            return []
        
        # for row in rows:
        #     ngay, doanhthu, chiphi = row
        #     loinhuan = doanhthu - chiphi
        #     result.append({"ngay": ngay, "chiphi": chiphi, "doanhthu": doanhthu, "loinhuan": loinhuan})

        # return result

    
# Example usage (in a separate main.py or similar):
if __name__ == "__main__":
    dao = ThongKeDAO()
 