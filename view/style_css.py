

class stylecss:
    def __init__(self,main=None):
        self.main = main
    def background(self,color="white",background="black"):
        self.main.setStyleSheet(f"""
        form'{''}
""")
    def set_default(self):
        self.main.setStyleSheet("""
        `QWidget {
            background-color: #2e2e2e;
            color: #f1f1f1;
            font-family: 'Segoe UI';
            font-size: 12pt;
        }

        QPushButton {
            background-color: #4CAF50;
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }

        QLineEdit {
            background-color: #3e3e3e;
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 5px;
            color: white;
        }

        QTableWidget {
            background-color: #222;
            alternate-background-color: #333;
            border: none;
            height:500px;
        }

        QHeaderView::section {
            background-color: #555;
            color: white;
            padding: 5px;
            border: none;
        }

        QLabel {
            font-weight: bold;
        }

        QComboBox {
            background-color: #3e3e3e;
            border-radius: 5px;
            padding: 4px;
            color: white;
        }

        QDateTimeEdit {
            background-color: #3e3e3e;
            color: white;
            border: 1px solid #ccc;
            border-radius: 5px;
            padding: 4px;
        }
    """)
    def set_datphong2(self):
        # Main form style
        self.main.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                font-family: 'Segoe UI';
            }
            
            /* LineEdit styles */
            QLineEdit {
                background-color: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px;
                color: #ffffff;
            }
            
            QLineEdit:focus {
                border: 1px solid #45a049;
            }
            
            /* PushButton styles */
            QPushButton {
                background-color: #4f4a4f;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #45a049;
            }
            
            QPushButton:pressed {
                background-color: #3a8c3d;
            }
            
            /* Table styles */
            QTableWidget {
                background-color: #3d3d3d;
                border: 1px solid #4d4d4d;
                gridline-color: #4d4d4d;
                color: #ffffff;
            }
            
            QTableWidget QHeaderView::section {
                background-color: #4f4a4f;
                color: white;
                padding: 5px;
                border: none;
            }
            
            QTableWidget::item {
                padding: 5px;
            }
            
            QTableWidget::item:selected {
                background-color: #45a049;
                color: white;
            }
            
            /* ComboBox styles */
            QComboBox {
                background-color: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px;
                color: #ffffff;
            }
            
            QComboBox QAbstractItemView {
                background-color: #3d3d3d;
                color: #ffffff;
                selection-background-color: #45a049;
            }
            
            /* DateTimeEdit styles */
            QDateTimeEdit {
                background-color: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px;
                color: #ffffff;
            }
            
            /* PlainTextEdit styles */
            QPlainTextEdit {
                background-color: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px;
                color: #ffffff;
            }
            
            /* Label styles */
            QLabel {
                color: #e0e0e0;
            }
            
            /* Special labels with border */
            QLabel[objectName="show_khachhang"],
            QLabel[objectName="show_phong"] {
                border: 5px solid #45a049;
                color: white;
                background: #394039;
                padding: 3px;
            }
        """)

        # Additional specific widget styles
        self.main.btn_submit.setStyleSheet("""
            QPushButton {
                background-color: #45a049;
                color: white;
                font-weight: bold;
                padding: 10px;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #3a8c3d;
            }
        """)

        self.main.note.setStyleSheet("""
            QPlainTextEdit {
                background-color: #3d3d3d;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px;
                color: #ffffff;
            }
        """)

        self.main.tienuoctinh.setStyleSheet("""
            QLabel {
                font-size: 14pt;
                color: #45a049;
                font-weight: bold;
            }
        """)

        self.main.tienlucdat.setStyleSheet("""
            QLabel {
                font-size: 14pt;
                color: #45a049;
                font-weight: bold;
            }
        """)

        # ... (rest of your existing setup code)`