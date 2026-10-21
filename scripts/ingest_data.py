
from pathlib import Path

from dotenv import load_dotenv

from app.data.loader import load_dataset
from app.rag.document_builder import build_customer_document
from app.rag.embeddings import get_embedding_model
from app.rag.milvus_store import (
    BATCH_SIZE,
    COLLECTION_NAME,
    create_collection,
    get_milvus_client,
    insert_documents,
)


load_dotenv()


DATA_PATH = r"C:\Users\Acer\Desktop\project_Single_agent\single-agent-genai\app\data\RewardSphere_1M_Customers.csv"

BATCH_SIZE = 500


def ingest_data():
    print("Loading customer dataset...")

    df = load_dataset(str(DATA_PATH))
    total_customers = len(df)

    print(f"Total customers: {total_customers:,}")

    client = get_milvus_client()
    embedding_model = get_embedding_model()

    try:
        create_collection(client)

        inserted_total = 0

        for start in range(0, total_customers, BATCH_SIZE):
            batch_df = df.iloc[start:start + BATCH_SIZE]

            documents = []
            records = []

            for row in batch_df.itertuples(index=False, name=None):
                customer = dict(zip(df.columns, row))
                content = build_customer_document(customer)

                if not content:
                    continue

                documents.append(content)
                records.append({
                    "user_id": str(customer["UserID"]),
                    "customer_segment": str(customer["CustomerSegment"]),
                    "account_status": str(customer["AccountStatus"]),
                })

            if not documents:
                continue

            vectors = embedding_model.embed_documents(documents)

            milvus_records = []

            for metadata, vector in zip(records, vectors):
                milvus_records.append({
                    **metadata,
                    "embedding": vector,
                })

            inserted = insert_documents(client, milvus_records)
            inserted_total += inserted

            print(
                f"Progress: {min(start + len(batch_df), total_customers):,}"
                f"/{total_customers:,} | Inserted: {inserted_total:,}"
            )

        print("\nIngestion completed!")
        print(f"Total records inserted: {inserted_total:,}")

    finally:
        client.close()


if __name__ == "__main__":
    ingest_data()
