from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
import sys

class InnerWidget(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)  # Horizontal layout for the inner widget
        label = QLabel(text)
        button = QPushButton("Click Me")

        layout.addWidget(label)
        layout.addWidget(button)

        self.setLayout(layout)

class OuterWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widget within Widget")

        outer_layout = QVBoxLayout(self)  # Vertical layout for the outer widget

        inner_widget1 = InnerWidget("Widget 1")
        inner_widget2 = InnerWidget("Widget 2")
        label_outer = QLabel("This is the outer widget")

        outer_layout.addWidget(label_outer)
        outer_layout.addWidget(inner_widget1)
        outer_layout.addWidget(inner_widget2)

        self.setLayout(outer_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OuterWidget()
    window.show()
    sys.exit(app.exec())