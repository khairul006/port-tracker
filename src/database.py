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
                    service TEXT,
                    product TEXT,
                    version TEXT,
                    cpe TEXT,
                    scripts_output TEXT,
                    is_authorized BOOLEAN
                )
            ''')

    def log_port_event(self, port, status, audit_data=None, is_authorized=True):
        # If no audit_data is passed, we use empty strings to avoid errors
        if audit_data is None:
            audit_data = {}

        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''
                INSERT INTO port_logs 
                (timestamp, port, status, service, product, version, cpe, scripts_output, is_authorized) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                port,
                status,
                audit_data.get('service', 'unknown'),
                audit_data.get('product', 'unknown'),
                audit_data.get('version', 'unknown'),
                audit_data.get('cpe', ''),
                audit_data.get('script', ''), # This is the Nmap script output
                is_authorized
            ))