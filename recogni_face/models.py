import cv2
import numpy as np
from PIL import Image
import os
import time
PATH = "recogni_face"
PATH_IMAGE = "dataset"
PATH_TRAINER = "trainner"

class Train_models:
    def __init__(self, path_image):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.imagePaths = [os.path.join(path_image, f) for f in os.listdir(path=path_image)]
        self.faceSample = []
        self.IDs = []

    def get_Image_Label(self):
        print("Dữ liệu đang được train!")
        for imagePath in self.imagePaths:
            try:
                PILimage = Image.open(imagePath).convert("L")
                img_array = np.array(PILimage, "uint8")
                id = int(os.path.split(imagePath)[-1].split(".")[0])
                faces = self.detector.detectMultiScale(image=img_array)
                for (x, y, w, h) in faces:
                    self.faceSample.append(img_array[y:y + h, x:x + w])
                    self.IDs.append(id)
            except Exception as e:
                print(f"Error processing {imagePath}: {e}")
        return self.faceSample, self.IDs

    def trainning(self, pathtrain):
        faces, ids = self.get_Image_Label()
        self.recognizer.train(faces, np.array(ids))
        self.recognizer.write(pathtrain)
        print('Dữ liệu đã được train thành công')

class Recognition_face:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    def open_cam_recogni(self,id_cus, bordersize=2, bordercolor=(255, 140, 130)):
        image_cam = cv2.VideoCapture(0)
        if not image_cam.isOpened():
            print("Không thể mở camera!")
            return

        count = 0
        while True:
            ok, frame = image_cam.read()
            if not ok:
                print("Không thể nhận frame từ camera!")
                break

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_locations = self.face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in face_locations:
                cv2.rectangle(frame, (x, y), (x + w, y + h), bordercolor, bordersize)
                if count >= 30:
                    face_human = frame[y + bordersize:y + h - bordersize, x + bordersize:x + w - bordersize]
                    face_human = cv2.resize(face_human, (100, 100))
                    cv2.imwrite(f"{PATH}/{PATH_IMAGE}/{id_cus}/{id_cus}.{str(int(time.time()))}.jpg", face_human)#{PATH_IMAGE}/{id_cus}/{id_cus}
                    count = 0

            cv2.imshow("Face Detection", frame)
            count += 1
            print(f"Frame count: {count}")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        image_cam.release()
        cv2.destroyAllWindows()

    def facial_recognition(self, path_trainner, id_cus,color_RGB=(250, 150, 100), size_rectangle=3):
        if not os.path.exists(path_trainner):
            print(f"Trainner file {path_trainner} không tồn tại!")
            return

        self.recognizer.read(path_trainner)
        font = cv2.FONT_HERSHEY_SIMPLEX
        id = 0
        name = [0,"khoa"]
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            print("Không thể mở camera!")
            return

        while True:
            ret, img = cam.read()
            if not ret:
                print("Không thể nhận frame từ camera!")
                break

            img = cv2.flip(img, 1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=2, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), color_RGB, size_rectangle)
                id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])

                if confidence < 100:
                    id = name[id]
                    confidence = f"{round(confidence)}%"
                else:
                    id = "khong phai khuon mat cua ban"
                    confidence = f"{round(100 - confidence)}%"

                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)

            cv2.imshow("Tìm khuôn mặt", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()


# Khởi tạo mô hình
id_customer = 3
customer_file = f"id{id_customer}"
file_image_customer = f"{PATH}/{PATH_IMAGE}/{id_customer}"
XML_file = f"{PATH}/{PATH_TRAINER}/{customer_file}.xml"
face_input = Recognition_face()
face_input.open_cam_recogni(id_customer)
#convert_to_XML = Train_models(file_image_customer)
#convert_to_XML.trainning(XML_file)
#face_input.facial_recognition(XML_file,id_customer)