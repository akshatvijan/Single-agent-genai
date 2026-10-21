
from app.agent.tools import (
    search_customers,
    get_customer_profile,
    get_customer_subscription,
    get_customer_metrics,
)


def search_customer_service(query: str, limit: int = 5):
    """Search for customers relevant to a natural-language query."""
    return search_customers(query, limit=limit)


def customer_profile_service(df, user_id: str):
    """Retrieve a customer's profile."""
    return get_customer_profile(df, user_id)


def customer_subscription_service(df, user_id: str):
    """Retrieve a customer's subscription information."""
    return get_customer_subscription(df, user_id)


def customer_metrics_service(df, user_id: str):
    """Retrieve a customer's usage, revenue, and support metrics."""
    return get_customer_metrics(df, user_id)
