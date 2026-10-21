
from app.rag.embeddings import get_embedding_model
from app.rag.milvus_store import (
    COLLECTION_NAME,
    get_milvus_client,
)


def retrieve_customers(query: str, limit: int = 5, df=None):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Query cannot be empty.")

    if not 1 <= limit <= 20:
        raise ValueError("Limit must be between 1 and 20.")

    embedding_model = get_embedding_model()
    query_vector = embedding_model.embed_query(query.strip())

    client = get_milvus_client()

    try:
        results = client.search(
            collection_name=COLLECTION_NAME,
            data=[query_vector],
            limit=limit,
            output_fields=[
                "user_id",
                "customer_segment",
                "account_status",
            ],
        )

        customers = []

        for result in results[0]:
            data = result["entity"]
            user_id = data.get("user_id")

            customer = {
                "user_id": user_id,
                "customer_segment": data.get("customer_segment"),
                "account_status": data.get("account_status"),
                "similarity_score": result.get("distance"),
                "PlanName": None,
                "SubscriptionStatus": None,
                "TenureDays": None,
                "InvoiceCount": None,
                "NetRevenuePaise": None,
                "PlanInterval": None,
            }

            if df is not None and user_id is not None:
                matching_rows = df.loc[df["UserID"] == user_id]

                if not matching_rows.empty:
                    record = matching_rows.iloc[0]

                    for field in [
                        "PlanName",
                        "SubscriptionStatus",
                        "TenureDays",
                        "InvoiceCount",
                        "NetRevenuePaise",
                        "PlanInterval",
                    ]:
                        if field in df.columns:
                            value = record[field]

                            if value is not None:
                                try:
                                    if value != value:
                                        value = None
                                except (TypeError, ValueError):
                                    pass

                            customer[field] = value

            customers.append(customer)

        return customers

    finally:
        client.close()


if __name__ == "__main__":
    question = input("Enter your customer query: ")
    results = retrieve_customers(question)

    print("\nRelevant customers:")

    for customer in results:
        print(customer)
