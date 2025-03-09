# khai bao de tai sua dung db tat ca dung dung file vi tri cua file .db
from database import SQLiteDB 

db = SQLiteDB()


select_name_query = "SELECT * FROM user ;"
name_results = db.execute_query(select_name_query)
if name_results:
    print("Result", name_results)

"""
 # Insert data
    insert_query = "INSERT INTO users (name, age) VALUES (?, ?);"
    db.execute_query(insert_query, ("Alice", 36))
    db.execute_query(insert_query, ("Bob", 25))

    # Select data
    select_query = "SELECT * FROM users;"
    results = db.execute_query(select_query)
    if results:
        print("Users:")
        for row in results:
            print(row)

    # Insert many rows
    many_insert_query = "INSERT INTO users (name, age) VALUES (?, ?);"
    data = [("Charlie", 35), ("David", 40)]
    db.execute_many(many_insert_query, data)

    # Select all data again, after the many insert
    results = db.execute_query(select_query)
    if results:
        print("\nAll Users after many insert:")
        for row in results:
            print(row)

    # Select data with parameters
    select_age_query = "SELECT * FROM users WHERE age > ?;"
    age_results = db.execute_query(select_age_query, (30,))
    if age_results:
        print("\nUsers older than 30:")
        for row in age_results:
            print(row)
"""