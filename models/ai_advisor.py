from utils.constants import (

    EXCELLENT_SAVINGS_RATE,

    HEALTHY_SAVINGS_RATE,

    TARGET_SAVINGS_RATE,

    EXCELLENT_STABILITY_SCORE,

    GOOD_STABILITY_SCORE,

    HIGH_SPENDING_THRESHOLD,

    VERY_HIGH_SPENDING_THRESHOLD,

    MODERATE_ANOMALY_THRESHOLD,

    HIGH_ANOMALY_THRESHOLD,

    CONFIDENCE_PENALTY_PER_ANOMALY,

    MIN_ADVISOR_CONFIDENCE,

    MAX_ADVISOR_CONFIDENCE,

    DEFAULT_ADVISOR_CONFIDENCE,

    CURRENCY_SYMBOL

)


# ==================================================
# MAIN RECOMMENDATIONS
# ==================================================

def generate_recommendations(

    total_income,
    total_expense,
    total_savings,

    savings_rate,

    top_category,
    spending_share,

    stability_score,

    anomaly_count,

    forecast_expense=None,

    budget_risk=None

):

    recommendations = []

    # ==========================================
    # SAVINGS ANALYSIS
    # ==========================================

    if savings_rate >= EXCELLENT_SAVINGS_RATE:

        recommendations.append(
            f"Excellent financial discipline. You are saving {savings_rate:.1f}% of your income."
        )

    elif savings_rate >= HEALTHY_SAVINGS_RATE:

        recommendations.append(
            f"Your savings rate of {savings_rate:.1f}% is healthy."
        )

    else:

        recommendations.append(
            "Consider reducing discretionary expenses to improve savings."
        )

    # ==========================================
    # CATEGORY ANALYSIS
    # ==========================================

    if spending_share >= HIGH_SPENDING_THRESHOLD:

        recommendations.append(
            f"{top_category} accounts for {spending_share:.1f}% of total spending. Consider setting a monthly budget for this category."
        )

    # ==========================================
    # INCOME VS EXPENSE
    # ==========================================

    if total_expense > total_income:

        recommendations.append(
            "Warning: Your expenses currently exceed your income."
        )

    elif total_savings > 0:

        recommendations.append(
            f"You currently retain {CURRENCY_SYMBOL}{total_savings:,.0f} as savings."
        )

    # ==========================================
    # STABILITY SCORE
    # ==========================================

    if stability_score >= EXCELLENT_STABILITY_SCORE:

        recommendations.append(
            f"Financial Stability Score is {stability_score}/100 indicating low financial risk."
        )

    elif stability_score >= GOOD_STABILITY_SCORE:

        recommendations.append(
            f"Financial Stability Score is {stability_score}/100. Monitor spending habits to improve long-term resilience."
        )

    else:

        recommendations.append(
            f"Financial Stability Score is {stability_score}/100. Immediate budget optimization is recommended."
        )

    # ==========================================
    # ANOMALIES
    # ==========================================

    if anomaly_count > 0:

        recommendations.append(
            f"{anomaly_count} unusual transaction(s) were detected. Review recent spending activity."
        )

    else:

        recommendations.append(
            "No unusual spending behaviour detected."
        )

    # ==========================================
    # FORECAST
    # ==========================================

    if forecast_expense is not None:

        recommendations.append(
            f"Predicted upcoming expenses are approximately {CURRENCY_SYMBOL}{forecast_expense:,.0f}."
        )

    # ==========================================
    # BUDGET RISK
    # ==========================================

    if budget_risk == "High":

        recommendations.append(
            "Budget overshoot is likely based on current spending trends."
        )

    elif budget_risk == "Moderate":

        recommendations.append(
            "Spending is approaching budget limits."
        )

    elif budget_risk == "Low":

        recommendations.append(
            "Current spending remains within planned budget limits."
        )

    # ==========================================
    # OVERALL FINANCIAL HEALTH
    # ==========================================

    if savings_rate >= TARGET_SAVINGS_RATE and total_savings > 0:

        recommendations.append(
            "Current financial behaviour suggests strong long-term stability."
        )

    return recommendations


