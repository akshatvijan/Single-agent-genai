
def test_get_existing_customer(sample_df):
    from app.data.repository import get_customer

    result = get_customer(sample_df, "CUST001")

    assert result is not None
    assert result["UserID"] == "CUST001"


def test_get_missing_customer(sample_df):
    from app.data.repository import get_customer

    result = get_customer(sample_df, "UNKNOWN_CUSTOMER")

    assert result is None


def test_get_existing_subscription(sample_df):
    from app.data.repository import get_subscription

    result = get_subscription(sample_df, "CUST001")

    assert result is not None


def test_get_existing_customer_analytics(sample_df):
    from app.data.repository import get_customer_analytics

    result = get_customer_analytics(sample_df, "CUST001")

    assert result is not None
