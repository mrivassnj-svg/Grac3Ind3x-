import sqlite3
import json

DB_PATH = "clinical_vault.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Table for entries
    cursor.execute('''CREATE TABLE IF NOT EXISTS entries 
        (id INTEGER PRIMARY KEY, user_id TEXT, timestamp TEXT, score REAL, data TEXT)''')
    # Table for clinician audit logs
    cursor.execute('''CREATE TABLE IF NOT EXISTS audit_logs 
        (id INTEGER PRIMARY KEY, clinician_id TEXT, action TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def save_entry_and_get_history(user_id, score, data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Save current
    cursor.execute("INSERT INTO entries (user_id, timestamp, score, data) VALUES (?, ?, ?, ?)",
                   (user_id, datetime.now().isoformat(), score, json.dumps(data)))
    # Get last 5 for slope analysis
    cursor.execute("SELECT score FROM entries WHERE user_id = ? ORDER BY timestamp DESC LIMIT 6", (user_id,))
    history = [row[0] for row in cursor.fetchall()[1:]] # Exclude the one we just added
    conn.commit()
    conn.close()
    return history
