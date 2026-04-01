from pydantic import BaseModel
from typing import Optional

class TransactionRequest(BaseModel):
    TransactionAmt: float
    hour: Optional[float] = 0
    is_night: Optional[float] = 0
    is_weekend: Optional[float] = 0
    amt_zscore: Optional[float] = 0
    amt_above_avg: Optional[float] = 0
    txn_count_24h: Optional[float] = 1
    txn_count_1h: Optional[float] = 1
    amt_to_max_ratio: Optional[float] = 0.5
    amt_range: Optional[float] = 0

class TransactionResponse(BaseModel):
    fraud_score: float
    decision: str