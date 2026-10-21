
import pandas as pd


def get_dataset_summary(df: pd.DataFrame) -> dict:
    """Return a high-level summary of the customer dataset."""
    if df is None or df.empty:
        return {"error": "Customer dataset is empty."}

    summary = {
        "total_customers": int(len(df)),
        "total_columns": int(len(df.columns)),
        "columns": list(df.columns),
    }

    if "AccountStatus" in df.columns:
        summary["account_status_distribution"] = (
            df["AccountStatus"]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
            .to_dict()
        )

    if "SubscriptionStatus" in df.columns:
        summary["subscription_status_distribution"] = (
            df["SubscriptionStatus"]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
            .to_dict()
        )

    return summary


def get_segment_distribution(df: pd.DataFrame) -> dict:
    """Return customer counts by segment."""
    if df is None or df.empty:
        return {"error": "Customer dataset is empty."}

    if "CustomerSegment" not in df.columns:
        return {"error": "CustomerSegment column is unavailable."}

    counts = (
        df["CustomerSegment"]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
    )

    return {
        "total_customers": int(len(df)),
        "segments": {str(key): int(value) for key, value in counts.items()},
    }


def get_subscription_distribution(df: pd.DataFrame) -> dict:
    """Return subscription counts and percentages."""
    if df is None or df.empty:
        return {"error": "Customer dataset is empty."}

    if "SubscriptionStatus" not in df.columns:
        return {"error": "SubscriptionStatus column is unavailable."}

    counts = (
        df["SubscriptionStatus"]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
    )

    total = int(counts.sum())

    return {
        "total_customers": total,
        "subscriptions": {
            str(status): {
                "count": int(count),
                "percentage": round(float(count / total * 100), 2)
                if total else 0.0,
            }
            for status, count in counts.items()
        },
    }


def get_average_customer_metrics(df: pd.DataFrame) -> dict:
    """Return averages for available numeric customer metrics."""
    if df is None or df.empty:
        return {"error": "Customer dataset is empty."}

    metric_columns = [
        "TenureDays",
        "InvoiceCount",
        "TotalSettledPaise",
        "NetRevenuePaise",
        "TotalUsageUnits",
        "LoginEventCount",
        "SupportTicketCount",
        "OpenTicketCount",
        "AverageFeedbackScoreX100",
    ]

    available_columns = [
        column for column in metric_columns if column in df.columns
    ]

    if not available_columns:
        return {"error": "No supported customer metrics are available."}

    metrics = {}

    for column in available_columns:
        values = pd.to_numeric(df[column], errors="coerce").dropna()

        if not values.empty:
            metrics[column] = {
                "average": round(float(values.mean()), 2),
                "median": round(float(values.median()), 2),
                "minimum": float(values.min()),
                "maximum": float(values.max()),
                "available_records": int(values.count()),
            }

    return {
        "total_customers": int(len(df)),
        "metrics": metrics,
    }


def get_customers_by_account_status(df: pd.DataFrame) -> dict:
    """Compare customer metrics across account statuses."""
    if df is None or df.empty:
        return {"error": "Customer dataset is empty."}

    if "AccountStatus" not in df.columns:
        return {"error": "AccountStatus column is unavailable."}

    metric_columns = [
        "TenureDays",
        "InvoiceCount",
        "TotalSettledPaise",
        "NetRevenuePaise",
        "TotalUsageUnits",
        "LoginEventCount",
        "SupportTicketCount",
        "OpenTicketCount",
        "AverageFeedbackScoreX100",
    ]

    available_columns = [
        column for column in metric_columns if column in df.columns
    ]

    working_df = df.copy()
    working_df["AccountStatus"] = (
        working_df["AccountStatus"].fillna("Unknown").astype(str)
    )

    result = {}

    for status, group in working_df.groupby("AccountStatus"):
        status_data = {
            "customer_count": int(len(group)),
            "metrics": {},
        }

        for column in available_columns:
            values = pd.to_numeric(group[column], errors="coerce").dropna()

            if not values.empty:
                status_data["metrics"][column] = {
                    "average": round(float(values.mean()), 2),
                    "median": round(float(values.median()), 2),
                    "available_records": int(values.count()),
                }

        result[str(status)] = status_data

    return {
        "total_customers": int(len(working_df)),
        "comparison_by_account_status": result,
        "available_metrics": available_columns,
    }
