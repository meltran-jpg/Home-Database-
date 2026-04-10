#CSV data loader for the smart home database
from __future__ import annotations
import csv
from pathlib import Path
import sqlite3
# 
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "database" / "smarthome.db"
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "devices.csv"
# function to load devices from csv into the database-->returns number of inserted rows
def load_devices(
    db_path: str | Path = DEFAULT_DB_PATH,
    csv_path: str | Path = DEFAULT_CSV_PATH,
) -> int:
    #load devices from csv and return number of inserted rows
    inserted= 0
    resolved_db_path = Path(db_path)
    resolved_csv_path = Path(csv_path)
    # open the csv file and read it using csv.DictReader, then insert each row into the devices table in the database
    with resolved_csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        # connect to the database and insert each row into the devices table, using INSERT OR IGNORE to avoid duplicates
        with sqlite3.connect(resolved_db_path) as conn:
            cursor = conn.cursor()
            for row in reader:
                cursor.execute(
                    """INSERT OR IGNORE INTO devices (name, room_id, device_type, status) VALUES (?, ?, ?, ?)""",
                    (
                        row["name"].strip(),
                        int(row["room_id"]),
                        row["device_type"].strip(),
                        row.get("status", "off").strip().lower(),
                    ),
                )
                inserted += cursor.rowcount
            conn.commit()
    return inserted
#when run as a script -->load the devices and print the number of inserted rows
if __name__ == "__main__":
    count = load_devices()
    print(f"Loaded {count} device rows.")