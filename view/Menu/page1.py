import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication
PAGE1_UI = "page1.ui"
class Page1(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/Menu/page1.ui", self)
        # Initialize page-specific logic here
        self.label = self.findChild(QtWidgets.QLabel, "labelPage1") # Example: Find a QLabel
        self.button = self.findChild(QtWidgets.QPushButton, "buttonPage1") # Example: Find a QPushButton
        if self.button: # Check if the button exists (important in case of UI changes)
            self.button.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):
        # Example action when the button is clicked
        if self.label:
            self.label.setText("Button on Page 1 clicked!")

