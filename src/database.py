import sqlite3
from datetime import datetime

class PortDatabase:
    def __init__(self, db_name="ports.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS port_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME,
                    port INTEGER,
                    status TEXT,
                    is_authorized BOOLEAN
                )
            ''')

    def log_port_event(self, port, status, is_authorized=True):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                "INSERT INTO port_logs (timestamp, port, status, is_authorized) VALUES (?, ?, ?, ?)",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), port, status, is_authorized)
            )