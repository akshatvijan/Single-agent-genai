
from typing import Any

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class ErrorResponse(BaseModel):
    detail: str



class CustomerSearchResult(BaseModel):
    user_id: str | None = None
    customer_segment: str | None = None
    account_status: str | None = None
    similarity_score: float | None = None

    PlanName: str | None = None
    SubscriptionStatus: str | None = None
    TenureDays: int | None = None
    InvoiceCount: int | None = None
    NetRevenuePaise: float | None = None
    PlanInterval: str | None = None



class ChatResponse(BaseModel):
    answer: str


class AnalyticsResponse(BaseModel):
    data: dict[str, Any]
