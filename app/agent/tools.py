
from app.rag.retriever import retrieve_customers
from app.rag.milvus_store import (
    COLLECTION_NAME,
    get_milvus_client,
)
from app.data.repository import (
    get_customer,
    get_subscription,
    get_customer_analytics,
)


def search_customers(query: str, limit: int = 5):
    """Search customers using semantic similarity."""
    return retrieve_customers(query, limit=limit)


def get_customer_by_id(user_id: str):
    """Check whether an exact customer ID exists in Milvus."""
    if not isinstance(user_id, str) or not user_id.strip():
        return None

    client = get_milvus_client()

    try:
        results = client.query(
            collection_name=COLLECTION_NAME,
            filter=f'user_id == "{user_id.strip()}"',
            output_fields=[
                "user_id",
                "customer_segment",
                "account_status",
            ],
            limit=1,
        )

        if not results:
            return None

        return results[0]

    finally:
        client.close()


def get_customer_profile(df, user_id: str):
    """Get a customer's complete profile."""
    customer = get_customer(df, user_id)

    if customer is None:
        return {"error": f"Customer {user_id} not found in the dataset."}

    return customer


def get_customer_subscription(df, user_id: str):
    """Get subscription details for a customer."""
    subscription = get_subscription(df, user_id)

    if subscription is None:
        return {"error": f"Customer {user_id} not found in the dataset."}

    return subscription


def get_customer_metrics(df, user_id: str):
    """Get usage, revenue, engagement, and support metrics."""
    analytics = get_customer_analytics(df, user_id)

    if analytics is None:
        return {"error": f"Customer {user_id} not found in the dataset."}

    return analytics
