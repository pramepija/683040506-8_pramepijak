"""
Pramepijak ueasri
683040506-8

"""

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow,
                             QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QWidget, QLabel, QLineEdit)
from PySide6.QtWidgets import QPushButton, QComboBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

kg = "kilograms"
lb = "pounds"
cm = "centimeters"
m = "meters"
ft = "feet"
adult = "Adults 20+"
child = "Children and Teenagers (5-19)"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("P1: BMI Calculator")
        self.setGeometry(100, 100, 400, 520)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header label
        header = QLabel("Adult and Child BMI Calculator")
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(45)
        header.setStyleSheet(
            "background-color: #8B1A1A;"
            "color: white;"
            "font-size: 16px;"
            "font-weight: bold;"
        )
        main_layout.addWidget(header)

        # Create an input section object  (return QWidget)
        input_section = InputSection()

        # Create an output section object (return QWidget)
        output_section = OutputSection()

        # Connect signals from clicking submit and clear buttons
        input_section.btn_submit.clicked.connect(
            lambda: input_section.submit_reg(output_section)
        )
        input_section.btn_clear.clicked.connect(
            lambda: input_section.clear_form(output_section)
        )

        main_layout.addWidget(input_section)
        main_layout.addWidget(output_section, stretch=1)


# ─────────────────────────────────────────────────────────────────────────────

