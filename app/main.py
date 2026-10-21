
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.api.routes import router
from app.data.loader import load_dataset
from app.data.quality_checks import check_data
from app.data.repository import (
    get_customer,
    get_subscription,
    get_customer_analytics,
)
from app.rag.document_builder import build_customer_document
from app.rag.document_loader import create_documents


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "RewardSphere_1M_Customers.csv"


def load_customer_data():
    print("\nLoading Dataset")

    df = load_dataset(str(DATA_PATH))

    print("Dataset loaded successfully!")
    print(f"Total customers : {len(df):,}")
    print(f"Total columns   : {len(df.columns)}")

    return df


def run_quality_checks(df):
    print("\nData Quality Check")
    check_data(df)


def show_customer_details(df):
    print("\nCustomer Details")

    user_id = df["UserID"].iloc[0]
    customer = get_customer(df, user_id)

    if customer is None:
        print("Customer not found.")
        return

    print(f"User ID          : {customer['UserID']}")
    print(f"Customer Name    : {customer['SyntheticName']}")
    print(f"Customer Segment : {customer['CustomerSegment']}")
    print(f"Account Status   : {customer['AccountStatus']}")

    print("\nSubscription Details")
    subscription = get_subscription(df, user_id)

    if subscription is not None:
        for key, value in subscription.items():
            print(f"{key:<30}: {value}")

    print("\nCustomer Analytics")
    analytics = get_customer_analytics(df, user_id)

    if analytics is not None:
        for key, value in analytics.items():
            print(f"{key:<30}: {value}")


def show_document_preview(df):
    print("\nCustomer Document")

    customer = get_customer(df, df["UserID"].iloc[0])
    document = build_customer_document(customer)

    if document:
        print("Customer document created successfully.")
        print(document[:500])


def show_langchain_documents(df):
    print("\nLangChain Documents")

    documents = create_documents(df, limit=3)

    print(f"Documents created: {len(documents)}")

    if documents:
        print("Metadata:", documents[0].metadata)
        print("Content preview:")
        print(documents[0].page_content[:200])


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.df = load_customer_data()
    yield


app = FastAPI(
    title="Single-Agent GenAI Knowledge Assistant",
    description="Customer search, profile, and analytics API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


def main():
    print("=" * 50)
    print("SINGLE-AGENT GENAI KNOWLEDGE ASSISTANT")
    print("=" * 50)

    df = load_customer_data()

    run_quality_checks(df)
    show_customer_details(df)
    show_document_preview(df)
    show_langchain_documents(df)

    print("\nExecution Completed Successfully")


if __name__ == "__main__":
    main()
