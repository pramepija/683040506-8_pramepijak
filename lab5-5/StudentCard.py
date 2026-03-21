from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame,
)
from PySide6.QtCore import Qt, Signal, QMimeData, QPoint
from PySide6.QtGui import QFont, QCursor, QDrag, QPixmap

from style import C


class StudentCard(QFrame):

    # Signal for delete request: emits self
    card_de = Signal(object)

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data

        # for drag and drop
        self._drag_start: QPoint | None = None
        self.setAcceptDrops(False)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        self._build()


    def _build(self):
        # height depends on number of courses selected
        courses = [
            self.data.get("c1", ""),
            self.data.get("c2", ""),
            self.data.get("c3", ""),
        ]
        courses = [c for c in courses if c]

        # base height: name + dept rows, plus 18px per course line
        self.setMinimumHeight(70 + len(courses) * 20)

        self.setStyleSheet(f"""
            QFrame {{
                background:{C['card']};
            }}
            QFrame:hover {{
                background:{C['surface']};
            }}
        """)

        row = QHBoxLayout(self)
        row.setContentsMargins(12, 10, 12, 10)

        # drag handle
        handle = QLabel("⠿")
        handle.setFixedWidth(16)
        handle.setAlignment(Qt.AlignTop)
        handle.setStyleSheet(f"background:transparent; color:{C['muted']};font-size:18px;padding-top:2px;")

        #info
        info = QVBoxLayout()
        info.setSpacing(2)

        name_row = QHBoxLayout()
        name_row.setSpacing(8)

        name = QLabel(f"{self.data.get('first_name', '')} {self.data.get('last_name', '')}")
        name.setFont(QFont("Segoe UI", 13, QFont.Bold))
        name.setStyleSheet(f"color:{C['text']};")

        id_lbl = QLabel(self.data.get('id', ''))
        id_lbl.setStyleSheet(f"color:{C['muted']}; font-size:12px;")

        name_row.addWidget(name)
        name_row.addWidget(id_lbl)
        name_row.addStretch()

        dept = QLabel(f"{self.data.get('fa', '')}  ·  {self.data.get('ma', '')}")
        dept.setStyleSheet(f"color:{C['muted']}; font-size:12px;")

        info.addLayout(name_row) 
        info.addWidget(dept)

        # แสดง courses
        for c in courses:
            if c == "—":
                continue
            lbl = QLabel(f"• {c}")
            lbl.setStyleSheet(f"color:{C['muted']}; font-size:12px;")
            info.addWidget(lbl)
            
        # delete button
        btn_del = QPushButton("✕")
        btn_del.setFixedSize(28, 28)
        btn_del.setCursor(QCursor(Qt.PointingHandCursor))
        btn_del.setStyleSheet(f"""
            QPushButton {{
                background:transparent;
                color:{C['muted']};
                border:none;
                border-radius:14px;
                font-size:11px;
                font-weight:bold;
            }}
            QPushButton:hover {{
                background:{C['red']};
                color:white;
                border:none;
            }}
        """)
        btn_del.clicked.connect(lambda: self.card_de.emit(self))
        
        row.addWidget(handle)
        row.addLayout(info, stretch=1)
        row.addWidget(btn_del, alignment=Qt.AlignTop)


    # ── Drag support ──────────────────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self._drag_start is not None:
            if (event.pos() - self._drag_start).manhattanLength() > 10:
                drag = QDrag(self)
                mime = QMimeData()
                mime.setText("student_card")
                drag.setMimeData(mime)

                pix = QPixmap(self.size())
                pix.fill(Qt.transparent)
                self.render(pix)
                drag.setPixmap(pix)
                drag.setHotSpot(event.pos())
                drag.exec(Qt.MoveAction)
        super().mouseMoveEvent(event)