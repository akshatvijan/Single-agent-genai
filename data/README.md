
# RewardSphere AI Assistant

A customer intelligence application that combines semantic search, an AI agent, and customer analytics to answer questions about the RewardSphere customer dataset.

## Features

- **Customer Search:** Find relevant customer records using semantic similarity.
- **AI Chat:** Ask natural-language questions about customers and the dataset.
- **Customer Profile:** Retrieve customer details using a customer ID.
- **Subscription Details:** View customer subscription information.
- **Customer Metrics:** Retrieve revenue, usage, and support metrics.
- **Dataset Analytics:** Analyze customer segments, subscription statuses, account statuses, and average metrics.
- **Input Guardrails:** Validate user input and check for basic prompt-injection patterns.

## Tech Stack

- Python
- FastAPI
- Streamlit
- Pydantic AI
- Ollama (`qwen3:4b`)
- Milvus / Zilliz Cloud
- LangChain
- Hugging Face Embeddings
- Pandas

## Project Structure

```text
single-agent-genai/
├── app/
│   ├── agent/
│   │   ├── instructions.py
│   │   ├── orchestrator.py
│   │   └── tools.py
│   ├── api/
│   │   └── routes.py
│   ├── data/
│   │   ├── loader.py
│   │   ├── quality_checks.py
│   │   └── repository.py
│   ├── guardrails/
│   │   ├── input_checks.py
│   │   ├── injection_checks.py
│   │   ├── content_safety.py
│   │   └── output_validation.py
│   ├── rag/
│   │   ├── document_builder.py
│   │   ├── document_loader.py
│   │   ├── embeddings.py
│   │   ├── milvus_store.py
│   │   └── retriever.py
│   ├── schemas/
│   │   ├── requests.py
│   │   └── responses.py
│   ├── services/
│   │   ├── analytics_service.py
│   │   └── customer_service.py
│   └── main.py
├── scripts/
│   └── ingest_data.py
├── frontend/
│   └── streamlit_app.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.11 or later
- Ollama installed and running
- The `qwen3:4b` model downloaded in Ollama
- A configured Milvus or Zilliz Cloud collection
- The RewardSphere customer CSV dataset

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Download the Ollama model:

```bash
ollama pull qwen3:4b
```

Ensure Ollama is running before using the AI assistant.

## Environment Variables

Create a `.env` file in the project root:

```env
MILVUS_ENDPOINT=your_milvus_endpoint
MILVUS_TOKEN=your_milvus_token
OLLAMA_BASE_URL=http://localhost:11434/v1
```

Use your actual Milvus credentials locally. Never commit `.env` or expose credentials publicly.

## Dataset

Place `RewardSphere_1M_Customers.csv` at the location expected by `app/main.py`.

The application uses the dataset for customer profiles, subscription details, customer metrics, and aggregate analytics.

## Running the Backend

From the project root, run:

```bash
uvicorn app.main:app --reload
```

The FastAPI server will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Running the Frontend

Open another terminal from the project root:

```bash
streamlit run frontend/streamlit_app.py
```

The Streamlit interface provides AI Chat and Customer Search tabs.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| POST | `/search` | Search relevant customers |
| POST | `/chat` | Ask the AI assistant |
| GET | `/customers/{user_id}` | Retrieve customer profile |
| GET | `/customers/{user_id}/subscription` | Retrieve subscription details |
| GET | `/customers/{user_id}/metrics` | Retrieve customer metrics |
| GET | `/analytics/summary` | Dataset summary |
| GET | `/analytics/segments` | Customer segment distribution |
| GET | `/analytics/subscriptions` | Subscription distribution |
| GET | `/analytics/averages` | Average customer metrics |
| GET | `/analytics/account-status` | Compare account-status metrics |

## Important Notes

- Semantic search returns relevant matches, not guaranteed exact-filter results.
- Dataset-wide questions should use aggregate analytics tools.
- Correlation does not necessarily establish causation.
- Prompt-injection checks use basic pattern matching and are not a complete security solution.
- Customer data and credentials should be handled securely.
- The existing Milvus collection should not be re-ingested unless explicitly required.

## Current Status

The project includes a FastAPI backend, Streamlit interface, semantic customer retrieval, AI-agent tools, and analytics services.

Testing and observability setup are planned for a later stage.
