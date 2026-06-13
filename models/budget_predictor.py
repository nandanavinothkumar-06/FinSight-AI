from utils.constants import (

    LOW_RISK_OVERSHOOT,

    MODERATE_RISK_OVERSHOOT

)


def predict_budget_risk(

    forecast_daily_average,

    budget

):

    # ==========================================
    # PROJECTED MONTHLY EXPENSE
    # ==========================================

    projected_expense = (

        forecast_daily_average * 30

    )

    # ==========================================
    # NO BUDGET SET
    # ==========================================

    if budget <= 0:

        return {

            "projected_expense":
            round(projected_expense, 2),

            "expected_overshoot":
            0,

            "overshoot_percent":
            0,

            "budget_utilization":
            0,

            "risk_level":
            "No Budget",

            "recommendation":
            "Set a monthly budget to enable budget risk analysis."

        }

    # ==========================================
    # OVERSHOOT
    # ==========================================

    expected_overshoot = max(

        projected_expense - budget,

        0

    )

    overshoot_percent = (

        expected_overshoot /

        budget

    ) * 100

    budget_utilization = (

        projected_expense /

        budget

    ) * 100

    # ==========================================
    # RISK CLASSIFICATION
    # ==========================================

    if overshoot_percent <= LOW_RISK_OVERSHOOT:

        risk_level = "Low"

        recommendation = (
            "Current spending is within budget."
        )

    elif overshoot_percent <= MODERATE_RISK_OVERSHOOT:

        risk_level = "Moderate"

        recommendation = (
            "Monitor spending carefully to avoid overshooting your budget."
        )

    else:

        risk_level = "High"

        recommendation = (
            "Reduce discretionary spending immediately."
        )

    # ==========================================
    # RETURN
    # ==========================================

    return {

        "projected_expense":
        round(projected_expense, 2),

        "expected_overshoot":
        round(expected_overshoot, 2),

        "overshoot_percent":
        round(overshoot_percent, 2),

        "budget_utilization":
        round(budget_utilization, 2),

        "risk_level":
        risk_level,

        "recommendation":
        recommendation

    }