# ==================================================
# FINANCIAL SUMMARY
# ==================================================

def generate_financial_summary(

    stability_score,

    savings_rate,

    anomaly_count

):

    if (

        stability_score >= EXCELLENT_STABILITY_SCORE

        and

        anomaly_count == 0

    ):

        return (

            "Your financial profile is strong. Savings are healthy, spending is controlled and no unusual financial behaviour has been detected."

        )

    elif stability_score >= GOOD_STABILITY_SCORE:

        return (

            "Your finances are stable, but there are opportunities to improve savings and reduce long-term financial risk."

        )

    else:

        return (

            "Financial risk is elevated. Immediate budget optimization is recommended."

        )


# ==================================================
# BEHAVIOURAL RISK
# ==================================================

def determine_behavioural_risk(

    anomaly_count,

    spending_share

):

    if (

        anomaly_count >= HIGH_ANOMALY_THRESHOLD

        or

        spending_share >= VERY_HIGH_SPENDING_THRESHOLD

    ):

        return "High"

    elif (

        anomaly_count >= MODERATE_ANOMALY_THRESHOLD

        or

        spending_share >= HIGH_SPENDING_THRESHOLD

    ):

        return "Moderate"

    return "Low"


# ==================================================
# ACTION PLAN
# ==================================================

def generate_action_plan(

    savings_rate,

    anomaly_count,

    spending_share,

    top_category

):

    actions = []

    if spending_share >= HIGH_SPENDING_THRESHOLD:

        actions.append(
            f"Reduce spending in {top_category}"
        )

    if anomaly_count > 0:

        actions.append(
            "Review unusual transactions"
        )

    if savings_rate < TARGET_SAVINGS_RATE:

        actions.append(
            f"Increase savings rate to at least {TARGET_SAVINGS_RATE}%"
        )

    return actions


# ==================================================
# FORECAST INTERPRETATION
# ==================================================

def interpret_forecast(

    forecast_expense,

    total_expense

):

    if forecast_expense is None:

        return None

    current_weekly = total_expense / 4

    if current_weekly == 0:

        return (

            "Insufficient spending history for forecast comparison."

        )

    change = (

        (forecast_expense - current_weekly)

        / current_weekly

    ) * 100

    if change > 10:

        return (

            f"Expenses may increase by {change:.1f}% in the coming weeks."

        )

    elif change < -10:

        return (

            f"Expenses may decrease by {abs(change):.1f}% in the coming weeks."

        )

    return (

        "Expenses are expected to remain stable."

    )


# ==================================================
# PRIORITY ACTION
# ==================================================

def generate_priority_action(

    spending_share,

    anomaly_count,

    savings_rate,

    top_category

):

    if spending_share >= HIGH_SPENDING_THRESHOLD:

        return (

            f"Primary focus should be reducing {top_category} spending."

        )

    if anomaly_count > 0:

        return (

            "Review unusual transactions."

        )

    if savings_rate < TARGET_SAVINGS_RATE:

        return (

            "Increase monthly savings."

        )

    return (

        "Current financial habits are healthy."

    )


# ==================================================
# FINANCIAL PERSONALITY
# ==================================================

def detect_financial_personality(

    savings_rate,

    spending_share,

    anomaly_count

):

    if (

        savings_rate >= 40

        and

        anomaly_count <= 2

    ):

        return "Saver"

    elif (

        spending_share >= 45

        and

        savings_rate < 20

    ):

        return "Spender"

    return "Balanced"


# ==================================================
# ADVISOR CONFIDENCE
# ==================================================

def calculate_advisor_confidence(

    stability_score,

    anomaly_count,

    savings_rate

):

    confidence = DEFAULT_ADVISOR_CONFIDENCE

    confidence += min(

        savings_rate / 5,

        15

    )

    confidence -= (

        anomaly_count *

        CONFIDENCE_PENALTY_PER_ANOMALY

    )

    if stability_score >= EXCELLENT_STABILITY_SCORE:

        confidence += 10

    confidence = max(

        MIN_ADVISOR_CONFIDENCE,

        min(

            confidence,

            MAX_ADVISOR_CONFIDENCE

        )

    )

    return round(confidence)