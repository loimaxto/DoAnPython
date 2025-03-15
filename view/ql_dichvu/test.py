import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
print(project_path) #vi tri tu file hien tai toi root !! phai toi root moi dung duoc

from dao.dich_vu_dao import DichVuDAO

db = DichVuDAO()

e = db.get_dich_vu_by_id(1)

print(e)