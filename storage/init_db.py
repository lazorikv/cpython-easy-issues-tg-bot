import sqlite3
from pathlib import Path


def init_db():
    db_path = Path("storage/issues.db")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posted_issues (
                issue_id INTEGER PRIMARY KEY,
                issue_number INTEGER NOT NULL,
                posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


if __name__ == "__main__":
    init_db()
