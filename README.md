# DoAnPython

### Initialize to run project:
-python -m venv env

-windown: env\Scripts\activate // vao terminal python cua project
 || git bash(linux): source env/bin/activate

-pip freeze > requirements.txt // liet ke package va version co trong project and update
-pip install -r requirements.txt // tai package duoc liet ke
-pip install opencv-python // install cv2 library turn on and off cam
-pip install opencv-contrib-python// install library that adds some features to cv2
-pip install numpy
-pip install torch torchvision torchaudio matplotlib opencv-python
-pip install scikit-learn

### chuyen file .ui thanh .py
-pyuic6 C:\Code\DoAnPython\view\khach_hang\kh_ui.ui -o kh_ui.py 

### Qui uoc dat ten:

folder
-view  : LoginV
-model: LoginM
-dto: user_dto

### instruction

// dùng để import từ 2 file từ 2 directory khác nhau
import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) 
sys.path.append(project_path)
print(project_path) #vi tri tu file hien tai toi root !! phai toi root moi dung duoc

my_project/
├── main.py        # Main entry point of the application
├── database/      # Database-related files
│   ├── __init__.py
│   └── database.py  # Database connection and utility functions
├── dto/        # Data Transfer Objects (DTOs)
│   ├── __init__.py
│   └── dto.py
├── data_access/   # Data Access Objects (DAOs)
│   ├── __init__.py
│   └── customer_dao.py
│   └── product_dao.py
│   └── order_dao.py
├── utils/        # Utility modules
│   ├── __init__.py
│   └── helpers.py
└── requirements.txt # List of project dependencies

### Giao dien chung
muc view/css.py chứa thuộc tính css dùng chung cho tất cả trang chức năng
tên của tablewidget trong trang là dis_pla có thể copy hàm rồi sửa lại để sử dụng, chỉ lưu trong file css.py