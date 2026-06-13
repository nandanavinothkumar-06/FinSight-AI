import streamlit as st

from models.ai_advisor import (
    generate_recommendations,
    interpret_forecast,
    calculate_advisor_confidence,
)

from services.gemini_advisor import (
    generate_ai_financial_advice
)


def show_ai_advisor(

    df,

    total_income,
    total_expense,
    total_savings,

    savings_rate,

    stability_score,

    anomaly_count,

    forecast_expense=None,

    budget_risk=None

):

    st.header(
        "🤖 AI Financial Advisor"
    )

    st.caption(
        "AI-powered financial insights and recommendations."
    )

    # ==========================================
    # CATEGORY ANALYSIS
    # ==========================================

    if not df.empty:

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

        top_category = (
            category_expense_sorted
            .iloc[0]["Category"]
        )

        top_amount = (
            category_expense_sorted
            .iloc[0]["Amount"]
        )

        spending_share = (

            (top_amount / total_expense)

            * 100

            if total_expense > 0

            else 0

        )

    else:

        top_category = "N/A"
        spending_share = 0

    # ==========================================
    # GEMINI ASSESSMENT
    # ==========================================

    st.subheader(
        "🧠 Gemini Financial Assessment"
    )

    ai_assessment = (

        generate_ai_financial_advice(

            total_income,
            total_expense,
            total_savings,

            savings_rate,

            stability_score,

            anomaly_count,

            budget_risk,

            forecast_expense

        )

    )

    st.info(
        ai_assessment
    )

    # ==========================================
    # SNAPSHOT
    # ==========================================

    st.subheader(
        "📊 Financial Snapshot"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Savings Rate",
            f"{savings_rate:.1f}%"
        )

    with col2:

        st.metric(
            "Top Category",
            top_category
        )

    with col3:

        st.metric(
            "Financial Score",
            f"{stability_score:.1f}/100"
        )

    with col4:

        st.metric(
            "Anomalies",
            anomaly_count
        )

    # ==========================================
    # HEALTH SCORE
    # ==========================================

    st.subheader(
        "🛡 Financial Health"
    )

    st.progress(
        stability_score / 100
    )

    confidence = calculate_advisor_confidence(

        stability_score,

        anomaly_count,

        savings_rate

    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Financial Score",
            f"{stability_score:.1f}/100"
        )

    with col2:

        st.metric(
            "Advisor Confidence",
            f"{confidence}%"
        )

    if stability_score >= 85:

        st.success(
            "Excellent financial health."
        )

    elif stability_score >= 70:

        st.info(
            "Good financial health with room for improvement."
        )

    elif stability_score >= 50:

        st.warning(
            "Moderate financial risk detected."
        )

    else:

        st.error(
            "High financial risk detected."
        )

    # ==========================================
    # FORECAST & BUDGET
    # ==========================================

    st.subheader(
        "📈 Forecast & Budget Outlook"
    )

    forecast_message = interpret_forecast(

        forecast_expense,

        total_expense

    )

    if forecast_message:

        st.info(
            forecast_message
        )

    if forecast_expense is not None:

        st.metric(

            "Predicted Next 7-Day Expense",

            f"₹ {forecast_expense:,.0f}"

        )

    if budget_risk:

        if budget_risk == "Low":

            st.success(
                "Budget remains within safe limits."
            )

        elif budget_risk == "Moderate":

            st.warning(
                "Budget utilization is increasing."
            )

        elif budget_risk == "High":

            st.error(
                "Budget overshoot risk detected."
            )

    # ==========================================
    # RECOMMENDATIONS
    # ==========================================

    recommendations = generate_recommendations(

        total_income,
        total_expense,
        total_savings,

        savings_rate,

        top_category,
        spending_share,

        stability_score,

        anomaly_count,

        forecast_expense,

        budget_risk

    )

    st.subheader(
        "🤖 Personalized Recommendations"
    )

    for recommendation in recommendations:

        text = recommendation.lower()

        if (
            "risk" in text
            or "warning" in text
            or "overshoot" in text
        ):

            st.warning(
                recommendation
            )

        elif (
            "excellent" in text
            or "healthy" in text
            or "strong" in text
        ):

            st.success(
                recommendation
            )

        else:

            st.info(
                recommendation
            )
        
    return recommendations[:3]