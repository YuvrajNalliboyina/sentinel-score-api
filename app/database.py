import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data" / "predictions.db"

def init_db():
    """Create the predictions table if it doesn't exist."""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            transaction_amt REAL,
            fraud_score REAL,
            decision TEXT,
            top_reasons TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_prediction(transaction_amt: float, fraud_score: float, 
                   decision: str, top_reasons: str = None):
    """Log a prediction to the database."""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (timestamp, transaction_amt, fraud_score, decision, top_reasons)
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.utcnow().isoformat(), transaction_amt, fraud_score, decision, top_reasons))
    conn.commit()
    conn.close()

def get_recent_predictions(limit: int = 100) -> list:
    """Get the most recent predictions."""
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, transaction_amt, fraud_score, decision, top_reasons
        FROM predictions
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows