import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
# ==================================================
# GEMINI CLIENT
# ==================================================

try:

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )

except Exception:

    client = None

# ==================================================
# CATEGORIES
# ==================================================

CATEGORIES = [

    "Food",
    "Groceries",
    "Transport",
    "Fuel",

    "Shopping",

    "Bills",
    "Utilities",

    "Entertainment",
    "Subscriptions",

    "Healthcare",
    "Pharmacy",

    "Education",

    "Travel",

    "Rent",
    "EMI",

    "Insurance",

    "Investments",

    "Salary",

    "Transfers",

    "ATM Withdrawal",

    "Taxes",

    "Cash Deposit",

    "Cash Withdrawal",

    "Bank Charges",

    "Interest",

    "UPI",

    "Stationary",

    "Other"
]

# ==================================================
# RULE ENGINE
# ==================================================

RULES = {

    # FOOD

    "swiggy": "Food",
    "zomato": "Food",
    "kfc": "Food",
    "mcdonald": "Food",
    "burger king": "Food",
    "dominos": "Food",
    "pizza hut": "Food",
    "subway": "Food",
    "barista": "Food",
    "starbucks": "Food",
    "coffee": "Food",
    "restaurant": "Food",

    # GROCERIES

    "instamart": "Groceries",
    "blinkit": "Groceries",
    "bigbasket": "Groceries",
    "dmart": "Groceries",
    "reliance fresh": "Groceries",
    "supermarket": "Groceries",
    "grocery": "Groceries",
    "more": "Groceries",

    # TRANSPORT

    "uber": "Transport",
    "ola": "Transport",
    "rapido": "Transport",

    # FUEL

    "petrol": "Fuel",
    "bharat petroleum": "Fuel",
    "indian oil": "Fuel",
    "hpcl": "Fuel",

    # SHOPPING

    "amazon": "Shopping",
    "flipkart": "Shopping",
    "myntra": "Shopping",
    "ajio": "Shopping",
    "meesho": "Shopping",
    "nykaa": "Shopping",

    # BILLS

    "airtel": "Bills",
    "jio": "Bills",
    "bsnl": "Bills",

    # UTILITIES

    "electricity": "Utilities",
    "water bill": "Utilities",
    "waterboard": "Utilities",

    # ENTERTAINMENT

    "pvr": "Entertainment",
    "cinema": "Entertainment",
    "movie": "Entertainment",
    "bookmyshow": "Entertainment",

    # SUBSCRIPTIONS

    "netflix": "Subscriptions",
    "spotify": "Subscriptions",
    "hotstar": "Subscriptions",
    "zee5": "Subscriptions",
    "prime": "Subscriptions",

    # HEALTHCARE

    "practo": "Healthcare",
    "hospital": "Healthcare",
    "clinic": "Healthcare",
    "doctor": "Healthcare",
    "pharmeasy": "Healthcare",

    # PHARMACY

    "apollo": "Pharmacy",
    "netmeds": "Pharmacy",
    "pharmacy": "Pharmacy",

    # EDUCATION

    "coursera": "Education",
    "udemy": "Education",
    "unacademy": "Education",
    "byjus": "Education",
    "tuition": "Education",

    # TRAVEL

    "irctc": "Travel",
    "indigo": "Travel",
    "air india": "Travel",
    "makemytrip": "Travel",
    "oyo": "Travel",
    "hotel": "Travel",

    # RENT

    "rent": "Rent",

    # EMI

    "emi": "EMI",

    # INSURANCE

    "insurance": "Insurance",
    "lic": "Insurance",
    "star health": "Insurance",
    "hdfc ergo": "Insurance",

    # INVESTMENTS

    "sip": "Investments",
    "mutual fund": "Investments",
    "groww": "Investments",
    "zerodha": "Investments",
    "upstox": "Investments",
    "nps": "Investments",
    "ppf": "Investments",

    # SALARY

    "salary": "Salary",
    "bonus": "Salary",

    # TRANSFERS

    "imps": "Transfers",
    "neft": "Transfers",
    "rtgs": "Transfers",

    # ATM

    "atm": "ATM Withdrawal",

    # TAXES

    "gst": "Taxes",
    "tax": "Taxes",

    # UPI

    "upi": "UPI",
    "gpay": "UPI",
    "google pay": "UPI",
    "phonepe": "UPI",
    "paytm": "UPI",

    # CASH

    "cash deposit": "Cash Deposit",
    "cash withdrawal": "Cash Withdrawal",
    "withdrawal": "Cash Withdrawal",

    # BANK CHARGES

    "bank charge": "Bank Charges",
    "charges": "Bank Charges",

    # INTEREST

    "interest": "Interest",

    # OTHERS

    "bmtc": "Transport",
    "ksrtc": "Transport",
    "metro": "Transport",
    "bus": "Transport",

    "biryani": "Food",
    "haldiram": "Food",

    "jewellery": "Shopping",
    "jewel": "Shopping",

    "1mg": "Pharmacy",

    "ecs": "Bills",

    "loan": "EMI",

    "sbi card": "Bills",
    "credit card": "Bills"
}

# ==================================================
# CATEGORIZATION FUNCTION
# ==================================================

def categorize_transaction(description):

    description_lower = str(
        description
    ).strip().lower()

    # ------------------------------------------
    # RULE ENGINE FIRST
    # ------------------------------------------

    for keyword, category in RULES.items():

        if keyword in description_lower:

            return category

    # ------------------------------------------
    # NO MATCH FOUND
    # ------------------------------------------

    return "Other"