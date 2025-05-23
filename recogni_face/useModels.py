from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel,QPushButton,QMessageBox
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer
import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
from recogni_face.modelsCNN import FaceRecognitionCNN,FaceRecognitionCNN2
import torch
from torchvision import transforms
import cv2
import numpy as np
from PIL import Image
import time
# hàm sẽ kiểm tra nếu khuôn mặt khớp với hệ thống thì sẽ mở cửa trong vòng 4s
class FaceRecognitionWidget(QWidget):
    def __init__(self, id_customer=33,room_name="Phong 0", class_names=["known", "unKnown"], parent=None):
        super().__init__(parent)
        self.id_customer = id_customer
        self.class_names = class_names
        self.time_count = 200
        self.count = 0
        self.check = False
        self.capture_mode = False
        # Initialize UI
        self.init_ui()
        self.room_name = room_name
        
        
        
    def init_ui(self):
        try:
            self.layout = QVBoxLayout()
            self.setLayout(self.layout)
            self.btn_start = QPushButton("Check in thôi!")
            self.btn_back = QPushButton("quay lại!")
            self.image_label = QLabel()
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.image_label)
            self.layout.addWidget(self.btn_start)
            self.layout.addWidget(self.btn_back)
            
            self.btn_start.clicked.connect(self.start_capture)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Có lỗi: {str(e)}")
    def start_capture(self):
        try:
            self.btn_start.setEnabled(False)
            self.begintime = time.time()
            # Initialize model
            self.init_model()
            
            # Setup camera
            self.cap = cv2.VideoCapture(0)
            self.timer = QTimer()
            
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)  # Update every 30ms
            self.btn_start.setEnabled(True)
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra khi tìm kiếm: {str(e)}")
    def stop_capture(self):
        """Dừng chế độ chụp ảnh"""
        print("cửa đã được mở")
        self.count = 0
        self.capture_mode = False
        self.btn_start.setEnabled(True)
    def init_model(self):
        model_path = f"recogni_face/trainner/face_{self.id_customer}.pth"
        
        # Load model
        self.model = FaceRecognitionCNN2(2)
        checkpoint = torch.load(model_path)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        
        # Load class names từ checkpoint nếu có
        self.class_names = checkpoint.get('classes', ["Unknown", "Known"])

        self.model.eval()
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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
        self.timerun = time.time() - self.begintime
        
        
        # Flip frame horizontally
        frame = cv2.flip(frame, 1)
        
        # Process frame for face recognition
        processed_frame = self.process_frame(frame)
        
        # Convert to QImage and display
        rgb_image = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_image))
        print(self.check,self.count)
        
    
    def process_frame(self, frame):
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
            
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
                
                # Trong vòng lặp nhận diện
                if w*h > 50000:
                    if confidence < 0.8:
                        label = "Invalid Face"
                        self.count = 0
                    else:
                        predicted_name = self.class_names[predicted_label]
                        print([predicted_label])
                        if predicted_name.lower() == "nocustomer":
                            label = "Invalid Face"
                            self.count = 0
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        else:
                            label = "Valid Face" if predicted_name.lower()=="customer" else "Invalid Face"
                            self.count += 1
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                else:
                    self.count = 0
                    label = "Bring face closer"
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

                print(predicted)
                # Draw rectangle and label
                #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                time_code = self.timerun-9
                if time_code<=0:
                    time_code=0
                cv2.putText(frame, f"time: {time_code:.2f}", 
                        (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"num lock: {self.count}", 
                        (x, y+h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                if self.count >= self.time_count:
                    print("đã mở cửa!")
                    cv2.putText(frame, f"Open {self.room_name}", 
                        (x, y-50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    self.check = True
                    self.closeEvent()
                    break
                elif(time_code>=15):
                    print("chưa mở cửa!")
                    cv2.putText(frame, f"Close {self.room_name}",
                        (x, y-50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    self.check =False
                    self.closeEvent()
                    break
            
            return frame
        except Exception as e:
            print(str(e))
            QMessageBox.critical(self, "Lỗi", f"Có lỗi: {str(e)}")
    
    def closeEvent(self):
        if hasattr(self, 'timer') and self.timer.isActive():
            self.timer.stop()
        
        if hasattr(self, 'camera') and self.cap.isOpened():
            
            self.cap.release()
        
        
from PyQt6.QtWidgets import QApplication, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognition App")
        
        # Create the face recognition widget
        self.face_widget = FaceRecognitionWidget(
            id_customer=5,
            class_names=["Unknown", "Khoa"]  # Your class names here
        )
        print(self.face_widget.check)
        self.setCentralWidget(self.face_widget)

if __name__=="__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
