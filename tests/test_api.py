from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_score_valid_transaction():
    response = client.post("/api/v1/score", json={
        "TransactionAmt": 100.0
    })
    assert response.status_code == 200
    data = response.json()
    assert "fraud_score" in data
    assert "decision" in data
    assert 0 <= data["fraud_score"] <= 1
    assert data["decision"] in ["APPROVE", "FLAG", "REJECT"]

def test_score_negative_amount():
    response = client.post("/api/v1/score", json={
        "TransactionAmt": -100.0
    })
    assert response.status_code == 422

def test_score_zero_amount():
    response = client.post("/api/v1/score", json={
        "TransactionAmt": 0
    })
    assert response.status_code == 422

def test_score_invalid_hour():
    response = client.post("/api/v1/score", json={
        "TransactionAmt": 100.0,
        "hour": 25
    })
    assert response.status_code == 422

def test_explain_valid_transaction():
    response = client.post("/api/v1/explain", json={
        "TransactionAmt": 1500.0,
        "amt_zscore": 4.5,
        "txn_count_1h": 12
    })
    assert response.status_code == 200
    data = response.json()
    assert "fraud_score" in data
    assert "decision" in data
    assert "top_reasons" in data
    assert len(data["top_reasons"]) == 3