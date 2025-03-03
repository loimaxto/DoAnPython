
class Phong:
    def __init__(self, id: int, ten_phong: str, so_giuong: int, id_gia: int):
        """
        Khởi tạo đối tượng phòng
        
        :param id: Mã phòng
        :param ten_phong: Tên phòng
        :param so_giuong: Số giường trong phòng
        :param id_gia: Mã giá phòng (liên kết với bảng gia_phong)
        """
        self.id = id
        self.ten_phong = ten_phong
        self.so_giuong = so_giuong
        self.id_gia = id_gia

    def update_info(self, ten_phong=None, so_giuong=None, id_gia=None):
        """
        Cập nhật thông tin phòng
        
        :param ten_phong: Tên phòng mới (nếu có)
        :param so_giuong: Số giường mới (nếu có)
        :param id_gia: ID giá mới (nếu có)
        """
        if ten_phong:
            self.ten_phong = ten_phong
        if so_giuong:
            self.so_giuong = so_giuong
        if id_gia:
            self.id_gia = id_gia

    def __str__(self):
        return f"Phong(id={self.id}, ten_phong='{self.ten_phong}', so_giuong={self.so_giuong}, id_gia={self.id_gia})"


