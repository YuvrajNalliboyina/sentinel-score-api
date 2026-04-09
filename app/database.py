import os
import psycopg2
from datetime import datetime

# Use PostgreSQL if DATABASE_URL is set, otherwise fall back to SQLite
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_connection():
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    else:
        import sqlite3
        from pathlib import Path
        db_path = Path(__file__).parent.parent / "predictions.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(str(db_path))

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id SERIAL PRIMARY KEY,
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (timestamp, transaction_amt, fraud_score, decision, top_reasons)
        VALUES (%s, %s, %s, %s, %s)
    """, (datetime.utcnow().isoformat(), transaction_amt, fraud_score, decision, top_reasons))
    conn.commit()
    conn.close()

def get_recent_predictions(limit: int = 100) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, transaction_amt, fraud_score, decision, top_reasons
        FROM predictions
        ORDER BY id DESC
        LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows