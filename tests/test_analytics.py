
from unittest.mock import patch


def test_dataset_summary_api(client):
    with patch(
        "app.api.routes.get_dataset_summary",
        return_value={"total_customers": 2},
    ):
        response = client.get("/analytics/summary")

    assert response.status_code == 200
    assert response.json()["total_customers"] == 2


def test_segment_distribution_api(client):
    with patch(
        "app.api.routes.get_segment_distribution",
        return_value={"INDIVIDUAL": 1, "PROFESSIONAL": 1},
    ):
        response = client.get("/analytics/segments")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_subscription_distribution_api(client):
    with patch(
        "app.api.routes.get_subscription_distribution",
        return_value={"Active": 1, "Cancelled": 1},
    ):
        response = client.get("/analytics/subscriptions")

    assert response.status_code == 200
    assert "Active" in response.json()


def test_average_metrics_api(client):
    with patch(
        "app.api.routes.get_average_customer_metrics",
        return_value={"average_tenure": 227.5},
    ):
        response = client.get("/analytics/averages")

    assert response.status_code == 200
    assert response.json()["average_tenure"] == 227.5


def test_account_status_analytics_api(client):
    with patch(
        "app.api.routes.get_customers_by_account_status",
        return_value={"Active": {"count": 1}},
    ):
        response = client.get("/analytics/account-status")

    assert response.status_code == 200
    assert "Active" in response.json()
