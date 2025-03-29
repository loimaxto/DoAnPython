from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QTableView,
    QHBoxLayout,
    QPushButton,
    QStyledItemDelegate,
    QVBoxLayout
)
from PyQt6.QtCore import Qt, QModelIndex, pyqtSignal
from PyQt6.QtGui import QColor
import sys

class CustomerTableModel(QAbstractTableModel):
    """
    A table model that displays customer data with a status column.
    """

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.header = ["Name", "Age", "Status"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.header)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return self.data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.header[section]
        return None

class CustomerCellDelegate(QStyledItemDelegate):
    """
    A delegate that displays buttons in the status column.
    """

    button_clicked = pyqtSignal(int, str)  # Signal to emit row and button name

    def createEditor(self, parent, option, index):
        if index.column() == 2:  # Status column
            return CustomerCellWidget(index.data(), parent)
        return super().createEditor(parent, option, index)

    def setModelData(self, editor, model, index):
        if index.column() == 2:
            editor.button_clicked.connect(lambda button_name: self.button_clicked.emit(index.row(), button_name))

    def updateEditorGeometry(self, editor, option, index):
        if index.column() == 2:
            editor.setGeometry(option.rect)
        else:
            super().updateEditorGeometry(editor, option, index)

class CustomerCellWidget(QWidget):
    """
    A widget that displays three buttons (A, B, C) based on an input value.
    """

    button_clicked = pyqtSignal(str)  # Signal to emit which button was clicked

    def __init__(self, input_value, parent=None):
        super().__init__(parent)

        self.input_value = input_value

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.button_a = QPushButton("A")
        self.button_b = QPushButton("B")
        self.button_c = QPushButton("C")

        self.button_a.clicked.connect(lambda: self.button_clicked.emit("A"))
        self.button_b.clicked.connect(lambda: self.button_clicked.emit("B"))
        self.button_c.clicked.connect(lambda: self.button_clicked.emit("C"))

        if self.input_value == 1:
            layout.addWidget(self.button_a)
            layout.addWidget(self.button_b)
        elif self.input_value == 0:
            layout.addWidget(self.button_c)

def handle_button_click(row, button_name):
    print(f"Button {button_name} clicked in row {row}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)

    data = [
        ["Alice", 25, 1],
        ["Bob", 30, 0],
        ["Charlie", 35, 1],
    ]

    model = CustomerTableModel(data)
    table_view = QTableView()
    table_view.setModel(model)

    delegate = CustomerCellDelegate()
    delegate.button_clicked.connect(handle_button_click)
    table_view.setItemDelegateForColumn(2, delegate)  # Apply delegate to the status column

    layout.addWidget(table_view)
    window.show()
    sys.exit(app.exec())