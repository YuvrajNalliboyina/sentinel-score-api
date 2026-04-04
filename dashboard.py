import streamlit as st
import pandas as pd
import sqlite3
import requests
from pathlib import Path
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="SentinelScore Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# API URL — local for now, Railway URL in Week 4
API_URL = "http://127.0.0.1:8000"

DB_PATH = Path(__file__).parent / "data" / "predictions.db"

def load_predictions():
    """Load predictions from SQLite."""
    try:
        conn = sqlite3.connect(str(DB_PATH))
        df = pd.read_sql_query("""
            SELECT timestamp, transaction_amt, fraud_score, decision
            FROM predictions
            ORDER BY timestamp DESC
        """, conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

# Header
st.title("🛡️ SentinelScore — Real-Time Fraud Detection")
st.markdown("Live transaction monitoring dashboard")
st.divider()

# Load data
df = load_predictions()

if df.empty:
    st.warning("No predictions yet. Score some transactions first.")
else:
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(df)
    fraud_count = len(df[df['decision'] == 'REJECT'])
    flag_count = len(df[df['decision'] == 'FLAG'])
    fraud_rate = round((fraud_count / total) * 100, 1)
    
    with col1:
        st.metric("Total Transactions", total)
    with col2:
        st.metric("Rejected", fraud_count)
    with col3:
        st.metric("Flagged", flag_count)
    with col4:
        st.metric("Fraud Rate", f"{fraud_rate}%")
    
    st.divider()
    
    # Fraud rate gauge
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Fraud Rate Gauge")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=fraud_rate,
            title={'text': "% Rejected"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkred"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "salmon"}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
    
    with col_right:
        st.subheader("Recent Alerts")
        alerts = df[df['decision'].isin(['REJECT', 'FLAG'])].head(10)
        if alerts.empty:
            st.info("No alerts yet.")
        else:
            st.dataframe(
                alerts[['timestamp', 'transaction_amt', 'fraud_score', 'decision']],
                use_container_width=True
            )
    
    st.divider()
    
    # Recent transactions table
    st.subheader("All Recent Transactions")
    st.dataframe(df.head(20), use_container_width=True)

st.divider()

# SHAP Explanation Viewer
st.subheader("🔬 Explain a Transaction")
st.markdown("Enter a transaction to see the top 3 reasons for the fraud decision.")

explain_amount = st.number_input("Transaction Amount ($) for Explanation", 
                                  min_value=0.01, max_value=50000.0, value=1500.0,
                                  key="explain_amount")
explain_zscore = st.number_input("Amount Z-Score", value=4.5, key="explain_zscore")
explain_txn_1h = st.number_input("Transactions in last hour", min_value=1, value=12,
                                  key="explain_txn")

if st.button("Explain Transaction", type="secondary"):
    payload = {
        "TransactionAmt": explain_amount,
        "amt_zscore": explain_zscore,
        "txn_count_1h": explain_txn_1h
    }
    
    try:
        response = requests.post(f"{API_URL}/api/v1/explain", json=payload)
        result = response.json()
        
        fraud_score = result['fraud_score']
        decision = result['decision']
        top_reasons = result['top_reasons']
        
        if decision == "REJECT":
            st.error(f"🚨 REJECTED — Fraud Score: {fraud_score}")
        elif decision == "FLAG":
            st.warning(f"⚠️ FLAGGED — Fraud Score: {fraud_score}")
        else:
            st.success(f"✅ APPROVED — Fraud Score: {fraud_score}")
        
        st.markdown("**Top 3 Reasons:**")
        for i, reason in enumerate(top_reasons, 1):
            st.markdown(f"{i}. {reason}")
            
    except Exception as e:
        st.error(f"API Error: {e}. Make sure the API is running.")
st.divider()

# Live scorer
st.subheader("🔍 Score a Transaction Live")
col_a, col_b = st.columns(2)

with col_a:
    amount = st.number_input("Transaction Amount ($)", min_value=0.01, value=100.0)
    hour = st.slider("Hour of Day", 0, 23, 12)
    is_night = 1 if hour < 6 else 0
    txn_count_1h = st.number_input("Transactions in last hour", min_value=1, value=1)

with col_b:
    amt_zscore = st.number_input("Amount Z-Score", value=0.0)
    amt_to_max_ratio = st.slider("Amount to Max Ratio", 0.0, 1.0, 0.5)
    is_weekend = st.checkbox("Weekend transaction")

if st.button("Score Transaction", type="primary"):
    payload = {
        "TransactionAmt": amount,
        "hour": hour,
        "is_night": is_night,
        "txn_count_1h": txn_count_1h,
        "amt_zscore": amt_zscore,
        "amt_to_max_ratio": amt_to_max_ratio,
        "is_weekend": int(is_weekend)
    }
    
    try:
        response = requests.post(f"{API_URL}/api/v1/score", json=payload)
        result = response.json()
        
        fraud_score = result['fraud_score']
        decision = result['decision']
        
        if decision == "REJECT":
            st.error(f"🚨 REJECTED — Fraud Score: {fraud_score}")
        elif decision == "FLAG":
            st.warning(f"⚠️ FLAGGED — Fraud Score: {fraud_score}")
        else:
            st.success(f"✅ APPROVED — Fraud Score: {fraud_score}")
            
    except Exception as e:
        st.error(f"API Error: {e}. Make sure the API is running.")