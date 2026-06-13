"""
Database Connection Manager
"""

import sqlite3
import streamlit as st


@st.cache_resource
def get_connection():

    conn = sqlite3.connect(
        "finance_tracker.db",
        check_same_thread=False
    )

    return conn
