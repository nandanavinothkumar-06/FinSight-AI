import pandas as pd
import streamlit as st


def load_expenses(_conn):

    query = """
    SELECT
        id,
        amount,
        category,
        expense_date,
        description
    FROM expenses
    """

    df = pd.read_sql_query(
        query,
        _conn
    )
    return df


def load_income(_conn):

    query = """
    SELECT
        id,
        amount,
        income_date,
        source,
        description
    FROM income
    """

    return pd.read_sql_query(
        query,
        _conn
    )