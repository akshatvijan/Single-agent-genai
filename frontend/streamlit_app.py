
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 120

st.set_page_config(
    page_title="RewardSphere AI",
    page_icon="🤖",
    layout="wide",
)

st.title("RewardSphere AI Assistant")
st.caption(
    "Customer intelligence powered by semantic search, "
    "AI tools, and customer analytics."
)


def api_get(endpoint):
    """Send a GET request to the backend."""
    try:
        return requests.get(
            f"{API_URL}{endpoint}",
            timeout=REQUEST_TIMEOUT,
        )
    except requests.Timeout:
        st.error("Request timed out. Please try again.")
    except requests.RequestException as exc:
        st.error(
            f"Could not connect to backend: {exc}. "
            "Make sure FastAPI is running."
        )

    return None


def api_post(endpoint, payload):
    """Send a POST request to the backend."""
    try:
        return requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.Timeout:
        st.error("Request timed out. Please try again.")
    except requests.RequestException as exc:
        st.error(
            f"Could not connect to backend: {exc}. "
            "Make sure FastAPI is running."
        )

    return None


def show_response(response):
    """Display the response returned by the backend."""
    if response is None:
        return

    if response.ok:
        try:
            data = response.json()
        except ValueError:
            st.error("Backend returned an invalid JSON response.")
            return

        if isinstance(data, list):
            if data:
                st.dataframe(
                    data,
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("No records found.")

        elif isinstance(data, dict):
            st.json(data)

        else:
            st.write(data)

    else:
        try:
            detail = response.json().get("detail", response.text)
        except ValueError:
            detail = response.text

        st.error(f"API error ({response.status_code}): {detail}")


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "AI Chat",
        "Customer Search",
        "Customer Lookup",
        "Analytics",
    ]
)


# 1. POST /chat
with tab1:
    st.subheader("Ask the AI Assistant")

    with st.form("chat_form"):
        question = st.text_input(
            "Enter your question",
            placeholder="Why are customers churning?",
        )
        ask_clicked = st.form_submit_button("Ask AI")

    if ask_clicked:
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Analyzing your question..."):
                response = api_post(
                    "/chat",
                    {"message": question.strip()},
                )

            if response is not None and response.ok:
                try:
                    answer = response.json().get("answer")

                    if answer:
                        st.markdown("### Answer")
                        st.markdown(answer)
                    else:
                        st.warning("The API returned an empty answer.")
                except ValueError:
                    st.error("Backend returned an invalid JSON response.")

            elif response is not None:
                show_response(response)


# 2. POST /search
with tab2:
    st.subheader("Semantic Customer Search")
    st.caption(
        "Find customers using semantic similarity. "
        "Results are relevant matches, not guaranteed exact filters."
    )

    with st.form("search_form"):
        query = st.text_input(
            "Search query",
            placeholder="Find customers with premium subscriptions",
        )

        limit = st.number_input(
            "Number of results",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
        )

        search_clicked = st.form_submit_button("Search Customers")

    if search_clicked:
        if not query.strip():
            st.warning("Please enter a search query.")
        else:
            with st.spinner("Searching customer records..."):
                response = api_post(
                    "/search",
                    {
                        "query": query.strip(),
                        "limit": int(limit),
                    },
                )

            show_response(response)


# 3. GET customer profile, subscription, and metrics
with tab3:
    st.subheader("Customer Details")

    with st.form("customer_lookup_form"):
        user_id = st.text_input(
            "Customer ID",
            placeholder="Enter an existing customer ID",
        )

        lookup_type = st.selectbox(
            "Select information",
            [
                "Customer Profile",
                "Subscription Details",
                "Customer Metrics",
            ],
        )

        lookup_clicked = st.form_submit_button("Get Customer Details")

    if lookup_clicked:
        if not user_id.strip():
            st.warning("Please enter a customer ID.")
        else:
            customer_id = user_id.strip()

            endpoints = {
                "Customer Profile": f"/customers/{customer_id}",
                "Subscription Details": (
                    f"/customers/{customer_id}/subscription"
                ),
                "Customer Metrics": (
                    f"/customers/{customer_id}/metrics"
                ),
            }

            with st.spinner("Fetching customer information..."):
                response = api_get(endpoints[lookup_type])

            show_response(response)


# 4. GET analytics endpoints
with tab4:
    st.subheader("Customer Analytics Dashboard")

    analytics_options = {
        "Dataset Summary": "/analytics/summary",
        "Customer Segments": "/analytics/segments",
        "Subscription Distribution": "/analytics/subscriptions",
        "Average Customer Metrics": "/analytics/averages",
        "Account Status Comparison": "/analytics/account-status",
    }

    selected_analysis = st.selectbox(
        "Choose an analysis",
        list(analytics_options.keys()),
    )

    if st.button("Run Analysis", key="run_analytics"):
        with st.spinner("Loading analytics..."):
            response = api_get(analytics_options[selected_analysis])

        if response is not None and response.ok:
            try:
                data = response.json()

                if isinstance(data, dict):
                    st.markdown("### Results")

                    numeric_items = [
                        (key, value)
                        for key, value in data.items()
                        if isinstance(value, (int, float))
                        and not isinstance(value, bool)
                    ]

                    if numeric_items:
                        columns = st.columns(
                            min(len(numeric_items), 3)
                        )

                        for index, (key, value) in enumerate(numeric_items):
                            with columns[index % len(columns)]:
                                if isinstance(value, int):
                                    display_value = f"{value:,}"
                                else:
                                    display_value = f"{value:,.2f}"

                                st.metric(
                                    label=key.replace("_", " ").title(),
                                    value=display_value,
                                )

                    st.json(data)

                elif isinstance(data, list):
                    if data:
                        st.dataframe(
                            data,
                            use_container_width=True,
                            hide_index=True,
                        )
                    else:
                        st.info("No analytics records returned.")

                else:
                    st.write(data)

                st.success("Analysis completed successfully.")

            except ValueError:
                st.error("Backend returned an invalid JSON response.")

        elif response is not None:
            show_response(response)
