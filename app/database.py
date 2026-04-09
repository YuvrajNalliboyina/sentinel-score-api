import os
import sqlite3
from pathlib import Path
from datetime import datetime

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_connection():
    if DATABASE_URL:
        import psycopg2
        return psycopg2.connect(DATABASE_URL), '%s'
    else:
        db_path = Path(__file__).parent.parent / "predictions.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(str(db_path)), '?'

def init_db():
    conn, ph = get_connection()
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
    conn, ph = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        INSERT INTO predictions (timestamp, transaction_amt, fraud_score, decision, top_reasons)
        VALUES ({ph}, {ph}, {ph}, {ph}, {ph})
    """, (datetime.utcnow().isoformat(), transaction_amt, fraud_score, decision, top_reasons))
    conn.commit()
    conn.close()

def get_recent_predictions(limit: int = 100) -> list:
    conn, ph = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT timestamp, transaction_amt, fraud_score, decision, top_reasons
        FROM predictions
        ORDER BY id DESC
        LIMIT {ph}
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows