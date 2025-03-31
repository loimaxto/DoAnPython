import sys
import os

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

# Example usage (in a separate main.py or similar):
if __name__ == "__main__":
    dao = PhongDAO()
    
