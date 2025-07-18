import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path

DB_FOLDER = Path(__file__).parent  # folderul curent al fișierului db.py
DB_NAME = "history.db"
DB_PATH = DB_FOLDER / DB_NAME


def init_db():
    if not DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT,
                input TEXT,
                result TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()


def save_request(operation: str, input_val: str, result: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO requests (operation, input, result, timestamp)
        VALUES (?, ?, ?, ?)
    """, (operation, input_val, result, timestamp))
    conn.commit()
    conn.close()


def export_requests_to_txt(txt_path="requests_log.txt"):
    if DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM requests", conn)
        conn.close()
        Path(txt_path).write_text(df.to_string(index=False))
