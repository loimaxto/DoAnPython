
class train_AI:
    def __init__(self,filepath):
        self.Xtrain = []
        self.Ytrain = []
        for whatever in os.listdir(filepath):
            list_filename_path=[]
            whatever_path = os.path.join(filepath,whatever)
            for filename in os.listdir(whatever_path):
                filename_path = os.path.join(whatever_path,filename)
                print(filename_path)
                img = np.array(Image.open(filename_path))
                list_filename_path.append(img)
            self.Xtrain.extend(list_filename_path)

model_face_recog = train_AI("dataset")
