import cv2
import numpy
import matplotlib.pyplot as plt
from relu import *

image = cv2.imread("recogni_face/image/shin.jpg")
image = cv2.resize(image,(200,200))
gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)/255
numpy.random.seed(47)
print(gray_image.shape)

class conv2D:
    def __init__(self,input,numkernel=10,kernelsize=3,stride=1):
        self.input = input
        self.height,self.width = input.shape
        self.stride = stride
        self.kernel = numpy.random.randn(numkernel,kernelsize,kernelsize)
        self.result = numpy.zeros((self.getheight()+1,
                                   self.getwidth()+1,
                                   numkernel))# số layer
    def getheight(self):
        return int((self.height-self.kernel.shape[1])/self.stride)
    def getwidth(self):
        return int((self.width-self.kernel.shape[2])/self.stride)
    def getROI(self):
        for row in range(0,self.getheight()+1):
            for col in range(0,self.getwidth()+1):
                roi = self.input[row*self.stride: row*self.stride+self.kernel.shape[1],
                                 col*self.stride: col*self.stride+self.kernel.shape[2]]
                # trả về các giá trị mà không ngừng vong lặp
                yield row,col,roi
    def operate(self):
        for layer in range(self.kernel.shape[0]):
            for row,col,roi in self.getROI():
                self.result[row,col,layer] = numpy.sum(roi*self.kernel[layer])
        return self.result
conv2d = conv2D(gray_image,kernelsize=4,numkernel=20,stride=5).operate()
conv2d_relu= Relu(conv2d).operate()
conv2d_leakyrelu = LeakyRelu(conv2d).operate()
conv2d_leakyrelu_maxpooling=  MaxPooling(conv2d_leakyrelu,poolingsize=4).operate()
fig = plt.figure(figsize=(10,10))
print(SoftMax(conv2d_leakyrelu_maxpooling,10).operate())
for i in range(20):
    plt.subplot(4,5,i+1)
    plt.imshow(conv2d_leakyrelu[:,:,i],cmap="gray")
    plt.axis("off")
plt.savefig("imagetest_leakyrelu.jpg")
plt.show()
