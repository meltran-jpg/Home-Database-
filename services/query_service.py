
# connects to the SQLite database
#validates that the SQL command is a safe read or update operation
from __future__ import annotations
from pathlib import Path
import sqlite3
from typing import Any
from services.llm_adapter import SQLCommand
from services.validator import validate_sql
# defines a function to execute a SQL command against the SQLite database and return results in a structured format for the cli to display
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "database" / "smarthome.db"
#helper function
def _to_row_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]
# 
def run_query(command: SQLCommand | str, db_path: str | Path | None = None) -> dict[str, Any]:
    #validate and execute a SQL command to SQLite
    #returns a structured dictionary so the CLI can display clear output
    if isinstance(command, str):
        sql_command = SQLCommand(command, ())
    else:
        sql_command = command
    # validate that the SQL command is a safe read or update operation before executing
    is_valid, reason = validate_sql(sql_command.query)
    if not is_valid:
        return {"ok": False, "error": reason, "results": []}
    # connect to the sql database and execute the command
    resolved_db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
    try:
        with sqlite3.connect(resolved_db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(sql_command.query, sql_command.params)
            # 
            if sql_command.query.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall()
                return {"ok": True, "error": None, "results": _to_row_dicts(rows),"rows_affected": 0,}
# for non select types of queries --> return success and number of rows affected
            conn.commit()
            return {"ok": True, "error": None, "results": [], "rows_affected": cursor.rowcount,}
    except sqlite3.Error as exc:
        return {"ok": False, "error": f"Database error: {exc}", "results": []}