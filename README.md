# sentinel-score-api

# 🛡️ SentinelScore — Real-Time Transaction Fraud Scoring API

![CI/CD](https://github.com/YuvrajNalliboyina/sentinel-score-api/actions/workflows/deploy.yml/badge.svg)

> A production-grade fraud detection system that scores financial transactions in real-time, explains every decision via SHAP, and deploys automatically via CI/CD.

## 🔴 Live Demo
- **API:** https://sentinelscore-api-production.up.railway.app/docs
- **Dashboard:** https://huggingface.co/spaces/YuvrajN/sentinelscore-dahboard

## 🏗️ Architecture
Transaction Request (JSON)
↓
Input Validation (FastAPI + Pydantic)
↓
XGBoost Fraud Scoring (<50ms)
↓
Decision: APPROVE / FLAG / REJECT
↓
SHAP Explanation (async)
↓
SQLite Logging → Streamlit Dashboard

## ⚡ Quick Test
```bash
curl -X POST https://sentinelscore-api-production.up.railway.app/api/v1/score \
  -H "Content-Type: application/json" \
  -d '{"TransactionAmt": 1500, "amt_zscore": 4.5, "txn_count_1h": 12}'
```

## 🧠 Tech Stack

| Layer | Tools |
|-------|-------|
| ML Model | XGBoost (AUC: 0.9610) |
| Explainability | SHAP |
| Experiment Tracking | MLflow |
| API | FastAPI + Pydantic |
| Dashboard | Streamlit + Plotly |
| Drift Detection | Evidently |
| Containerization | Docker |
| Deployment | Railway (API) + HuggingFace (Dashboard) |
| CI/CD | GitHub Actions |
| Testing | pytest (6/6 passing) |

## 📊 Model Performance

| Metric | Value |
|--------|-------|
| AUC-ROC | 0.9610 |
| F1 Score | 0.5047 |
| Training Data | 590,540 IEEE-CIS transactions |
| Fraud Rate | 3.5% (class imbalance handled with SMOTE) |

## 🚀 Run Locally
```bash
git clone https://github.com/YuvrajNalliboyina/sentinel-score-api
cd sentinel-score-api
conda create -n sentinelscore python=3.10
conda activate sentinelscore
pip install -r requirements.prod.txt
uvicorn app.main:app --reload
```

## 🏗️ Project Structure
sentinel-score-api/
├── app/
│   ├── main.py          # FastAPI app
│   ├── routers/         # API endpoints
│   ├── schemas/         # Pydantic models
│   └── models/          # XGBoost inference
├── notebooks/           # Training pipeline
├── tests/               # pytest suite
├── dashboard.py         # Streamlit dashboard
├── Dockerfile
└── .github/workflows/   # CI/CD pipeline