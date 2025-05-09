import torch
import torch.optim as optim
import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

class Prepare_Data:
    def __init__(self, image_dir, batch_size=32):
        self.image_dir = image_dir
        self.batch_size = batch_size
        self.classes = ["Known"]  # Chỉ 1 lớp

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],
                                 [0.229, 0.224, 0.225])
        ])
    
    def load_data(self):
        from torchvision.datasets import ImageFolder
        dataset = ImageFolder(root=self.image_dir, transform=self.transform)

        # Gán tất cả nhãn = 0 (Known)
        dataset.targets = [0] * len(dataset.targets)

        train_size = int(0.8 * len(dataset))
        test_size = len(dataset) - train_size
        train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

        train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=self.batch_size, shuffle=False)

        return train_loader, test_loader, self.classes
