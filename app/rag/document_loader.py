
from langchain_core.documents import Document

from app.rag.document_builder import build_customer_document


def create_documents(df, limit=3):
    documents = []

    for _, row in df.head(limit).iterrows():
        customer = row.to_dict()
        content = build_customer_document(customer)

        if content:
            document = Document(
                page_content=content,
                metadata={
                    "user_id": str(customer["UserID"]),
                    "customer_segment": str(customer["CustomerSegment"]),
                    "account_status": str(customer["AccountStatus"]),
                },
            )

            documents.append(document)

    return documents
