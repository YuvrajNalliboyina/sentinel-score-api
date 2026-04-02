from fastapi import APIRouter
from app.schemas.transaction import TransactionRequest, TransactionResponse, ExplainResponse
from app.models.model import predict, explain
from app.database import log_prediction

router = APIRouter()

@router.post("/score", response_model=TransactionResponse)
def score_transaction(transaction: TransactionRequest):
    """
    Score a single transaction for fraud probability.
    Fast path — no SHAP, under 50ms.
    """
    features = transaction.model_dump()
    result = predict(features)
    
    # Log to database
    log_prediction(
        transaction_amt=features['TransactionAmt'],
        fraud_score=result['fraud_score'],
        decision=result['decision']
    )
    
    return result

@router.post("/explain", response_model=ExplainResponse)
def explain_transaction(transaction: TransactionRequest):
    """
    Score a transaction AND explain the top 3 reasons.
    Slow path — uses SHAP, takes 200-800ms.
    """
    features = transaction.model_dump()
    result = explain(features)
    
    # Log to database with reasons
    log_prediction(
        transaction_amt=features['TransactionAmt'],
        fraud_score=result['fraud_score'],
        decision=result['decision'],
        top_reasons=str(result['top_reasons'])
    )
    
    return result