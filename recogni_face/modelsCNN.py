
import torch.nn as nn

import torch.nn.functional as F
import torch
#class FaceRecognitionCNN(nn.Module):
#    def __init__(self, num_classes):
#        super(FaceRecognitionCNN, self).__init__()
#        
#        # Lớp tích chập 1
#        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
#        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
#        
#        # Lớp tích chập 2
#        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
#        
#        # Lớp tích chập 3
#        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
#        
#        # Lớp fully connected 1
#        self.fc1 = nn.Linear(128 * 8 * 8, 512)  # Giả sử kích thước ảnh đầu vào là 64x64
#        self.fc2 = nn.Linear(512, num_classes)
#    
#    def forward(self, x):
#        # Convolutional layers
#        x = self.pool(F.relu(self.conv1(x)))
#        x = self.pool(F.relu(self.conv2(x)))
#        x = self.pool(F.relu(self.conv3(x)))
#        
#        # Flatten
#        x = x.view(-1, 128 * 8 * 8)
#        
#        # Fully connected layers
#        x = F.relu(self.fc1(x))
#        x = self.fc2(x)
#        
#        return x

import torch.nn as nn
import torch
import torch.nn.functional as F

class FaceRecognitionCNN(nn.Module):
    def __init__(self, num_classes):
        super(FaceRecognitionCNN, self).__init__()
        
        # Lớp tích chập 1
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        
        # Lớp tích chập 2
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        
        # Lớp tích chập 3
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)
        
        # Lớp fully connected 1
        self.fc1 = nn.Linear(128 * 8 * 8, 512)  # Giả sử kích thước ảnh đầu vào là 64x64
        self.fc2 = nn.Linear(512, num_classes)
    def forward(self, x):
        # Convolutional layers
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        
        # Flatten
        x = x.view(-1, 128 * 8 * 8)
        
        # Fully connected layers
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        
        return x

import torch
import torch.nn as nn
import torch.nn.functional as F

class FaceRecognitionCNN2(nn.Module):
    def __init__(self, num_classes=10, input_size=(3, 224, 224)):  # Ảnh đầu vào mặc định 224x224
        super(FaceRecognitionCNN2, self).__init__()
        self.input_size = input_size
        
        self.conv1 = self.create_convolution(3, 8)
        self.conv2 = self.create_convolution(8, 16)
        self.conv3 = self.create_convolution(16, 32)
        self.conv4 = self.create_convolution(32, 64)
        self.conv5 = self.create_convolution(64, 64)

        # Tính kích thước đầu vào cho FC bằng dummy input
        with torch.no_grad():
            dummy = torch.zeros(1, *input_size)
            x = self.conv1(dummy)
            x = self.conv2(x)
            x = self.conv3(x)
            x = self.conv4(x)
            x = self.conv5(x)
            flattened_size = x.view(1, -1).shape[1]

        self.fc1 = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(flattened_size, 1024),
            nn.ReLU()
        )
        self.fc2 = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(1024, 512),
            nn.ReLU()
        )
        self.fc3 = nn.Linear(512, num_classes)

    def create_convolution(self, in_channels, out_channels, kernel_size=3):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size, padding=1, stride=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
            nn.Conv2d(out_channels, out_channels, kernel_size, padding=1, stride=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = self.conv5(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        return x



if __name__ == "__main__":
    data = torch.rand(8, 3, 224, 224)
    loadmodel = FaceRecognitionCNN2()
    output = loadmodel(data)
    print(output.shape)  # Should print torch.Size([8, 10])