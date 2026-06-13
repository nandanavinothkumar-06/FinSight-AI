import pandas as pd
import plotly.express as px
import streamlit as st

from utils.constants import (
    EXCELLENT_STABILITY_SCORE,
    GOOD_STABILITY_SCORE,
    CURRENCY_SYMBOL,
    TOP_TRANSACTIONS_LIMIT
)

from models.ai_advisor import (
    detect_financial_personality
)

def show_dashboard(
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
    anomaly_component
):

    # ==================================================
    # HEADER
    # ==================================================

    st.image(
        "assets/Finsight Banner.png",
        width=3100
    )

    # ==================================================
    # MAIN KPI CARDS
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.metric(
                "💰 Income",
                f"{CURRENCY_SYMBOL}{total_income:,.2f}"
            )

    with col2:
        with st.container(border=True):
            st.metric(
                "💸 Expenses",
                f"₹ {total_expense:,.2f}"
            )

    with col3:
        with st.container(border=True):
            st.metric(
                "🏦 Savings",
                f"₹ {total_savings:,.2f}"
            )

    with col4:
        with st.container(border=True):
            st.metric(
            "🛡 Stability Score",
            f"{stability_score}/100"
        )

    st.subheader("🧠 AI Insights")

    insights = []

    if savings_rate >= 30:
        insights.append(
            "Savings rate exceeds recommended levels."
        )

    if spending_share >= 35:
        insights.append(
            f"{top_category} accounts for a large portion of total spending."
        )

    if budget > 0 and total_expense <= budget:
        insights.append(
            "Budget utilization remains healthy."
        )

    if total_savings > 0:
        insights.append(
            "Positive savings indicate healthy cash flow."
        )

    for insight in insights:
        st.info(insight)
    
    
    
    st.subheader(
        " Financial Personality"
    )

    personality = detect_financial_personality(
        savings_rate,
        spending_share,
        anomaly_count
    )

    if personality == "Saver":

        st.success(
            "💰 Saver: You consistently prioritize savings and maintain healthy financial discipline."
        )

    elif personality == "Spender":

        st.warning(
            "🛒 Spender: A significant portion of your income is directed toward spending categories."
        )

    else:

        st.info(
            "⚖️ Balanced: You maintain a reasonable balance between spending and saving."
        )

    # ==================================================
    # QUICK SUMMARY
    # ==================================================

    st.subheader("⚡ Quick Summary")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.metric(
                "📋 Transactions",
                total_transactions
            )

    with col2:
        with st.container(border=True):
            st.metric(
                "📈 Savings Rate",
                f"{savings_rate:.1f}%"
            )

    st.divider()

    # ==================================================
    # SPENDING BY CATEGORY CHART
    # ==================================================

    st.subheader(
        "📊 Spending by Category"
    )

    if not df.empty:

        category_df = (
            df.groupby("Category")["Amount"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            category_df,
            x="Category",
            y="Amount",
            color="Category",
            color_discrete_sequence=
            px.colors.qualitative.Set3
        )

        fig.update_layout(
            template="plotly_white",
            height=400
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # ==================================================
    # MONTHLY EXPENSE TREND
    # ==================================================
    st.divider()

    st.subheader(
        "📈 Monthly Expense Trend"
    )

    if not df.empty:

        trend_df = df.copy()

        trend_df["Date"] = pd.to_datetime(
            trend_df["Date"]
        )

        monthly = (
            trend_df.groupby(
                trend_df["Date"]
                .dt.to_period("M")
            )["Amount"]
            .sum()
            .reset_index()
        )

        monthly["Date"] = (
            monthly["Date"]
            .astype(str)
        )

        st.dataframe(
            monthly
        )

        fig = px.line(
            monthly,
            x="Date",
            y="Amount",
            markers=True
        )

        fig.update_layout(
            template="plotly_white",
            height=400
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # ==================================================
    # BUDGET STATUS
    # ==================================================

    st.subheader("💸 Budget Status")

    if budget > 0:

        budget_used = (
            total_expense /
            budget
        ) * 100

    else:

        budget_used = 0

    remaining_budget = max(
        budget - total_expense,
        0
    )

    col1, col2 = st.columns(2)

    with col1:
         with st.container(border=True):
            st.metric(
                "Budget Used",
                f"{budget_used:.1f}%"
            )

    with col2:
        with st.container(border=True):
            st.metric(
                "Remaining Budget",
                f"₹ {remaining_budget:,.2f}"
            )

    st.progress(
        min(
            budget_used / 100,
            1.0
        )
    )

    st.caption(
        f"Budget Utilized: {budget_used:.1f}%"
    )

    if budget_used > 100:

        st.error(
            "🚨 Budget Exceeded"
        )

    elif budget_used > 80:

        st.warning(
            "⚠️ Approaching Budget Limit"
        )

    else:

        st.success(
            "✅ Budget Healthy"
        )

    st.divider()

    # ==================================================
    #RECENT TRANSACTIONS
    # ==================================================

    st.subheader(
        "🕒 Recent Transactions"
    )

    if not df.empty:

        recent_df = (
            df.sort_values(
                "ID",
                ascending=False
            )[[
                "Amount",
                "Category",
                "Date",
                "Description"
            ]]
            .head(TOP_TRANSACTIONS_LIMIT)
        )

        recent_df = recent_df.copy()

        recent_df["Amount"] = (
            CURRENCY_SYMBOL
            + recent_df["Amount"]
            .round(2)
            .astype(str)
        )

        st.dataframe(
            recent_df,
            hide_index=True,
            width="stretch"
        )

    else:

        st.info(
            "No transactions found."
        )

    st.divider()

    # ==================================================
    # FINANCIAL STABILITY
    # ==================================================

    st.subheader(
        "🛡 Financial Stability"
    )

    if stability_score >= EXCELLENT_STABILITY_SCORE:

        st.success(
            "Excellent Financial Stability"
        )

    elif stability_score >= GOOD_STABILITY_SCORE:

        st.warning(
            "Moderate Financial Stability"
        )

    else:

        st.error(
            "Financial Stability Needs Improvement"
        )