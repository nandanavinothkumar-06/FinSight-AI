import streamlit as st

from models.risk_scoring import (
    calculate_financial_stability_score
)


def show_scenario_simulator(

    df,

    total_income,

    total_expense,

    total_savings,

    stability_score

):

    st.header(
        "🧮 Financial Scenario Simulator"
    )

    st.caption(
        "Explore how financial decisions affect your future financial health."
    )

    # ==========================================
    # CURRENT POSITION
    # ==========================================

    st.subheader(
        "📊 Current Financial Position"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Income",
            f"₹ {total_income:,.0f}"
        )

    with col2:

        st.metric(
            "Expenses",
            f"₹ {total_expense:,.0f}"
        )

    with col3:

        st.metric(
            "Savings",
            f"₹ {total_savings:,.0f}"
        )

    with col4:

        st.metric(
            "Stability Score",
            f"{stability_score}"
        )

    st.divider()

    # ==========================================
    # INCOME GROWTH SIMULATOR
    # ==========================================

    st.subheader(
        "💰 Income Growth Simulation"
    )

    simulated_income = st.slider(

        "What if your income increases?",

        min_value=int(total_income),

        max_value=int(total_income * 2),

        value=int(total_income),

        step=500

    )

    simulated_savings = (

        simulated_income -

        total_expense
    )

    simulated_savings_rate = (

        (simulated_savings / simulated_income) * 100

        if simulated_income > 0

        else 0
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Projected Savings",

            f"₹ {simulated_savings:,.0f}",

            delta=
            f"₹ {simulated_savings-total_savings:,.0f}"

        )

    with col2:

        st.metric(

            "Projected Savings Rate",

            f"{simulated_savings_rate:.1f}%"

        )

    st.divider()

    # ==========================================
    # SMART SPENDING OPTIMIZER
    # ==========================================

    st.divider()

    st.subheader(
        "🛒 Smart Spending Optimizer"
    )

    st.caption(
        "Explore how reducing spending across major categories affects your savings and financial health."
    )

    category_expense = (

        df.groupby("Category")["Amount"]

        .sum()

        .reset_index()

        .sort_values(
            by="Amount",
            ascending=False
        )
    )

    top_categories = (
        category_expense.head(3)
    )

    optimized_expense = total_expense

    reductions = {}

    for _, row in top_categories.iterrows():

        category = row["Category"]

        amount = row["Amount"]

        reduction = st.slider(

            f"{category} Reduction (%)",

            min_value=0,

            max_value=50,

            value=0,

            key=f"slider_{category}"
        )

        reductions[category] = reduction

        optimized_expense -= (

            amount *

            reduction / 100
        )

    # ==========================================
    # FINANCIAL IMPACT
    # ==========================================

    new_savings = (

        total_income -

        optimized_expense
    )

    monthly_gain = (

        new_savings -

        total_savings
    )

    annual_gain = (

        monthly_gain * 12
    )

    new_savings_rate = (

        (new_savings / total_income) * 100

        if total_income > 0

        else 0
    )

    improvement_percent = (

        (monthly_gain / total_savings) * 100

        if total_savings > 0

        else 0
    )

    st.progress(

        min(
            improvement_percent / 100,
            1.0
        )
    )

    st.caption(
        f"Savings improved by {improvement_percent:.1f}%"
    )

    st.divider()

    st.subheader(
        "💰 Financial Impact"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "New Savings",
            f"₹ {new_savings:,.0f}",
            delta=f"₹ {monthly_gain:,.0f}"
        )

    with col2:

        st.metric(
            "Savings Rate",
            f"{new_savings_rate:.1f}%"
        )

    with col3:

        st.metric(
            "Monthly Improvement",
            f"₹ {monthly_gain:,.0f}"
        )

    with col4:

        st.metric(
            "Annual Improvement",
            f"₹ {annual_gain:,.0f}"
        )

    # ==========================================
    # GOAL TRACKER
    # ==========================================

    st.divider()

    st.subheader(
        "🎯 Savings Goal Tracker"
    )

    goal = st.number_input(

        "Target Monthly Savings",

        min_value=0,

        value=int(total_savings + 5000),

        step=1000
    )

    goal_progress = (

        new_savings / goal

        if goal > 0

        else 0
    )

    st.progress(
        min(goal_progress, 1.0)
    )

    st.caption(
        f"{goal_progress * 100:.1f}% of target achieved"
    )

    # ==========================================
    # STABILITY SCORE PROJECTION
    # ==========================================

    st.divider()

    st.subheader(
        "🛡 Stability Score Projection"
    )

    new_budget_utilization = (

        (optimized_expense / total_income) * 100

        if total_income > 0

        else 0
    )

    volatility = (

        df["Amount"].std()

        if not df.empty

        else 0
    )

    simulated_results = (

        calculate_financial_stability_score(

            new_savings_rate,

            new_budget_utilization,

            volatility,

            df["Amount"].mean(),

            0
        )
    )

    simulated_score = (
        simulated_results["score"]
    )

    risk_label = (
        simulated_results["risk"]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Current Score",
            f"{stability_score}/100"
        )

    with col2:

        st.metric(
            "Projected Score",
            f"{simulated_score:.1f}/100",
            delta=round(
                simulated_score -
                stability_score,
                1
            )
        )

    st.info(
        f"Projected Risk Classification: {risk_label}"
    )

    # ==========================================
    # BEFORE VS AFTER
    # ==========================================

    st.divider()

    st.subheader(
        "📊 Current vs Optimized"
    )

    comparison_df = {

        "Metric": [

            "Income",
            "Expenses",
            "Savings",
            "Savings Rate"
        ],

        "Current": [

            f"₹ {total_income:,.0f}",
            f"₹ {total_expense:,.0f}",
            f"₹ {total_savings:,.0f}",
            f"{(total_savings / total_income) * 100:.1f}%"
        ],

        "Optimized": [

            f"₹ {total_income:,.0f}",
            f"₹ {optimized_expense:,.0f}",
            f"₹ {new_savings:,.0f}",
            f"{new_savings_rate:.1f}%"
        ]
    }

    st.dataframe(
        comparison_df,
        hide_index=True,
        width="stretch"
    )

    # ==========================================
    # AI INSIGHTS
    # ==========================================

    st.divider()

    st.subheader(
        "🤖 AI Optimization Insights"
    )

    best_category = max(
        reductions,
        key=reductions.get
    )

    if monthly_gain > 0:

        st.success(

            f"""
    💡 Additional Monthly Savings: ₹ {monthly_gain:,.0f}

    📈 Annual Wealth Increase: ₹ {annual_gain:,.0f}

    🎯 Biggest Optimization Opportunity: {best_category}
    """
        )

        if annual_gain > 10000:

            st.success(
                "Excellent optimization potential detected."
            )

        elif annual_gain > 5000:

            st.info(
                "Moderate optimization opportunity available."
            )

        else:

            st.info(
                "Small improvements compound significantly over time."
            )

    else:

        st.warning(
            "Move the sliders to explore savings opportunities."
        )

    # ==========================================
    # FINANCIAL HEALTH GRADE
    # ==========================================

    st.divider()

    st.subheader(
        "🏆 Financial Health Grade"
    )

    if simulated_score >= 90:

        grade = "A+"

    elif simulated_score >= 80:

        grade = "A"

    elif simulated_score >= 70:

        grade = "B"

    elif simulated_score >= 60:

        grade = "C"

    else:

        grade = "D"

    st.metric(
        "Financial Grade",
        grade
    )