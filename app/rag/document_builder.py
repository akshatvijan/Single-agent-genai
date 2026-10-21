
def build_customer_document(customer):
    if customer is None:
        return None

    document = f"""
Customer Profile
User ID: {customer.get('UserID')}
Name: {customer.get('SyntheticName')}
Region: {customer.get('RegionCode')}
City: {customer.get('CityCode')}
Customer Segment: {customer.get('CustomerSegment')}
Account Status: {customer.get('AccountStatus')}
Registration Platform: {customer.get('RegistrationPlatform')}
Acquisition Channel: {customer.get('AcquisitionChannel')}

Subscription Details
Plan Name: {customer.get('PlanName')}
Plan Interval: {customer.get('PlanInterval')}
Subscription Status: {customer.get('SubscriptionStatus')}
Auto Renew Enabled: {customer.get('AutoRenewEnabled')}
Plan Price (Paise): {customer.get('PlanPricePaise')}

Payment and Revenue
Invoice Count: {customer.get('InvoiceCount')}
Total Settled (Paise): {customer.get('TotalSettledPaise')}
Net Revenue (Paise): {customer.get('NetRevenuePaise')}
Refund Amount (Paise): {customer.get('RefundAmountPaise')}

Usage and Engagement
Total Usage Units: {customer.get('TotalUsageUnits')}
Login Events: {customer.get('LoginEventCount')}
Engagement Seconds: {customer.get('TotalEngagementSeconds')}

Customer Support
Support Tickets: {customer.get('SupportTicketCount')}
Open Tickets: {customer.get('OpenTicketCount')}
Resolved Tickets: {customer.get('ResolvedTicketCount')}

Feedback and Risk
Average Feedback Score (x100): {customer.get('AverageFeedbackScoreX100')}
Risk Events: {customer.get('RiskEventCount')}
Confirmed Risk Events: {customer.get('ConfirmedRiskEvents')}
"""

    return document.strip()
