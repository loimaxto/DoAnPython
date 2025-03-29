import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QSizePolicy,
)
from PyQt6.QtCore import Qt

class ItemWidget(QWidget):
    def __init__(self, name, quantity=1):
        super().__init__()

        self.name = name
        self.quantity = quantity

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        self.name_label = QLabel(self.name)
        self.name_label.setFixedWidth(150)
        main_layout.addWidget(self.name_label)

        quantity_layout = QHBoxLayout()
        main_layout.addLayout(quantity_layout)

        self.decrease_button = QPushButton("-")
        self.decrease_button.clicked.connect(self.decrease_quantity)
        self.decrease_button.setFixedWidth(50)
        quantity_layout.addWidget(self.decrease_button)
        self.decrease_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.quantity_input = QLineEdit(str(self.quantity))
        self.quantity_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quantity_input.setFixedWidth(50)
        quantity_layout.addWidget(self.quantity_input)
        self.quantity_input.textChanged.connect(self.quantity_changed)
        self.quantity_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.increase_button = QPushButton("+")
        self.increase_button.clicked.connect(self.increase_quantity)
        self.increase_button.setFixedWidth(50)
        quantity_layout.addWidget(self.increase_button)
        self.increase_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def increase_quantity(self):
        self.quantity += 1
        self.quantity_input.setText(str(self.quantity))

    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.quantity_input.setText(str(self.quantity))

    def quantity_changed(self, text):
        try:
            self.quantity = int(text)
            if self.quantity < 1:
                self.quantity = 1
                self.quantity_input.setText("1")
        except ValueError:
            self.quantity_input.setText(str(self.quantity))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)

    item1 = ItemWidget("Product A", 2)
    item2 = ItemWidget("Product B", 5)

    layout.addWidget(item1)
    layout.addWidget(item2)

    window.show()
    sys.exit(app.exec())