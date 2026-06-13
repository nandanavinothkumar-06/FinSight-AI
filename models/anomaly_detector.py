import pandas as pd

from sklearn.ensemble import IsolationForest

from utils.constants import (

    MIN_TRANSACTIONS_FOR_ANOMALY,

    ANOMALY_CONTAMINATION,

    ANOMALY_RANDOM_STATE

)


def detect_spending_anomalies(df):

    # ==========================================
    # EMPTY ANOMALY TEMPLATE
    # ==========================================

    empty_anomalies = pd.DataFrame(

        columns=[

            "Amount",

            "anomaly",

            "anomaly_score"

        ]

    )

    # ==========================================
    # VALIDATION
    # ==========================================

    if df.empty:

        return empty_anomalies.copy()

    if len(df) < MIN_TRANSACTIONS_FOR_ANOMALY:

        return empty_anomalies.copy()

    if "Amount" not in df.columns:

        return empty_anomalies.copy()

    anomaly_df = df.copy()

    # ==========================================
    # CLEAN AMOUNT COLUMN
    # ==========================================

    anomaly_df["Amount"] = pd.to_numeric(

        anomaly_df["Amount"],

        errors="coerce"

    )

    anomaly_df = anomaly_df.dropna(

        subset=["Amount"]

    )

    if anomaly_df.empty:

        return empty_anomalies.copy()

    # ==========================================
    # ISOLATION FOREST
    # ==========================================

    try:

        model = IsolationForest(

            contamination=
            ANOMALY_CONTAMINATION,

            random_state=
            ANOMALY_RANDOM_STATE

        )

        anomaly_df["anomaly"] = (

            model.fit_predict(

                anomaly_df[["Amount"]]

            )

        )

        anomaly_df["anomaly_score"] = (

            model.decision_function(

                anomaly_df[["Amount"]]

            )

        )

    except Exception:

        return empty_anomalies.copy()

    # ==========================================
    # EXTRACT ANOMALIES
    # ==========================================

    anomalies = (

        anomaly_df[

            anomaly_df["anomaly"] == -1

        ]

        .sort_values(

            by="anomaly_score",

            ascending=True

        )

        .reset_index(

            drop=True

        )

    )

    # ==========================================
    # RETURN
    # ==========================================

    return anomalies