
from unittest.mock import patch


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@patch("app.api.routes.retrieve_customers")
def test_search_endpoint(mock_search, client):
    mock_search.return_value = []

    response = client.post(
        "/search",
        json={"query": "premium customers", "limit": 5},
    )

    assert response.status_code == 200
    assert response.json() == []


@patch("app.api.routes.run_agent")
def test_chat_endpoint(mock_agent, client):
    mock_agent.return_value = "Customer dataset summary."

    response = client.post(
        "/chat",
        json={"message": "Summarize the customer dataset"},
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "Customer dataset summary."


@patch("app.api.routes.get_customer")
def test_customer_profile_endpoint(mock_customer, client):
    mock_customer.return_value = {"UserID": "CUST001"}

    response = client.get("/customers/CUST001")

    assert response.status_code == 200
    assert response.json()["UserID"] == "CUST001"


@patch("app.api.routes.get_subscription")
def test_subscription_endpoint(mock_subscription, client):
    mock_subscription.return_value = {"PlanName": "Premium"}

    response = client.get("/customers/CUST001/subscription")

    assert response.status_code == 200
    assert response.json()["PlanName"] == "Premium"


@patch("app.api.routes.get_customer_analytics")
def test_customer_metrics_endpoint(mock_metrics, client):
    mock_metrics.return_value = {"InvoiceCount": 12}

    response = client.get("/customers/CUST001/metrics")

    assert response.status_code == 200
    assert response.json()["InvoiceCount"] == 12


@patch("app.api.routes.get_dataset_summary")
def test_analytics_summary_endpoint(mock_service, client):
    mock_service.return_value = {"total_customers": 2}

    response = client.get("/analytics/summary")

    assert response.status_code == 200
    assert response.json()["total_customers"] == 2


@patch("app.api.routes.get_segment_distribution")
def test_analytics_segments_endpoint(mock_service, client):
    mock_service.return_value = {"INDIVIDUAL": 1}

    response = client.get("/analytics/segments")

    assert response.status_code == 200
    assert response.json() == {"INDIVIDUAL": 1}


@patch("app.api.routes.get_subscription_distribution")
def test_analytics_subscriptions_endpoint(mock_service, client):
    mock_service.return_value = {"Active": 1}

    response = client.get("/analytics/subscriptions")

    assert response.status_code == 200
    assert response.json() == {"Active": 1}


@patch("app.api.routes.get_average_customer_metrics")
def test_analytics_averages_endpoint(mock_service, client):
    mock_service.return_value = {"average_tenure": 227.5}

    response = client.get("/analytics/averages")

    assert response.status_code == 200
    assert response.json()["average_tenure"] == 227.5


@patch("app.api.routes.get_customers_by_account_status")
def test_analytics_account_status_endpoint(mock_service, client):
    mock_service.return_value = {"Active": {"count": 1}}

    response = client.get("/analytics/account-status")

    assert response.status_code == 200
    assert response.json() == {"Active": {"count": 1}}
