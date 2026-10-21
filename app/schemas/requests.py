
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=1000,
        description="Question or search query about customers",
    )
    limit: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of customers to retrieve",
    )


class CustomerRequest(BaseModel):
    user_id: str = Field(
        min_length=1,
        max_length=64,
        description="Unique customer ID",
    )


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
        description="Question asked to the AI assistant",
    )
