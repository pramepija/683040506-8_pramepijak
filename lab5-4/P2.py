import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QComboBox, QSlider, QSpinBox, QPushButton, QHBoxLayout,
    QVBoxLayout, QFormLayout, QProgressBar, QStatusBar,
    QAction, QToolBar, QFileDialog, QMessageBox, QFrame,
    QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon



class CharacterSheet(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(250)
        self.setStyleSheet("background-color: #1a1a2e; border: none;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Name
        self.name_label = QLabel("— Character Name —")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setStyleSheet(
            "color: #c9a84c; font-family: Georgia; font-size: 15px; font-weight: bold;"
        )
        layout.addWidget(self.name_label)

        # Sub (Race • Class)
        self.sub_label = QLabel("Race  •  Class")
        self.sub_label.setAlignment(Qt.AlignCenter)
        self.sub_label.setStyleSheet(
            "color: #9994cc; font-family: Georgia; font-size: 12px; font-style: italic;"
        )
        layout.addWidget(self.sub_label)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #3a3860;")
        layout.addWidget(line)

        # Stat bars
        self.stat_bars = {}
        self.stat_nums = {}
        stat_icons = {"STR": "💪", "DEX": "🏃", "INT": "🧠", "VIT": "❤️"}

        for stat in ["STR", "DEX", "INT", "VIT"]:
            row = QHBoxLayout()
            row.setSpacing(2)

            lbl = QLabel(f"{stat_icons[stat]} {stat}")
            lbl.setFixedWidth(60)
            lbl.setStyleSheet(
                "color: #9994cc; font-family: Georgia; font-size: 11px; font-weight: bold;"
            )
            row.addWidget(lbl)

            bar = QProgressBar()
            bar.setRange(0, 20)
            bar.setValue(0)
            bar.setTextVisible(False)
            bar.setFixedHeight(10)
            bar.setStyleSheet("""
                QProgressBar {
                    background-color: #2a2850;
                    border-radius: 5px;
                    border: none;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5b4fcf, stop:1 #9b8fe8);
                    border-radius: 5px;
                }
            """)
            row.addWidget(bar, 1)

            num = QLabel("—")
            num.setFixedWidth(24)
            num.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            num.setStyleSheet(
                "color: #e0ddf8; font-family: Georgia; font-size: 11px; font-weight: bold;"
            )
            row.addWidget(num)

            self.stat_bars[stat] = bar
            self.stat_nums[stat] = num

            container = QWidget()
            container.setLayout(row)
            container.setStyleSheet("background: transparent;")
            layout.addWidget(container)

        layout.addStretch()

    def update_sheet(self, name, race, cls, stats: dict, show_values=False):
        self.name_label.setText(f"— {name or 'Character Name'} —")
        r = race if race else "Race"
        c = cls if cls else "Class"
        self.sub_label.setText(f"{r}  •  {c}")

        for stat, val in stats.items():
            self.stat_bars[stat].setValue(val)
            self.stat_nums[stat].setText(str(val) if show_values else "—")

    def clear(self):
        self.name_label.setText("— Character Name —")
        self.sub_label.setText("Race  •  Class")
        for stat in ["STR", "DEX", "INT", "VIT"]:
            self.stat_bars[stat].setValue(0)
            self.stat_nums[stat].setText("—")



class RPGBuilder(QMainWindow):
    MAX_POINTS = 40
    DEFAULT_STAT = 5

    def __init__(self):
        super().__init__()
        self.setWindowTitle("RPG Character Builder")
        self.setMinimumWidth(760)

        self._build_menu()
        self._build_toolbar()
        self._build_central()
        self._build_statusbar()

        self.update_points_display()

    # ── Menu Bar ──────────────────────────────
    def _build_menu(self):
        mb = self.menuBar()

        # Game menu
        game_menu = mb.addMenu("Game")
        act_new = QAction("📄  New Character", self)
        act_new.triggered.connect(self.new_character)
        act_gen = QAction("⚔️  Generate Sheet", self)
        act_gen.triggered.connect(self.generate_sheet)
        act_save = QAction("💾  Save Sheet", self)
        act_save.triggered.connect(self.save_sheet)
        act_exit = QAction("🚪  Exit", self)
        act_exit.triggered.connect(self.close)
        game_menu.addAction(act_new)
        game_menu.addAction(act_gen)
        game_menu.addAction(act_save)
        game_menu.addSeparator()
        game_menu.addAction(act_exit)

        # Edit menu
        edit_menu = mb.addMenu("Edit")
        act_reset = QAction("🔄  Reset Stats", self)
        act_reset.triggered.connect(self.reset_stats)
        act_rand = QAction("🎲  Randomize", self)
        act_rand.triggered.connect(self.randomize)
        edit_menu.addAction(act_reset)
        edit_menu.addAction(act_rand)

    # ── Toolbar ───────────────────────────────
    def _build_toolbar(self):
        tb = QToolBar("Main Toolbar")
        tb.setIconSize(QSize(16, 16))
        tb.setMovable(False)
        self.addToolBar(tb)

        def make_action(icon, label, slot):
            act = QAction(f"{icon}  {label}", self)
            act.triggered.connect(slot)
            return act

        tb.addAction(make_action("📄", "New", self.new_character))
        tb.addAction(make_action("⚔️", "Generate", self.generate_sheet))
        tb.addSeparator()
        tb.addAction(make_action("🎲", "Randomize", self.randomize))
        tb.addSeparator()
        tb.addAction(make_action("💾", "Save", self.save_sheet))

    # ── Central Widget ────────────────────────
    def _build_central(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Left Panel ──
        left = QWidget()
        left.setStyleSheet("background-color: #f5f3f0;")
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(16, 16, 16, 16)
        left_layout.setSpacing(8)

        # Form fields
        form = QFormLayout()
        form.setSpacing(8)
        form.setLabelAlignment(Qt.AlignRight)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter character name...")
        self.name_edit.textChanged.connect(self.on_form_changed)
        form.addRow("Character Name:", self.name_edit)

        self.race_combo = QComboBox()
        self.race_combo.addItems(["Choose race", "Human", "Elf", "Dwarf", "Orc", "Undead"])
        self.race_combo.currentIndexChanged.connect(self.on_form_changed)
        form.addRow("Race:", self.race_combo)

        self.class_combo = QComboBox()
        self.class_combo.addItems(["Choose class", "Warrior", "Mage", "Rogue", "Paladin", "Ranger"])
        self.class_combo.currentIndexChanged.connect(self.on_form_changed)
        form.addRow("Class:", self.class_combo)

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Choose gender", "Male", "Female", "Other"])
        form.addRow("Gender:", self.gender_combo)

        left_layout.addLayout(form)

        # Stat Allocation label
        stat_title = QLabel("⚡ Stat Allocation")
        stat_title.setStyleSheet(
            "color: #5b4fcf; font-weight: bold; font-size: 16px; font-family: Georgia;"
        )
        left_layout.addWidget(stat_title)

        # Stat rows
        self.sliders = {}
        self.spinboxes = {}
        stat_icons = {"STR": "💪", "DEX": "🏃", "INT": "🧠", "VIT": "❤️"}

        for stat in ["STR", "DEX", "INT", "VIT"]:
            row = QHBoxLayout()
            row.setSpacing(3)

            icon_lbl = QLabel(f"{stat_icons[stat]}  {stat}")
            icon_lbl.setFixedWidth(60)
            icon_lbl.setStyleSheet("font-size: 13px; font-weight: bold;")
            row.addWidget(icon_lbl)

            slider = QSlider(Qt.Horizontal)
            slider.setRange(1, 20)
            slider.setValue(self.DEFAULT_STAT)
            slider.setStyleSheet("""
                QSlider::groove:horizontal {
                    height: 6px; background: #ddd; border-radius: 3px;
                }
                QSlider::handle:horizontal {
                    background: #5b4fcf; width: 14px; height: 14px;
                    margin: -4px 0; border-radius: 7px;
                }
                QSlider::sub-page:horizontal {
                    background: #5b4fcf; border-radius: 3px;
                }
            """)
            row.addWidget(slider, 1)

            spin = QSpinBox()
            spin.setRange(1, 20)
            spin.setValue(self.DEFAULT_STAT)
            spin.setFixedWidth(52)
            row.addWidget(spin)

            # Connect slider ↔ spinbox
            slider.valueChanged.connect(lambda v, sp=spin: sp.setValue(v))
            spin.valueChanged.connect(lambda v, sl=slider: sl.setValue(v))
            slider.valueChanged.connect(self.update_points_display)

            self.sliders[stat] = slider
            self.spinboxes[stat] = spin

            container = QWidget()
            container.setLayout(row)
            left_layout.addWidget(container)

        # Points used label
        self.points_label = QLabel("Points used: 20 / 40")
        self.points_label.setStyleSheet("font-size: 13px;")
        left_layout.addWidget(self.points_label)

        # Generate button
        self.gen_btn = QPushButton("⚔️  Generate Character Sheet")
        self.gen_btn.setFixedHeight(36)
        self.gen_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e8e3ff, stop:1 #d0c8f8);
                border: 1px solid #a89ee8;
                color: #5b4fcf;
                font-family: Georgia;
                font-size: 13px;
                font-weight: bold;
                border-radius: 3px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d0c8f8, stop:1 #b8aef0);
            }
            QPushButton:pressed { background: #a89ee8; }
        """)
        self.gen_btn.clicked.connect(self.generate_sheet)
        left_layout.addWidget(self.gen_btn)

        left_layout.addStretch()

        # ── Right Panel ──
        self.sheet = CharacterSheet()

        # Separator line
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet("color: #d0ccc4;")

        main_layout.addWidget(left, 1)
        main_layout.addWidget(sep)
        main_layout.addWidget(self.sheet)

    # ── Status Bar ────────────────────────────
    def _build_statusbar(self):
        sb = QStatusBar()
        self.setStatusBar(sb)
        self.status_temp = QLabel("Ready — create your character.")
        self.status_perm = QLabel("Created by Student")
        self.status_perm.setStyleSheet("color: gray; font-style: italic;")
        sb.addWidget(self.status_temp, 1)
        sb.addPermanentWidget(self.status_perm)

    # ── Helpers ───────────────────────────────
    def set_status(self, msg, color="black"):
        self.status_temp.setText(msg)
        self.status_temp.setStyleSheet(f"color: {color};")

    def total_points(self):
        return sum(self.sliders[s].value() for s in ["STR", "DEX", "INT", "VIT"])

    def update_points_display(self):
        total = self.total_points()
        self.points_label.setText(f"Points used: {total} / {self.MAX_POINTS}")
        color = "#c0392b" if total > self.MAX_POINTS else "black"
        self.points_label.setStyleSheet(f"font-size: 13px; color: {color};")
        # Update sheet bars live (no numbers yet)
        self.on_form_changed()

    def get_stats(self):
        return {s: self.sliders[s].value() for s in ["STR", "DEX", "INT", "VIT"]}

    def on_form_changed(self):
        name = self.name_edit.text().strip()
        race = self.race_combo.currentText() if self.race_combo.currentIndex() > 0 else ""
        cls  = self.class_combo.currentText() if self.class_combo.currentIndex() > 0 else ""
        self.sheet.update_sheet(name, race, cls, self.get_stats(), show_values=False)

    # ── Actions ───────────────────────────────
    def new_character(self):
        self.name_edit.clear()
        self.race_combo.setCurrentIndex(0)
        self.class_combo.setCurrentIndex(0)
        self.gender_combo.setCurrentIndex(0)
        self.reset_stats()
        self.sheet.clear()
        self.set_status("New character — all fields reset.", "black")

    def reset_stats(self):
        for stat in ["STR", "DEX", "INT", "VIT"]:
            self.sliders[stat].setValue(self.DEFAULT_STAT)
            self.spinboxes[stat].setValue(self.DEFAULT_STAT)
        self.update_points_display()
        self.set_status("Stats reset to default (5).", "#27ae60")

    def randomize(self):
        names = ["Aelthar", "Brimok", "Cyvara", "Drath", "Elyndra",
                 "Fargoth", "Gwen", "Halvard", "Ixara", "Jorin"]
        races = ["Human", "Elf", "Dwarf", "Orc", "Undead"]
        classes = ["Warrior", "Mage", "Rogue", "Paladin", "Ranger"]
        genders = ["Male", "Female", "Other"]

        self.name_edit.setText(random.choice(names))
        self.race_combo.setCurrentText(random.choice(races))
        self.class_combo.setCurrentText(random.choice(classes))
        self.gender_combo.setCurrentText(random.choice(genders))

        # Random stats with total <= 40
        vals = [1, 1, 1, 1]
        pool = self.MAX_POINTS - 4
        for _ in range(pool):
            i = random.randint(0, 3)
            if vals[i] < 20:
                vals[i] += 1

        for i, stat in enumerate(["STR", "DEX", "INT", "VIT"]):
            self.sliders[stat].setValue(vals[i])
            self.spinboxes[stat].setValue(vals[i])

        self.update_points_display()
        self.set_status("Character randomized!", "#27ae60")

    def generate_sheet(self):
        name = self.name_edit.text().strip()
        if not name:
            self.set_status("⚠ Please enter a character name!", "#c0392b")
            return
        if self.race_combo.currentIndex() == 0:
            self.set_status("⚠ Please choose a race!", "#c0392b")
            return
        if self.class_combo.currentIndex() == 0:
            self.set_status("⚠ Please choose a class!", "#c0392b")
            return

        total = self.total_points()
        if total > self.MAX_POINTS:
            self.set_status(
                f"⚠ Total points ({total}) exceed {self.MAX_POINTS}! Reduce stats.", "#c0392b"
            )
            return

        race = self.race_combo.currentText()
        cls  = self.class_combo.currentText()
        self.sheet.update_sheet(name, race, cls, self.get_stats(), show_values=True)
        self.set_status(f"✔ Character sheet generated for {name}!", "#27ae60")

    def save_sheet(self):
        name   = self.name_edit.text().strip() or "Unknown"
        race   = self.race_combo.currentText() if self.race_combo.currentIndex() > 0 else "Unknown"
        cls    = self.class_combo.currentText() if self.class_combo.currentIndex() > 0 else "Unknown"
        gender = self.gender_combo.currentText() if self.gender_combo.currentIndex() > 0 else "Unknown"
        stats  = self.get_stats()
        total  = self.total_points()

        text = (
            "=== RPG CHARACTER SHEET ===\n"
            f"Name:   {name}\n"
            f"Race:   {race}\n"
            f"Class:  {cls}\n"
            f"Gender: {gender}\n\n"
            "--- STATS ---\n"
            f"STR: {stats['STR']}\n"
            f"DEX: {stats['DEX']}\n"
            f"INT: {stats['INT']}\n"
            f"VIT: {stats['VIT']}\n"
            f"Total: {total} / {self.MAX_POINTS}\n\n"
            "Generated by RPG Character Builder\n"
            "Created by Student\n"
        )

        path, _ = QFileDialog.getSaveFileName(
            self, "Save Character Sheet", f"{name.replace(' ', '_')}_sheet.txt",
            "Text Files (*.txt)"
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            self.set_status(f"✔ Saved: {path}", "#27ae60")
        else:
            self.set_status("Save cancelled.", "gray")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = RPGBuilder()
    window.show()
    sys.exit(app.exec_())
