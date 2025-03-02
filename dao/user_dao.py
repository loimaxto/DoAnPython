# dao/user_dao.py
from utils.database import Database

class UserDAO:
    def __init__(self):
        self.db = Database()

    def get_user_by_username(self, username):
        query = "SELECT id, username, password, role FROM users WHERE username = %s"
        result = self.db.execute_query(query, (username,), fetch=True)

        if result:
            user_data = result[0]  # Assuming username is unique
            from dto.user_dto import UserDTO # avoid circular dependency
            return UserDTO(user_id=user_data[0], username=user_data[1], password=user_data[2], role=user_data[3])
        else:
            return None

    def create_user(self, username, password, role="user"):
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        self.db.execute_query(query, (username, password, role))  # No fetch required.
        print(f"User {username} successfully registered")