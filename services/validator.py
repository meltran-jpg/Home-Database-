
from __future__ import annotations
import re
# Keep rules explicit and easy to audit.
BANNED_KEYWORDS = {"DROP", "DELETE", "ALTER", "TRUNCATE", "PRAGMA","ATTACH","DETACH","VACUUM","REPLACE",}
ALLOWED_PREFIXES = ("SELECT", "UPDATE")
#a simple validator to check that generated sqlcommands are safe to execute against our database
def validate_sql(query: str) -> tuple[bool, str]:
    # validate that the sql command is a safe read or update operation
    sql = query.strip()
    #
    if not sql:
        return False, "Query cannot be empty."
    statement_count = len([part for part in sql.split(";") if part.strip()])
    if statement_count > 1:
        return False, "Only one SQL statement is allowed per request."
    upper_sql = sql.upper()
    if not upper_sql.startswith(ALLOWED_PREFIXES):
        return False, "Only SELECT and UPDATE statements are allowed."
    for word in BANNED_KEYWORDS:
        if re.search(rf"\b{word}\b", upper_sql):
            return False, f"Unsafe keyword blocked: {word}."
    if upper_sql.startswith("UPDATE") and " WHERE " not in f" {upper_sql} ":
        return False, "UPDATE statements must include a WHERE clause."
    # if we pass all checks then the query is considered valid
    return True, "ok"