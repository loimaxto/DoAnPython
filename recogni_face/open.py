import torch
import sys
import os
import time
from torchvision import transforms
from PIL import Image
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
from recogni_face.Load_Data import Prepare_Data
from recogni_face.modelsCNN import FaceRecognitionCNN,FaceRecognitionCNN2

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)

class Train_Models:
    def __init__(self, hozi=None):
        self.load_data = Prepare_Data()
        self.model = FaceRecognitionCNN2(num_classes=2)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.hozi = hozi
        self.best_accuracy = 0.0
        self.classes = []  # Thêm để lưu tên class
        
    def set_idcustomer(self, id_customer):
        """Thiết lập dữ liệu cho khách hàng cụ thể"""
        self.id_customer = id_customer
        self.load_data.Data_Loader(f"recogni_face/dataset/{self.id_customer}")
        self.classes = self.load_data.classes  # Cập nhật tên lớp
        
    def train(self, num_epochs=15, lr=0.001, save_best=True):
        """Phương thức huấn luyện"""
        try:
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(self.model.parameters(), lr=lr)
            scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=3, factor=0.1)
            
            print(f"Bắt đầu huấn luyện {num_epochs} epochs...")
            
            for epoch in range(num_epochs):
                start_time = time.time()
                self.model.train()
                running_loss = 0.0
                correct = 0
                total = 0
                
                for images, labels in self.load_data.train_loader:
                    images, labels = images.to(self.device), labels.to(self.device)
                    
                    optimizer.zero_grad()
                    outputs = self.model(images)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()
                    
                    _, predicted = torch.max(outputs, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()
                    running_loss += loss.item()
                
                val_accuracy = self.evaluate(loader=self.load_data.test_loader)
                epoch_loss = running_loss / len(self.load_data.train_loader)
                epoch_acc = 100 * correct / total
                
                scheduler.step(epoch_loss)
            
                if save_best and val_accuracy > self.best_accuracy:
                    self.best_accuracy = val_accuracy
                    torch.save(self.model.state_dict(), f"recogni_face/trainner/face_{self.id_customer}.pth")
                    print(f"Đã lưu model tốt nhất với accuracy: {val_accuracy:.2f}%")
                
                epoch_time = time.time() - start_time
                print(f"Epoch [{epoch+1}/{num_epochs}] - Loss: {epoch_loss:.4f} | "
                    f"Train Acc: {epoch_acc:.2f}% | Val Acc: {val_accuracy:.2f}% | "
                    f"Time: {epoch_time:.2f}s")
                if self.hozi != None:
                    self.hozi.setText("""Đang huấn luyện mô hình của bạn...
                                        Vui lòng đợi giây lát!
                                    """)
            if self.hozi != None:
                self.hozi.setText("Đã hoàn thành thu thập khuôn mặt khách hàng!")
            print("Kết thúc huấn luyện!")
            self.best_accuracy = val_accuracy
            #torch.save(self.model.state_dict(), f"recogni_face/trainner/face_{self.id_customer}.pth")
            print(f"Đã lưu model tốt nhất với accuracy: {val_accuracy:.2f}%")
        except Exception as e:
            print(str(e))
            return
    
    def evaluate(self, loader=None):
        """Đánh giá model trên tập dữ liệu"""
        if loader is None:
            loader = self.load_data.test_loader
            
        self.model.eval()
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        return 100 * correct / total
    
    def save(self, path_trainer):
        """Lưu model"""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'classes': self.classes,
        }, path_trainer)
    
    def predict(self, image_path):
        """Dự đoán ảnh đầu vào"""
        self.model.eval()
        
        try:
            image = Image.open(image_path).convert('RGB')
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.RandomHorizontalFlip(p=0.5),  # Lật ảnh ngang ngẫu nhiên
                transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.05),  # Biến đổi màu sắc nhẹ
                transforms.RandomRotation(degrees=10),  # Xoay nhẹ ảnh ±10 độ
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                    std=[0.229, 0.224, 0.225])
            ])
            image = transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.model(image)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
                conf, preds = torch.max(probabilities, 1)
            
            class_name = self.classes[preds.item()] if self.classes else str(preds.item())
            confidence = conf.item()
            
            return class_name, confidence
        except Exception as e:
            print(f"Lỗi khi dự đoán ảnh: {str(e)}")
            return None, 0.0

if __name__ == "__main__":
    id_customer = 3
    train_model = Train_Models()
    train_model.set_idcustomer(id_customer)
    train_model.train()
    train_model.save(f"recogni_face/trainner/face_{id_customer}.pth")
    
    test_image_path = "recogni_face/dataset/4/4.1.jpg"
    class_name, confidence = train_model.predict(test_image_path)
    if class_name is not None:
        print(f"\nKết quả dự đoán: {class_name} (Độ tin cậy: {confidence*100:.2f}%)")
