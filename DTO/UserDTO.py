# file chua class doi duoc

class UserDTO:
    """
    Data Transfer Object (DTO) for user information.
    """

    def __init__(self, username, password, user_id):

        self.username = username
        self.password = password
        self.user_id = user_id

    def __repr__(self):
        return f"UserDTO(username='{self.username}', user_id={self.user_id})"  # Exclude password from repr for security

    def to_dict(self):
      return {
          'username': self.username,
          'user_id': self.user_id, # Exclude password from dict for security.
          # 'password': self.password # if you absolutely needed it.
      }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a UserDTO object from a dictionary.

        Args:
            data (dict): A dictionary containing user information.

        Returns:
            UserDTO: A UserDTO object.
        """
        return cls(
            username=data.get('username'),
            password=data.get('password'),
            user_id=data.get('user_id'),
        )

# Example Usage
if __name__ == "__main__":
    user_data = {
        "username": "john_doe",
        "password": "secure_password",
        "user_id": 123
    }

    user_dto = UserDTO.from_dict(user_data)

    print(user_dto) #repr
    print(user_dto.to_dict())

    another_user_dto = UserDTO("jane_doe", "another_password", 456)
    print(another_user_dto)