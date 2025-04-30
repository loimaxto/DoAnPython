def css(page):
    page.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Arial, sans-serif;
            }
            QLabel {
                color: #333;
            }
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
                background-color: #fff;
            }
            QPushButton {
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QTableWidget {
                border: 1px solid #ccc;
                background-color: #fff;
            }
            QHeaderView::section {
                background-color: #007bff;
                color: #fff;
                padding: 5px;
                border: none;
            }
        """)
    page.dis_pla.setStyleSheet("""
        QTableWidget {
            gridline-color: #ccc;
        }
        QTableWidget::item {
            padding: 5px;
        }
    """)
    page.dis_pla.setStyleSheet("""
        QTableWidget::item:selected {
            background-color: #d9edf7;
            color: #333;
        }
    """)