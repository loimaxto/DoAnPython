

class stylecss:
    def __init__(self,main=None):
        self.main = main
    def background(self,color="white",background="black"):
        self.main.setStyleSheet(f"""
        form'{''}
""")
    def set_default(self):
        self.main.setStyleSheet("""
            /* Style chung cho toàn bộ form */
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
              color: #c1cacc;
            }
            
            /* Background chính */
            QWidget#Form {
                background-color: #3a3a3a;
                color:#a8d2d8;
            }
            
            /* Style cho các QLabel */
            QLabel {
                font-size: 11pt;
                color: white;
            }
            
            /* Style cho các QPushButton */
            QPushButton {
                background-color: #4a6fa5;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
                min-width: 80px;
            }
            
            QPushButton:hover {
                background-color: #3a5a8f;
            }
            
            QPushButton:pressed {
                background-color: #2a4a7f;
            }
            
            /* Style cho QLineEdit */
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px;
                font-size: 11pt;
            }
            
            QLineEdit:focus {
                border: 1px solid #4a6fa5;
            }
            
            /* Style cho QComboBox */
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px;
                font-size: 11pt;
            }
            
            QComboBox::drop-down {
                width: 20px;
                border-left: 1px solid #ccc;
            }
            
            /* Style cho QTableWidget */
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: #232e30;
                alternate-background-color: #f9f9f9;
                gridline-color: #eee;
                
            }
            
            QTableWidget::item {
                padding: 6px;
            }
            
            QHeaderView::section {
                background-color: #4a6fa5;
                color: white;
                padding: 6px;
                border: none;
            }
            QListView{
                                max-height:100px;}
            
            /* Style cho QDateTimeEdit */
            QDateTimeEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px;
            }
            
            /* Style cho QPlainTextEdit */
            QPlainTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px;
                font-size: 11pt;
            }
        """)