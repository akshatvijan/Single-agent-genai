
def get_customer(df, user_id):
    if df is None or df.empty or "UserID" not in df.columns:
        return None

    customer = df.loc[
        df["UserID"].astype(str).str.strip()
        == str(user_id).strip()
    ]

    if customer.empty:
        return None

    return customer.iloc[0].to_dict()


def get_subscription(df, user_id):
    customer = get_customer(df, user_id)

    if customer is None:
        return None

    columns = [
        "UserID",
        "PlanName",
        "PlanInterval",
        "SubscriptionStatus",
        "AutoRenewEnabled",
        "PlanPricePaise",
    ]

    return {
        column: customer.get(column)
        for column in columns
        if column in customer
    }


def get_customer_analytics(df, user_id):
    customer = get_customer(df, user_id)

    if customer is None:
        return None

    columns = [
        "UserID",
        "TenureDays",
        "InvoiceCount",
        "TotalSettledPaise",
        "NetRevenuePaise",
        "TotalUsageUnits",
        "LoginEventCount",
        "SupportTicketCount",
        "OpenTicketCount",
        "AverageFeedbackScoreX100",
        "PlanName",
        "SubscriptionStatus",
        "PlanInterval",
    ]

    return {
        column: customer.get(column)
        for column in columns
        if column in customer
    }
