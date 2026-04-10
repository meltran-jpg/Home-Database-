#database initialization script
from __future__ import annotations
from pathlib import Path
import sqlite3
# 
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "database" /"smarthome.db"
DEFAULT_SCHEMA_PATH = PROJECT_ROOT/ "database" / "schema.sql"
# function to initialize the database using the schema.sql file
def init_db(
    db_path: str| Path = DEFAULT_DB_PATH,
    schema_path: str | Path = DEFAULT_SCHEMA_PATH,
) -> None:
    #create or reset the SQLite database using schema.sql
    resolved_db_path = Path(db_path)
    resolved_schema_path = Path(schema_path)
    # read the schema.sql file and execute it against the SQLite database to create the necessary tables
    with resolved_schema_path.open("r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()
    #execute the schema SQL script to create the necessary tables
    with sqlite3.connect(resolved_db_path) as conn:
        cursor= conn.cursor()
        cursor.executescript(schema_sql)
        conn.commit()
if __name__ == "__main__":
    init_db()
    print("Database initialized.")