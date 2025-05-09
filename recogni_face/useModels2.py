import sys
import os
import torch
import cv2
import numpy as np
from PIL import Image
import time
from torchvision import transforms
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox,
    QApplication, QMainWindow
)
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer

# Add project path to sys
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)

from recogni_face.modelsCNN import FaceRecognitionCNN2


class FaceRecognitionWidget(QWidget):
    def __init__(self, id_customer=5, parent=None):
        super().__init__(parent)
        self.id_customer = id_customer
        self.check = False
        self.count = 0
        self.threshold = 200
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_start = QPushButton("Bắt đầu nhận diện")
        self.btn_start.clicked.connect(self.start_capture)

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.btn_start)

    def start_capture(self):
        self.btn_start.setEnabled(False)
        self.begintime = time.time()
        self.init_model()

        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def init_model(self):
        model_path = f"recogni_face/trainner/face_{self.id_customer}.pth"

        if not os.path.exists(model_path):
            QMessageBox.critical(self, "Lỗi", f"Không tìm thấy model: {model_path}")
            return

        self.model = FaceRecognitionCNN2(num_classes=2)
        checkpoint = torch.load(model_path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        

        # Load class names từ checkpoint nếu có
        loaded_classes = checkpoint.get('classes', ["unknown", "Known"])

        # Đảm bảo "Unknown" luôn là label 0
        if "Unknown" in loaded_classes:
            loaded_classes.remove("Unknown")
        self.class_names = ["Unknown"] + loaded_classes
        self.model.eval()

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.transform = transforms.Compose([
            transforms.RandomHorizontalFlip(p=0.5),  # Lật ảnh ngang ngẫu nhiên
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.05),  # Biến đổi màu sắc nhẹ
            transforms.RandomRotation(degrees=10),  # Xoay nhẹ ảnh ±10 độ
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                std=[0.229, 0.224, 0.225])
        ])

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        frame = self.process_frame(frame)

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        qt_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (224, 224))
            face_img = Image.fromarray(face_img)
            face_img = self.transform(face_img).unsqueeze(0)

            with torch.no_grad():
                outputs = self.model(face_img)
                probabilities = torch.softmax(outputs, dim=1)
                confidence, predicted = torch.max(probabilities, 1)
                confidence = confidence.item()
                predicted_label = predicted.item()

            if w * h > 50000:
                if confidence < 0.8:
                    label = "Unknown"
                    self.count = 0
                else:
                    if predicted_label == 0:
                        label = "Unknown"
                        self.count = 0
                    else:
                        label = self.class_names[predicted_label]
                        self.count += 1
            else:
                label = "Bring face closer"
                self.count = 0

            # Vẽ lên frame
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            time_code = self.timerun - 9
            if time_code <= 0:
                time_code = 0

            cv2.putText(frame, f"time: {time_code:.2f}",
                        (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"num lock: {self.count}",
                        (x, y+h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if self.count >= self.time_count:
                print("đã mở cửa!")
                cv2.putText(frame, f"Open the door!!!!!!",
                            (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                self.check = True
                self.closeEvent()
                break
            elif time_code >= 60:
                print("chưa mở cửa!")
                cv2.putText(frame, f"Close the door!!",
                            (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                self.check = False
                self.closeEvent()
                break

    def closeEvent(self):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        self.btn_start.setEnabled(True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Use Face Recognition Model")

        self.widget = FaceRecognitionWidget(id_customer=5)
        self.setCentralWidget(self.widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
