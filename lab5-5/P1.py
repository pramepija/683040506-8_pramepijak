import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QDateEdit, QSpinBox,
    QPushButton, QDialog, QMessageBox, QScrollArea,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QDate, QLocale, QRegularExpression
from PySide6.QtGui import QFont, QRegularExpressionValidator


# ── ข้อมูลความจุและราคาของแต่ละห้อง ──
ROOM_CAPACITY = {
    "Standard Room": 1,   # รองรับ 1 คน / ห้อง
    "Deluxe Room":   2,   # รองรับ 2 คน / ห้อง
    "Suite Room":    2,   # รองรับ 2 คน / ห้อง
    "Family Room":   4,   # รองรับ 4 คน / ห้อง
}


class RoomCard(QWidget):
    """
    Room information card — Custom Widget Class
    """

    room_selected = Signal(str, int)  # สัญญาณส่งชื่อห้องและราคาเมื่อกด Select

    def __init__(self, room_name: str, price: int, description: str, emoji: str = "🏨"):
        # กำหนดค่าเริ่มต้น: ชื่อห้อง, ราคา, และสถานะยังไม่ถูกเลือก
        super().__init__()
        self._is_selected = False
        self.room_name = room_name
        self.price = price

        self._build_ui(emoji, room_name, price, description)
        self.deselect()

    def _build_ui(self, emoji: str, room_name: str, price: int, description: str):
        # สร้างหน้าตาของการ์ดห้องพัก (emoji, ชื่อ, ราคา, คำอธิบาย, ปุ่ม)
        self.setFixedSize(200, 200)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        emoji_lbl = QLabel(emoji)
        emoji_lbl.setAlignment(Qt.AlignCenter)
        emoji_lbl.setFont(QFont("Segoe UI", 28))

        name_lbl = QLabel(room_name)
        name_lbl.setAlignment(Qt.AlignCenter)
        name_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))
        name_lbl.setStyleSheet("color: #1e1b4b;")

        price_lbl = QLabel(f"${price} / night")
        price_lbl.setAlignment(Qt.AlignCenter)
        price_lbl.setFont(QFont("Segoe UI", 10))
        price_lbl.setStyleSheet("color: #6b7280;")

        desc_lbl = QLabel(description)
        desc_lbl.setAlignment(Qt.AlignCenter)
        desc_lbl.setWordWrap(True)
        desc_lbl.setFont(QFont("Segoe UI", 8))
        desc_lbl.setStyleSheet("color: #9ca3af;")

        self.select_btn = QPushButton("Select Room")
        self.select_btn.setFixedHeight(30)
        self.select_btn.setCursor(Qt.PointingHandCursor)
        self.select_btn.clicked.connect(self._on_select_clicked)

        layout.addWidget(emoji_lbl)
        layout.addWidget(name_lbl)
        layout.addWidget(price_lbl)
        layout.addWidget(desc_lbl)
        layout.addWidget(self.select_btn)

    def _on_select_clicked(self):
        # เมื่อกดปุ่ม Select ให้ส่งสัญญาณพร้อมชื่อห้องและราคาออกไป
        self.room_selected.emit(self.room_name, self.price)

    def select(self):
        # เปลี่ยนสีการ์ดเป็นสีเขียว และข้อความปุ่มเป็น "✓ Selected"
        self._is_selected = True
        self.setStyleSheet("""
            RoomCard {
                background-color: #f0fdf4;
                border: 2px solid #22c55e;
                border-radius: 12px;
            }
        """)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.select_btn.setText("✓ Selected")

    def deselect(self):
        # รีเซ็ตสีการ์ดกลับเป็นสีขาวปกติ และข้อความปุ่มเป็น "Select Room"
        self._is_selected = False
        self.setStyleSheet("""
            RoomCard {
                background-color: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 12px;
            }
            RoomCard:hover {
                border: 2px solid #6366f1;
                background-color: #f5f3ff;
            }
        """)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 5px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)
        self.select_btn.setText("Select Room")

    def is_selected(self):
        # คืนค่า True/False ว่าการ์ดนี้ถูกเลือกอยู่หรือไม่
        return self._is_selected


