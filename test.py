from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                              QPushButton, QLabel)
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint,Qt



class VerticalPageSlider(QWidget):
    def __init__(self):
        super().__init__()
        self.current_index = 0
        self.pages = []
        self.animation = None
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Tạo các trang
        colors = ["lightblue", "lightgreen", "lightyellow"]
        for i in range(3):
            page = QLabel(f"Page {i+1}")
            page.setAlignment(Qt.AlignCenter)
            page.setStyleSheet(f"background-color: {colors[i]}; font-size: 24px;")
            page.setFixedSize(400, 300)
            layout.addWidget(page)
            self.pages.append(page)
            if i != 0:
                page.hide()
        
        # Tạo nút điều khiển
        button_layout = QHBoxLayout()
        prev_btn = QPushButton("Previous")
        next_btn = QPushButton("Next")
        button_layout.addWidget(prev_btn)
        button_layout.addWidget(next_btn)
        layout.addLayout(button_layout)
        
        # Kết nối tín hiệu
        prev_btn.clicked.connect(self.show_previous_page)
        next_btn.clicked.connect(self.show_next_page)
    
    def show_next_page(self):
        if self.current_index < len(self.pages) - 1:
            self.show_page(self.current_index + 1)
    
    def show_previous_page(self):
        if self.current_index > 0:
            self.show_page(self.current_index - 1)
    
    def show_page(self, new_index):
        if new_index == self.current_index or (
            self.animation and self.animation.state() == QPropertyAnimation.Running
        ):
            return
        
        current_page = self.pages[self.current_index]
        next_page = self.pages[new_index]
        
        next_page.show()
        next_page.raise_()
        
        direction = 1 if new_index > self.current_index else -1
        
        # Thiết lập vị trí ban đầu
        next_page.move(0, direction * self.height())
        
        # Tạo animation
        self.animation = QPropertyAnimation(next_page, b"pos")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.setStartValue(QPoint(0, direction * self.height()))
        self.animation.setEndValue(QPoint(0, 0))
        
        current_animation = QPropertyAnimation(current_page, b"pos")
        current_animation.setDuration(300)
        current_animation.setEasingCurve(QEasingCurve.OutQuad)
        current_animation.setStartValue(QPoint(0, 0))
        current_animation.setEndValue(QPoint(0, -direction * self.height()))
        
        def on_animation_finished():
            current_page.hide()
            current_page.move(0, 0)
            self.current_index = new_index
            self.animation = None
        
        self.animation.finished.connect(on_animation_finished)
        
        self.animation.start()
        current_animation.start(QPropertyAnimation.DeleteWhenStopped)


if __name__ == "__main__":
    app = QApplication([])
    window = VerticalPageSlider()
    window.resize(400, 300)
    window.show()
    app.exec()