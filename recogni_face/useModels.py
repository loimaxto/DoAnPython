from modelsCNN import FaceRecognitionCNN
import torch
from torchvision import transforms
import cv2
import numpy as np
import time
from PIL import Image
import time
id_customer = 2
time_count = 1000
count = 0
model_path = f"recogni_face/trainner/face_{id_customer}.pth"
# Hàm để tải mô hình
class Load_Models:
    def __init__(self,num_classes):
        self.model = FaceRecognitionCNN(num_classes)
        #self.model.load_state_dict(torch.load())
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()  # Chuyển mô hình sang chế độ đánh giá
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Hàm để phát hiện khuôn mặt và nhận diện
    def recognize_faces_from_camera(self, class_names, confidence_threshold=0.8):
        # Tải bộ phát hiện khuôn mặt Haar Cascade
        check = False
        
        # Mở camera
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Lật hình ảnh theo chiều ngang để tạo hiệu ứng phản chiếu giống gương
            frame = cv2.flip(frame, 1)
            
            # Chuyển ảnh sang grayscale để phát hiện khuôn mặt
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            for (x, y, w, h) in faces:
                # Trích xuất ảnh khuôn mặt
                face_img = frame[y:y+h, x:x+w]
                
                # Tiền xử lý ảnh khuôn mặt
                face_img = cv2.resize(face_img, (64, 64))  # Resize về kích thước đầu vào của mô hình
                face_img = Image.fromarray(face_img)  # Chuyển sang PIL Image
                transform = transforms.Compose([
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])
                face_img = transform(face_img).unsqueeze(0)  # Thêm chiều batch
                # Dự đoán khuôn mặt
                with torch.no_grad():
                    outputs = self.model(face_img)
                    probabilities = torch.softmax(outputs, dim=1)  # Chuyển đổi logits thành xác suất
                    confidence, predicted = torch.max(probabilities, 1)
                    
                    confidence = confidence.item()  # Lấy giá trị độ tin cậy
                    print(confidence)
                    predicted_label = predicted.item()  # Lấy nhãn dự đoán
                
                # Kiểm tra độ tin cậy và kích thước khuôn mặt
                if w*h > 50000:
                    if confidence < confidence_threshold:
                        label = "Unknown"  # Khuôn mặt không khớp
                        count = 0
                    else:
                        label = class_names[predicted_label]  # Khuôn mặt khớp
                        count+=1
                else:
                    count=0
                    label = "Bring face closer"  # Khuôn mặt quá nhỏ
                
                # Vẽ khung và hiển thị nhãn
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.putText(frame, f"Confidence: {confidence:.2f}", (x, y+h+20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            if count==time_count:
                break
            # Hiển thị khung hình
            cv2.imshow('Face Recognition', frame)
            
            # Thoát nếu nhấn phím 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Giải phóng camera và đóng cửa sổ
        cap.release()
        cv2.destroyAllWindows() 
        return check

# Hàm chính
models = Load_Models(2)
models.recognize_faces_from_camera(["unknow","thai"])