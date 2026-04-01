from fastapi import APIRouter
from app.schemas.transaction import TransactionRequest, TransactionResponse
from app.models.model import predict

router = APIRouter()

@router.post("/score", response_model=TransactionResponse)
def score_transaction(transaction: TransactionRequest):
    """
    Score a single transaction for fraud probability.
    Returns fraud_score between 0-1 and a decision of APPROVE/FLAG/REJECT.
    """
    features = transaction.model_dump()
    result = predict(features)
    return result