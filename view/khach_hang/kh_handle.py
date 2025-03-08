import sys
import random
from PyQt6 import QtWidgets, QtCore, QtGui
from kh_ui import Ui_CustomerManagement  # Assuming you saved the UI as kh_ui.py

class CustomerManagementWindow(QtWidgets.QWidget, Ui_CustomerManagement):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.model = QtGui.QStandardItemModel(0, 4)  # rows, columns
        self.model.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Image"])
        self.customerTableView.setModel(self.model)
        # Resize columns
        self.customerTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch) 
       
        # Load fake data
        self.load_fake_data()

        # Connect buttons to functions
        self.addButton.clicked.connect(self.add_customer)
        self.updateButton.clicked.connect(self.update_customer)
        self.deleteButton.clicked.connect(self.delete_customer)
        self.clearButton.clicked.connect(self.clear_fields)
        self.imageButton.clicked.connect(self.select_image)
        self.searchButton.clicked.connect(self.search_customers)

    def load_fake_data(self, search_term=None):
        fake_data = self.generate_fake_data()

        self.model.setRowCount(0)
        for row in fake_data:
            if search_term:
                if search_term.lower() not in row[1].lower() and search_term not in row[2]:
                    continue
            items = []
            for item in row:
                item_obj = QtGui.QStandardItem(str(item))
                item_obj.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter) #Center the text.
                items.append(item_obj)
            self.model.appendRow(items)
            
    def generate_fake_data(self, num_rows=20):
        fake_data = []
        for i in range(num_rows):
            fake_id = i + 1
            fake_name = f"Customer {i+1}"
            fake_phone = f"123-456-{random.randint(1000, 9999)}"
            fake_image = "" #leave empty for now, or add fake paths if you have them.
            fake_data.append((fake_id, fake_name, fake_phone, fake_image))
        return fake_data

    def add_customer(self):
        # Add fake customer data
        new_id = self.model.rowCount() + 1
        new_name = self.nameLineEdit.text() or f"Customer {new_id}"
        new_phone = self.phoneLineEdit.text() or f"123-456-{random.randint(1000, 9999)}"
        new_image = self.imagePathLabel.text()

        self.model.appendRow([QtGui.QStandardItem(str(new_id)), QtGui.QStandardItem(new_name), QtGui.QStandardItem(new_phone), QtGui.QStandardItem(new_image)])
        self.clear_fields()
        self.load_fake_data()

    def update_customer(self):
        selected_indexes = self.customerTableView.selectionModel().selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            self.model.setItem(row, 1, QtGui.QStandardItem(self.nameLineEdit.text()))
            self.model.setItem(row, 2, QtGui.QStandardItem(self.phoneLineEdit.text()))
            self.model.setItem(row, 3, QtGui.QStandardItem(self.imagePathLabel.text()))
            self.clear_fields()
            self.load_fake_data()

    def delete_customer(self):
        selected_indexes = self.customerTableView.selectionModel().selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            self.model.removeRow(row)
            self.clear_fields()
            self.load_fake_data()

    def clear_fields(self):
        self.idLineEdit.clear()
        self.nameLineEdit.clear()
        self.phoneLineEdit.clear()
        self.imagePathLabel.setText("Image Path")

    def select_image(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.imagePathLabel.setText(file_path)

    def search_customers(self):
        search_term = self.searchLineEdit.text()
        self.load_fake_data(search_term)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CustomerManagementWindow()
    window.show()
    sys.exit(app.exec())