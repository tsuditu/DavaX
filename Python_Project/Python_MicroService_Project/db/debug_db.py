import sqlite3
import pandas as pd
from pathlib import Path

DB_FOLDER = Path(__file__).parent
DB_PATH = DB_FOLDER / "history.db"

print(f"Database path: {DB_PATH}\n")

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query("SELECT * FROM requests", conn)
print("\nDatabase content:")
print(df.to_string(index=False))

conn.close()
