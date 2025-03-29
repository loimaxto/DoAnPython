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
    QSpacerItem,
)
from PyQt6.QtCore import Qt

class ItemWidget(QWidget):
    def __init__(self, name, price, quantity=1):
        super().__init__()

        self.name = name
        self.price = price
        self.quantity = quantity

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)

        name_price_layout = QHBoxLayout()
        left_layout.addLayout(name_price_layout)

        self.name_label = QLabel(self.name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        name_price_layout.addWidget(self.name_label)

        self.price_label = QLabel(f"Price: ${self.price:.2f}")
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        name_price_layout.addWidget(self.price_label)

        quantity_layout = QHBoxLayout()
        left_layout.addLayout(quantity_layout)

        self.decrease_button = QPushButton("-")
        self.decrease_button.clicked.connect(self.decrease_quantity)
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
        quantity_layout.addWidget(self.increase_button)
        self.increase_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Remove the spacer that was stretching the quantity_layout.
        # Instead, we will wrap the quantity_layout into a widget with fixed width.

        quantity_widget = QWidget()
        quantity_widget.setLayout(quantity_layout)
        quantity_widget.setFixedWidth(300) # set fixed width of the widget.
        left_layout.addWidget(quantity_widget)

        self.sum_label = QLabel(f"Sum: ${self.calculate_sum():.2f}")
        self.sum_label.setAlignment(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        left_layout.addWidget(self.sum_label)
    def increase_quantity(self):
        self.quantity += 1
        self.quantity_input.setText(str(self.quantity))
        self.update_sum_label()

    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.quantity_input.setText(str(self.quantity))
            self.update_sum_label()

    def quantity_changed(self, text):
        try:
            self.quantity = int(text)
            if self.quantity < 1:
                self.quantity = 1
                self.quantity_input.setText("1")
            self.update_sum_label()
        except ValueError:
            self.quantity_input.setText(str(self.quantity))
            self.update_sum_label()

    def calculate_sum(self):
        return self.price * self.quantity

    def update_sum_label(self):
        self.sum_label.setText(f"Sum: ${self.calculate_sum():.2f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)

    item1 = ItemWidget("Product A", 19.99)
    item2 = ItemWidget("Product B", 29.95, 3)  # Initial quantity of 3

    layout.addWidget(item1)
    layout.addWidget(item2)

    window.show()
    sys.exit(app.exec())