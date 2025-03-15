import cv2
import numpy as np
from PIL import Image
import os
import time
import os
class Train_models:
    def __init__(self,path_image):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.imagePaths = [os.path.join(path_image,f) for f in os.listdir(path = path_image)]    
        self.faceSample = []
        self.IDs = []
    def get_Image_Label(self):
        print("dữ liệu đang được train!")
        for imagePath in self.imagePaths:
            # convert to grayscale
            PILimage = Image.open(imagePath).convert("L")
            img_array = np.array(PILimage,"uint8")
            id = int(os.path.split(imagePath)[-1].split(".")[0])
            faces = self.detector.detectMultiScale(image=img_array)
            for(x,y,w,h) in faces:
                self.faceSample.append(img_array[y:y+h,x:x+w])
                self.IDs.append(id)
        return self.faceSample,self.IDs
    def trainning(self,pathtrain):
        faces,ids = self.get_Image_Label()
        self.recognizer.train(faces,np.array(ids))
        self.recognizer.write(pathtrain)
        print('dữ liệu đã được train thành công')

# Khởi động camera
class Recognition_face:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        
    def open_cam_recogni(self,bordersize=2,bordercolor = (255,140,130)):
        image_cam = cv2.VideoCapture(0)
        count = 0
        while True:
            ok,frame = image_cam.read()
            # Xác định vị trí khuôn mặt
            face_locations = self.face_cascade.detectMultiScale(frame,1.3,5)

            # Vẽ hình tròn quanh khuôn mặt
    
            for (x, y, w, h) in face_locations:
            # lưu ảnh khuôn mặt vào trong bộ máy
                if count>=100:
                    face_human = cv2.resize(frame[y+bordersize+1:y+h-bordersize-1,
                                                  x+bordersize+1:x+w-bordersize-1],(100,100))
                    cv2.imwrite(f"dataset/khoa/1.{str(int(time.time()))}.jpg",face_human)
                    count=0
        

                cv2.rectangle(frame, (x, y), (x+w,y+h),bordercolor, bordersize)
        
                
                # Hiển thị kết quả
            cv2.imshow("Face Detection", frame)
            count+=1
            print(count)
            # Nhấn 'q' để thoát
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        image_cam.release()
        cv2.destroyAllWindows()
        image_cam = cv2.VideoCapture(0)
    def facial_recognition(self,path_trainner):
        self.recognizer.read(path_trainner)
        font = cv2.FONT_HERSHEY_SIMPLEX
        id = 0
        name = [0,"khoa"]
        cam = cv2.VideoCapture(0)
        while True:
            ret,img = cam.read()
            img = cv2.flip(img,-1)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#chuyen sang mau den trang
            face = self.face_cascade.detectMultiScale(
                gray,scaleFactor=2,
                minNeighbors=5,
            )
            for (x,y,w,h) in face:
                cv2.rectangle(img,(x,y),(x+w,y+h),(250,240,240),1)
                id,configdence = self.recognizer.predict(gray[y:y+h,x:x+w])
                #configdence: độ chính xác
                if(configdence<100):
                    id=name[id]
                    configdence = f"{round(100-configdence)}%"
                else:
                    id = "unknown"
                    configdence = f"{round(100-configdence)}"
                cv2.putText(img,str(id),(x+5,y-5),font,1,(255,255,255),2)
                cv2.putText(img,str(configdence),(x+5,y+h-5),font,1,(25,255,255),1)
            cv2.imshow("tìm khuôn mặt",img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
myface = Recognition_face()
myface.facial_recognition("trainner/trainkhoa.xml")



