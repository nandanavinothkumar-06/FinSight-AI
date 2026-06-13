from utils.constants import (

    MAX_SAVINGS_RATE_SCORE,

    IDEAL_BUDGET_UTILIZATION,

    MAX_BUDGET_UTILIZATION,

    ANOMALY_PENALTY,

    SAVINGS_WEIGHT,

    BUDGET_WEIGHT,

    VOLATILITY_WEIGHT,

    ANOMALY_WEIGHT,

    EXCELLENT_STABILITY_SCORE,

    GOOD_STABILITY_SCORE

)


def calculate_financial_stability_score(

    savings_rate,

    budget_utilization,

    volatility,

    average_expense,

    anomaly_count

):

    # ==========================================
    # SAVINGS COMPONENT
    # ==========================================

    savings_component = max(

        0,

        min(
            savings_rate,
            MAX_SAVINGS_RATE_SCORE
        )

    ) * 2

    # ==========================================
    # BUDGET COMPONENT
    # ==========================================

    if budget_utilization <= IDEAL_BUDGET_UTILIZATION:

        budget_component = 100

    elif budget_utilization <= MAX_BUDGET_UTILIZATION:

        budget_component = (

            100 -

            (budget_utilization -
             IDEAL_BUDGET_UTILIZATION)

        )

    else:

        budget_component = max(

            0,

            80 -

            (

                (budget_utilization -
                 MAX_BUDGET_UTILIZATION)

                * 2

            )
        )

    # ==========================================
    # VOLATILITY COMPONENT
    # ==========================================

    if average_expense > 0:

        volatility_ratio = (
            volatility /
            average_expense
        )

    else:

        volatility_ratio = 0

    volatility_component = max(
        0,
        100 - (volatility_ratio * 50)
    )

    # ==========================================
    # ANOMALY COMPONENT
    # ==========================================

    anomaly_component = max(

        0,

        100 -

        (

            anomaly_count *

            ANOMALY_PENALTY

        )

    )

    # ==========================================
    # FINAL SCORE
    # ==========================================

    score = (

        savings_component *

        SAVINGS_WEIGHT +

        budget_component *

        BUDGET_WEIGHT +

        volatility_component *

        VOLATILITY_WEIGHT +

        anomaly_component *

        ANOMALY_WEIGHT

    )

    score = round(

        score,

        1

    )

    score = max(

        0,

        min(
            score,
            100
        )

    )

    # ==========================================
    # RISK CLASSIFICATION
    # ==========================================

    if score >= EXCELLENT_STABILITY_SCORE:

        risk = "Low"

    elif score >= GOOD_STABILITY_SCORE:

        risk = "Moderate"

    else:

        risk = "High"

    return {

        "score":
        score,

        "risk":
        risk,

        "savings_component":
        round(
            savings_component,
            1
        ),

        "budget_component":
        round(
            budget_component,
            1
        ),

        "volatility_component":
        round(
            volatility_component,
            1
        ),

        "anomaly_component":
        round(
            anomaly_component,
            1
        )

    }

    # ==========================================
    # COMPONENT PERCENTAGE
    # ==========================================

    #"component_weights": {

    #"Savings":
    #SAVINGS_WEIGHT,

    #"Budget":
    #BUDGET_WEIGHT,

    #"Volatility":
    #VOLATILITY_WEIGHT,

    #"Anomaly":
    #ANOMALY_WEIGHT}