import os
from dotenv import load_dotenv
from google import genai
from models.ai_advisor import (
    generate_financial_summary,
)

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_ai_financial_advice(
    total_income,
    total_expense,
    total_savings,
    savings_rate,
    stability_score,
    anomaly_count,
    budget_risk,
    forecast_expense
):

    prompt = f"""
You are a professional personal finance advisor.

Financial Data:

Income: ₹{total_income}
Expenses: ₹{total_expense}
Savings: ₹{total_savings}
Savings Rate: {savings_rate:.1f}%
Financial Stability Score: {stability_score}/100
Anomalies Detected: {anomaly_count}
Budget Risk: {budget_risk}
Forecast Expense: ₹{forecast_expense}

Provide:

1. Financial Assessment
2. Risks
3. Recommendations
4. One Priority Action

Keep response under 120 words.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception:

        return generate_financial_summary(
            stability_score,
            savings_rate,
            anomaly_count
        )