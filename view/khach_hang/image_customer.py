import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                            QScrollArea, QGridLayout, QLabel,QPushButton)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import os
import random

class FaceGalleryWidget(QWidget):
    def __init__(self, id_customer=None,name_customer=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Thư viện khuôn mặt")
        self.setMinimumSize(800, 600)
        self.back_btn1 = QPushButton("Quay lại!")
        # Tạo layout chính
        self.main_layout = QVBoxLayout(self)
        
        # Tạo scroll area để xem nhiều ảnh
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        # Widget chứa các ảnh
        self.container = QWidget()
        self.grid_layout = QGridLayout(self.container)
        self.grid_layout.setSpacing(10)
        
        # Thêm các ảnh demo (hoặc từ thư mục)
        self.load_images(f"recogni_face/dataset/{id_customer}")
        
        self.scroll_area.setWidget(self.container)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.back_btn1)
    def load_images(self, image_folder=None):
        """Tải ảnh từ thư mục hoặc tạo ảnh demo"""
        # Xóa các widget cũ nếu có
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        # Tạo 30 ảnh demo nếu không có thư mục ảnh
        if image_folder is None or not os.path.exists(image_folder):
            self.create_demo_faces()
        else:
            self.load_from_folder(image_folder)
    
    def create_demo_faces(self):
        """Tạo 30 ảnh khuôn mặt demo màu ngẫu nhiên"""
        for i in range(30):
            # Tạo ảnh màu ngẫu nhiên (thay bằng ảnh thực tế)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            image = QImage(100, 100, QImage.Format.Format_RGB32)
            image.fill(Qt.GlobalColor(color[0], color[1], color[2]))
            
            pixmap = QPixmap.fromImage(image)
            label = QLabel()
            label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("border: 1px solid gray;")
            
            # Thêm nhãn ID
            id_label = QLabel(f"Face {i+1}")
            id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Tạo widget chứa ảnh và nhãn
            face_widget = QWidget()
            face_layout = QVBoxLayout(face_widget)
            face_layout.addWidget(label)
            face_layout.addWidget(id_label)
            
            # Thêm vào grid layout (5 cột)
            row = i // 5
            col = i % 5
            self.grid_layout.addWidget(face_widget, row, col)
    
    def load_from_folder(self, folder_path):
        """Tải ảnh từ thư mục"""
        image_files = [f for f in os.listdir(folder_path) 
                     if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for i, filename in enumerate(image_files[:30]):  # Giới hạn 30 ảnh
            try:
                image_path = os.path.join(folder_path, filename)
                pixmap = QPixmap(image_path)
                
                if pixmap.isNull():
                    continue
                
                label = QLabel()
                label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("border: 1px solid gray;")
                
                # Thêm nhãn tên file
                id_label = QLabel(os.path.splitext(filename)[0])
                id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Tạo widget chứa ảnh và nhãn
                face_widget = QWidget()
                face_layout = QVBoxLayout(face_widget)
                face_layout.addWidget(label)
                face_layout.addWidget(id_label)
                
                # Thêm vào grid layout (5 cột)
                row = i // 5
                col = i % 5
                self.grid_layout.addWidget(face_widget, row, col)
                
            except Exception as e:
                print(f"Không thể tải ảnh {filename}: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Tạo widget với ảnh demo
    gallery = FaceGalleryWidget(1)
    
    # Hoặc tải ảnh từ thư mục (bỏ comment dòng dưới)
    # gallery = FaceGalleryWidget("đường_dẫn_đến_thư_mục_ảnh")
    
    gallery.show()
    sys.exit(app.exec())