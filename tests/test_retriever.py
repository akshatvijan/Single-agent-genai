
from unittest.mock import MagicMock, patch

from app.rag.retriever import retrieve_customers


def test_retrieve_customers_returns_matches():
    fake_client = MagicMock()

    fake_client.search.return_value = [
        [
            {
                "id": 1,
                "distance": 0.82,
                "entity": {
                    "user_id": "CUST001",
                    "customer_segment": "INDIVIDUAL",
                    "account_status": "ACTIVE",
                },
            }
        ]
    ]

    fake_model = MagicMock()
    fake_model.embed_query.return_value = [0.1, 0.2, 0.3]

    with (
        patch(
            "app.rag.retriever.get_embedding_model",
            return_value=fake_model,
        ),
        patch(
            "app.rag.retriever.get_milvus_client",
            return_value=fake_client,
        ),
    ):
        results = retrieve_customers(
            "active customers",
            limit=5,
        )

    assert len(results) == 1
    assert results[0]["user_id"] == "CUST001"
    assert results[0]["customer_segment"] == "INDIVIDUAL"
    assert results[0]["account_status"] == "ACTIVE"

    fake_client.close.assert_called_once()


def test_empty_query_is_rejected():
    import pytest

    with pytest.raises(ValueError):
        retrieve_customers("")


def test_invalid_limit_is_rejected():
    import pytest

    with pytest.raises(ValueError):
        retrieve_customers("active customers", limit=0)
