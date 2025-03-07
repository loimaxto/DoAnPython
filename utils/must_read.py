# khai bao de tai sua dung db tat ca dung dung file vi tri cua file .db
from database import SQLiteDB 

db = SQLiteDB()

create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER
    );
    """
select_name_query = "SELECT * FROM user ;"
name_results = db.execute_query(select_name_query)
if name_results:
    print("Result", name_results)
