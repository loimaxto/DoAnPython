from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableView, QPushButton,
    QHBoxLayout, QWidget, QVBoxLayout, QAbstractItemView
)
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt


class ButtonWidget(QWidget):
    """Custom widget that contains three buttons in a table cell."""
    def __init__(self, value, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create buttons
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")
        self.btn_view = QPushButton("View")

        # Set button visibility based on the value
        self.btn_edit.setVisible(value in ["edit_delete", "edit_view", "all", "edit"])
        self.btn_delete.setVisible(value in ["edit_delete", "delete_view", "all"])
        self.btn_view.setVisible(value in ["edit_view", "delete_view", "all"])

        # Add buttons to layout
        layout.addWidget(self.btn_edit)
        layout.addWidget(self.btn_delete)
        layout.addWidget(self.btn_view)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        
        super().__init__()

        self.setWindowTitle("QTableView with Always Visible Buttons")
        self.setGeometry(100, 100, 600, 300)

        # Create table view and model
        self.table = QTableView(self)
        self.model = QStandardItemModel(5, 3)  # 5 rows, 3 columns
        self.model.setHorizontalHeaderLabels(["Name", "Description", "Actions"])  # Last column has buttons

        # Populate model
        data = [
            ("Item 1", "Some text", "edit_delete"),
            ("Item 2", "More text", "edit_view"),
            ("Item 3", "Another text", "delete_view"),
            ("Item 4", "Example text", "all"),
            ("Item 5", "Final text", "edit")
        ]
        for row, (name, desc, action) in enumerate(data):
            self.model.setItem(row, 0, QStandardItem(name))
            self.model.setItem(row, 1, QStandardItem(desc))
            self.model.setItem(row, 2, QStandardItem(action))  # Store value for actions

        self.table.setModel(self.model)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # Prevent editing

        # Add custom button widgets to the last column
        for row in range(self.model.rowCount()):
            action_value = self.model.item(row, 2).text()  # Get stored action value
            widget = ButtonWidget(action_value, self.table)
            self.table.setIndexWidget(self.model.index(row, 2), widget)  # Set custom widget

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
