from pydantic import BaseModel, field_validator, Field
from typing import Optional, List

class TransactionRequest(BaseModel):
    TransactionAmt: float = Field(..., gt=0, le=50000, 
                                  description="Transaction amount must be between 0 and 50000")
    hour: Optional[float] = Field(default=0, ge=0, le=23)
    is_night: Optional[float] = Field(default=0, ge=0, le=1)
    is_weekend: Optional[float] = Field(default=0, ge=0, le=1)
    amt_zscore: Optional[float] = Field(default=0, ge=-10, le=10)
    amt_above_avg: Optional[float] = Field(default=0)
    txn_count_24h: Optional[float] = Field(default=1, ge=0)
    txn_count_1h: Optional[float] = Field(default=1, ge=0)
    amt_to_max_ratio: Optional[float] = Field(default=0.5, ge=0, le=1)
    amt_range: Optional[float] = Field(default=0, ge=0)

    @field_validator('TransactionAmt')
    @classmethod
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("TransactionAmt must be greater than 0")
        return round(v, 2)

class TransactionResponse(BaseModel):
    fraud_score: float
    decision: str

class ExplainResponse(BaseModel):
    fraud_score: float
    decision: str
    top_reasons: List[str]
#Why Pydantic:
#Pydantic validates incoming data automatically. If someone sends a request with TransactionAmt = "hello" instead of a number, Pydantic rejects it immediately with a clear error message before it ever reaches your model.
