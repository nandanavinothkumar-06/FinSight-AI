# ==================================================
# FinSight AI
# Personal Finance Analytics Platform
# ==================================================
# ---------------- Core libraries ---------------- #
import streamlit as st
from utils.styling import load_css
from utils.metrics import calculate_global_metrics
from components.forecast import (show_forecast)
from database.db import get_connection
from database.queries import create_tables
from database.data_loader import (load_expenses,load_income)
from components.sidebar import (render_sidebar)
from components.dashboard import show_dashboard
from components.analytics import show_analytics
from components.transactions import show_transactions
from components.reports import (show_reports)
from components.scenario_simulator import (show_scenario_simulator)
from components.ai_advisor import (show_ai_advisor)
from components.copilot import (show_copilot)
from models.budget_predictor import (
    predict_budget_risk
)
from models.forecast_model import (
    generate_forecast
)

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="FinSight AI",
    page_icon="assets/Finsight Favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)
load_css()


# ---------------- DATABASE---------------- #

conn = get_connection()
cursor = conn.cursor()
create_tables(conn, cursor)

# ---------------- lOAD DATA---------------- #

df = load_expenses(conn)
income_df = load_income(conn)


df.columns = [
    "ID",
    "Amount",
    "Category",
    "Date",
    "Description"
]

income_df.columns = [
    "ID",
    "Amount",
    "Date",
    "Source",
    "Description"
]

# ---------------- METRICS---------------- #

metrics = calculate_global_metrics(df,income_df)

total_income = metrics["total_income"]
total_expense = metrics["total_expense"]
total_savings = metrics["total_savings"]
total_transactions = metrics["total_transactions"]
highest_expense = metrics["highest_expense"]
average_expense = metrics["average_expense"]
stability_score = metrics["stability_score"]
savings_rate = metrics["savings_rate"]

savings_component = (
    metrics["savings_component"]
)

budget_component = (
    metrics["budget_component"]
)

volatility_component = (
    metrics["volatility_component"]
)

anomaly_component = (
    metrics["anomaly_component"]
)

anomaly_count = (
    metrics["anomaly_count"]
)

anomalies = (
    metrics["anomalies"]
)


# ---------------- RENDER SIDEBAR ---------------- #
menu, budget = render_sidebar(
    total_income,
    stability_score
)

# ---------------- COPILOT DATA ---------------- #

if not df.empty:

    forecast_data = generate_forecast(df)

    forecast_results = (
        forecast_data["forecast_results"]
    )

    if (
        not forecast_results.empty
        and "Predicted Expense"
        in forecast_results.columns
    ):

        forecast_expense = (
            forecast_results[
                "Predicted Expense"
            ].sum()
        )

    else:

        forecast_expense = 0

    forecast_confidence = (
        forecast_data["confidence"]
    )

else:

    forecast_expense = 0
    forecast_confidence = "Low"

forecast_daily_average = (
    forecast_expense / 7
)

budget_result = (

    predict_budget_risk(

        forecast_daily_average,

        budget

    )
)

budget_risk = (
    budget_result["risk_level"]
)

category_expense = (

    df.groupby("Category")["Amount"]

    .sum()

    .reset_index()
)

category_expense_sorted = (

    category_expense

    .sort_values(
        by="Amount",
        ascending=False
    )
)

if not category_expense_sorted.empty:

    top_category = (
        category_expense_sorted
        .iloc[0]["Category"]
    )

    top_amount = (
        category_expense_sorted
        .iloc[0]["Amount"]
    )

    spending_share = (

        (top_amount / total_expense) * 100

        if total_expense > 0

        else 0

    )

else:

    top_category = "N/A"

    spending_share = 0


if menu != "Dashboard":

        st.image(
            "assets/Finsight Logo.png",
            width=300
        )

        st.caption(
            "AI-Powered Personal Finance Analytics, Forecasting and Budget Intelligence Platform"
        )

if menu == "Dashboard":

    show_dashboard(
        
        df,
        total_income,
        total_expense,
        total_savings,
        total_transactions,
        stability_score,
        savings_rate,
        budget,
        anomaly_count,
        top_category,
        spending_share,
        savings_component,
        budget_component,
        volatility_component,
        anomaly_component,
    )
    

elif menu == "Analytics":

    show_analytics(
        df,
        total_income,
        total_expense,
        total_savings
    )

elif menu == "Transactions":

    show_transactions(
        conn,
        df,
        income_df
    )

elif menu == "Reports":

    show_reports(
        df,
        income_df,
        total_income,
        total_expense,
        total_savings,
        stability_score,
        savings_component,
        budget_component,
        volatility_component,
        anomaly_component
    )

elif menu == "Forecast":

    show_forecast(

        df,
        budget

    )

elif menu == "Scenario Simulator":

    show_scenario_simulator(
        df,

        total_income,

        total_expense,

        total_savings,

        stability_score

    )
elif menu == "AI Advisor":

    show_ai_advisor(

        df,

        total_income,
        total_expense,
        total_savings,

        savings_rate,

        stability_score,

        anomaly_count,

        forecast_expense,

        budget_risk

    )

elif menu == "FinSight Copilot":

        show_copilot(

        total_income,
        total_expense,
        total_savings,

        savings_rate,

        stability_score,

        anomaly_count,

        top_category,

        spending_share,

        budget_risk,

        forecast_expense,

        forecast_confidence

    )

st.markdown("---")

st.caption(
    "FinSight AI • Personal Finance Analytics Platform • Version 1.0"
)