# dto/user_dto.py
class UserDTO:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f"UserDTO(user_id={self.user_id}, username='{self.username}', role='{self.role}')"