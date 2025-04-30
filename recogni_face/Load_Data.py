import torch
import torch.optim as optim
import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

import torch.nn as nn
from recogni_face.load import CustomImageDataset
class Prepare_Data:
    def __init__(self):
        self.classes = ['class0', 'class1']  # 0: img_dir_class1, 1: dataset/1
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                 std=[0.229, 0.224, 0.225])
        ])
    
    def Data_Loader(self, path_image="dataset"):
        dataset = CustomImageDataset(path_image, transform=self.transform)
        
        # Không dùng ImageFolder nữa
        # Không cần gán self.classes = dataset.classes
        
        # Chia tập train/test
        train_size = int(0.8 * len(dataset))
        test_size = len(dataset) - train_size
        self.train_dataset, self.test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

        self.train_loader = DataLoader(self.train_dataset, batch_size=32, shuffle=True)
        self.test_loader = DataLoader(self.test_dataset, batch_size=32, shuffle=False)
        self.classes = ['Customer','NotCustomer']
