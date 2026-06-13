"""
Project Constants
Reusable values used across the application
"""

# ==================================================
# EXPENSE CATEGORIES
# ==================================================

CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills",
    "Healthcare",
    "Education",
    "Travel",
    "Stationary",
    "Other"
]

# ==================================================
# NEEDS CATEGORIES
# ==================================================

NEEDS_CATEGORIES = [
    "Food",
    "Transport",
    "Bills",
    "Healthcare",
    "Education"
]

# ==================================================
# WANTS CATEGORIES
# ==================================================

WANTS_CATEGORIES = [
    "Shopping",
    "Entertainment",
    "Travel",
    "Stationary",
    "Other"
]

# ==================================================
# SAVINGS RATE THRESHOLDS
# ==================================================

EXCELLENT_SAVINGS_RATE = 50
HEALTHY_SAVINGS_RATE = 20
TARGET_SAVINGS_RATE = 30

# ==================================================
# STABILITY SCORE THRESHOLDS
# ==================================================

EXCELLENT_STABILITY_SCORE = 85
GOOD_STABILITY_SCORE = 65
MODERATE_STABILITY_SCORE = 50

# ==================================================
# BUDGET RISK THRESHOLDS
# ==================================================

LOW_RISK_OVERSHOOT = 10
MODERATE_RISK_OVERSHOOT = 25

# ==================================================
# SPENDING THRESHOLDS
# ==================================================

HIGH_SPENDING_THRESHOLD = 35

VERY_HIGH_SPENDING_THRESHOLD = 50

MODERATE_ANOMALY_THRESHOLD = 1

HIGH_ANOMALY_THRESHOLD = 3

# ==================================================
# ANOMALY DETECTION
# ==================================================

ANOMALY_ZSCORE_THRESHOLD = 2.5

# ==================================================
# STABILITY SCORE SETTINGS
# ==================================================

MAX_SAVINGS_RATE_SCORE = 50

IDEAL_BUDGET_UTILIZATION = 80
MAX_BUDGET_UTILIZATION = 100

ANOMALY_PENALTY = 20

# ==================================================
# STABILITY WEIGHTS
# ==================================================

SAVINGS_WEIGHT = 0.40
BUDGET_WEIGHT = 0.30
VOLATILITY_WEIGHT = 0.20
ANOMALY_WEIGHT = 0.10

# ==================================================
# BUDGET PREDICTION
# ==================================================

WEEKS_PER_MONTH = 4

# ==================================================
# FORECAST SETTINGS
# ==================================================

FORECAST_WINDOW_DAYS = 7

LOW_CONFIDENCE_DAYS = 10

MEDIUM_CONFIDENCE_DAYS = 30

FORECAST_METHOD = "Random Forest"

# ==================================================
# ANOMALY DETECTION
# ==================================================

MIN_TRANSACTIONS_FOR_ANOMALY = 10

ANOMALY_CONTAMINATION = 0.10

ANOMALY_RANDOM_STATE = 42

# ==================================================
# APPLICATION
# ==================================================

APP_NAME = "FinSight AI"

APP_TAGLINE = (
    "AI-Powered Personal Finance Analytics Platform"
)

CURRENCY_SYMBOL = "₹"

# ==================================================
# DASHBOARD
# ==================================================

TOP_TRANSACTIONS_LIMIT = 5

RECENT_DAYS_LIMIT = 30

# ==================================================
# AI ADVISOR
# ==================================================

HEALTHY_SAVINGS_RATE = 20

TARGET_SAVINGS_RATE = 30

DEFAULT_ADVISOR_CONFIDENCE = 70

MIN_ADVISOR_CONFIDENCE = 50

MAX_ADVISOR_CONFIDENCE = 100

CONFIDENCE_PENALTY_PER_ANOMALY = 5

CURRENCY_SYMBOL = "₹"

# ==================================================
# COPILOT
# ==================================================

MAX_CHAT_HISTORY = 50