class OutputSection(QWidget):
    def __init__(self):
        super().__init__()

        # Outer layout holds a single result_container widget (for background colour)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        result_container = QWidget()
        result_container.setStyleSheet("background-color: #FAF0E6;")   # Linen colour
        self.layout_output = QVBoxLayout(result_container)
        self.layout_output.setContentsMargins(20, 20, 20, 20)
        self.layout_output.setSpacing(6)

        # "Your BMI" label
        your_bmi_label = QLabel("Your BMI")
        your_bmi_label.setAlignment(Qt.AlignCenter)
        your_bmi_label.setStyleSheet("font-size: 14px; color: #333;")
        self.layout_output.addWidget(your_bmi_label)

        # BMI numeric value
        self.bmi_text = QLabel("0.00")
        self.bmi_text.setAlignment(Qt.AlignCenter)
        self.bmi_text.setStyleSheet(
            "font-size: 38px; font-weight: bold; color: #4169E1;"
        )
        self.layout_output.addWidget(self.bmi_text)

        # Adult BMI table (hidden initially)
        self.adult_table = self.show_adult_table()
        self.layout_output.addWidget(self.adult_table)
        self.adult_table.hide()

        # Child links (hidden initially)
        self.child_table = self.show_child_link()
        self.layout_output.addWidget(self.child_table)
        self.child_table.hide()

        self.layout_output.addStretch()
        outer.addWidget(result_container)

    # ── Adult BMI reference table ────────────────────────────────────
    def show_adult_table(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        table_layout = QGridLayout(container)
        table_layout.setContentsMargins(30, 10, 30, 5)
        table_layout.setHorizontalSpacing(40)
        table_layout.setVerticalSpacing(4)

        bold_style = "font-size: 13px; font-weight: bold; color: #222;"
        cell_style = "font-size: 13px; color: #444;"

        # Headers
        lbl_bmi = QLabel("BMI")
        lbl_bmi.setFont(QFont("Arial", 10, QFont.Bold))
        lbl_bmi.setStyleSheet(bold_style)
        table_layout.addWidget(lbl_bmi, 0, 0, Qt.AlignCenter)

        lbl_cond = QLabel("Condition")
        lbl_cond.setFont(QFont("Arial", 10, QFont.Bold))
        lbl_cond.setStyleSheet(bold_style)
        table_layout.addWidget(lbl_cond, 0, 1)

        # Data rows
        rows = [
            ("< 18.5",      "Thin"),
            ("18.5 - 25.0", "Normal"),
            ("25.1 - 30.0", "Overweight"),
            ("> 30.0",      "Obese"),
        ]
        for i, (bmi_range, condition) in enumerate(rows, start=1):
            r = QLabel(bmi_range)
            r.setStyleSheet(cell_style)
            table_layout.addWidget(r, i, 0, Qt.AlignCenter)

            c = QLabel(condition)
            c.setStyleSheet(cell_style)
            table_layout.addWidget(c, i, 1)

        return container

    # ── Child / teenager links ───────────────────────────────────────
    def show_child_link(self):
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        child_layout = QVBoxLayout(container)
        child_layout.setContentsMargins(10, 10, 10, 5)
        child_layout.setSpacing(8)

        note = QLabel(
            "For child's BMI interpretation, please click one of the following links."
        )
        note.setWordWrap(True)
        note.setAlignment(Qt.AlignCenter)
        note.setStyleSheet("font-size: 12px; color: #555;")
        child_layout.addWidget(note)

        link_layout = QHBoxLayout()
        link_layout.setAlignment(Qt.AlignCenter)
        link_layout.setSpacing(20)

        boy_link = QLabel(
            '<a href="https://cdn.who.int/media/docs/default-source/child-growth/'
            'growth-reference-5-19-years/bmi-for-age-(5-19-years)/'
            'cht-bmifa-boys-z-5-19years.pdf?sfvrsn=4007e921_4">BMI graph for BOYS</a>'
        )
        girl_link = QLabel(
            '<a href="https://cdn.who.int/media/docs/default-source/child-growth/'
            'growth-reference-5-19-years/bmi-for-age-(5-19-years)/'
            'cht-bmifa-girls-z-5-19years.pdf?sfvrsn=c708a56b_4">BMI graph for GIRLS</a>'
        )
        boy_link.setOpenExternalLinks(True)
        girl_link.setOpenExternalLinks(True)
        boy_link.setStyleSheet("font-size: 12px;")
        girl_link.setStyleSheet("font-size: 12px;")

        link_layout.addWidget(boy_link)
        link_layout.addWidget(girl_link)
        child_layout.addLayout(link_layout)

        return container

    # ── Update results panel ─────────────────────────────────────────
    def update_results(self, bmi, age_group):
        # ถ้า bmi เป็น string แสดงว่าเป็น error message
        if isinstance(bmi, str):
            self.bmi_text.setStyleSheet(
                "font-size: 16px; font-weight: bold; color: #CC0000;"
            )
            self.bmi_text.setText(bmi)
            self.adult_table.hide()
            self.child_table.hide()
            return

        self.bmi_text.setStyleSheet(
            "font-size: 38px; font-weight: bold; color: #4169E1;"
        )
        self.bmi_text.setText(f"{bmi:.2f}")

        if age_group == adult:
            self.child_table.hide()
            self.adult_table.show()
        else:
            self.adult_table.hide()
            self.child_table.show()

    # ── Clear results panel ──────────────────────────────────────────
    def clear_result(self):
        self.bmi_text.setText("0.00")
        self.bmi_text.setStyleSheet(
            "font-size: 38px; font-weight: bold; color: #4169E1;"
        )
        self.adult_table.hide()
        self.child_table.hide()


# ─────────────────────────────────────────────────────────────────────────────

class InputSection(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white;")

        form_layout = QFormLayout(self)
        form_layout.setContentsMargins(20, 15, 20, 5)
        form_layout.setHorizontalSpacing(10)
        form_layout.setVerticalSpacing(12)

        label_style = "font-size: 13px; color: #222;"
        combo_style = (
            "QComboBox { font-size: 13px; padding: 3px 6px; border: 1px solid #aaa; "
            "border-radius: 3px; background: white; }"
        )
        entry_style = (
            "QLineEdit { font-size: 13px; padding: 3px 6px; border: none; "
            "border-bottom: 1px solid #555; background: transparent; }"
        )

        # BMI age group
        lbl_group = QLabel("BMI age group:")
        lbl_group.setStyleSheet(label_style)
        self.combo_group = QComboBox()
        self.combo_group.addItems([adult, child])
        self.combo_group.setStyleSheet(combo_style)
        form_layout.addRow(lbl_group, self.combo_group)

        # Weight row
        lbl_weight = QLabel("Weight:")
        lbl_weight.setStyleSheet(label_style)
        weight_row = QHBoxLayout()
        self.entry_weight = QLineEdit()
        self.entry_weight.setStyleSheet(entry_style)
        self.entry_weight.setFixedWidth(130)
        self.combo_weight_unit = QComboBox()
        self.combo_weight_unit.addItems([kg, lb])
        self.combo_weight_unit.setStyleSheet(combo_style)
        weight_row.addWidget(self.entry_weight)
        weight_row.addWidget(self.combo_weight_unit)
        form_layout.addRow(lbl_weight, weight_row)

        # Height row
        lbl_height = QLabel("Height:")
        lbl_height.setStyleSheet(label_style)
        height_row = QHBoxLayout()
        self.entry_height = QLineEdit()
        self.entry_height.setStyleSheet(entry_style)
        self.entry_height.setFixedWidth(130)
        self.combo_height_unit = QComboBox()
        self.combo_height_unit.addItems([cm, ft])
        self.combo_height_unit.setStyleSheet(combo_style)
        height_row.addWidget(self.entry_height)
        height_row.addWidget(self.combo_height_unit)
        form_layout.addRow(lbl_height, height_row)

        # Buttons row
        btn_style = (
            "QPushButton { font-size: 13px; padding: 6px 20px; "
            "border: 1px solid #aaa; border-radius: 3px; background: #f0f0f0; }"
            "QPushButton:hover { background: #ddd; }"
            "QPushButton:pressed { background: #bbb; }"
        )
        self.btn_clear  = QPushButton("clear")
        self.btn_submit = QPushButton("Submit Registration")
        self.btn_clear.setStyleSheet(btn_style)
        self.btn_submit.setStyleSheet(btn_style)
        self.btn_clear.setFixedWidth(130)
        self.btn_submit.setFixedWidth(180)

        btn_widget = QWidget()
        btn_widget.setStyleSheet("background: white;")
        btn_row = QHBoxLayout(btn_widget)
        btn_row.setContentsMargins(0, 5, 0, 10)
        btn_row.setSpacing(15)
        btn_row.addWidget(self.btn_clear)
        btn_row.addWidget(self.btn_submit)
        form_layout.addRow(btn_widget)

    # ── Clear form + output ──────────────────────────────────────────
    def clear_form(self, output_section):
        # Clear input form
        self.entry_weight.clear()
        self.entry_height.clear()
        self.combo_group.setCurrentIndex(0)
        self.combo_weight_unit.setCurrentIndex(0)
        self.combo_height_unit.setCurrentIndex(0)

        # Clear output section
        output_section.clear_result()

    # ── Submit → calculate → update output ──────────────────────────
    def submit_reg(self, output_section):
        age_group = self.combo_group.currentText()
        try:
            bmi = self.calculate_BMI()          # คืนตัวเลข หรือ raise ValueError
            output_section.update_results(bmi, age_group)
        except ValueError as e:
            output_section.update_results(str(e), age_group)

    # ── BMI calculation (metric + English) ──────────────────────────
    def calculate_BMI(self):
        weight_text = self.entry_weight.text().strip()
        height_text = self.entry_height.text().strip()

        # กรณีช่องว่างเปล่า
        if weight_text == "" or height_text == "":
            raise ValueError("Please fill in both Weight and Height.")

        # กรณีพิมพ์ตัวอักษรที่ไม่ใช่ตัวเลข
        try:
            weight = float(weight_text)
        except ValueError:
            raise ValueError(f"Invalid weight: '{weight_text}' is not a number.")

        try:
            height = float(height_text)
        except ValueError:
            raise ValueError(f"Invalid height: '{height_text}' is not a number.")

        # กรณีค่าติดลบหรือศูนย์
        if weight <= 0:
            raise ValueError(f"Weight must be positive (got {weight}).")
        if height <= 0:
            raise ValueError(f"Height must be positive (got {height}).")

        weight_unit = self.combo_weight_unit.currentText()
        height_unit = self.combo_height_unit.currentText()

        # Convert to metric
        if weight_unit == lb:
            weight = weight * 0.453592      # pounds → kg
        if height_unit == ft:
            height = height * 30.48         # feet   → cm

        height_m = height / 100.0           # cm → m
        bmi = weight / (height_m ** 2)
        return bmi


# ─────────────────────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()