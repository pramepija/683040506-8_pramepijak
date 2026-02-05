import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                             QVBoxLayout, QWidget)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFormLayout, QLineEdit, QSpinBox, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PySide6 Demo App")
        self.setGeometry(100, 100, 400, 500)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.reg = RegistrationForm()
        layout.addWidget(self.reg)

        # Add a button to process the data
        get_data_btn = QPushButton("Process Registration")
        get_data_btn.clicked.connect(self.process_registration)
        layout.addWidget(get_data_btn)

    def process_registration(self):
        # Get data directly from the form
        data = self.reg.get_values()

        # Now you can use the data
        print(f"Name: {data['name']}")
        print(f"Email: {data['email']}")
        print(f"Age: {data['age']}")
        print(f"Id: {data['Id']}")

# Inherited from QWidget
class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()

        # Basic form fields
        self.name = QLineEdit()
        self.age = QSpinBox()
        self.id = QLineEdit()
        layout.addRow("Name:", self.name)
        layout.addRow("Age:", self.age)
        layout.addRow("Id:", self.id)
        # Customize field labels
        self.email = QLineEdit()
        layout.addRow("Email:", self.email)
        layout.labelForField(self.email).setStyleSheet("font-weight: bold;")

        # Spacing and margins
        layout.setSpacing(10)  # Space between rows
        layout.setContentsMargins(20, 20, 20, 20)  # left, top, right, bottom

        # Field alignment
        layout.setLabelAlignment(Qt.AlignRight)  # Right-align labels
        layout.setFormAlignment(Qt.AlignLeft)     # Left-align fields

        # Add a widget that spans both columns
        submit = QPushButton("Submit")
        submit.clicked.connect(self.on_submit)
        layout.addRow(submit)

        self.setLayout(layout)

    def on_submit(self):
        # You can add any validation here if needed
        pass

    def get_values(self):
        """Get the current values from the form fields"""
        return {
            'name': self.name.text(),
            'email': self.email.text(),
            'age': self.age.value(),
            'Id' : self.id.text()}


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()