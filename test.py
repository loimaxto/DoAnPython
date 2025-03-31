import sys
import cv2
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget


class CameraApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PyQt6 Camera App")
        self.setGeometry(100, 100, 800, 600)
        
        # Tạo widget trung tâm và layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Tạo label để hiển thị hình ảnh từ camera
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)
        
        # Tạo nút để bật/tắt camera
        self.toggle_button = QPushButton("Bật Camera")
        self.toggle_button.clicked.connect(self.toggle_camera)
        layout.addWidget(self.toggle_button)
        
        # Khởi tạo camera
        self.camera = None
        self.camera_active = False
        
        # Timer để cập nhật hình ảnh từ camera
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
    
    def toggle_camera(self):
        if not self.camera_active:
            # Mở camera
            self.camera = cv2.VideoCapture(0)  # 0 là camera mặc định
            
            if not self.camera.isOpened():
                print("Không thể mở camera")
                return
            
            self.camera_active = True
            self.toggle_button.setText("Tắt Camera")
            self.timer.start(30)  # Cập nhật mỗi 30ms
        else:
            # Tắt camera
            self.camera_active = False
            self.toggle_button.setText("Bật Camera")
            self.timer.stop()
            self.camera.release()
            self.image_label.clear()
    
    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            # Chuyển đổi frame từ OpenCV sang QImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
            # Hiển thị hình ảnh lên QLabel
            self.image_label.setPixmap(QPixmap.fromImage(q_img).scaled(
                self.image_label.width(), 
                self.image_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio
            ))
    
    def closeEvent(self, event):
        # Đảm bảo camera được giải phóng khi đóng ứng dụng
        if self.camera_active:
            self.timer.stop()
            self.camera.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec())