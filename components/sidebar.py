import streamlit as st
from utils.constants import (
    CURRENCY_SYMBOL
)

def render_sidebar(
    total_income,
    stability_score
):

    # ==========================================
    # LOGO
    # ==========================================

    st.sidebar.image(
        "assets/Finsight Logo.png",
        width='stretch'
    )

    st.sidebar.caption(
        "💡 AI-Powered Finance Intelligence"
    )

    st.sidebar.markdown("---")

    # ==========================================
    # KEY METRICS
    # ==========================================

    st.sidebar.metric(
        "💰 Total Income",
        f"{CURRENCY_SYMBOL}{total_income:,.0f}"
    )

    st.sidebar.metric(
        "📊 Stability Score",
        f"{stability_score:.1f}/100"
    )

    st.sidebar.progress(
        min(stability_score / 100, 1.0)
    )

    if stability_score >= 80:

        st.sidebar.success(
            "🟢 Excellent Financial Stability"
        )

    elif stability_score >= 60:

        st.sidebar.info(
            "🔵 Good Financial Stability"
        )

    else:

        st.sidebar.warning(
            "🟠 Stability Needs Improvement"
        )

    st.sidebar.markdown("---")

    # ==========================================
    # NAVIGATION
    # ==========================================

    menu = st.sidebar.selectbox(
        "🧭 Navigation",
        [
            "🏠 Dashboard",
            "📈 Analytics",
            "💳 Transactions",
            "🔮 Forecast",
            "🎯 Scenario Simulator",
            "📄 Reports",
            "🤖 AI Advisor",
            "💬 FinSight Copilot"
        ],
        key="navigation_menu"
    )

    st.sidebar.markdown("---")

    # ==========================================
    # MONTHLY BUDGET
    # ==========================================

    st.sidebar.subheader(
        "💸 Monthly Budget"
    )

    if "budget" not in st.session_state:

        st.session_state.budget = max(
            (total_income / 12) * 0.8,
            10000
        )

    budget = st.sidebar.number_input(
        "Budget Limit",
        min_value=0.0,
        value=float(
            st.session_state.budget
        ),
        step=1000.0,
        key="monthly_budget_input"
    )

    st.session_state.budget = budget

    # ==========================================
    # BUDGET HEALTH
    # ==========================================

    budget_ratio = (
        budget / total_income
        if total_income > 0
        else 0
    )

    st.sidebar.progress(
        min(budget_ratio, 1.0)
    )

    st.sidebar.caption(
        f"Budget Allocation: {budget_ratio*100:.1f}% of Income"
    )

    if budget_ratio <= 0.60:

        st.sidebar.success(
            "✅ Conservative Budget"
        )

    elif budget_ratio <= 0.80:

        st.sidebar.info(
            "ℹ️ Balanced Budget"
        )

    else:

        st.sidebar.warning(
            "⚠️ High Budget Allocation"
        )

    st.sidebar.markdown("---")

    st.sidebar.caption(
        "🚀 FinSight AI v1.0"
    )

    return (
        menu.replace("🏠 ", "")
            .replace("📈 ", "")
            .replace("💳 ", "")
            .replace("🔮 ", "")
            .replace("🎯 ", "")
            .replace("📄 ", "")
            .replace("🤖 ", "")
            .replace("💬 ", ""),
        budget
    )