import os
import sqlite3
import logging
from typing import Set, List

logger = logging.getLogger(__name__)


class Database:
    def __init__(self) -> None:
        self.db_path: str = os.getenv("DB_PATH", "issues.db")
        self._init_db()
        logger.info(f"Initialized database at {self.db_path}")
        
    def _init_db(self) -> None:
        """Initialize database and create tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posted_issues (
                    issue_id INTEGER PRIMARY KEY,
                    issue_number INTEGER NOT NULL,
                    posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            
    def get_posted_issues(self) -> Set[int]:
        """Get set of posted issue IDs"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT issue_id FROM posted_issues")
            return {row[0] for row in cursor.fetchall()}
            
    def add_posted_issue(self, issue_id: int, issue_number: int) -> None:
        """Add new posted issue to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO posted_issues (issue_id, issue_number) VALUES (?, ?)",
                (issue_id, issue_number)
            )
            conn.commit()
            logger.info(f"Added issue #{issue_number} to database")
