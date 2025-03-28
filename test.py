from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Button Example")
        self.setGeometry(100, 100, 300, 200)
        
        # Tạo button
        self.button = QPushButton("Click Me!", self)
        self.button.setGeometry(100, 50, 100, 40)
        
        # Tạo label để hiển thị
        self.label = QLabel("", self)
        self.label.setGeometry(50, 100, 200, 30)
        
        # Kết nối sự kiện
        self.button.clicked.connect(self.update_label)

    def update_label(self):
        self.label.setText("Nút đã được bấm!")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()