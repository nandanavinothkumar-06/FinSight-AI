import streamlit as st

from utils.constants import (
    CURRENCY_SYMBOL,
    TARGET_SAVINGS_RATE,
    HIGH_SPENDING_THRESHOLD
)

from services.gemini_copilot import ask_gemini


# ==========================================
# INTENT DETECTION
# ==========================================

def detect_intent(question):

    question = question.lower().strip()

    intents = {

        "greeting": [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good evening"
        ],

        "income": [
            "income",
            "salary",
            "earning",
            "earn",
            "pay",
            "money earned"
        ],

        "expense": [
            "expense",
            "expenses",
            "spending",
            "spent",
            "cost"
        ],

        "saving": [
            "save",
            "saving",
            "savings"
        ],

        "score": [
            "score",
            "stability",
            "financial score"
        ],

        "risk": [
            "risk",
            "financial risk",
            "safe"
        ],

        "anomaly": [
            "anomaly",
            "unusual",
            "abnormal",
            "suspicious"
        ],

        "budget": [
            "budget",
            "overspend",
            "budget risk"
        ],

        "forecast": [
            "forecast",
            "future",
            "prediction",
            "predict"
        ],

        "category": [
            "category",
            "overspending",
            "top category",
            "highest spending"
        ],

        "personality": [
            "personality",
            "spender",
            "saver",
            "financial personality"
        ],

        "advice": [
            "advice",
            "suggestion",
            "recommendation",
            "improve"
        ],

        "summary": [
            "summary",
            "overall",
            "how am i doing",
            "financial summary"
        ]
    }

    for intent, keywords in intents.items():

        if any(keyword in question for keyword in keywords):

            return intent

    return "unknown"


# ==========================================
# RESPONSE ENGINE
# ==========================================

def generate_copilot_response(

    question,

    total_income,
    total_expense,
    total_savings,

    savings_rate,

    stability_score,

    anomaly_count,

    top_category,

    spending_share,

    budget_risk,

    forecast_expense,

    forecast_confidence

):

    intent = detect_intent(question)

    # ----------------------------------

    if intent == "greeting":

        return (
            "Hello! I'm FinSight Copilot.\n\n"
            "I can help you understand your income, expenses, savings, forecasts and financial stability."
        )

    # ----------------------------------

    elif intent == "income":

        return (
            f"Your total recorded income is "
            f"{CURRENCY_SYMBOL}{total_income:,.0f}."
        )

    # ----------------------------------

    elif intent == "expense":

        return (
            f"Your total recorded expenses are "
            f"{CURRENCY_SYMBOL}{total_expense:,.0f}."
        )

    # ----------------------------------

    elif intent == "saving":

        return (
            f"You currently save "
            f"{CURRENCY_SYMBOL}{total_savings:,.0f}, "
            f"which represents "
            f"{savings_rate:.1f}% "
            f"of your income."
        )

    # ----------------------------------

    elif intent == "score":

        return (
            f"Your Financial Stability Score is "
            f"{stability_score}/100."
        )

    # ----------------------------------

    elif intent == "risk":

        if stability_score >= 85:
            risk = "Low"

        elif stability_score >= 65:
            risk = "Moderate"

        else:
            risk = "High"

        return (
            f"Your current financial risk level is {risk}."
        )

    # ----------------------------------

    elif intent == "anomaly":

        return (
            f"{anomaly_count} unusual transaction(s) have been detected."
        )

    # ----------------------------------

    elif intent == "category":

        return (
            f"Your highest spending category is "
            f"{top_category}, accounting for "
            f"{spending_share:.1f}% "
            f"of total expenses."
        )

    # ----------------------------------

    elif intent == "budget":

        return (
            f"Current budget risk is {budget_risk}."
        )

    # ----------------------------------

    elif intent == "forecast":

        return (
            f"Predicted expenses for the next 7 days are approximately "
            f"{CURRENCY_SYMBOL}{forecast_expense:,.0f}.\n\n"
            f"Forecast Confidence: {forecast_confidence}"
        )

    # ----------------------------------

    elif intent == "personality":

        if savings_rate >= 40 and anomaly_count <= 2:

            personality = "Saver"

        elif spending_share >= 45 and savings_rate < 20:

            personality = "Spender"

        else:

            personality = "Balanced"

        return (
            f"Your current financial personality is: {personality}."
        )

    # ----------------------------------

    elif intent == "summary":

        overall = (

            "Strong"

            if stability_score >= 80

            else

            "Moderate"

            if stability_score >= 60

            else

            "At Risk"

        )

        return (

            f"Financial Overview\n\n"

            f"• Income: {CURRENCY_SYMBOL}{total_income:,.0f}\n"

            f"• Expenses: {CURRENCY_SYMBOL}{total_expense:,.0f}\n"

            f"• Savings: {CURRENCY_SYMBOL}{total_savings:,.0f}\n"

            f"• Savings Rate: {savings_rate:.1f}%\n"

            f"• Stability Score: {stability_score}/100\n"

            f"• Budget Risk: {budget_risk}\n"

            f"• Top Spending Category: {top_category}\n\n"

            f"Overall Financial Position: {overall}"
        )

    # ----------------------------------

    elif intent == "advice":

        advice = []

        if savings_rate < TARGET_SAVINGS_RATE:

            advice.append(
                "Increase monthly savings."
            )

        if spending_share > HIGH_SPENDING_THRESHOLD:

            advice.append(
                f"Reduce spending in {top_category}."
            )

        if anomaly_count > 0:

            advice.append(
                "Review unusual transactions."
            )

        if budget_risk == "High":

            advice.append(
                "Budget overshoot risk is high."
            )

        if not advice:

            advice.append(
                "Your financial profile currently looks healthy."
            )

        return "\n".join(
            [f"• {item}" for item in advice]
        )

    # ----------------------------------

    return (

        "I didn't recognize that question yet.\n\n"

        "Try asking:\n"

        "• How am I doing financially?\n"

        "• What is my savings rate?\n"

        "• Where am I overspending?\n"

        "• What is my forecast?\n"

        "• Do I have unusual transactions?\n"

        "• Give me financial advice"
    )


