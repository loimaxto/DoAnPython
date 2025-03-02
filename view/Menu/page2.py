import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QWidget

PAGE2_UI = "page2.ui"

class Page2(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("view/Menu/page2.ui", self)
        # Initialize page-specific logic here
        self.label = self.findChild(QtWidgets.QLabel, "labelPage2") # Example: Find a QLabel
        self.lineEdit = self.findChild(QtWidgets.QLineEdit, "lineEditPage2") # Example: Find a QLineEdit

        if self.lineEdit:
            self.lineEdit.textChanged.connect(self.on_line_edit_changed)

    def on_line_edit_changed(self, text):
        # Example action when the text in the line edit changes
        if self.label:
            self.label.setText(f"Text in LineEdit on Page 2: {text}")

# --- Main application ---

