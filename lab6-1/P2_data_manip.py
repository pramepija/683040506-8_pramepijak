import json
import pandas as pd
import pyqtgraph as pg

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt

# ══════════════════════════════════════════════════════════════════════════
#  CONSTANTS - do not change
# ══════════════════════════════════════════════════════════════════════════

REQUIRED_COLS = {"date", "city", "temp_c", "humidity", "rainfall_mm", "condition"}
CONDITIONS    = ["Sunny", "Cloudy", "Rainy", "Stormy"]
CITIES        = ["Bangkok", "Chiang Mai", "Phuket"]


# ══════════════════════════════════════════════════════════════════════════
#  YOUR WORK — complete the 6 functions below
# ══════════════════════════════════════════════════════════════════════════

def read_csv(path: str) -> pd.DataFrame:
    """
    To do 1 — Read a CSV file and return a clean DataFrame.
    - อ่านไฟล์ CSV
    - ตรวจว่ามีคอลัมน์ครบตาม REQUIRED_COLS
    - แปลงชนิดข้อมูลให้ถูกต้อง
    """
    df = pd.read_csv(path)

    # ตรวจสอบว่ามีคอลัมน์ครบ
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # แปลงชนิดข้อมูล
    df["date"]         = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["temp_c"]       = pd.to_numeric(df["temp_c"],       errors="coerce")
    df["humidity"]     = pd.to_numeric(df["humidity"],     errors="coerce")
    df["rainfall_mm"]  = pd.to_numeric(df["rainfall_mm"],  errors="coerce")
    df["condition"]    = df["condition"].astype(str).str.strip()
    df["city"]         = df["city"].astype(str).str.strip()

    return df.reset_index(drop=True)


def read_json(path: str) -> pd.DataFrame:
    """
    To do 2 — Read a JSON file and return a DataFrame.
    - อ่านไฟล์ JSON (list of records)
    - ตรวจคอลัมน์และแปลงชนิดข้อมูลเหมือน read_csv
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["date"]         = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df["temp_c"]       = pd.to_numeric(df["temp_c"],       errors="coerce")
    df["humidity"]     = pd.to_numeric(df["humidity"],     errors="coerce")
    df["rainfall_mm"]  = pd.to_numeric(df["rainfall_mm"],  errors="coerce")
    df["condition"]    = df["condition"].astype(str).str.strip()
    df["city"]         = df["city"].astype(str).str.strip()

    return df.reset_index(drop=True)


def write_csv(df: pd.DataFrame, path: str) -> None:
    """
    To do 3 — Save a DataFrame to a CSV file.
    - บันทึก DataFrame เป็น CSV โดยไม่เอา index
    """
    df.to_csv(path, index=False, encoding="utf-8")


def write_json(df: pd.DataFrame, path: str) -> None:
    """
    To do 4 — Save a DataFrame to a JSON file.
    - บันทึก DataFrame เป็น JSON แบบ list of records
    - indent=2 เพื่อให้อ่านง่าย
    """
    records = df.to_dict(orient="records")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)


def build_stats(df: pd.DataFrame) -> QTableWidget:
    """
    To do 5 — Return a QTableWidget showing summary statistics per city.
    คอลัมน์: City | Avg Temp | Avg Humidity | Total Rainfall | Records
    """
    # จัดกลุ่มตาม city แล้วคำนวณค่าสถิติ
    grouped = df.groupby("city").agg(
        avg_temp    =("temp_c",      "mean"),
        avg_humidity=("humidity",    "mean"),
        total_rain  =("rainfall_mm", "sum"),
        records     =("city",        "count"),
    ).reset_index()

    headers = ["City", "Avg Temp (°C)", "Avg Humidity (%)", "Total Rainfall (mm)", "Records"]

    table = QTableWidget(len(grouped), len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.verticalHeader().setVisible(False)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setAlternatingRowColors(True)

    for ri, row in grouped.iterrows():
        values = [
            row["city"],
            f"{row['avg_temp']:.1f}",
            f"{row['avg_humidity']:.1f}",
            f"{row['total_rain']:.1f}",
            str(row["records"]),
        ]
        for ci, val in enumerate(values):
            item = QTableWidgetItem(val)
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(ri, ci, item)

    table.resizeColumnsToContents()
    return table


def show_chart(df: pd.DataFrame, chart_type: str) -> pg.PlotWidget:
    """
    To do 6 — Draw a Rainfall Histogram per city using pyqtgraph.
    - แสดง bar chart ปริมาณฝนรวมแต่ละเมือง
    - สีแต่ละแท่งต่างกัน
    """
    # คำนวณฝนรวมต่อเมือง
    rain_by_city = df.groupby("city")["rainfall_mm"].sum()
    cities  = list(rain_by_city.index)
    values  = list(rain_by_city.values)

    # สีแต่ละเมือง (R, G, B)
    colors = [
        (70,  130, 220),   # Bangkok  — น้ำเงิน
        (60,  180, 100),   # Chiang Mai — เขียว
        (220, 120,  60),   # Phuket   — ส้ม
    ]

    plot = pg.PlotWidget()
    plot.setBackground("w")
    plot.setTitle("Total Rainfall by City (mm)", color="k", size="12pt")
    plot.setLabel("left",   "Rainfall (mm)", color="k")
    plot.setLabel("bottom", "City",          color="k")

    # วาด bar ทีละแท่ง
    bar_width = 0.6
    for i, (city, val) in enumerate(zip(cities, values)):
        r, g, b = colors[i % len(colors)]
        bar = pg.BarGraphItem(
            x=[i],
            height=[val],
            width=bar_width,
            brush=pg.mkBrush(r, g, b, 200),
            pen=pg.mkPen("k", width=1),
        )
        plot.addItem(bar)

    # ตั้ง x-axis label เป็นชื่อเมือง
    x_ticks = [(i, city) for i, city in enumerate(cities)]
    plot.getAxis("bottom").setTicks([x_ticks])
    plot.getAxis("bottom").setTextPen("k")
    plot.getAxis("left").setTextPen("k")

    return plot
