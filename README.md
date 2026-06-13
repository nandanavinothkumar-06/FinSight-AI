# FinSight AI

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Enabled-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Gemini AI](https://img.shields.io/badge/Gemini-AI-orange)

<img width="1429" height="381" alt="Finsight Banner" src="https://github.com/user-attachments/assets/ca21bb28-639c-4764-8a21-0be0d9def4e3" />

## Overview

FinSight AI is an AI-powered Personal Finance Analytics and Budget Intelligence Platform designed to help users track expenses, analyze spending patterns, forecast future expenses, assess budget risks, and receive personalized financial recommendations.

The platform combines Data Analytics, Machine Learning, Financial Intelligence, and Generative AI to transform raw transaction data into actionable financial insights.

### Live Demo

https://finsight-ai-personal-finance-tracker.streamlit.app/

### GitHub Repository

https://github.com/nandanavinothkumar-06/FinSight-AI

---

# Problem Statement

Managing personal finances is challenging due to:

- Lack of spending visibility
- Inefficient budgeting
- Limited forecasting tools
- Difficulty identifying overspending
- Absence of personalized financial guidance

Most users possess financial data but lack intelligent systems to transform it into meaningful insights.

FinSight AI addresses this challenge through analytics, forecasting, machine learning, and AI-powered recommendations.

---

# Objectives

- Build a practical personal finance intelligence platform
- Implement Machine Learning-based forecasting
- Provide budget risk assessment
- Generate financial insights through AI
- Automate financial reporting
- Demonstrate end-to-end Data Science workflows

---

# Key Features

## Financial Dashboard

- Income & Expense Tracking
- Savings Monitoring
- Financial Stability Score
- Budget Monitoring
- KPI Visualizations

## Analytics

- Expense Distribution Analysis
- Spending Trends
- Category-wise Insights
- Interactive Charts

## Transaction Management

- Transaction Recording
- Income Tracking
- Statement Upload & Parsing
- Historical Analysis

## Machine Learning Forecasting

- Random Forest Regression
- Expense Forecasting
- Trend Analysis
- Forecast Confidence
- Feature Importance Analysis

## Budget Intelligence

- Budget Risk Assessment
- Spending Projection
- Overspending Alerts
- Budget Utilization Analysis

## AI Features

### AI Financial Advisor

- Personalized Recommendations
- Spending Improvement Suggestions
- Financial Health Analysis

### FinSight Copilot

- Gemini-Powered Assistant
- Conversational Financial Guidance
- Context-Aware Insights

## Reporting

- Automated PDF Reports
- Expense Distribution
- Financial Summary
- Trend Analysis
- Stability Assessment

---

# Machine Learning Components

## Expense Forecasting

Random Forest Regression is used to analyze historical spending patterns and forecast future expenses.

## Budget Risk Prediction

Predicts the likelihood of exceeding budget limits based on projected expenses.

## Anomaly Detection

Identifies unusual spending behavior and potential financial risks.

## Financial Stability Scoring

Calculates financial health using:

- Savings Rate
- Budget Discipline
- Spending Volatility
- Transaction Anomalies

---

# Tech Stack

## Programming & Analytics

- Python
- Pandas
- NumPy

## Machine Learning

- Scikit-Learn
- Random Forest Regression

## Visualization

- Plotly
- Matplotlib

## Frontend

- Streamlit

## Database

- SQLite

## AI Integration

- Google Gemini API

## Reporting

- ReportLab

---

# Project Architecture

```bash
FinSight-AI/
│
├── assets/
├── components/
├── database/
├── models/
├── services/
├── utils/
│
├── app.py
├── requirements.txt
└── README.md
```

---

# Working Flow

1. Upload transaction data or bank statements
2. Clean and process data
3. Calculate financial metrics
4. Generate visual analytics
5. Forecast future expenses
6. Assess budget risks
7. Generate AI recommendations
8. Create automated financial reports

---

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/nandanavinothkumar-06/FinSight-AI.git
```

## Navigate to Project Folder

```bash
cd FinSight-AI
```

## Create Virtual Environment

```bash
python -m venv finsight
```

## Activate Environment

### Windows

```bash
finsight\Scripts\activate
```

### Linux/Mac

```bash
source finsight/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create a `.env` file

```env
GEMINI_API_KEY=your_api_key_here
```

## Run Application

```bash
streamlit run app.py
```

---

# Deployment

Deployed using Streamlit Cloud.

Application URL:

https://finsight-ai-personal-finance-tracker.streamlit.app/

---

# Future Enhancements

- Multi-user Authentication
- Investment Portfolio Tracking
- Financial Goal Planning
- Explainable AI Features
- Advanced Forecasting Models
- Real-Time Banking Integration

---

# Learning Outcomes

- Data Cleaning & Preprocessing
- Data Visualization
- Machine Learning Forecasting
- Financial Analytics
- Generative AI Integration
- Streamlit Development
- Cloud Deployment
- End-to-End Data Science Workflow

---

# Challenges Faced

- Statement Parsing
- Data Cleaning
- Forecasting Accuracy
- Gemini AI Integration
- PDF Report Generation
- Deployment Configuration

---

# Screenshots

## Dashboard

<img width="1918" height="1006" alt="image" src="https://github.com/user-attachments/assets/0ee9e285-3102-4285-b539-15ade21288f6" />


## Analytics

<img width="1918" height="1017" alt="image" src="https://github.com/user-attachments/assets/e08728e8-47ec-40a2-af10-64302a5c8784" />

## Transactions

<img width="1917" height="1017" alt="image" src="https://github.com/user-attachments/assets/2fe52d1b-b8d8-4839-abe6-8589216a4d03" />
<img width="1918" height="1015" alt="image" src="https://github.com/user-attachments/assets/544a1f84-11a5-42ce-a0b6-7d67ac305fbf" />


## Forecasting

<img width="1917" height="1017" alt="image" src="https://github.com/user-attachments/assets/f7c1b2b3-a83e-48a9-a6a8-ff7f4ee3c77d" />
<img width="1918" height="1017" alt="image" src="https://github.com/user-attachments/assets/47bae280-867b-4eb2-a7c0-10abf21deb2a" />
<img width="1918" height="1015" alt="image" src="https://github.com/user-attachments/assets/f169c3ad-0fbd-4489-bbb8-1b8ce590cc30" />

## Scenario simulator

<img width="1918" height="1020" alt="image" src="https://github.com/user-attachments/assets/4bbe8487-173b-49c0-81e4-9163345a6d92" />


## AI Advisor

<img width="1918" height="1021" alt="image" src="https://github.com/user-attachments/assets/8c228a9d-e97d-4bea-bdea-21b250658820" />


## FinSight Copilot

<img width="1918" height="1013" alt="image" src="https://github.com/user-attachments/assets/6b763e8b-7c2a-4f35-8f02-dac4d9ae2a33" />


## PDF Report

<img width="651" height="827" alt="image" src="https://github.com/user-attachments/assets/990247ec-86b8-4386-8b4c-97143b69386c" />


---

# Author

## Nandana Vinothkumar
Integrated M.Tech CSE (Data Science)  
VIT Vellore

### Areas of Interest

- Data Science
- Machine Learning
- Data Analytics
- Artificial Intelligence
- Financial Analytics

---

# License

This project is developed for educational, research, learning, and portfolio purposes.
