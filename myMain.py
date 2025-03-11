import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QWidget, QStackedWidget, QApplication
from view.Menu.page1 import Page1
from view.Menu.page2 import Page2
from view.ql_dichvu import ql_dichvu_handle

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        
        super().__init__()
        uic.loadUi("view/Menu/dashboard.ui", self)  # Load the main window UI

        self.stacked_widget = self.findChild(QStackedWidget, "stackedWidget") # Find your QStackedWidget

        # Create instances of your page widgets
        self.page1 = Page1()
        self.page2 = Page2()
        self.ql_dichvu = ql_dichvu_handle()

        # Add more page instances

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.ql_dichvu)

        self.homeBtn = self.findChild(QtWidgets.QPushButton, "datPhongBtn")
        if self.homeBtn:
            self.homeBtn.clicked.connect(lambda: self.switch_page(0))

        self.roomBtn = self.findChild(QtWidgets.QPushButton, "dichVuBtn")
        if self.roomBtn:
            self.roomBtn.clicked.connect(lambda: self.switch_page(2))
        self.show()  # Show the main window

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()  # Create the main window
    sys.exit(app.exec())