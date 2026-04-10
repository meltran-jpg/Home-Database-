
# this module defines the LLM adapter that translates natural language commands into SQL commands for safe execution against the smart home database
# uses simple pattern matching and normalization to handle common queries about devices and their statuses
# while ensuring that all generated SQL commands are parameterized to prevent injection attacks

from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class SQLCommand:
    # carries a sql statement and parameters for execution
    query: str
    params: tuple = ()
def _normalize_device_name(raw_name: str) -> str:
    # keep generated labels human-readable but consistent with seed data.
    return " ".join(part.capitalize() for part in raw_name.strip().split())


def nl_to_sql(command: str) -> SQLCommand:
    #translate a natural language command into a parameterized sql command
    cleaned= command.strip()
    lower = cleaned.lower()
    # handle some common queries with specific sql patterns
    #otherwise return a safe default query that shows all devices
    if not cleaned:
        # empty input  then fallback
        return SQLCommand("SELECT id, name, device_type, status FROM devices ORDER BY id")
    if "show devices"in lower or lower in {"list devices", "devices"}:
        return SQLCommand("SELECT id, name, device_type, status FROM devices ORDER BY id")
    if "show on devices" in lower or "show active devices" in lower:
        return SQLCommand(
            "SELECT id, name, device_type, status FROM devices WHERE status = ? ORDER BY id",("on",),
)
    if "show off devices" in lower or "show inactive devices" in lower:
        return SQLCommand(
            "SELECT id, name, device_type, status FROM devices WHERE status = ? ORDER BY id",("off",),
        )
    if "count devices" in lower or "how many devices" in lower:
        return SQLCommand("SELECT COUNT(*) AS device_count FROM devices")
    in_room_match = re.search(r"show devices in (?:the )?(.+)", lower)
    if in_room_match:
        room_name = _normalize_device_name(in_room_match.group(1))
        return SQLCommand(
            """
            SELECT d.id, d.name, d.device_type, d.status
            FROM devices d
            JOIN rooms r ON r.id = d.room_id
            WHERE r.name = ?
            ORDER BY d.id
            """.strip(),
            (room_name,),
        )
    # handle power commands 
    power_match = re.search(r"turn\s+(on|off)\s+(.+)", lower)
    if power_match:
        target_state = power_match.group(1)
        device_name = _normalize_device_name(power_match.group(2))
        return SQLCommand(
            "UPDATE devices SET status = ? WHERE name = ?",
            (target_state, device_name),
        )
    # fallback is intentionally read only and safe
    return SQLCommand("SELECT id, name, device_type, status FROM devices ORDER BY id")