class ConfirmDialog(QDialog):
    """
    Booking confirmation popup — Custom Dialog Class
    """

    def __init__(self, guest_name: str, room_name: str, parent=None):
        # สร้างหน้าต่าง popup ยืนยันการจอง
        super().__init__(parent)
        self.setWindowTitle("Booking Confirmed")
        self.setFixedSize(360, 240)
        self.setModal(True)
        self._build_ui(guest_name, room_name)

    def _build_ui(self, guest_name: str, room_name: str):
        # สร้างหน้าตา popup (ไอคอน ✅, ข้อความยืนยัน, ปุ่ม OK)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        check_lbl = QLabel("✅")
        check_lbl.setAlignment(Qt.AlignCenter)
        check_lbl.setFont(QFont("Segoe UI", 36))
        check_lbl.setStyleSheet("""
            QLabel {
                background-color: #dcfce7;
                border-radius: 12px;
                padding: 6px;
            }
        """)

        title_lbl = QLabel("Booking Successful!")
        title_lbl.setAlignment(Qt.AlignCenter)
        title_lbl.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_lbl.setStyleSheet("color: #16a34a;")

        msg_lbl = QLabel(f"Dear {guest_name},\n{room_name} is ready to welcome you! 🎉")
        msg_lbl.setAlignment(Qt.AlignCenter)
        msg_lbl.setFont(QFont("Segoe UI", 10))
        msg_lbl.setStyleSheet("color: #374151;")
        msg_lbl.setWordWrap(True)

        ok_btn = QPushButton("OK")
        ok_btn.setFixedHeight(38)
        ok_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        ok_btn.setCursor(Qt.PointingHandCursor)
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #16a34a; }
        """)
        ok_btn.clicked.connect(self.accept)

        layout.addWidget(check_lbl)
        layout.addWidget(title_lbl)
        layout.addWidget(msg_lbl)
        layout.addWidget(ok_btn)


#  Page 1: Booking Page

class BookingPage(QWidget):
    """
    Page 1 — Guest information form and room selection
    """

    def __init__(self):
        # กำหนดค่าเริ่มต้น: ยังไม่มีห้องที่เลือก และรายการการ์ดว่างเปล่า
        super().__init__()
        self.selected_room = None
        self.selected_price = 0
        self.cards = []
        self._build_ui()

    def _build_ui(self):
        # สร้างหน้า 1 ทั้งหมด: ฟอร์มกรอกข้อมูล + การ์ดเลือกห้อง + ปุ่ม
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 24, 30, 24)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("🏨 Book Your Stay at CozyStay")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #1e1b4b;")

        subtitle = QLabel("Fill in your details and choose your room")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #6b7280;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # ── Section 1: Guest Info Form ──
        form_title = QLabel("📋 Guest Information")
        form_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        form_title.setStyleSheet("color: #374151; margin-top: 8px;")
        main_layout.addWidget(form_title)

        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 10px;
            }
        """)

        # Create input widgets
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g. John Smith")

        # ── [เพิ่ม] ป้องกัน phone กรอกได้เฉพาะตัวเลข 0-9 เท่านั้น ──
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("e.g. 0812345678")
        rx = QRegularExpression(r'^\d{0,15}$')                              # รับแค่ตัวเลข 0-9 ไม่เกิน 15 หลัก
        self.phone_input.setValidator(QRegularExpressionValidator(rx, self))

        en_locale = QLocale(QLocale.English, QLocale.UnitedStates) 

        self.checkin_input.setDate(QDate.currentDate())
        self.checkin_input.setDisplayFormat("dd/MM/yyyy")
        self.checkin_input.setCalendarPopup(True)

        self.checkout_input = QDateEdit()
        self.checkout_input.setLocale(en_locale)                   
        self.checkout_input.setDate(QDate.currentDate().addDays(1))
        self.checkout_input.setDisplayFormat("dd/MM/yyyy")
        self.checkout_input.setCalendarPopup(True)

        self.guests_input = QSpinBox()
        self.guests_input.setLocale(en_locale)               
        self.guests_input.setMinimum(1)
        self.guests_input.setMaximum(10)
        self.guests_input.setValue(1)
        self.guests_input.setSuffix(" guest(s)")

        # ── [เพิ่ม] เมื่อเปลี่ยนจำนวนแขก ให้คำนวณห้องโดยอัตโนมัติ ──
        self.guests_input.valueChanged.connect(self._on_guests_changed)

        # Styles
        input_style = """
            QLineEdit, QDateEdit, QSpinBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
                background: white;
            }
            QLineEdit:focus, QDateEdit:focus, QSpinBox:focus {
                border: 1px solid #6366f1;
            }
        """
        for w in [self.name_input, self.phone_input,
                  self.checkin_input, self.checkout_input, self.guests_input]:
            w.setStyleSheet(input_style)
            w.setMinimumWidth(200)

        label_style = "font-size: 13px; color: #374151; font-weight: bold;"

        form_grid = QGridLayout(form_frame)
        form_grid.setContentsMargins(20, 16, 20, 16)
        form_grid.setSpacing(10)
        form_grid.setColumnStretch(1, 1)

        for row, (text, widget) in enumerate([
            ("Full Name :",       self.name_input),
            ("Phone Number :",    self.phone_input),
            ("Check-in Date :",   self.checkin_input),
            ("Check-out Date :",  self.checkout_input),
            ("Guests :",          self.guests_input),
        ]):
            lbl = QLabel(text)
            lbl.setStyleSheet(label_style)
            lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            form_grid.addWidget(lbl, row, 0)
            form_grid.addWidget(widget, row, 1)

        main_layout.addWidget(form_frame)

        # ── Section 2: Room Selection ──
        room_title = QLabel("🛏 Select a Room")
        room_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        room_title.setStyleSheet("color: #374151; margin-top: 8px;")
        main_layout.addWidget(room_title)

        rooms_data = [
            ("Standard Room", 50,  "Single bed, Free Wi-Fi",             "🛏"),
            ("Deluxe Room",   120, "Double bed, Ocean view, Wi-Fi",      "🌊"),
            ("Suite Room",    250, "Living room, Jacuzzi, Premium view", "👑"),
            ("Family Room",   160, "2 Bedrooms, Perfect for families",   "👨‍👩‍👧‍👦"),
        ]

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(14)
        cards_layout.setContentsMargins(0, 0, 0, 0)

        for room_name, price, description, emoji in rooms_data:
            card = RoomCard(room_name, price, description, emoji)
            card.room_selected.connect(self._on_room_selected)
            self.cards.append(card)
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        main_layout.addLayout(cards_layout)

        # ── [เพิ่ม] label แจ้งจำนวนห้องที่ต้องจอง ──
        self.rooms_needed_label = QLabel("")
        self.rooms_needed_label.setFont(QFont("Segoe UI", 10))
        self.rooms_needed_label.setStyleSheet("color: #0369a1; margin-top: 4px;")
        main_layout.addWidget(self.rooms_needed_label)

        # ── Buttons ──
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.clear_btn = QPushButton("🗑  Clear Info")
        self.clear_btn.setFixedHeight(42)
        self.clear_btn.setFont(QFont("Segoe UI", 11))
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0 20px;
            }
            QPushButton:hover { background-color: #e5e7eb; }
        """)
        self.clear_btn.clicked.connect(self.clear_form)

        self.next_btn = QPushButton("Next  →")
        self.next_btn.setFixedHeight(42)
        self.next_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 28px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)

        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_btn)

        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

        scroll.setWidget(container)

        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.addWidget(scroll)

    # ── [เพิ่ม] คำนวณจำนวนห้องที่ต้องจองให้พอดีกับจำนวนแขก ──
    def _on_guests_changed(self, guests: int):
        # คำนวณเฉพาะเมื่อมีห้องที่เลือกอยู่แล้ว
        if not self.selected_room:
            self.rooms_needed_label.setText("")
            return

        capacity = ROOM_CAPACITY.get(self.selected_room, 1)

        # คำนวณจำนวนห้องที่ต้องการ (ปัดขึ้น)
        import math
        rooms_needed = math.ceil(guests / capacity)

        self.selected_rooms_count = rooms_needed  # เก็บไว้ใช้ตอนคำนวณราคา

        total_per_night = rooms_needed * self.selected_price
        self.rooms_needed_label.setText(
            f"ℹ️  {guests} ผู้เข้าพัก → ต้องการ {rooms_needed} ห้อง "
            f"({self.selected_room})  =  ${total_per_night} / คืน"
        )

    def _on_room_selected(self, room_name: str, price: int):
        # รับสัญญาณจากการ์ด แล้ว select การ์ดที่เลือก / deselect การ์ดอื่นทั้งหมด
        self.selected_room = room_name
        self.selected_price = price
        self.selected_rooms_count = 1  # reset

        for card in self.cards:
            if card.room_name == room_name:
                card.select()
            else:
                card.deselect()

        # คำนวณห้องทันทีหลังเลือกห้อง
        self._on_guests_changed(self.guests_input.value())

    def clear_form(self):
        # ล้างข้อมูลในฟอร์มและการเลือกห้องทั้งหมดกลับเป็นค่าเริ่มต้น
        self.name_input.clear()
        self.phone_input.clear()
        self.checkin_input.setDate(QDate.currentDate())
        self.checkout_input.setDate(QDate.currentDate().addDays(1))
        self.guests_input.setValue(1)
        self.selected_room = None
        self.selected_price = 0
        self.selected_rooms_count = 1
        self.rooms_needed_label.setText("")
        for card in self.cards:
            card.deselect()

    def get_booking_data(self):
        # ตรวจสอบความถูกต้องของฟอร์ม แล้วคืน dict ข้อมูลการจองทั้งหมด (หรือ None ถ้าข้อมูลไม่ครบ)
        name = self.name_input.text().strip()
        phone = self.phone_input.text().strip()
        checkin = self.checkin_input.date()
        checkout = self.checkout_input.date()

        if not name:
            QMessageBox.warning(self, "Missing Information", "Please enter your full name.")
            return None
        if not phone:
            QMessageBox.warning(self, "Missing Information", "Please enter your phone number.")
            return None
        if checkin >= checkout:
            QMessageBox.warning(self, "Invalid Dates",
                                "Check-out date must be after check-in date.")
            return None
        if not self.selected_room:
            QMessageBox.warning(self, "No Room Selected",
                                "Please select a room before proceeding.")
            return None

        nights = checkin.daysTo(checkout)
        guests = self.guests_input.value()

        # ── [เพิ่ม] คำนวณจำนวนห้องและราคารวมที่ถูกต้อง ──
        import math
        capacity = ROOM_CAPACITY.get(self.selected_room, 1)
        rooms_needed = math.ceil(guests / capacity)
        total = nights * self.selected_price * rooms_needed

        data_dict = {
            "room":         self.selected_room,
            "price":        self.selected_price,
            "rooms":        rooms_needed,           # จำนวนห้องที่ต้องจอง
            "name":         name,
            "phone":        phone,
            "checkin":      checkin.toString("dd/MM/yyyy"),
            "checkout":     checkout.toString("dd/MM/yyyy"),
            "nights":       nights,
            "guests":       guests,
            "total":        total,
        }

        return data_dict


#  PAGE 2 ReviewPage

class ReviewPage(QWidget):
    """
    Page 2 — Review booking details before submitting
    """

    def __init__(self):
        # กำหนดค่าเริ่มต้น: ข้อมูลการจองว่างเปล่า
        super().__init__()
        self.current_data = {}
        self._build_ui()

    def _build_ui(self):
        # สร้างหน้า 2 ทั้งหมด: ตารางสรุปข้อมูล + ยอดรวม + ปุ่ม Back/Confirm
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(16)

        title = QLabel("📋 Booking Summary")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #1e1b4b;")

        subtitle = QLabel("Please review your details before confirming")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #6b7280;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.info_frame = QFrame()
        self.info_frame.setStyleSheet("""
            QFrame {
                background-color: #f9fafb;
                border-radius: 12px;
            }
        """)

        self.info_layout = QGridLayout(self.info_frame)
        self.info_layout.setContentsMargins(24, 20, 24, 20)
        self.info_layout.setSpacing(10)
        self.info_layout.setColumnStretch(1, 1)

        # ── [เพิ่ม] เพิ่มแถว "Rooms" ในตารางสรุป ──
        self.display_rows = [
            ("🛏  Room",            ""),
            ("🔢  Rooms",           "- room(s)"),   # แถวใหม่: จำนวนห้อง
            ("💰  Price / Night",   "$ -"),
            ("👤  Guest Name",      ""),
            ("📞  Phone",           ""),
            ("📅  Check-in",        ""),
            ("📅  Check-out",       ""),
            ("🌙  Nights",          "- night(s)"),
            ("👥  Guests",          "- guest(s)"),
        ]

        key_style = "font-weight: bold; color: #374151; font-size: 13px;"
        val_style = "color: #1f2937; font-size: 13px;"

        self.val_labels = []
        for row, (key, val) in enumerate(self.display_rows):
            key_lbl = QLabel(key)
            key_lbl.setStyleSheet(key_style)
            val_lbl = QLabel(val)
            val_lbl.setStyleSheet(val_style)
            self.val_labels.append(val_lbl)
            self.info_layout.addWidget(key_lbl, row, 0)
            self.info_layout.addWidget(val_lbl, row, 1)

        layout.addWidget(self.info_frame)

        # hline
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #e5e7eb;")
        layout.addWidget(line)

        # Total label
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        total_icon = QLabel("💳")
        total_icon.setFont(QFont("Segoe UI", 13))
        self.total_label = QLabel("Total Amount:  $0")
        self.total_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.total_label.setStyleSheet("color: #0d9488;")
        total_layout.addWidget(total_icon)
        total_layout.addWidget(self.total_label)
        layout.addLayout(total_layout)

        layout.addStretch()

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.back_btn = QPushButton("←  Back")
        self.back_btn.setFixedHeight(44)
        self.back_btn.setFont(QFont("Segoe UI", 11))
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0 22px;
            }
            QPushButton:hover { background-color: #e5e7eb; }
        """)

        self.submit_btn = QPushButton("✅  Confirm Booking")
        self.submit_btn.setFixedHeight(44)
        self.submit_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.submit_btn.setCursor(Qt.PointingHandCursor)
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0 28px;
            }
            QPushButton:hover { background-color: #16a34a; }
        """)

        btn_layout.addWidget(self.back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.submit_btn)
        layout.addLayout(btn_layout)

    def load_data(self, data: dict):
        # รับ dict ข้อมูลการจองจากหน้า 1 แล้วนำไปแสดงในตารางสรุป
        self.current_data = data

        # ── [เพิ่ม] เพิ่มค่า rooms ในลำดับให้ตรงกับ display_rows ──
        values = [
            data.get("room", ""),
            f"{data.get('rooms', 1)} room(s)",      # จำนวนห้อง
            f"${data.get('price', 0)}",
            data.get("name", ""),
            data.get("phone", ""),
            data.get("checkin", ""),
            data.get("checkout", ""),
            f"{data.get('nights', 0)} night(s)",
            f"{data.get('guests', 0)} guest(s)",
        ]

        for lbl, val in zip(self.val_labels, values):
            lbl.setText(val)

        self.total_label.setText(f"Total Amount:  ${data.get('total', 0)}")


class MainWindow(QMainWindow):
    """
    Main window — uses QStackedWidget to manage 2 pages
    """

    def __init__(self):
        # สร้างหน้าต่างหลัก และเพิ่มทั้ง 2 หน้าเข้า QStackedWidget
        super().__init__()
        self.setWindowTitle("CozyStay — Hotel Booking System")
        self.setMinimumSize(820, 680)
        self.resize(900, 720)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.booking_page = BookingPage()
        self.review_page = ReviewPage()

        self.stack.addWidget(self.booking_page)   # index 0
        self.stack.addWidget(self.review_page)    # index 1

        self.booking_page.next_btn.clicked.connect(self._go_to_review)
        self.review_page.back_btn.clicked.connect(self._go_to_booking)
        self.review_page.submit_btn.clicked.connect(self._on_submit)

        self.stack.setCurrentIndex(0)

        self.setStyleSheet("""
            QMainWindow { background-color: #f0f0ff; }
            QScrollArea  { background-color: transparent; }
            QWidget      {
                font-family: 'Segoe UI', 'Tahoma', sans-serif;
                background-color: #ffffff;
                color: #111111;
            }
            QLabel { background-color: transparent; color: #111111; }
            QLineEdit, QDateEdit, QSpinBox {
                background-color: #ffffff;
                color: #111111;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 13px;
            }
            QLineEdit:focus, QDateEdit:focus, QSpinBox:focus {
                border: 1px solid #6366f1;
            }
            QScrollArea { background-color: transparent; }
            QFrame { background-color: transparent; }
        """)

    def _go_to_review(self):
        # ดึงข้อมูลจากหน้า 1 แล้วสลับไปหน้า 2 (ถ้าข้อมูลครบถ้วน)
        data = self.booking_page.get_booking_data()
        if data is None:
            return
        self.review_page.load_data(data)
        self.stack.setCurrentIndex(1)

    def _go_to_booking(self):
        # สลับกลับไปหน้า 1
        self.stack.setCurrentIndex(0)

    def _on_submit(self):
        # แสดง popup ยืนยันการจอง แล้ว reset ฟอร์มและกลับหน้า 1
        name = self.review_page.current_data.get("name", "Guest")
        room = self.review_page.current_data.get("room", "Room")

        dlg = ConfirmDialog(name, room, self)
        dlg.exec()

        self.booking_page.clear_form()
        self.stack.setCurrentIndex(0)


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
