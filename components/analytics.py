import streamlit as st
import pandas as pd
import plotly.express as px

from models.anomaly_detector import (
    detect_spending_anomalies
)

from models.risk_scoring import (
    calculate_financial_stability_score
)

from utils.constants import (
    NEEDS_CATEGORIES,
    WANTS_CATEGORIES,
    CURRENCY_SYMBOL
)


def show_analytics(
    df,
    total_income,
    total_expense,
    total_savings
):

    st.header("📈 Financial Analytics")

    st.caption(
        "Analyze spending patterns, trends and financial health."
    )

    # ==================================================
    # EMPTY DATA CHECK
    # ==================================================

    if df.empty:

        st.warning(
            "No expense data available."
        )

        return

    # ==================================================
    # KPI CARDS
    # ==================================================

    savings_rate = (
        (total_savings / total_income) * 100
        if total_income > 0
        else 0
    )

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
                "💸 Expense",
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
                "📈 Savings Rate",
                f"{savings_rate:.1f}%"
            )

    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 Categories",
            "📈 Trends",
            "📋 Statistics",
            "🛡 Stability",
            "🚨 Anomalies"
        ]
    )

    # ==================================================
    # CATEGORY DATA
    # ==================================================

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

    # ==================================================
    # PIE + BAR CHART
    # ==================================================

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "🥧 Expense Distribution"
            )

            pie_fig = px.pie(
                category_expense,
                names="Category",
                values="Amount",
                hole=0.4
            )

            pie_fig.update_layout(
                template="plotly_white",
                showlegend=False
            )

            st.plotly_chart(
                pie_fig,
                width="stretch"
            )

        with col2:

            st.subheader(
                "📊 Category Spending"
            )

            bar_fig = px.bar(
                category_expense_sorted,
                x="Category",
                y="Amount",
                color="Category",
                text="Amount",
                color_discrete_sequence=
                px.colors.qualitative.Set3
            )

            bar_fig.update_traces(
                textposition="outside"
            )

            bar_fig.update_layout(
                template="plotly_white",
                showlegend=False
            )

            st.plotly_chart(
                bar_fig,
                width="stretch"
            )

    # ==================================================
    # MONTHLY TREND & NEEDS / WANTS / SAVINGS
    # ==================================================

    with tab2:

        st.subheader(
            "📅 Monthly Expense Trend"
        )

        trend_df = df.copy()

        trend_df["Date"] = pd.to_datetime(
            trend_df["Date"]
        )

        trend_df["Month"] = (
            trend_df["Date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_expense = (
            trend_df
            .groupby("Month")["Amount"]
            .sum()
            .reset_index()
        )

        trend_fig = px.line(
            monthly_expense,
            x="Month",
            y="Amount",
            markers=True
        )

        st.plotly_chart(
            trend_fig,
            width="stretch"
        )

        st.markdown("### 🎯 Needs • Wants • Savings")

        needs_spending = df[
            df["Category"].isin(
                NEEDS_CATEGORIES
            )
        ]["Amount"].sum()

        wants_spending = df[
            df["Category"].isin(
                WANTS_CATEGORIES
            )
        ]["Amount"].sum()

        savings_amount = max(
            total_savings,
            0
        )

        allocation_df = pd.DataFrame({

            "Category": [
                "Needs",
                "Wants",
                "Savings"
            ],

            "Amount": [
                needs_spending,
                wants_spending,
                savings_amount
            ]
        })

        allocation_fig = px.pie(
            allocation_df,
            names="Category",
            values="Amount"
        )

        allocation_fig.update_layout(
            showlegend=False,
            template="plotly_white"
        )

        st.plotly_chart(
            allocation_fig,
            width="stretch"
        )

    # ==================================================
    # STATISTICAL ANALYSIS & CATEGORY STATISTICS
    # ==================================================

    with tab3:

        st.subheader(
            "📊 Statistical Analysis"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            with st.container(border=True):

                st.metric(
                    "Average",
                    f"₹ {df['Amount'].mean():.2f}"
                )

        with col2:

            with st.container(border=True):

                st.metric(
                    "Median",
                    f"₹ {df['Amount'].median():.2f}"
                )

        with col3:

            with st.container(border=True):

                st.metric(
                    "Highest",
                    f"₹ {df['Amount'].max():.2f}"
                )

        with col4:

            with st.container(border=True):

                st.metric(
                    "Std Dev",
                    f"₹ {df['Amount'].std():.2f}"
                )

        st.markdown("---")

        st.subheader(
            "📋 Category Statistics"
        )

        category_stats = (
            df.groupby("Category")["Amount"]
            .agg([
                "sum",
                "mean",
                "count",
                "std"
            ])
            .reset_index()
        )

        category_stats.columns = [
            "Category",
            "Total Spend",
            "Average Spend",
            "Transactions",
            "Standard Deviation"
        ]

        st.dataframe(
            category_stats,
            hide_index=True,
            width="stretch"
        )

    # ==================================================
    # STABILITY
    # ==================================================
    with tab4:

        st.subheader(
            "🛡 Financial Stability Analysis"
        )

        outliers = detect_spending_anomalies(df)

        volatility = (
            df["Amount"].std()
        )

        anomaly_count = (
            len(outliers)
        )

        budget_utilization = (

            (total_expense / total_income) * 100

            if total_income > 0

            else 0
        )

        average_expense = (
            df["Amount"].mean()
        )

        risk_results = (
            calculate_financial_stability_score(

                savings_rate,

                budget_utilization,

                volatility,

                average_expense,

                anomaly_count
            )
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Stability Score",
                f"{risk_results['score']}/100"
            )

        with col2:

            st.metric(
                "Risk Level",
                risk_results["risk"]
            )

        with col3:

            st.metric(
                "Anomalies",
                anomaly_count
            )

        st.divider()

        st.subheader(
            "📊 Explainable AI Breakdown"
        )

        breakdown_df = pd.DataFrame({

            "Factor": [
                "Savings",
                "Budget",
                "Volatility",
                "Anomalies"
            ],

            "Score": [

                risk_results["savings_component"],

                risk_results["budget_component"],

                risk_results["volatility_component"],

                risk_results["anomaly_component"]

            ]
        })

        fig = px.bar(

            breakdown_df,

            x="Factor",

            y="Score",

            color="Factor",

            text="Score"

        )

        fig.update_traces(
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

        best_factor = (

            breakdown_df

            .sort_values(
                by="Score",
                ascending=False
            )

            .iloc[0]["Factor"]
        )

        worst_factor = (

            breakdown_df

            .sort_values(
                by="Score"
            )

            .iloc[0]["Factor"]
        )

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                f"✅ Strongest Area: {best_factor}"
            )

        with col2:

            st.warning(
                f"⚠ Needs Improvement: {worst_factor}"
            )
    # ==================================================
    # OUTLIER DETECTION 
    # ==================================================

    with tab5:

        st.subheader(
            "🚨 Spending Anomaly Detection"
        )

        st.caption(
            "AI-powered identification of unusual spending behaviour."
        )

        outliers = detect_spending_anomalies(df)

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Anomalies Detected",
                len(outliers)
            )

        with col2:

            st.metric(
                "Total Transactions",
                len(df)
            )

        with col3:

            anomaly_rate = (

                (len(outliers) / len(df)) * 100

                if len(df) > 0

                else 0
            )

            st.metric(
                "Anomaly Rate",
                f"{anomaly_rate:.1f}%"
            )

        st.divider()

        # ==========================================
        # ANOMALY VISUALIZATION
        # ==========================================

        scatter_df = df.copy()

        scatter_df["Date"] = pd.to_datetime(
            scatter_df["Date"]
        )

        scatter_df["Status"] = "Normal"

        if not outliers.empty:

            scatter_df.loc[
                outliers.index,
                "Status"
            ] = "Anomaly"

        anomaly_fig = px.scatter(

            scatter_df,

            x="Date",

            y="Amount",

            color="Status",

            size="Amount",

            hover_data=[
                "Category",
                "Description"
            ],

            title="Spending Anomaly Visualization"
        )

        st.plotly_chart(
            anomaly_fig,
            width="stretch"
        )

        st.divider()

        # ==========================================
        # ANOMALY TABLE
        # ==========================================

        st.subheader(
            "📋 Flagged Transactions"
        )

        if not outliers.empty:

            st.dataframe(

                outliers,

                hide_index=True,

                width="stretch"
            )

            largest_anomaly = (
                outliers["Amount"].max()
            )

            st.warning(

                f"Largest unusual transaction detected: "
                f"₹ {largest_anomaly:,.2f}"
            )

        else:

            st.success(
                "No unusual expenses detected."
            )

        st.divider()

        # ==========================================
        # AI INTERPRETATION
        # ==========================================

        st.subheader(
            "🤖 AI Interpretation"
        )

        if anomaly_rate > 20:

            st.error(
                "High anomaly frequency detected. Spending behaviour appears inconsistent."
            )

        elif anomaly_rate > 10:

            st.warning(
                "Moderate anomaly frequency detected. Review unusually large transactions."
            )

        else:

            st.success(
                "Spending behaviour appears stable with very few unusual transactions."
            )