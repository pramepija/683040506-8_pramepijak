import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel,
                             QVBoxLayout, QWidget, QHBoxLayout,
                             QGridLayout, QFormLayout, QLineEdit,
                             QSpinBox, QPushButton, QSizePolicy)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont

# Configure logging for error tracking
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('calculator_errors.log'),
        logging.StreamHandler()
    ]
)

class CalculatorLayout(QWidget):
    def __init__(self):
        try:
            super().__init__()
            main_layout = QVBoxLayout()
            
            header_layout = QHBoxLayout()
            
            menu_btn = QPushButton("☰")
            menu_btn.setMaximumWidth(50)
            menu_btn.setFont(QFont("Arial", 12))
            header_layout.addWidget(menu_btn)
            
            standard_label = QLabel("Standard")
            standard_label.setFont(QFont("Arial", 16, QFont.Bold))
            header_layout.addWidget(standard_label)

            header_layout.addStretch()
            
            history_btn = QPushButton("🕐")
            history_btn.setMaximumWidth(50)
            history_btn.setFont(QFont("Arial", 16))
            header_layout.addWidget(history_btn)
            
            main_layout.addLayout(header_layout)
            
            self.display = QLineEdit()
            self.display.setReadOnly(True)
            self.display.setAlignment(Qt.AlignRight)
            self.display.setText("0")
            self.display.setMinimumHeight(80)
            self.display.setFont(QFont("Arial", 32))
            main_layout.addWidget(self.display)
            
            layout = QGridLayout()
            layout.setSpacing(5)
            layout.setContentsMargins(5, 5, 5, 5)
            
            def create_button(text):
                try:
                    btn = QPushButton(text)
                    btn.setMinimumSize(65, 55)
                    btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    btn.setFont(QFont("Arial", 12))
                    return btn
                except Exception as e:
                    logging.error(f"Error creating button '{text}': {str(e)}")
                    raise


            layout.addWidget(create_button("%"), 1, 0)
            layout.addWidget(create_button("CE"), 1, 1)
            layout.addWidget(create_button("C"), 1, 2)
            layout.addWidget(create_button("⌫"), 1, 3)

            layout.addWidget(create_button("¹/ₓ"), 2, 0)
            layout.addWidget(create_button("x²"), 2, 1)
            layout.addWidget(create_button("²√x"), 2, 2)
            layout.addWidget(create_button("÷"), 2, 3)

            layout.addWidget(create_button("7"), 3, 0)
            layout.addWidget(create_button("8"), 3, 1)
            layout.addWidget(create_button("9"), 3, 2)
            layout.addWidget(create_button("×"), 3, 3)

            layout.addWidget(create_button("4"), 4, 0)
            layout.addWidget(create_button("5"), 4, 1)
            layout.addWidget(create_button("6"), 4, 2)
            layout.addWidget(create_button("−"), 4, 3)

            layout.addWidget(create_button("1"), 5, 0)
            layout.addWidget(create_button("2"), 5, 1)
            layout.addWidget(create_button("3"), 5, 2)
            layout.addWidget(create_button("+"), 5, 3)

            layout.addWidget(create_button("+/-"), 6, 0)
            layout.addWidget(create_button("0"), 6, 1)
            layout.addWidget(create_button("."), 6, 2)
            
            btn_equal = create_button("=")
            btn_equal.setStyleSheet("background-color: #0078D4; color: white;")
            layout.addWidget(btn_equal, 6, 3)

            main_layout.addLayout(layout)
            self.setLayout(main_layout)
            logging.info("CalculatorLayout initialized successfully")
            
        except Exception as e:
            logging.error(f"Error initializing CalculatorLayout: {str(e)}")
            raise

class MainWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle("Calculator")
            self.setCentralWidget(CalculatorLayout())
            self.resize(320, 470)
            logging.info("MainWindow initialized successfully")
        except Exception as e:
            logging.error(f"Error initializing MainWindow: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        logging.info("QApplication initialized successfully")
        
        window = MainWindow()
        window.show()
        
        logging.info("Application started successfully")
        sys.exit(app.exec())
        
    except ImportError as e:
        logging.critical(f"Import error: Missing required module - {str(e)}")
        print(f"ERROR: Missing required module: {str(e)}")
        sys.exit(1)
        
    except Exception as e:
        logging.critical(f"Critical error during application startup: {str(e)}")
        print(f"CRITICAL ERROR: {str(e)}")
        sys.exit(1)