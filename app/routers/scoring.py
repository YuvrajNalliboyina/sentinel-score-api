from fastapi import APIRouter
from app.schemas.transaction import TransactionRequest, TransactionResponse, ExplainResponse
from app.models.model import predict, explain

router = APIRouter()

@router.post("/score", response_model=TransactionResponse)
def score_transaction(transaction: TransactionRequest):
    """
    Score a single transaction for fraud probability.
    Returns fraud_score between 0-1 and a decision of APPROVE/FLAG/REJECT.
    Fast path — no SHAP, under 50ms.
    """
    features = transaction.model_dump()
    result = predict(features)
    return result

@router.post("/explain", response_model=ExplainResponse)
def explain_transaction(transaction: TransactionRequest):
    """
    Score a transaction AND explain the top 3 reasons.
    Slow path — uses SHAP, takes 200-800ms.
    """
    features = transaction.model_dump()
    result = explain(features)
    return result