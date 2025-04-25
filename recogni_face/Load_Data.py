import torch
import torch.optim as optim
import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from recogni_face.modelsCNN import FaceRecognitionCNN
import torch.nn as nn
from recogni_face.load import CustomImageDataset
class Prepare_Data:
    def __init__(self):
        self.transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    def Data_Loader(self,path_image = "dataset"):
        dataset = CustomImageDataset(path_image,  transform=self.transform)

        # Chia tập dữ liệu thành tập huấn luyện và tập kiểm tra
        train_size = int(0.8 * len(dataset))  # 80% cho huấn luyện
        test_size = len(dataset) - train_size  # 20% cho kiểm tra
        self.train_dataset, self.test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

        # Tạo DataLoader cho tập huấn luyện và tập kiểm tra
        self.train_loader = DataLoader(self.train_dataset, batch_size=32, shuffle=True)
        self.test_loader = DataLoader(self.test_dataset, batch_size=32, shuffle=False)