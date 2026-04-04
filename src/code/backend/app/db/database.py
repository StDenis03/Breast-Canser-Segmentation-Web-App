import sqlite3
from pathlib import Path
from contextlib import contextmanager
from app.core.config import settings

class Database:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        with self.get_connection() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS studies (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         filename TEXT NOT NULL, 
                         dicom_path TEXT NOT NULL,
                         png_path TEXT,
                         status TEXT DEFAULT 'pending',
                         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    
    @contextmanager
    def get_connection(self):
        #Возвращает соединение с БД
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
settings.DICOM_DIR.mkdir(parents=True, exist_ok=True)
settings.RESULTS_DIR.mkdir(parents=True, exist_ok=True)

db = Database(settings.DB_PATH)