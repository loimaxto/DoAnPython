import os
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from PIL import Image

class CustomImageDataset(Dataset):
    def __init__(self, img_dir_class1, transform=None):
        self.img_dir_class1 = "recogni_face/dataset/3"
        self.img_dir_class2 = img_dir_class1
        self.transform = transform
        
        # Lấy danh sách hình ảnh từ cả hai thư mục
        self.img_names_class1 = os.listdir(self.img_dir_class1)
        self.img_names_class2 = os.listdir(self.img_dir_class2)
        
        # Gán nhãn: 0 cho class1, 1 cho class2
        self.images = []
        self.labels = []
        
        for img_name in self.img_names_class1:
            self.images.append(os.path.join(self.img_dir_class1, img_name))
            self.labels.append(0)  # Nhãn 0 cho class1
        
        for img_name in self.img_names_class2:
            self.images.append(os.path.join(self.img_dir_class2, img_name))
            self.labels.append(1)  # Nhãn 1 cho class2

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = self.images[idx]
        image = Image.open(img_path).convert('RGB')  # Mở hình ảnh và chuyển đổi sang RGB
        label = self.labels[idx]  # Nhãn tương ứng
        
        if self.transform:
            image = self.transform(image)
        
        return image, label