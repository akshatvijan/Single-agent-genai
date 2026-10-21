
import pandas as pd
import pytest

from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        [
            {
                "UserID": "CUST001",
                "CustomerID": "CUST001",
                "PlanName": "Premium",
                "SubscriptionStatus": "Active",
                "TenureDays": 365,
                "InvoiceCount": 12,
                "NetRevenuePaise": 120000,
                "PlanInterval": "Monthly",
                "Segment": "INDIVIDUAL",
                "AccountStatus": "Active",
            },
            {
                "UserID": "CUST002",
                "CustomerID": "CUST002",
                "PlanName": "Basic",
                "SubscriptionStatus": "Cancelled",
                "TenureDays": 90,
                "InvoiceCount": 3,
                "NetRevenuePaise": 15000,
                "PlanInterval": "Monthly",
                "Segment": "PROFESSIONAL",
                "AccountStatus": "Churned",
            },
        ]
    )


@pytest.fixture
def client(sample_df):
    previous_df = getattr(app.state, "df", None)
    app.state.df = sample_df

    with TestClient(app) as test_client:
        yield test_client

    app.state.df = previous_df
