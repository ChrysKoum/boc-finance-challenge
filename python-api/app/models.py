from pydantic import BaseModel, Field


class FinanceAskRequest(BaseModel):
    correlation_id: str = Field(..., alias="correlationId", min_length=1)
    question: str = Field(..., min_length=1)

    model_config = {
        "populate_by_name": True,
    }


class FinanceAskResponse(BaseModel):
    correlation_id: str = Field(..., alias="correlationId")
    answer: str
    blocked: bool

    model_config = {
        "populate_by_name": True,
    }
