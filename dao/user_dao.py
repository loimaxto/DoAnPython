import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(project_path)

from dto.dto import UserDTO
from utils.database import SQLiteDB

class UserDAO:
    def __init__(self):
        self.db = SQLiteDB()

    def get_user_by_username(self, username):
        query = "SELECT id, username, password, role FROM users WHERE username = %s"
        result = self.db.execute_query(query, (username,), fetch=True)

        if result:
            user_data = result[0]  # Assuming username is unique
            return UserDTO(user_id=user_data[0], username=user_data[1], password=user_data[2], role=user_data[3])
        else:
            return None

    def create_user(self, username, password, role="user"):
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (username, password, role))  # No fetch required.
        print(f"User {username} successfully registered")
        

if __name__ == "__main__":
    user_dao = UserDAO()
    user = user_dao.get_user_by_username("admin")
    print(user)