class KhachHangDTO:
    def __init__(self, kh_id=None, ten=None, sdt=None, image=None):
        self.kh_id = kh_id
        self.ten = ten
        self.sdt = sdt
        self.image = image

    def __str__(self):
        return f"KhachHang(kh_id={self.kh_id}, ten='{self.ten}', sdt='{self.sdt}', image='{self.image}')"
    
class UserDTO:
    def __init__(self, user_id, username, password, role):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f"UserDTO(user_id={self.user_id}, username='{self.username}', role='{self.role}')"