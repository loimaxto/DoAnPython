import torch
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from modelsCNN import FaceRecognitionCNN
import torch.nn as nn
from Load_Data import Prepare_Data
# Khởi tạo mô hình
id_customer = 5
class Train_Models:
    def __init__(self):
        self.load_data = Prepare_Data()
        self.load_data.Data_Loader(f"recogni_face/dataset/{id_customer}")
        self.model = FaceRecognitionCNN(2)
    def Evaluate(self):

        # Định nghĩa hàm mất mát và optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.001)

            # Huấn luyện mô hình
        num_epochs = 10
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)

        for epoch in range(num_epochs):
            self.model.train()
            running_loss = 0.0
            for images, labels in self.load_data.train_loader:
                images, labels = images.to(device), labels.to(device)
        
                # Zero the parameter gradients
                optimizer.zero_grad()
        
                # Forward pass
                outputs = self.model(images)
                loss = criterion(outputs, labels)
        
                # Backward pass và optimize
                loss.backward()
                optimizer.step()
        
                running_loss += loss.item()
    
            print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(self.load_data.train_loader):.4f}")
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in self.load_data.test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = self.model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        print(f"Accuracy on test set: {100 * correct / total:.2f}%")


        # Định nghĩa hàm mất mát và optimizer
        
    def save(self,path_trainner):
        # Lưu mô hình
        torch.save(self.model.state_dict(), path_trainner)

train_model = Train_Models()
train_model.Evaluate()
train_model.save(f"recogni_face/trainner/face_{id_customer}.pth")
