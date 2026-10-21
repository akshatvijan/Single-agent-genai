
import os

from dotenv import load_dotenv
from pymilvus import MilvusClient


load_dotenv()

COLLECTION_NAME = "customer_knowledge"
EMBEDDING_DIMENSION = 384
BATCH_SIZE = 500


def get_milvus_client():
    endpoint = os.getenv("MILVUS_ENDPOINT")
    token = os.getenv("MILVUS_TOKEN")

    if not endpoint or not token:
        raise ValueError(
            "MILVUS_ENDPOINT and MILVUS_TOKEN must be configured in .env"
        )

    return MilvusClient(
        uri=endpoint,
        token=token,
    )


def create_collection(client):
    if client.has_collection(COLLECTION_NAME):
        print(f"Collection '{COLLECTION_NAME}' already exists.")
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        dimension=EMBEDDING_DIMENSION,
        primary_field_name="user_id",
        id_type="string",
        vector_field_name="embedding",
        metric_type="COSINE",
        auto_id=False,
        max_length=64,
    )

    print(f"Collection '{COLLECTION_NAME}' created successfully.")


def insert_documents(client, records):
    if not records:
        return 0

    result = client.insert(
        collection_name=COLLECTION_NAME,
        data=records,
    )

    return result.get("insert_count", len(records))


def close_milvus_client(client):
    client.close()
