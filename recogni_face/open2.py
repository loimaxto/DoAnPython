import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)

import torch
import torch.nn as nn
import torch.optim as optim
from recogni_face.modelsCNN import FaceRecognitionCNN2
from recogni_face.load_Data2 import Prepare_Data
from datetime import datetime

class Train_Models:
    def __init__(self, hozi=None, id_customer=5, dataset_path='dataset/5', save_path=None):
        self.hozi = hozi
        self.id_customer = id_customer
        self.dataset_path = dataset_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.num_classes = 2  # Known (0), Unknown (1)
        self.model = FaceRecognitionCNN2(num_classes=self.num_classes).to(self.device)

        if save_path is None:
            save_path = f"recogni_face/trainner/face_{self.id_customer}.pth"
        self.save_path = save_path

    def train(self, num_epochs=10, lr=0.001, batch_size=32):
        try:
            # Load dữ liệu
            data_loader = Prepare_Data(image_dir=self.dataset_path, batch_size=batch_size)
            train_loader, test_loader, _ = data_loader.load_data()

            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(self.model.parameters(), lr=lr)

            if self.hozi:
                self.hozi.setText("Đang huấn luyện mô hình của bạn...\nVui lòng đợi giây lát!")

            print(f"Training on device: {self.device}")
            for epoch in range(num_epochs):
                self.model.train()
                running_loss = 0.0
                for inputs, labels in train_loader:
                    inputs, labels = inputs.to(self.device), labels.to(self.device)

                    # Since only "Known" exists, label = 0
                    fake_labels = torch.zeros_like(labels)  # label 0 for Known

                    optimizer.zero_grad()
                    outputs = self.model(inputs)
                    loss = criterion(outputs, fake_labels)
                    loss.backward()
                    optimizer.step()

                    running_loss += loss.item()

                print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss:.4f}")

            if self.hozi:
                self.hozi.setText("Đã hoàn thành huấn luyện mô hình!")

            self.save_model()
            print("Training complete. Model saved.")

        except Exception as e:
            print(f"Lỗi khi huấn luyện mô hình: {str(e)}")
            if self.hozi:
                self.hozi.setText("Huấn luyện thất bại!")
            return

    def save_model(self):
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'class_names': ["Known", "Unknown"],
            'id_customer': self.id_customer,
            'timestamp': str(datetime.now())
        }, self.save_path)


if __name__ == "__main__":
    trainer = Train_Models(id_customer=5, dataset_path="dataset/5")
    trainer.train(num_epochs=10)
