
from fastapi import APIRouter, HTTPException, Request

from app.agent.orchestrator import run_agent
from app.data.repository import (
    get_customer,
    get_subscription,
    get_customer_analytics,
)
from app.rag.retriever import retrieve_customers
from app.schemas.requests import SearchRequest, ChatRequest
from app.schemas.responses import (
    HealthResponse,
    CustomerSearchResult,
    ChatResponse,
)
from app.services.analytics_service import (
    get_dataset_summary,
    get_segment_distribution,
    get_subscription_distribution,
    get_average_customer_metrics,
    get_customers_by_account_status,
)

router = APIRouter()


def get_dataframe(request: Request):
    """Get the dataset loaded during application startup."""
    df = getattr(request.app.state, "df", None)

    if df is None:
        raise HTTPException(
            status_code=503,
            detail="Customer dataset is not available.",
        )

    return df


@router.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "healthy"}


@router.post("/search", response_model=list[CustomerSearchResult])
def search_customers(search_request: SearchRequest, request: Request):
    """Search relevant customers using semantic similarity."""
    try:
        return retrieve_customers(
            search_request.query,
            limit=search_request.limit,
            df=get_dataframe(request),
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Customer search failed.",
        ) from exc


@router.post("/chat", response_model=ChatResponse)
def chat(chat_request: ChatRequest, request: Request):
    """Process a question using the AI agent and its available tools."""
    try:
        df = get_dataframe(request)
        answer = run_agent(chat_request.message, df)

        return {"answer": answer}

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Agent failed to process the question.",
        ) from exc


@router.get("/customers/{user_id}")
def customer_profile(user_id: str, request: Request):
    df = get_dataframe(request)
    customer = get_customer(df, user_id)

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found.",
        )

    return customer


@router.get("/customers/{user_id}/subscription")
def customer_subscription(user_id: str, request: Request):
    df = get_dataframe(request)
    subscription = get_subscription(df, user_id)

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found.",
        )

    return subscription


@router.get("/customers/{user_id}/metrics")
def customer_metrics(user_id: str, request: Request):
    df = get_dataframe(request)
    metrics = get_customer_analytics(df, user_id)

    if metrics is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found.",
        )

    return metrics


@router.get("/analytics/summary")
def analytics_summary(request: Request):
    return get_dataset_summary(get_dataframe(request))


@router.get("/analytics/segments")
def analytics_segments(request: Request):
    return get_segment_distribution(get_dataframe(request))


@router.get("/analytics/subscriptions")
def analytics_subscriptions(request: Request):
    return get_subscription_distribution(get_dataframe(request))


@router.get("/analytics/averages")
def analytics_averages(request: Request):
    return get_average_customer_metrics(get_dataframe(request))


@router.get("/analytics/account-status")
def analytics_account_status(request: Request):
    return get_customers_by_account_status(get_dataframe(request))
