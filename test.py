from recogni_face.open import Train_Models
if __name__ == "__main__":
    id_customer = 3
    train_model = Train_Models()
    train_model.set_idcustomer(id_customer)
    train_model.train()
    train_model.save(f"recogni_face/trainner/face_{id_customer}.pth")
    
    test_image_path = "recogni_face/dataset/0/41.2.jpg"
    
    
    class_name, confidence = train_model.predict(test_image_path)
    if class_name is not None:
        print(f"\nKết quả dự đoán: {class_name} (Độ tin cậy: {confidence*100:.2f}%)")