# ==========================================
# UI
# ==========================================

def show_copilot(

    total_income,
    total_expense,
    total_savings,

    savings_rate,

    stability_score,

    anomaly_count,

    top_category,

    spending_share,

    budget_risk,

    forecast_expense,

    forecast_confidence

):

    st.header(
        "💬 FinSight Copilot"
    )

    st.caption(
        "Your AI-powered financial assistant."
    )

    if "messages" not in st.session_state:

        st.session_state.messages = []

    # Display history

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    prompt = st.chat_input(
        "Ask FinSight Copilot..."
    )

    if prompt:

        st.session_state.messages.append({

            "role": "user",

            "content": prompt

        })

        financial_context = f"""
        Financial Summary

        Total Income: ₹{total_income:,.0f}
        Total Expenses: ₹{total_expense:,.0f}
        Total Savings: ₹{total_savings:,.0f}

        Savings Rate: {savings_rate:.1f}%

        Financial Stability Score: {stability_score}/100

        Budget Risk: {budget_risk}

        Top Spending Category: {top_category}

        Spending Share: {spending_share:.1f}%

        Forecast Expense: ₹{forecast_expense:,.0f}

        Forecast Confidence: {forecast_confidence}

        Anomaly Count: {anomaly_count}
        """

        gemini_prompt = f"""
        You are FinSight AI Financial Copilot.

        Use the following financial data:

        {financial_context}

        User Question:
        {prompt}

        Give personalized financial insights and recommendations.
        """

        response = ask_gemini(
            gemini_prompt
        )

        st.session_state.messages.append({

            "role": "assistant",

            "content": response

        })

        st.rerun()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🗑 Clear Chat",
            width='stretch'
        ):

            st.session_state.messages = []

            st.rerun()

    with col2:

        chat_text = ""

        for msg in st.session_state.messages:

            chat_text += (
                f"{msg['role']}: "
                f"{msg['content']}\n\n"
            )

        st.download_button(

            "📥 Export Chat",

            chat_text,

            file_name=
            "finsight_copilot_chat.txt",

            width='stretch'
        )

    st.divider()

    st.subheader(
        "⚡ Suggested Questions"
    )

    st.markdown(
        """
        - How am I doing financially?
        - What is my savings rate?
        - What is my financial score?
        - Where am I overspending?
        - Do I have unusual transactions?
        - What is my budget risk?
        - What are my predicted expenses?
        - Give me financial advice
        """
    )