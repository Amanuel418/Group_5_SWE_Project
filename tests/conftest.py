import pytest
import sqlite3
import database


@pytest.fixture(autouse=True)
def use_in_memory_db(monkeypatch, tmp_path):
    """
    Redirect every test to a fresh in-memory SQLite database
    so tests never touch the real budget_optimizer.db file.
    """
    db_file = str(tmp_path / "test.db")
    monkeypatch.setattr(database, "DB_PATH", db_file)
    database.init_db()
    yield