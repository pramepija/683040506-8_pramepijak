"""
Student Registration System — PySide6
======================================
3 pages via QStackedWidget + Signal/Slot.

Page 1 : Card list (drag-drop reorder, delete)
Page 2 : Add student form
Page 3 : Review & confirm
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QScrollArea,
    QLabel, QLineEdit, QPushButton, QComboBox, QFrame,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor

from data import COURSES
from style import C, BASE, INPUT_SS, COMBO_SS, SCROLL_SS
from style import btn_ss, section_label, field_label, divider
from StudentCard import StudentCard


# ─────────────────────────────────────────────────────────────
#  Page 1 — Student List
# ─────────────────────────────────────────────────────────────
class StudentListPage(QWidget):


    def __init__(self):
        super().__init__()

        self.setAcceptDrops(True)
        self._build()


    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(0)

        # ── top bar ──
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)

        title = QLabel("Students")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet(f"color:{C['text']};")

        self.lbl_count = QLabel("0 enrolled")
        self.lbl_count.setStyleSheet(
            f"color:{C['muted']};font-size:13px;"
        )

        self.btn_add = QPushButton("+ Add Student")
        self.btn_add.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn_add.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))

        bl.addWidget(title)
        bl.addSpacing(12)
        bl.addWidget(self.lbl_count, alignment=Qt.AlignVCenter)
        bl.addStretch()
        bl.addWidget(self.btn_add)
        root.addWidget(bar)

        # ── scroll area ──
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        root.addWidget(self._scroll)

        self._cards = [] 
        
        self._container = QWidget()     
        self._container.setAcceptDrops(True)       
        self._card_lay = QVBoxLayout(self._container)
        self._card_lay.setAlignment(Qt.AlignTop)
        self._card_lay.setSpacing(8)

        self._lbl_empty = QLabel('No students registered yet.\nClick "+Add Student" to get started')   # แสดงเมื่อไม่มีการ์ด
        self._lbl_empty.setAlignment(Qt.AlignCenter)
        self._card_lay.addWidget(self._lbl_empty)

        self._scroll.setWidget(self._container)
        
    # ── public ───────────────────────────────────────────────
    def add_student(self, data: dict):

        # create card and connect the delete signal
        card = StudentCard(data)
        card.card_de.connect(lambda: self._remove_card(card))

        # Add card to the list
        self._cards.append(card)

        # insert card to the card layout
        self._card_lay.addWidget(card)

        self._refresh_count()
        self._refresh_empty()

    # ── private ──────────────────────────────────────────────
    def _remove_card(self, card: StudentCard):
        # inline confirmation — no popup, just ask once
        reply = QMessageBox.question(
            self, "Remove student",
            f"Remove {card.data['first_name']} {card.data['last_name']}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            # remove card from the list
            self._cards.remove(card)
            card.deleteLater()
            # remove card from layout
            self._refresh_count()
            self._refresh_empty()

    def _refresh_count(self):
        
        # get number of card
        n = len(self._cards)
        # update number of student label
        self.lbl_count.setText(f"{n} enrolled")
        

    def _refresh_empty(self):
        has = bool(self._cards)
        self._lbl_empty.setVisible(not has)

    # ── drag-drop reorder ────────────────────────────────────
    def dragEnterEvent(self, event):
        if event.mimeData().hasText() and event.mimeData().text() == "student_card":
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        src = event.source()
        if not isinstance(src, StudentCard) or src not in self._cards:
            return

        local_y = self._container.mapFrom(self, event.position().toPoint()).y()
        target = len(self._cards) - 1
        for i, card in enumerate(self._cards):
            if local_y < card.y() + card.height() // 2:
                target = i
                break

        src_idx = self._cards.index(src)
        if src_idx == target:
            return

        self._cards.pop(src_idx)
        self._cards.insert(target, src)
        for card in self._cards:
            self._card_lay.removeWidget(card)
        for i, card in enumerate(self._cards):
            self._card_lay.insertWidget(i, card)

        event.acceptProposedAction()


# ─────────────────────────────────────────────────────────────
#  Page 2 — Add Student Form
# ─────────────────────────────────────────────────────────────
class AddStudentPage(QWidget):

    # Add signals for going back and going forward
    data_form = Signal(dict)

    def __init__(self):
        super().__init__()
        self.data = {}
        self._build()

    def _inp(self, ph: str = "") -> QLineEdit:
        e = QLineEdit()
        e.setPlaceholderText(ph)
        e.setMinimumHeight(38)
        e.setStyleSheet(INPUT_SS)
        return e
    
    def _inp_combo(self) -> QComboBox:
        e = QComboBox()
        e.setMinimumHeight(38)
        e.addItems(COURSES)
        e.setStyleSheet(INPUT_SS)
        return e

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Add Student")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()

        # scrollable form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(SCROLL_SS)

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)

        # ── personal info ─────────────────────────────────────
        form.addWidget(section_label("Personal Information"))

        layout1 = QHBoxLayout()
        self.student_id = self._inp("e.g 683040492-3")

        layout1.addWidget(QLabel("Student ID *"))
        layout1.addWidget(self.student_id)

        layout2 = QHBoxLayout()
        self.first_name = self._inp("First name")
        self.last_name = self._inp("Last name")

        layout2.addWidget(QLabel("First Name *"))
        layout2.addWidget(self.first_name)
        layout2.addWidget(QLabel("Last Name *"))
        layout2.addWidget(self.last_name)

        layout3 = QHBoxLayout()
        self.faculty = self._inp("e.g Science & Technology")
        self.major = self._inp("e.g Computer Science")

        layout3.addWidget(QLabel("Faculty *"))
        layout3.addWidget(self.faculty)
        layout3.addWidget(QLabel("Major *"))
        layout3.addWidget(self.major)

        form.addLayout(layout1)
        form.addLayout(layout2)
        form.addLayout(layout3)
        form.addWidget(divider())

        # ── course selection ──────────────────────────────────
        form.addWidget(section_label("Course Selection  (choose 1–3)"))
        layout4 = QHBoxLayout()
        self.c1 = self._inp_combo()

        layout4.addWidget(QLabel("Course 1"))
        layout4.addWidget(self.c1)

        layout5 = QHBoxLayout()
        self.c2 = self._inp_combo()

        layout5.addWidget(QLabel("Course 1"))
        layout5.addWidget(self.c2)

        layout6 = QHBoxLayout()
        self.c3 = self._inp_combo()

        layout6.addWidget(QLabel("Course 1"))
        layout6.addWidget(self.c3)

        form.addLayout(layout4)
        form.addLayout(layout5)
        form.addLayout(layout6)
        # ── error label ───────────────────────────────────────
        self.lbl_err = QLabel("")
        self.lbl_err.setStyleSheet(f"color:{C['red']};font-size:13px;")
        form.addWidget(self.lbl_err)

        form.addStretch()

        # ── buttons ───────────────────────────────────────────
        btn_row = QHBoxLayout()
        self.bc = QPushButton("← Cancel")
        self.bc.setCursor(QCursor(Qt.PointingHandCursor))
        self.bc.setStyleSheet(
            btn_ss(C['bg'], C['surface'], C['muted'],
                   border=f"1px solid {C['border']}")
        )
        self.bc.clicked.connect(self.clear_form)

        self.br = QPushButton("Review →")
        self.br.setCursor(QCursor(Qt.PointingHandCursor))
        self.br.setStyleSheet(btn_ss(C['accent'], "#1d4ed8"))
        self.br.clicked.connect(lambda: self.save_data())

        btn_row.addWidget(self.bc)
        btn_row.addStretch()
        btn_row.addWidget(self.br)
        form.addLayout(btn_row)

        scroll.setWidget(body)
        root.addWidget(bar)
        root.addWidget(scroll, stretch=1)

    # For when coming back from the review page
    def save_data(self):
        if not self.student_id.text().strip() or not self.first_name.text().strip() or not self.last_name.text().strip() or not self.faculty.text().strip() or not self.major.text().strip():
            self.lbl_err.setText("Required Stydent ID, First Name, Last Name, Faculty, Major, at least 1 course")
            return
        
        courses = [self.c1.currentText(), self.c2.currentText(), self.c3.currentText()]
        have_some = False
        for i in courses:
            if i != "— Select Course —":
                have_some = True

        if have_some == False:
            self.lbl_err.setText("Required Stydent ID, First Name, Last Name, Faculty, Major, at least 1 course")
            return

        self.lbl_err.setText("")
        self.data["id"] = self.student_id.text().strip()
        self.data["first_name"] = self.first_name.text().strip()  
        self.data["last_name"] = self.last_name.text().strip()
        self.data["fa"] = self.faculty.text().strip()
        self.data["ma"] = self.major.text().strip()
        self.data["c1"] = self.c1.currentText()
        self.data["c2"] = self.c2.currentText()
        self.data["c3"] = self.c3.currentText()
        if self.c1.currentText() == "— Select Course —":
            self.data["c1"] = "—"
        if self.c2.currentText() == "— Select Course —":
            self.data["c2"] = "—"
        if self.c3.currentText() == "— Select Course —":
            self.data["c3"] = "—"

        self.data_form.emit(self.data)

    # For when going back to the home page
    def clear_form(self):
        self.student_id.clear()
        self.first_name.clear()
        self.last_name.clear()
        self.faculty.clear()
        self.major.clear()
        self.c1.setCurrentIndex(0)
        self.c2.setCurrentIndex(0)
        self.c3.setCurrentIndex(0)

    def load_data(self, d:dict):
        self.student_id.setText(d["id"])
        self.first_name.setText(d["first_name"])
        self.last_name.setText(d["last_name"])
        self.faculty.setText(d["fa"])
        self.major.setText(d["ma"])
        self.c1.setCurrentText(d["c1"])
        self.c2.setCurrentText(d["c2"])
        self.c3.setCurrentText(d["c3"])

# ─────────────────────────────────────────────────────────────
#  Page 3 — Review & Confirm
# ─────────────────────────────────────────────────────────────
class ReviewPage(QWidget):

    # Emit signals for confirming and going back to edit
    confirmed = Signal(dict)   # Confirm กด
    edit_req  = Signal(dict)

    def __init__(self):
        super().__init__()
        self._data: dict = {}
        self._build()

    def _row(self, layout: QVBoxLayout, label: str) -> QLabel:
        row = QHBoxLayout()
        row.setSpacing(0)
        lbl = QLabel(label)
        lbl.setFixedWidth(130)
        lbl.setStyleSheet(f"color:{C['muted']};font-size:13px;")
        val = QLabel("—")
        val.setStyleSheet(f"color:{C['text']};font-size:13px;")
        val.setWordWrap(True)
        row.addWidget(lbl)
        row.addWidget(val, stretch=1)
        layout.addLayout(row)
        return val

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # top bar
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setStyleSheet(
            f"background:{C['bg']}; border-bottom:1px solid {C['border']};"
        )
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(32, 0, 32, 0)
        t = QLabel("Review & Confirm")
        t.setFont(QFont("Segoe UI", 16, QFont.Bold))
        t.setStyleSheet(f"color:{C['text']};")
        bl.addWidget(t)
        bl.addStretch()

        body = QWidget()
        body.setStyleSheet(f"background:{C['bg']};")
        form = QVBoxLayout(body)
        form.setContentsMargins(40, 28, 40, 28)
        form.setSpacing(20)

        # ── summary section ───────────────────────────────────
        form.addWidget(section_label("Student Information"))

        self.id = self._row(form, "student ID")
        self.name =self._row(form, "Full Name")
        self.fa =self._row(form, "Faculty")
        self.ma =self._row(form, "Major")

        form.addWidget(divider())
        form.addWidget(section_label("Courses"))
        self.c1 =self._row(form, "Course 1")
        self.c2 =self._row(form, "Course 2")
        self.c3 =self._row(form, "Course 3")
        
        # ── buttons ───────────────────────────────────────────
        btn_row = QHBoxLayout()
        self.be = QPushButton("← Edit")
        self.be.setCursor(QCursor(Qt.PointingHandCursor))
        self.be.setStyleSheet(
            btn_ss(C['bg'], C['surface'], C['muted'],
                   border=f"1px solid {C['border']}")
        )
        self.be.clicked.connect(lambda: self.edit_req.emit(self._data))

        self.bc = QPushButton("Confirm Registration")
        self.bc.setCursor(QCursor(Qt.PointingHandCursor))
        self.bc.setStyleSheet(btn_ss(C['green'], "#15803d"))
        self.bc.clicked.connect(lambda: self.confirmed.emit(self._data))

        btn_row.addWidget(self.be)
        btn_row.addStretch()
        btn_row.addWidget(self.bc)
        form.addLayout(btn_row)
        root.addWidget(bar)
        root.addWidget(body)
    
    def load_data(self, d: dict):
        self._data = d
        self.id.setText(d.get("id", "—"))
        self.name.setText(d.get("first_name", "") + " " + d.get("last_name", ""))
        self.fa.setText(d.get("fa", "—"))
        self.ma.setText(d.get("ma", "—"))
        self.c1.setText(d.get("c1", "—"))
        self.c2.setText(d.get("c2", "—"))
        self.c3.setText(d.get("c3", "—"))

    def save_data(self):
        self.data_form.emit(self._data)

# ─────────────────────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Registration")
        self.setMinimumSize(860, 580)
        self.resize(980, 660)
        self.setStyleSheet(BASE)
        self._build()

    def _build(self):
        # Add and Manage Stack
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.student_list = StudentListPage()
        self.student_add = AddStudentPage()
        self.review_page = ReviewPage()

        self.stack.addWidget(self.student_list)
        self.stack.addWidget(self.student_add)
        self.stack.addWidget(self.review_page)

        self.stack.setCurrentIndex(0)
        
        # signals
        self.student_list.btn_add.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.student_add.bc.clicked.connect(lambda: self.cancel_on())
        self.student_add.data_form.connect(lambda data: self.on_review(data))
        self.review_page.edit_req.connect(lambda data: self.go_to_add(data))
        self.review_page.confirmed.connect(lambda data: self.add_card(data))

    # Helper methods, if you need some
    def go_to_add(self, data:dict):
        self.stack.setCurrentIndex(1)
        self.student_add.load_data(data)
    
    def cancel_on(self):
        self.stack.setCurrentIndex(0)

    def on_review(self, data:dict):
        self.review_page.load_data(data)
        self.stack.setCurrentIndex(2)

    def add_card(self, data:dict):
        data = self.review_page._data     
        self.student_list.add_student(data) 
        self.student_add.clear_form()        
        self.stack.setCurrentIndex(0)
        QMessageBox.information(self, "Success", "Student registered successfully!")

# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())