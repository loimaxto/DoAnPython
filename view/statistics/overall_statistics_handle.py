import sys
import os
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(project_path)
print(project_path)
import random
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import (
    
    QMessageBox,
)
from view.statistics.overall_statistics_ui import Ui_OverallStatistic # Assuming you saved the UI as kh_ui.py




class OverallStatisticsWindow(QtWidgets.QWidget, Ui_OverallStatistic):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        

        # Load fake data
        

       
        # Connect buttons to functions
        
        
          
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = OverallStatisticsWindow()
    window.show()
    sys.exit(app.exec())

