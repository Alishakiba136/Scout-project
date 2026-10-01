import sqlite3

from scout.memory.memory import MemoryStore, remember, recall, list_facts


def test_memory_store_round_trip_and_recall():
    store = MemoryStore(database_path=":memory:")
    store.remember(subject="Ali", fact="works as a robotics technician")
    rows = store.recall(subject="Ali")
    assert any("robotics technician" in row["fact"] for row in rows)


def test_memory_wrapper_functions_work_on_sqlite_db():
    store = MemoryStore(database_path=":memory:")
    remember(store, subject="Scout", fact="runs locally on-device")
    results = recall(store, subject="Scout")
    assert any("on-device" in item["fact"] for item in results)
    assert len(list_facts(store)) >= 1


def test_memory_store_uses_sqlite_schema():
    store = MemoryStore(database_path=":memory:")
    table_names = [row["name"] for row in store.connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    assert "facts" in table_names
    store.close()
