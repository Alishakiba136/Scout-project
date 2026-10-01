from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class MemoryStore:
    """Generic local SQLite memory store for semantic, episodic, and people-related facts."""

    def __init__(self, database_path: str | Path = "scout.db") -> None:
        self.database_path = str(database_path)
        self.connection = sqlite3.connect(self.database_path)
        self.connection.row_factory = sqlite3.Row
        self._initialize()

    def _initialize(self) -> None:
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                fact TEXT NOT NULL,
                created_at TEXT NOT NULL,
                source TEXT DEFAULT 'system'
            )
            """
        )
        self.connection.commit()

    def remember(self, subject: str, fact: str, source: str = "system") -> dict[str, Any]:
        created_at = datetime.now(timezone.utc).isoformat()
        cursor = self.connection.execute(
            "INSERT INTO facts (subject, fact, created_at, source) VALUES (?, ?, ?, ?)",
            (subject, fact, created_at, source),
        )
        self.connection.commit()
        return {"id": cursor.lastrowid, "subject": subject, "fact": fact, "created_at": created_at, "source": source}

    def recall(self, subject: str | None = None, fact: str | None = None) -> list[dict[str, Any]]:
        query = "SELECT id, subject, fact, created_at, source FROM facts WHERE 1=1"
        params: list[Any] = []
        if subject is not None:
            query += " AND subject = ?"
            params.append(subject)
        if fact is not None:
            query += " AND fact LIKE ?"
            params.append(f"%{fact}%")
        query += " ORDER BY created_at DESC"
        rows = self.connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def list_facts(self) -> list[dict[str, Any]]:
        return self.recall()

    def close(self) -> None:
        self.connection.close()


def remember(store: MemoryStore, subject: str, fact: str, source: str = "system") -> dict[str, Any]:
    return store.remember(subject=subject, fact=fact, source=source)


def recall(store: MemoryStore, subject: str | None = None, fact: str | None = None) -> list[dict[str, Any]]:
    return store.recall(subject=subject, fact=fact)


def list_facts(store: MemoryStore) -> list[dict[str, Any]]:
    return store.list_facts()
