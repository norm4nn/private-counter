import sqlite3
from sqlite3 import Connection

from settings import APP_DIR

DB_PATH = APP_DIR / "private_counter.db"

def get_db_connection():
    """Create a new database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable row access by name
    return conn

def create_tables(conn: Connection):
    """Create necessary tables in the database."""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    print("[DB] Tables created or already exist.", flush=True)

def add_file(conn: Connection, file_path: str):
    """Add a file to the database."""
    cursor = conn.cursor()
    cursor.execute("INSERT INTO files (file_path) VALUES (?)", (file_path,))
    conn.commit()
    print(f"[DB] File added: {file_path}", flush=True)

def is_file_processed(conn: Connection, file_path: str) -> bool:
    """Check if a file has already been processed."""
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM files WHERE file_path = ?", (file_path,))
    res = cursor.fetchone()
    return res is not None
