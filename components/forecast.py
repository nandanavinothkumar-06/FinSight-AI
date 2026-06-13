import streamlit as st
import pandas as pd
import plotly.express as px
from models.forecast_model import (
    generate_forecast
)
from models.budget_predictor import (
    predict_budget_risk
)
from models.ai_advisor import (
    generate_recommendations
)

def show_forecast(
    df,
    budget
):

    st.header("🔮 Expense Forecasting")

    st.caption(
        "Expense forecasting using Random Forest Regression, feature engineering, and explainable AI."
    )

    # ==========================================
    # DATA VALIDATION
    # ==========================================

    if len(df) < 5:

        st.warning(
            "Need at least 5 transactions for forecasting."
        )

        return

    # ==========================================
    # PREPARE DATA
    # ==========================================
    results = generate_forecast(df)

    forecast_results = (
        results["forecast_results"]
    )

    daily_expense = (
        results["daily_expense"]
    )

    confidence = (
        results["confidence"]
    )

    forecast_method = (
        results["forecast_method"]
    )
    mae = results["mae"]
    rmse = results["rmse"]

    # ==========================================
    # KPIs
    # ==========================================

    avg_prediction = (
        forecast_results[
            "Predicted Expense"
        ].mean()
    )

    current_avg = (
        daily_expense[
            "Amount"
        ].mean()
    )


    st.subheader(
        "📈 Forecast Summary"
    )

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:

        st.metric(
            "Expected Daily Expense",
            f"₹ {avg_prediction:,.2f}"
        )

    with col2:

        st.metric(
            "Current Daily Average",
            f"₹ {current_avg:,.2f}"
        )

    with col3:

        st.metric(
            "Forecast Method",
            forecast_method
        )

    with col4:

        st.metric(
            "Forecast Confidence",
            confidence
        )

        if confidence == "🟢 High":

            st.success(
                "Strong historical data available"
            )

        elif confidence == "🟡 Medium":

            st.warning(
                "Moderate historical data available"
            )

        else:

            st.error(
                "Limited historical data available"
            )
    
    with col5:
        st.metric(
        "MAE",
        f"₹ {mae:,.2f}"
    )

    with col6:
        st.metric(
            "RMSE",
            f"₹ {rmse:,.2f}"
        )

    st.subheader(
        "🧠 Explainable AI - Forecast Drivers"
    )

    st.bar_chart(
        results["feature_importance"]
        .set_index("Feature")
    )

    top_feature = (
        results["feature_importance"]
        .iloc[0]["Feature"]
    )

    st.info(
        f"Most influential forecasting factor: {top_feature}"
    )

    st.divider()

    # ==========================================
    # CHART
    # ==========================================

    actual_chart = daily_expense[
        ["Date", "Amount"]
    ].copy()

    actual_chart["Type"] = (
        "Actual"
    )

    forecast_chart = (
        forecast_results.rename(
            columns={
                "Predicted Expense":
                "Amount"
            }
        )
    )

    forecast_chart["Type"] = (
        "Forecast"
    )

    chart_df = pd.concat(
        [
            actual_chart,
            forecast_chart
        ]
    )

    fig = px.line(

        chart_df,

        x="Date",

        y="Amount",

        color="Type",

        markers=True,

        title=
        "Actual vs Forecast Expense"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # ==========================================
    # FORECAST TABLE
    # ==========================================

    st.subheader(
        "📅 Next 7-Day Forecast"
    )

    st.dataframe(
        forecast_results,
        hide_index=True,
        width="stretch"
    )

    st.divider()

    # ==========================================
    # INSIGHTS
    # ==========================================

    st.subheader(
        "🤖 Forecast Insights"
    )

    if current_avg > 0:

        increase_percent = (

            (
                avg_prediction -
                current_avg
            )

            / current_avg

        ) * 100

    else:

        increase_percent = 0

    if avg_prediction > current_avg:

        st.warning(

            f"Expenses may increase by {increase_percent:.1f}% over the coming week."
        )

    else:

        st.success(

            f"Expenses are expected to remain stable with a {abs(increase_percent):.1f}% change."
        )

        st.info(
            f"Forecast generated using {forecast_method}."
        )

    st.success(
        f"Predicted weekly expense: ₹ {forecast_results['Predicted Expense'].sum():,.2f}"
    )

    # ==========================================
    # BUDGET RISK ASSESSMENT
    # ==========================================

    st.divider()

    st.subheader(
        "🎯 Budget Risk Assessment"
    )

    forecast_weekly_expense = (
        forecast_results[
            "Predicted Expense"
        ].sum()
    )

    forecast_daily_average = (
        forecast_weekly_expense / 7
    )

    risk_data = predict_budget_risk(

        forecast_daily_average,

        budget

    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Projected Monthly Expense",
            f"₹ {risk_data['projected_expense']:,.2f}"
        )

    with col2:

        st.metric(
            "Budget Utilization",
            f"{risk_data['budget_utilization']:.1f}%"
        )

    with col3:

        st.metric(
            "Expected Overshoot",
            f"₹ {risk_data['expected_overshoot']:,.2f}"
        )

    with col4:

        st.metric(
            "Risk Level",
            risk_data["risk_level"]
        )

    if risk_data["risk_level"] == "High":

        st.error(
            risk_data["recommendation"]
        )

    elif risk_data["risk_level"] == "Moderate":

        st.warning(
            risk_data["recommendation"]
        )

    elif risk_data["risk_level"] == "Low":

        st.success(
            risk_data["recommendation"]
        )

    else:

        st.info(
            risk_data["recommendation"]
        )