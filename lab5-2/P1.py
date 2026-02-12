"""
Pramepijak ueasri
683040506-8

"""
import sys
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QComboBox, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class BMICalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("P1: BMI Calculator")
        self.setFixedSize(420, 560)
        self.initUI()

    def initUI(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = QLabel("Adult and Child BMI Calculator")
        header.setAlignment(Qt.AlignCenter)
        header.setFixedHeight(45)
        header.setStyleSheet(
            "background-color: #8B1A1A;"
            "color: white;"
            "font-size: 16px;"
            "font-weight: bold;"
            "padding: 5px;"
        )
        main_layout.addWidget(header)

        # ── Input area ───────────────────────────────────────────────
        input_widget = QWidget()
        input_widget.setStyleSheet("background-color: white;")
        grid = QGridLayout(input_widget)
        grid.setContentsMargins(20, 20, 20, 15)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(12)

        label_style = "font-size: 13px; color: #222;"
        combo_style = (
            "QComboBox { font-size: 13px; padding: 3px 6px; border: 1px solid #aaa; "
            "border-radius: 3px; background: white; }"
            "QComboBox::drop-down { border: none; }"
        )
        entry_style = (
            "QLineEdit { font-size: 13px; padding: 3px 6px; border: none; "
            "border-bottom: 1px solid #555; background: transparent; }"
        )

        # BMI age group row
        lbl_group = QLabel("BMI age group:")
        lbl_group.setStyleSheet(label_style)
        self.combo_group = QComboBox()
        self.combo_group.addItems(["Adults 20+", "Children and Teenagers (5-19)"])
        self.combo_group.setStyleSheet(combo_style)
        self.combo_group.setFixedWidth(260)
        grid.addWidget(lbl_group, 0, 0, Qt.AlignRight)
        grid.addWidget(self.combo_group, 0, 1, 1, 2)

        # Weight row
        lbl_weight = QLabel("Weight:")
        lbl_weight.setStyleSheet(label_style)
        self.entry_weight = QLineEdit()
        self.entry_weight.setStyleSheet(entry_style)
        self.entry_weight.setFixedWidth(140)
        self.combo_weight_unit = QComboBox()
        self.combo_weight_unit.addItems(["kilograms", "pounds"])
        self.combo_weight_unit.setStyleSheet(combo_style)
        self.combo_weight_unit.setFixedWidth(115)
        grid.addWidget(lbl_weight, 1, 0, Qt.AlignRight)
        grid.addWidget(self.entry_weight, 1, 1)
        grid.addWidget(self.combo_weight_unit, 1, 2)

        # Height row
        lbl_height = QLabel("Height:")
        lbl_height.setStyleSheet(label_style)
        self.entry_height = QLineEdit()
        self.entry_height.setStyleSheet(entry_style)
        self.entry_height.setFixedWidth(140)
        self.combo_height_unit = QComboBox()
        self.combo_height_unit.addItems(["centimeters", "inches"])
        self.combo_height_unit.setStyleSheet(combo_style)
        self.combo_height_unit.setFixedWidth(115)
        grid.addWidget(lbl_height, 2, 0, Qt.AlignRight)
        grid.addWidget(self.entry_height, 2, 1)
        grid.addWidget(self.combo_height_unit, 2, 2)

        main_layout.addWidget(input_widget)

        # ── Buttons ──────────────────────────────────────────────────
        btn_widget = QWidget()
        btn_widget.setStyleSheet("background-color: white;")
        btn_layout = QHBoxLayout(btn_widget)
        btn_layout.setContentsMargins(20, 5, 20, 15)
        btn_layout.setSpacing(15)

        btn_style_clear = (
            "QPushButton { font-size: 13px; padding: 6px 20px; "
            "border: 1px solid #aaa; border-radius: 3px; background: #f0f0f0; }"
            "QPushButton:hover { background: #e0e0e0; }"
            "QPushButton:pressed { background: #ccc; }"
        )
        btn_style_submit = (
            "QPushButton { font-size: 13px; padding: 6px 20px; "
            "border: 1px solid #aaa; border-radius: 3px; background: #f0f0f0; }"
            "QPushButton:hover { background: #e0e0e0; }"
            "QPushButton:pressed { background: #ccc; }"
        )

        self.btn_clear = QPushButton("clear")
        self.btn_clear.setStyleSheet(btn_style_clear)
        self.btn_clear.setFixedWidth(140)

        self.btn_submit = QPushButton("Submit Registration")
        self.btn_submit.setStyleSheet(btn_style_submit)
        self.btn_submit.setFixedWidth(190)

        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_submit)

        main_layout.addWidget(btn_widget)

        # ── Result container ─────────────────────────────────────────
        self.result_container = QWidget()
        self.result_container.setStyleSheet("background-color: #FAF0E6;")  # Linen color

        layout_output = QVBoxLayout(self.result_container)
        layout_output.setContentsMargins(20, 20, 20, 20)
        layout_output.setSpacing(5)

        lbl_your_bmi = QLabel("Your BMI")
        lbl_your_bmi.setAlignment(Qt.AlignCenter)
        lbl_your_bmi.setStyleSheet("font-size: 14px; color: #333; background: transparent;")
        layout_output.addWidget(lbl_your_bmi)

        self.lbl_bmi_value = QLabel("0.00")
        self.lbl_bmi_value.setAlignment(Qt.AlignCenter)
        self.lbl_bmi_value.setStyleSheet(
            "font-size: 36px; font-weight: bold; color: #4169E1; background: transparent;"
        )
        layout_output.addWidget(self.lbl_bmi_value)

        # Adult BMI table (hidden by default; shown after adult calculation)
        self.frame_table = QFrame()
        self.frame_table.setStyleSheet("background: transparent;")
        table_layout = QGridLayout(self.frame_table)
        table_layout.setContentsMargins(30, 10, 30, 10)
        table_layout.setHorizontalSpacing(30)
        table_layout.setVerticalSpacing(4)

        header_style = "font-size: 13px; font-weight: bold; color: #222; background: transparent;"
        cell_style   = "font-size: 13px; color: #444; background: transparent;"

        table_layout.addWidget(self._lbl(header_style, "BMI"),       0, 0, Qt.AlignCenter)
        table_layout.addWidget(self._lbl(header_style, "Condition"),  0, 1, Qt.AlignCenter)

        rows = [("< 18.5", "Thin"), ("18.5 - 25.0", "Normal"),
                ("25.1 - 30.0", "Overweight"), ("> 30.0", "Obese")]
        for i, (bmi_range, condition) in enumerate(rows, start=1):
            table_layout.addWidget(self._lbl(cell_style, bmi_range),  i, 0, Qt.AlignCenter)
            table_layout.addWidget(self._lbl(cell_style, condition),   i, 1, Qt.AlignCenter)

        layout_output.addWidget(self.frame_table)
        self.frame_table.setVisible(False)

        # Child links (hidden by default; shown after child calculation)
        self.frame_child = QWidget()
        self.frame_child.setStyleSheet("background: transparent;")
        child_layout = QVBoxLayout(self.frame_child)
        child_layout.setContentsMargins(10, 10, 10, 5)
        child_layout.setSpacing(8)

        lbl_note = QLabel(
            "For child's BMI interpretation, please click one of the following links."
        )
        lbl_note.setWordWrap(True)
        lbl_note.setAlignment(Qt.AlignCenter)
        lbl_note.setStyleSheet("font-size: 12px; color: #555; background: transparent;")
        child_layout.addWidget(lbl_note)

        links_widget = QWidget()
        links_widget.setStyleSheet("background: transparent;")
        links_layout = QHBoxLayout(links_widget)
        links_layout.setContentsMargins(0, 0, 0, 0)
        links_layout.setSpacing(20)
        links_layout.setAlignment(Qt.AlignCenter)

        link_style = (
            "QPushButton { font-size: 12px; color: #1a0dab; background: transparent; "
            "border: none; text-decoration: underline; padding: 0; }"
            "QPushButton:hover { color: #c00; }"
        )
        btn_boys = QPushButton("BMI graph for BOYS")
        btn_boys.setStyleSheet(link_style)
        btn_boys.setCursor(Qt.PointingHandCursor)
        btn_boys.clicked.connect(lambda: webbrowser.open(
            "https://www.nhs.uk/live-well/healthy-weight/bmi-calculator/"
        ))

        btn_girls = QPushButton("BMI graph for GIRLS")
        btn_girls.setStyleSheet(link_style)
        btn_girls.setCursor(Qt.PointingHandCursor)
        btn_girls.clicked.connect(lambda: webbrowser.open(
            "https://www.nhs.uk/live-well/healthy-weight/bmi-calculator/"
        ))

        links_layout.addWidget(btn_boys)
        links_layout.addWidget(btn_girls)
        child_layout.addWidget(links_widget)

        layout_output.addWidget(self.frame_child)
        self.frame_child.setVisible(False)

        layout_output.addStretch()

        main_layout.addWidget(self.result_container)

        # ── Connect events ───────────────────────────────────────────
        self.btn_submit.clicked.connect(self.calculate_bmi)
        self.btn_clear.clicked.connect(self.clear_fields)

    # ── Helper ────────────────────────────────────────────────────────
    def _lbl(self, style, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(style)
        return lbl

    # ── BMI Calculation ───────────────────────────────────────────────
    def calculate_bmi(self):
        weight_text = self.entry_weight.text().strip()
        height_text = self.entry_height.text().strip()

        if not weight_text or not height_text:
            self.lbl_bmi_value.setText("Input Error")
            self.lbl_bmi_value.setStyleSheet(
                "font-size: 20px; font-weight: bold; color: red; background: transparent;"
            )
            self.frame_table.setVisible(False)
            self.frame_child.setVisible(False)
            return

        try:
            weight = float(weight_text)
            height = float(height_text)
        except ValueError:
            self.lbl_bmi_value.setText("Invalid Input")
            self.lbl_bmi_value.setStyleSheet(
                "font-size: 20px; font-weight: bold; color: red; background: transparent;"
            )
            self.frame_table.setVisible(False)
            self.frame_child.setVisible(False)
            return

        if weight <= 0 or height <= 0:
            self.lbl_bmi_value.setText("Enter positive values")
            self.lbl_bmi_value.setStyleSheet(
                "font-size: 16px; font-weight: bold; color: red; background: transparent;"
            )
            self.frame_table.setVisible(False)
            self.frame_child.setVisible(False)
            return

        # Convert to metric if needed
        weight_unit = self.combo_weight_unit.currentText()
        height_unit = self.combo_height_unit.currentText()

        if weight_unit == "pounds":
            weight = weight * 0.453592      # lb → kg
        if height_unit == "inches":
            height = height * 2.54          # in → cm

        # BMI = weight(kg) / height(m)^2
        height_m = height / 100.0
        bmi = weight / (height_m ** 2)

        self.lbl_bmi_value.setText(f"{bmi:.2f}")
        self.lbl_bmi_value.setStyleSheet(
            "font-size: 36px; font-weight: bold; color: #4169E1; background: transparent;"
        )

        age_group = self.combo_group.currentText()
        if age_group == "Adults 20+":
            self.frame_child.setVisible(False)
            self.frame_table.setVisible(True)
        else:
            # Children and Teenagers
            self.frame_table.setVisible(False)
            self.frame_child.setVisible(True)

        # Resize window to fit content
        self.adjustSize()

    # ── Clear ─────────────────────────────────────────────────────────
    def clear_fields(self):
        self.entry_weight.clear()
        self.entry_height.clear()
        self.combo_group.setCurrentIndex(0)
        self.combo_weight_unit.setCurrentIndex(0)
        self.combo_height_unit.setCurrentIndex(0)
        self.lbl_bmi_value.setText("0.00")
        self.lbl_bmi_value.setStyleSheet(
            "font-size: 36px; font-weight: bold; color: #4169E1; background: transparent;"
        )
        self.frame_table.setVisible(False)
        self.frame_child.setVisible(False)


def main():
    app = QApplication(sys.argv)
    window = BMICalculator()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
