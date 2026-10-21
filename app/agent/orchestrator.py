
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext

from app.agent.instructions import SYSTEM_INSTRUCTIONS
from app.agent.tools import (
    search_customers,
    get_customer_by_id,
    get_customer_profile,
    get_customer_subscription,
    get_customer_metrics,
)
from app.services.analytics_service import (
    get_dataset_summary,
    get_segment_distribution,
    get_subscription_distribution,
    get_average_customer_metrics,
    get_customers_by_account_status,
)
from app.guardrails.input_checks import validate_input
from app.guardrails.injection_checks import check_prompt_injection
from app.guardrails.content_safety import check_content_safety
from app.guardrails.output_validation import validate_output
from app.observability.langfuse_setup import setup_langfuse


load_dotenv()

# Initialize Langfuse
setup_langfuse()


@dataclass
class AgentDependencies:
    df: object

 
agent = Agent(
    "ollama:qwen3:4b",
    deps_type=AgentDependencies,
    instructions=SYSTEM_INSTRUCTIONS,
    retries=1,
)


@agent.tool
def search_customer_records(
    ctx: RunContext[AgentDependencies],
    query: str,
    limit: int = 5,
):
    """Search customer records using semantic similarity."""
    return search_customers(
        query=query,
        limit=max(1, min(limit, 20)),
    )


@agent.tool
def verify_customer_id(
    ctx: RunContext[AgentDependencies],
    user_id: str,
):
    """Check whether a customer ID exists."""
    return get_customer_by_id(user_id)


@agent.tool
def get_customer_details(
    ctx: RunContext[AgentDependencies],
    user_id: str,
):
    """Retrieve a customer's profile from the dataset."""
    return get_customer_profile(ctx.deps.df, user_id)


@agent.tool
def get_subscription_details(
    ctx: RunContext[AgentDependencies],
    user_id: str,
):
    """Retrieve subscription details for a customer."""
    return get_customer_subscription(ctx.deps.df, user_id)


@agent.tool
def get_customer_metrics_details(
    ctx: RunContext[AgentDependencies],
    user_id: str,
):
    """Retrieve usage, revenue, and support metrics for a customer."""
    return get_customer_metrics(ctx.deps.df, user_id)


@agent.tool
def analyze_dataset_summary(
    ctx: RunContext[AgentDependencies],
):
    """Get dataset-wide counts and status distributions."""
    return get_dataset_summary(ctx.deps.df)


@agent.tool
def analyze_customer_segments(
    ctx: RunContext[AgentDependencies],
):
    """Analyze customer counts by segment."""
    return get_segment_distribution(ctx.deps.df)


@agent.tool
def analyze_subscription_distribution(
    ctx: RunContext[AgentDependencies],
):
    """Analyze subscription status counts and percentages."""
    return get_subscription_distribution(ctx.deps.df)


@agent.tool
def analyze_average_customer_metrics(
    ctx: RunContext[AgentDependencies],
):
    """Calculate average and descriptive customer metrics."""
    return get_average_customer_metrics(ctx.deps.df)


@agent.tool
def compare_account_status_metrics(
    ctx: RunContext[AgentDependencies],
):
    """Compare metrics across account status groups."""
    return get_customers_by_account_status(ctx.deps.df)


def run_agent(query, df):
    """Validate a user query, run the AI agent, and validate its response."""
    query = validate_input(query)
    query = check_prompt_injection(query)
    query = check_content_safety(query)

    result = agent.run_sync(
        query,
        deps=AgentDependencies(df=df),
    )

    return validate_output(result.output)
