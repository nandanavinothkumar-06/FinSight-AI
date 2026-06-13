import pandas as pd
import numpy as np
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error
)
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from utils.constants import (

    FORECAST_WINDOW_DAYS,

    LOW_CONFIDENCE_DAYS,

    MEDIUM_CONFIDENCE_DAYS,

    FORECAST_METHOD

)


def generate_forecast(df):

    # ==========================================
    # EMPTY DATA PROTECTION
    # ==========================================

    if df.empty:

        return {

            "forecast_results":
            pd.DataFrame(),

            "daily_expense":
            pd.DataFrame(),

            "confidence":
            "🔴 Low",

            "forecast_method":
            FORECAST_METHOD,

            "forecast_total":
            0,

            "forecast_daily_average":
            0,

            "trend":
            "Stable"

        }

    forecast_df = df.copy()

    # ==========================================
    # CLEAN DATE COLUMN
    # ==========================================

    forecast_df["Date"] = pd.to_datetime(

        forecast_df["Date"],

        errors="coerce"

    )

    forecast_df = forecast_df.dropna(

        subset=["Date"]

    )

    # ==========================================
    # CLEAN AMOUNT COLUMN
    # ==========================================

    forecast_df["Amount"] = pd.to_numeric(

        forecast_df["Amount"],

        errors="coerce"

    )

    forecast_df = forecast_df.dropna(

        subset=["Amount"]

    )

    # ==========================================
    # EMPTY AFTER CLEANING
    # ==========================================

    if forecast_df.empty:

        return {

            "forecast_results":
            pd.DataFrame(),

            "daily_expense":
            pd.DataFrame(),

            "confidence":
            "🔴 Low",

            "forecast_method":
            FORECAST_METHOD,

            "forecast_total":
            0,

            "forecast_daily_average":
            0,

            "trend":
            "Stable"

        }

    # ==========================================
    # DAILY EXPENSE
    # ==========================================

    daily_expense = (

        forecast_df

        .groupby("Date")["Amount"]

        .sum()

        .reset_index()

        .sort_values("Date")

    )

    # ==========================================
    # NO VALID DAILY DATA
    # ==========================================

    if daily_expense.empty:

        return {

            "forecast_results":
            pd.DataFrame(),

            "daily_expense":
            daily_expense,

            "confidence":
            "🔴 Low",

            "forecast_method":
            FORECAST_METHOD,

            "forecast_total":
            0,

            "forecast_daily_average":
            0,

            "trend":
            "Stable"

        }

    # ==========================================
    # MOVING AVERAGE FORECAST
    # ==========================================

    if len(daily_expense) >= FORECAST_WINDOW_DAYS:

        recent_average = (

            daily_expense["Amount"]

            .tail(
                FORECAST_WINDOW_DAYS
            )

            .mean()

        )

    else:

        recent_average = (

            daily_expense["Amount"]

            .mean()

        )

    # ==========================================
    # TREND DETECTION
    # ==========================================

    if len(daily_expense) >= 14:

        recent_avg = (

            daily_expense["Amount"]

            .tail(7)

            .mean()

        )

        previous_avg = (

            daily_expense["Amount"]

            .tail(14)

            .head(7)

            .mean()

        )

        if recent_avg > previous_avg * 1.05:

            trend = "Increasing"

        elif recent_avg < previous_avg * 0.95:

            trend = "Decreasing"

        else:

            trend = "Stable"

    else:

        trend = "Stable"

    # ==========================================
    # PREDICTIONS
    # ==========================================

    if len(daily_expense) < 15:

        return {

            "forecast_results": pd.DataFrame(
                columns=[
                    "Date",
                    "Predicted Expense"
                ]
            ),

            "daily_expense": daily_expense,

            "confidence": "🔴 Low",

            "forecast_method": "Insufficient Data",

            "forecast_total": 0,

            "forecast_daily_average": round(
                recent_average,
                2
            ),

            "trend": trend,

            "accuracy": 0,

            "forecast_type":
            "Daily Expense Forecast"

        }

    daily_expense["Day"] = np.arange(len(daily_expense))

    daily_expense["DayOfWeek"] = (
        daily_expense["Date"]
        .dt.dayofweek
    )

    daily_expense["Month"] = (
        daily_expense["Date"]
        .dt.month
    )

    daily_expense["DayOfMonth"] = (
        daily_expense["Date"]
        .dt.day
    )

    daily_expense["IsWeekend"] = (
        daily_expense["DayOfWeek"] >= 5
    ).astype(int)

    daily_expense["RollingAvg7"] = (
        daily_expense["Amount"]
        .rolling(7)
        .mean()
    )

    daily_expense["RollingAvg7"] = (
        daily_expense["RollingAvg7"]
        .fillna(
            daily_expense["Amount"].mean()
        )
    )
    X = daily_expense[
        [
            "Day",
            "DayOfWeek",
            "DayOfMonth",
            "Month",
            "IsWeekend",
            "RollingAvg7"
        ]
    ]

    y = daily_expense["Amount"]

    split_index = int(len(X) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

    model.fit(
        X_train,
        y_train
    )

    feature_importance = pd.DataFrame({

        "Feature":
        X.columns,

        "Importance":
        model.feature_importances_

    }).sort_values(

        "Importance",

        ascending=False

    )

    y_pred = model.predict(
        X_test
    )

    try:

        mae = mean_absolute_error(
            y_test,
            y_pred
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_test,
                y_pred
            )
        )

    except:

        mae = 0
        rmse = 0


    # ==========================================
    # CONFIDENCE
    # ==========================================
    if len(daily_expense) >= 100:
        confidence = "🟢 High"

    elif len(daily_expense) >= 50:
        confidence = "🟡 Medium"

    else:
        confidence = "🔴 Low"

    last_date = daily_expense["Date"].max()

    future_dates = pd.date_range(

        start=

        daily_expense["Date"].max()

        +

        pd.Timedelta(days=1),

        periods=

        FORECAST_WINDOW_DAYS

    )

    future_df = pd.DataFrame({

        "Day":
        np.arange(
            len(daily_expense),
            len(daily_expense)
            + FORECAST_WINDOW_DAYS
        ),

        "DayOfWeek":
        future_dates.dayofweek,

        "DayOfMonth":
        future_dates.day,

        "Month":
        future_dates.month,

        "IsWeekend":
        (
            future_dates.dayofweek >= 5
        ).astype(int),

        "RollingAvg7":
        [
            daily_expense["Amount"]
            .tail(7)
            .mean()
        ] * FORECAST_WINDOW_DAYS

    })

    predictions = model.predict(
        future_df
    )

    predictions = np.maximum(
        predictions,
        0
    )

    future_dates = pd.date_range(

        start=

        daily_expense["Date"].max()

        +

        pd.Timedelta(days=1),

        periods=

        FORECAST_WINDOW_DAYS

    )

    forecast_results = pd.DataFrame({

        "Date":
        future_dates,

        "Predicted Expense":
        predictions.round(2)

    })

    # ==========================================
    # FORECAST SUMMARY
    # ==========================================

    forecast_total = (

        forecast_results[

            "Predicted Expense"

        ].sum()

    )

    # ==========================================
    # RETURN
    # ==========================================

    return {

        "forecast_results":
        forecast_results,

        "daily_expense":
        daily_expense,

        "confidence":
        confidence,

        "forecast_method":
        FORECAST_METHOD,

        "forecast_total":
        round(
            forecast_total,
            2
        ),

        "forecast_daily_average":
        round(
            recent_average,
            2
        ),

        "trend":
        trend,

        "mae":
        round(mae, 2),

        "rmse":
        round(rmse, 2),

        "feature_importance":
        feature_importance,

        "forecast_type":
        "Daily Expense Forecast",

    }