import sqlite3
import json
from datetime import datetime
from contextlib import contextmanager

DB_PATH = "clinical_vault.db"

def init_db():
    """Initializes the database with optimized PRAGMA settings and indices."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Enable Write-Ahead Logging for high-concurrency (Fast reads during writes)
        cursor.execute("PRAGMA journal_mode=WAL;")
        cursor.execute("PRAGMA synchronous=NORMAL;")

        # PILLAR: ENGINE - Core Clinical Data Store
        cursor.execute('''CREATE TABLE IF NOT EXISTS clinical_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_uuid TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            phq9_score REAL,
            q9_trigger INTEGER DEFAULT 0,
            sentiment_score REAL,
            velocity_delta REAL DEFAULT 0.0,
            metadata_json TEXT
        )''')

        # PILLAR: CARE - Clinician Audit & Action Logs (HIPAA Compliance)
        cursor.execute('''CREATE TABLE IF NOT EXISTS clinical_audit_trail (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clinician_id TEXT NOT NULL,
            action_type TEXT NOT NULL,
            target_uuid TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        # HIGH PERFORMANCE: Indices for sub-millisecond lookups on large datasets
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_uuid ON clinical_entries (user_uuid);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_time ON clinical_entries (timestamp);")
        
        conn.commit()

@contextmanager
def get_db_connection():
    """Connection factory using a context manager for safe resource handling."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
    conn.row_factory = sqlite3.Row  # Access columns by name
    try:
        yield conn
    finally:
        conn.close()

def log_entry(user_uuid, score, q9, sentiment, velocity, metadata):
    """Atomic write for new patient data."""
    with get_db_connection() as conn:
        conn.execute('''INSERT INTO clinical_entries 
            (user_uuid, phq9_score, q9_trigger, sentiment_score, velocity_delta, metadata_json) 
            VALUES (?, ?, ?, ?, ?, ?)''', 
            (user_uuid, score, q9, sentiment, velocity, json.dumps(metadata)))
        conn.commit()
    # Save current
    cursor.execute("INSERT INTO entries (user_id, timestamp, score, data) VALUES (?, ?, ?, ?)",
                   (user_id, datetime.now().isoformat(), score, json.dumps(data)))
    # Get last 5 for slope analysis
    cursor.execute("SELECT score FROM entries WHERE user_id = ? ORDER BY timestamp DESC LIMIT 6", (user_id,))
    history = [row[0] for row in cursor.fetchall()[1:]] # Exclude the one we just added
    conn.commit()
    conn.close()
    return history
