import sys
import csv
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QFileDialog, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt


class StudentManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Score Manager")
        self.resize(700, 500)
        self.current_path = None

        # ── Central widget & layout ──────────────────
        widget = QWidget()
        main_layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        # ── Toolbar: Load / Save buttons ─────────────
        toolbar = QHBoxLayout()
        self.btn_load = QPushButton("Load CSV")
        self.btn_save = QPushButton("Save CSV")
        self.lbl_file = QLabel("No file loaded")
        self.btn_save.setEnabled(False)

        toolbar.addWidget(self.btn_load)
        toolbar.addWidget(self.btn_save)
        toolbar.addWidget(self.lbl_file)
        toolbar.addStretch()

        # ── Table ─────────────────────────────────────
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Score", "Grade"])
        self.table.horizontalHeader().setStretchLastSection(True)

        # ── Add new student row ───────────────────────
        add_layout = QHBoxLayout()
        self.input_name  = QLineEdit()
        self.input_score = QLineEdit()
        self.input_grade = QLineEdit()
        self.input_name.setPlaceholderText("Name")
        self.input_score.setPlaceholderText("Score")
        self.input_grade.setPlaceholderText("Grade")
        self.btn_add = QPushButton("Add Row")

        add_layout.addWidget(self.input_name)
        add_layout.addWidget(self.input_score)
        add_layout.addWidget(self.input_grade)
        add_layout.addWidget(self.btn_add)

        # ── Status bar ────────────────────────────────
        self.statusBar().showMessage("Ready")

        # ── Assemble layout ───────────────────────────
        main_layout.addLayout(toolbar)
        main_layout.addWidget(self.table)
        main_layout.addLayout(add_layout)

        # ── Connect signals ───────────────────────────
        self.btn_load.clicked.connect(self.load_file)
        self.btn_save.clicked.connect(self.save_file)
        self.btn_add.clicked.connect(self.add_row)

    # ──────────────────────────────────────────────────
    # TODO 1: Open a file dialog, read the CSV,
    #         and populate self.table with the data
    # ──────────────────────────────────────────────────
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self,
                                                 "Open CSV File",
                                                 "",
                                                 "CSV Files (*.csv);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    header = next(reader)  # Read header
                    self.table.setColumnCount(len(header))
                    self.table.setHorizontalHeaderLabels(header)

                    self.table.setRowCount(0) # Clear existing data
                    for row_idx, row_data in enumerate(reader):
                        self.table.insertRow(row_idx)
                        for col_idx, item in enumerate(row_data):
                            self.table.setItem(row_idx, col_idx, QTableWidgetItem(item))

                self.current_path = file_path
                self.lbl_file.setText(self.current_path.split('/')[-1])
                self.btn_save.setEnabled(True)
                self.statusBar().showMessage(f"Loaded data from {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not load file: {e}")

    # ──────────────────────────────────────────────────
    # TODO 2: Read all rows from self.table,
    #         and write them to a CSV file
    # ──────────────────────────────────────────────────
    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self,
                                                 "Save CSV File",
                                                 "",
                                                 "CSV Files (*.csv);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # Write header
                    header = [self.table.horizontalHeaderItem(col).text() for col in range(self.table.columnCount())]
                    writer.writerow(header)

                    # Write data rows
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(self.table.columnCount()):
                            item = self.table.item(row, col)
                            row_data.append(item.text() if item else '')
                        writer.writerow(row_data)
                self.current_path = file_path
                self.lbl_file.setText(self.current_path.split('/')[-1])
                self.btn_save.setEnabled(True)
                self.statusBar().showMessage(f"Saved data to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {e}")

    # ──────────────────────────────────────────────────
    # Read the three input fields,
    #      and add a new row to self.table
    # ──────────────────────────────────────────────────
    def add_row(self):
        name  = self.input_name.text().strip()
        score = self.input_score.text().strip()
        grade = self.input_grade.text().strip()

        if not name or not score or not grade:
            QMessageBox.warning(self, "Missing Data", "Please fill in all fields")
            return

        r = self.table.rowCount()
        self.table.insertRow(r)
        self.table.setItem(r, 0, QTableWidgetItem(name))
        self.table.setItem(r, 1, QTableWidgetItem(score))
        self.table.setItem(r, 2, QTableWidgetItem(grade))

        self.input_name.clear()
        self.input_score.clear()
        self.input_grade.clear()

        self.statusBar().showMessage(f"Added {name}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = StudentManager()
    win.show()
    sys.exit(app.exec())