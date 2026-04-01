from pydantic import BaseModel
from typing import Optional, List

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

class ExplainResponse(BaseModel):
    fraud_score: float
    decision: str
    top_reasons: List[str]
#Why Pydantic:
#Pydantic validates incoming data automatically. If someone sends a request with TransactionAmt = "hello" instead of a number, Pydantic rejects it immediately with a clear error message before it ever reaches your model.
