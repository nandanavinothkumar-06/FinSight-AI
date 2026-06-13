import streamlit as st
import pandas as pd
import plotly.express as px

from utils.pdf_report import (
    generate_financial_report
)
from utils.constants import (
    CURRENCY_SYMBOL
)



def show_reports(
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
):

    # ==================================================
    # HEADER
    # ==================================================

    st.header(
        "📄 Reports & Exports"
    )

    st.caption(
        "Generate, preview and export your financial data."
    )

    # ==================================================
    # REPORT SUMMARY
    # ==================================================

    st.subheader(
        "📊 Report Summary"
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
                "🛡 Stability Score",
                f"{stability_score}/100"
            )

    st.divider()

    # ==================================================
    # EXPORT TABS
    # ==================================================

    csv_tab, pdf_tab = st.tabs(
        [
            "📊 CSV Exports",
            "📄 PDF Reports"
        ]
    )

    # ==================================================
    # CSV TAB
    # ==================================================

    with csv_tab:

        st.subheader(
            "📊 CSV Data Export"
        )

        st.info(
            "Download raw transaction data for Excel, Power BI, Tableau or further analysis."
        )

        col1, col2 = st.columns(2)

        with col1:

            expense_csv = df.to_csv(
                index=False
            )

            st.download_button(
                label=
                "📥 Download Expenses CSV",
                data=expense_csv,
                file_name="expenses.csv",
                mime="text/csv",
                width='stretch'
            )

        with col2:

            income_csv = income_df.to_csv(
                index=False
            )

            st.download_button(
                label=
                "📥 Download Income CSV",
                data=income_csv,
                file_name="income.csv",
                mime="text/csv",
                width='stretch'
            )

        st.divider()

        st.subheader(
            "👀 Data Preview"
        )

        preview_option = st.radio(
            "Select Preview",
            [
                "Expenses",
                "Income"
            ],
            horizontal=True
        )

        if preview_option == "Expenses":

            st.dataframe(
                df.head(10),
                hide_index=True,
                width="stretch"
            )

        else:

            st.dataframe(
                income_df.head(10),
                hide_index=True,
                width="stretch"
            )

    # ==================================================
    # PDF TAB
    # ==================================================

    with pdf_tab:
        
        st.subheader(
            "📄 PDF Report Generation"
        )

        savings_rate = (
            (total_savings / total_income) * 100
            if total_income > 0
            else 0
        )

        top_category = (
            df.groupby("Category")["Amount"]
            .sum()
            .idxmax()
            if not df.empty
            else "N/A"
        )

        st.divider()

        st.subheader(
            "🤖 AI Executive Summary"
        )

        st.success(
            f"You saved ₹{total_savings:,.2f}, representing {savings_rate:.1f}% of income."
        )

        st.info(
            f"Highest spending category: {top_category}"
        )

        if stability_score >= 85:

            st.success(
                "Financial position appears strong with low risk."
            )

        elif stability_score >= 65:

            st.warning(
                "Financial position is stable but can be improved."
            )

        else:

            st.error(
                "Financial stability requires attention."
            )
        
        st.divider()

        st.subheader(
            "📄 Financial Report"
        )

        st.info(
            "Generate a professional PDF summary of your financial performance."
        )

        with st.container(border=True):

            st.markdown("### 📋 Report Includes")

            st.markdown("""
            ✅ Executive Summary

            ✅ Financial Stability Assessment

            ✅ Top Spending Categories

            ✅ Expense Distribution Analysis

            ✅ Savings Performance

            ✅ AI Recommendations

            ✅ Stability Score Breakdown
            """)

        if st.button(
            "Generate PDF Report",
            width='stretch'
        ):

            generate_financial_report(

                "financial_report.pdf",

                df,

                total_income,
                total_expense,
                total_savings,
                stability_score,
                savings_component,
                budget_component,
                volatility_component,
                anomaly_component
            )

            st.success(
                "Report generated successfully!"
            )

            with open(
                "financial_report.pdf",
                "rb"
            ) as pdf_file:

                st.download_button(

                    label=
                    "📥 Download PDF Report",

                    data=pdf_file,

                    file_name=
                    "financial_report.pdf",

                    mime=
                    "application/pdf",

                    width='stretch'
                )

        st.divider()

        st.subheader(
            "📋 Report Preview"
        )

        with st.container(border=True):

            savings_rate = (

                (total_savings / total_income) * 100

                if total_income > 0

                else 0

            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Income",
                    f"{CURRENCY_SYMBOL}{total_income:,.2f}"
                )

                st.metric(
                    "Expenses",
                    f"₹ {total_expense:,.2f}"
                )

            with col2:

                st.metric(
                    "Savings",
                    f"₹ {total_savings:,.2f}"
                )

                st.metric(
                    "Savings Rate",
                    f"{savings_rate:.1f}%"
                )