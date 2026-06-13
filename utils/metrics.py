from models.risk_scoring import (
    calculate_financial_stability_score
)

from models.anomaly_detector import (
    detect_spending_anomalies
)

def calculate_global_metrics(
    df,
    income_df
):

    # ==========================================
    # EXPENSE METRICS
    # ==========================================

    if not df.empty:

        total_expense = df["Amount"].sum()
        total_transactions = len(df)
        highest_expense = df["Amount"].max()
        average_expense = df["Amount"].mean()

    else:

        total_expense = 0
        total_transactions = 0
        highest_expense = 0
        average_expense = 0

    # ==========================================
    # INCOME METRICS
    # ==========================================

    if not income_df.empty:

        total_income = income_df["Amount"].sum()

    else:

        total_income = 0

    # ==========================================
    # SAVINGS
    # ==========================================

    total_savings = (
        total_income -
        total_expense
    )

    if total_income > 0:

        savings_rate = (

            total_savings /

            total_income

        ) * 100

    else:

        savings_rate = 0

    # ==========================================
    # BUDGET UTILIZATION
    # ==========================================

    budget_utilization = (

        (total_expense / total_income) * 100

        if total_income > 0

        else 0

    )

    # ==========================================
    # VOLATILITY
    # ==========================================

    volatility = (

        df["Amount"].std()

        if len(df) > 1

        else 0

    )

    # ==========================================
    # ANOMALIES
    # ==========================================

    anomalies = detect_spending_anomalies(df)

    anomaly_count = len(anomalies)

    # ==========================================
    # STABILITY SCORE
    # ==========================================

    risk_results = (

        calculate_financial_stability_score(

            savings_rate,

            budget_utilization,

            volatility,

            average_expense,

            anomaly_count

        )

    )

    # ==========================================
    # FINANCIAL STATUS
    # ==========================================
    if total_savings > 0:

        financial_status = "Surplus"

    elif total_savings < 0:

        financial_status = "Deficit"

    else:

        financial_status = "Break-even"

    # ==========================================
    # RETURN
    # ==========================================

    return {

        "total_income":
        total_income,

        "total_expense":
        total_expense,

        "total_savings":
        total_savings,

        "total_transactions":
        total_transactions,

        "highest_expense":
        highest_expense,

        "average_expense":
        average_expense,

        "savings_rate":
        savings_rate,

        "budget_utilization":
        budget_utilization,

        "volatility":
        volatility,

        "stability_score":
        risk_results["score"],

        "savings_component":
        risk_results["savings_component"],

        "budget_component":
        risk_results["budget_component"],

        "volatility_component":
        risk_results["volatility_component"],

        "anomaly_component":
        risk_results["anomaly_component"],

        "anomaly_count":
        anomaly_count,

        "anomalies":
        anomalies,

        "financial_status":
        financial_status,

        "risk_level":
        risk_results["risk"],

        "net_cashflow":
        total_savings

    }