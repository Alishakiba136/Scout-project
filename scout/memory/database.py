from __future__ import annotations

import sqlite3
from pathlib import Path


def open_database(database_path: str | Path = "scout.db") -> sqlite3.Connection:
    """Open a local SQLite database for future memory subsystems."""
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.execute("CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT)")
    return connection
