import sqlite3
from pathlib import Path

DB_PATH = str(Path(__file__).parent / "budget_optimizer.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS USERS (
            user_id   TEXT PRIMARY KEY,
            email     TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            is_active  INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS SUBSCRIPTIONS (
            subscription_id   TEXT PRIMARY KEY,
            user_id           TEXT NOT NULL,
            name              TEXT NOT NULL,
            cost              REAL NOT NULL,
            billing_frequency TEXT NOT NULL,
            renewal_date      TEXT NOT NULL,
            category          TEXT NOT NULL,
            is_active         INTEGER NOT NULL DEFAULT 1,
            created_at        TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES USERS(user_id)
        );

        CREATE TABLE IF NOT EXISTS BUDGETS (
            user_id           TEXT PRIMARY KEY,
            monthly_limit     REAL NOT NULL,
            warning_threshold REAL NOT NULL DEFAULT 80.0,
            created_at        TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES USERS(user_id)
        );

        CREATE TABLE IF NOT EXISTS FINANCIAL_SUMMARIES (
            user_id             TEXT PRIMARY KEY,
            subscription_costs  TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES USERS(user_id)
        );
    """)

    conn.commit()
    conn.close()