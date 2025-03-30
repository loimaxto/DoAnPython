
import sys
import cv2
import os
import time
import numpy as np
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (QApplication, QLabel, QWidget, 
                            QVBoxLayout, QPushButton, QMessageBox)
from PyQt6 import QtWidgets
class FaceRecognitionWidget(QWidget):
    capture_completed = pyqtSignal()  # Signal khi hoàn thành chụp ảnh
    
    def __init__(self,id_customer=0, parent=None):

        super().__init__(parent)
        self.count = 0
        
        # Thiết lập các thông số đường dẫn
        self.PATH = "recogni_face"
        self.PATH_IMAGE = "dataset"
        self.PATH_TRAINER = "trainner"
        self.id_customer = id_customer  # ID khách hàng mặc định
        
        # Khởi tạo giao diện
        #self.setup_ui()
        
        
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        self.back_btn = QPushButton("Quay lại!")
        self.layout = QVBoxLayout(self)
        # Label hiển thị hình ảnh từ camera
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumSize(640, 480)
        self.layout.addWidget(self.image_label)
        
        # Nút bắt đầu chụp ảnh
        self.capture_btn = QPushButton("Bắt Đầu Thu Thập Dữ Liệu")
        self.capture_btn.clicked.connect(self.start_capture)
        self.layout.addWidget(self.capture_btn)
        
        self.layout.addWidget(self.back_btn)
        # Label hiển thị trạng thái
        self.status_label = QLabel("Sẵn sàng")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status_label)
        # Khởi tạo camera và các thành phần nhận diện
        """Khởi động lại camera"""
        self.camera_active = True
        self.camera = cv2.VideoCapture(0)
        
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        
        # Biến trạng thái
        self.capture_mode = False
        self.capture_count = 0
        self.max_capture = 10
        
        # Timer để cập nhật hình ảnh từ camera
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # 30ms mỗi frame
    
    
    def update_frame(self):
        """Cập nhật hình ảnh từ camera"""
        ret, frame = self.camera.read()
        if not ret:
            return
        
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if self.capture_mode:
            self.process_capture_mode(frame, gray)
        else:
            self.process_normal_mode(frame, gray)
        
        # Hiển thị hình ảnh lên QLabel
        self.display_image(frame)
    
    def process_normal_mode(self, frame, gray):
        """Xử lý khi ở chế độ bình thường"""
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 140, 130), 2)
        
    def process_capture_mode(self, frame, gray):
        """Xử lý khi ở chế độ chụp ảnh"""
        
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x-2, y-2), (x+w+2, y+h+2), (0, 255, 0), 2)  # Màu xanh khi đang chụp
            self.capture_count += 1
            if self.capture_count%15==0:
                # Chụp và lưu ảnh khuôn mặt
                face_img = frame[y:y+h, x:x+w]
                face_img = cv2.resize(face_img, (100, 100))
                    
                # Tạo thư mục nếu chưa tồn tại
                save_dir = f"{self.PATH}/{self.PATH_IMAGE}/{self.id_customer}"
                #os.makedirs(save_dir, exist_ok=True)
                    
                self.count+=1
                cv2.imwrite(f"{save_dir}/{self.id_customer}.{self.count}.jpg", face_img)
                    
                
                print(self.count)
                self.status_label.setText(f"Đang thu thập ảnh!")
                
            if self.count>=20:
                self.stop_capture()
                self.capture_completed.emit()  # Phát signal khi hoàn thành
                
    
    def display_image(self, frame):
        """Hiển thị hình ảnh lên QLabel"""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        
        # Scale ảnh phù hợp với kích thước label
        self.image_label.setPixmap(QPixmap.fromImage(qt_image).scaled(
            self.image_label.width(), 
            self.image_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio
        ))
    
    def start_capture(self):
        """Bắt đầu chế độ chụp ảnh"""
        self.capture_mode = True
        self.capture_count = 0
        self.capture_btn.setEnabled(False)
        
        self.status_label.setText("Bắt đầu thu thập dữ liệu...")
    
    def stop_capture(self):
        """Dừng chế độ chụp ảnh"""
        self.status_label.setText(f"Hoàn thành! Đã chụp {self.count} ảnh")
        self.count = 0
        self.capture_mode = False
        self.capture_btn.setEnabled(True)
        
    
    def set_customer_id(self, customer_id):
        """Thiết lập ID khách hàng"""
        os.makedirs(f"recogni_face/dataset/{customer_id}",exist_ok=True)
        self.id_customer = customer_id
    
    def closeEvent(self):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        
        if hasattr(self, 'camera') and self.camera.isOpened():
            self.camera.release()
        
        self.camera_active = False



# Ví dụ sử dụng widget trong cửa sổ chính
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("tìm kiếm khuôn mặt")
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout(self)
        
        # Thêm widget nhận diện khuôn mặt
        self.face_widget = FaceRecognitionWidget(5)
        layout.addWidget(self.face_widget)
        
        # Kết nối signal khi hoàn thành chụp ảnh
        self.face_widget.capture_completed.connect(self.on_capture_completed)
    
    def on_capture_completed(self):
        """Xử lý khi hoàn thành chụp ảnh"""
        QMessageBox.information(self, "Thông báo", "Đã hoàn thành thu thập dữ liệu khuôn mặt!")


if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    ui = FaceRecognitionWidget(1)
    ui.show()
    sys.exit(app.exec())