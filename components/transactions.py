import streamlit as st

import pandas as pd

from database.queries import (
    insert_expense,
    insert_income,
    delete_expense,
    delete_income,
    insert_statement,
    get_statements,
    delete_statement,
    statement_exists
)

from utils.statement_parser import (
    parse_statement
)

from services.gemini_service import (
    categorize_transaction
)


def show_transactions(
    conn,
    df,
    income_df
):

    # ---------------- SUCCESS MESSAGES ---------------- #

    if st.session_state.get("expense_added"):

        st.success(
            "Expense Added Successfully!"
        )

        del st.session_state["expense_added"]

    if st.session_state.get("income_added"):

        st.success(
            "Income Added Successfully!"
        )

        del st.session_state["income_added"]

    # ---------------- PAGE HEADER ---------------- #

    st.header("💳 Transactions")

    # ==================================================
    # ADD EXPENSE
    # ==================================================

    st.subheader("➕ Add Expense")

    with st.form("expense_form"):

        amount = st.number_input(
            "Amount",
            min_value=0.0
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Transport",
                "Shopping",
                "Entertainment",
                "Bills",
                "Healthcare",
                "Education",
                "Travel",
                "Groceries",
                "Fuel",
                "Insurance",
                "Investments",
                "Rent",
                "EMI",
                "Salary",
                "Transfers",
                "ATM Withdrawal",
                "Taxes",
                "Subscriptions",
                "Stationary",
                "Other"
            ]
        )

        expense_date = st.date_input(
            "Expense Date"
        )

        description = st.text_area(
            "Description"
        )

        submit_expense = st.form_submit_button(
            "Add Expense"
        )

        if submit_expense:

            if amount <= 0:

                st.error(
                    "Amount must be greater than 0"
                )

            else:

                insert_expense(
                    conn,
                    amount,
                    category,
                    str(expense_date),
                    description.strip()
                )

                st.session_state[
                    "expense_added"
                ] = True

                st.rerun()

    # ==================================================
    # ADD INCOME
    # ==================================================

    st.markdown("---")

    st.subheader("💰 Add Income")

    with st.form("income_form"):

        income_amount = st.number_input(
            "Income Amount",
            min_value=0.0
        )

        income_date = st.date_input(
            "Income Date"
        )

        source = st.text_input(
            "Source"
        )

        income_description = st.text_area(
            "Description"
        )

        submit_income = st.form_submit_button(
            "Add Income"
        )

        if submit_income:

            if income_amount <= 0:

                st.error(
                    "Income amount must be greater than 0"
                )

            elif source.strip() == "":

                st.error(
                    "Source cannot be empty"
                )

            else:

                insert_income(
                    conn,
                    income_amount,
                    str(income_date),
                    source.strip(),
                    income_description.strip()
                )

                st.session_state[
                    "income_added"
                ] = True

                st.rerun()
    
    # ==================================================
    # BANK STATEMENT UPLOAD
    # ==================================================

    st.markdown("---")

    st.subheader(
        "📄 Bank Statement Upload"
    )

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel Statement",
        type=["csv", "xlsx"]
    )

    if uploaded_file:

        try:

            if uploaded_file.name.endswith(".csv"):

                statement_df = pd.read_csv(
                    uploaded_file
                )

            else:

                statement_df = pd.read_excel(
                    uploaded_file
                )

            parsed_df = parse_statement(
                statement_df
            )

            st.success(
                "Statement Parsed Successfully"
            )

            st.dataframe(
                parsed_df.head(20),
                width="stretch"
            )

            # ==========================================
            # AI CATEGORIZATION
            # ==========================================

            if st.button(
                "🤖 Auto Categorize Transactions"
            ):

                with st.spinner(
                    "Gemini is categorizing transactions..."
                ):

                    categories = []

                    for _, row in parsed_df.iterrows():

                        transaction_type = str(
                            row["Type"]
                        ).strip()

                        if transaction_type == "Credit":

                            categories.append(
                                "Income"
                            )

                            continue

                        category = categorize_transaction(
                            str(
                                row["Description"]
                            )
                        )

                        categories.append(
                            category
                        )

                    parsed_df["Category"] = categories
                    st.session_state["categorized_df"] = parsed_df.copy()

                    st.session_state[
                        "categorized_df"
                    ] = parsed_df.copy()

                st.success(
                    "Categorization Complete"
                )
   

                st.dataframe(
                    parsed_df,
                    width="stretch"
                )

                debit_count = len(
                    parsed_df[
                        parsed_df["Type"] == "Debit"
                    ]
                )

                credit_count = len(
                    parsed_df[
                        parsed_df["Type"] == "Credit"
                    ]
                )

                total_expense_import = (
                    parsed_df[
                        parsed_df["Type"] == "Debit"
                    ]["Amount"]
                    .sum()
                )

                total_income_import = (
                    parsed_df[
                        parsed_df["Type"] == "Credit"
                    ]["Amount"]
                    .sum()
                )

                st.subheader(
                    "📊 Import Summary"
                )

                col1, col2, col3, col4, col5 = st.columns(5)

                with col1:
                    st.metric(
                        "Debit Txns",
                        debit_count
                    )

                with col2:
                    st.metric(
                        "Credit Txns",
                        credit_count
                    )

                with col3:
                    st.metric(
                        "Expenses",
                        f"₹ {total_expense_import:,.0f}"
                    )

                with col4:
                    st.metric(
                        "Income",
                        f"₹ {total_income_import:,.0f}"
                    )
                other_count = len(

                    parsed_df[
                        parsed_df["Category"] == "Other"
                    ]

                )

                other_percent = (
                    other_count /
                    len(parsed_df)
                ) * 100

                with col5:
                    st.metric(
                        "Uncategorized %",
                        f"{other_percent:.1f}%"
                    )
            
            if "categorized_df" in st.session_state:

                categorized_df = st.session_state[
                    "categorized_df"
                ]

                other_df = categorized_df[
                    categorized_df["Category"] == "Other"
                ]

                if not other_df.empty:

                    st.subheader(
                        "🔍 Review Uncategorized Transactions"
                    )

                    CATEGORY_OPTIONS = [

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

                    for idx in other_df.index:

                        current_value = (
                            st.session_state["categorized_df"]
                            .loc[idx, "Category"]
                        )

                        selected = st.selectbox(

                            other_df.loc[idx, "Description"],

                            CATEGORY_OPTIONS,

                            index=CATEGORY_OPTIONS.index(
                                current_value
                            ),

                            key=f"review_{idx}"

                        )

                        st.session_state[
                            "categorized_df"
                        ].loc[
                            idx,
                            "Category"
                        ] = selected

                    st.session_state[
                        "categorized_df"
                    ] = categorized_df

                    if st.button(
                        "💾 Save All Reviews"
                    ):

                        st.success(
                            "Review Saved"
                        )

            # ==========================================
            # IMPORT INTO DATABASE
            # ==========================================

            if (

                "categorized_df"

                in st.session_state

            ):

                if st.button(
                    "📥 Import Into FinSight"
                ):
                    if statement_exists(
                        conn,
                        uploaded_file.name
                    ):

                        st.warning(
                            "This statement has already been imported."
                        )

                        st.stop()

                    import_count = 0

                    categorized_df = st.session_state.get(
                        "categorized_df",
                        parsed_df
                    )

                    from datetime import datetime

                    total_expense_import = (
                        categorized_df[
                            categorized_df["Type"] == "Debit"
                        ]["Amount"].sum()
                    )

                    total_income_import = (
                        categorized_df[
                            categorized_df["Type"] == "Credit"
                        ]["Amount"].sum()
                    )

                    statement_id = insert_statement(
                        conn,
                        uploaded_file.name,
                        str(datetime.now().date()),
                        len(categorized_df),
                        float(total_expense_import),
                        float(total_income_import)
                    )

                    for _, row in categorized_df.iterrows():

                        transaction_type = str(
                            row.get(
                                "Type",
                                "Debit"
                            )
                        ).strip().lower()

                        if transaction_type == "debit":

                            insert_expense(
                                    conn,
                                    float(row["Amount"]),
                                    row["Category"],
                                    str(
                                        pd.to_datetime(
                                            row["Date"]
                                        ).date()
                                    ),
                                    str(
                                        row["Description"]
                                    ),
                                    statement_id
                                )

                        elif transaction_type == "credit":

                            insert_income(
                                conn,
                                float(row["Amount"]),
                                str(
                                    pd.to_datetime(
                                        row["Date"]
                                    ).date()
                                ),
                                "Bank Statement",
                                str(
                                    row["Description"]
                                ),
                                statement_id
                            )

                        import_count += 1

                    st.success(

                        f"{import_count} transactions imported successfully."

                    )

                    st.rerun()

        except Exception as e:

            st.error(
                f"Failed to parse statement: {e}"
            )

    # ==================================================
    # EXPENSE HISTORY
    # ==================================================

    st.markdown("---")

    st.subheader("📋 Expense History")

    if not df.empty:

        st.dataframe(
            df.sort_values(
                by="ID",
                ascending=False
            ),
            width="stretch"
        )

    else:

        st.info(
            "No expenses available."
        )

    st.markdown("---")

    st.subheader("🗑 Delete Expense")

    if not df.empty:

        expense_id = st.selectbox(
            "Select Expense ID",
            df["ID"]
        )

        if st.button(
            "Delete Expense",
            type="secondary"
        ):

            delete_expense(
                conn,
                int(expense_id)
            )

            st.success(
                "Expense Deleted Successfully!"
            )

            st.rerun()

    # ==================================================
    # INCOME HISTORY
    # ==================================================

    st.markdown("---")

    st.subheader("💰 Income History")

    if not income_df.empty:

        st.dataframe(
            income_df.sort_values(
                by="ID",
                ascending=False
            ),
            width="stretch"
        )

    else:

        st.info(
            "No income records available."
        )

    st.markdown("---")

    st.subheader("🗑 Delete Income")

    if not income_df.empty:

        income_id = st.selectbox(
            "Select Income ID",
            income_df["ID"]
        )

        if st.button(
            "Delete Income",
            type="secondary"
        ):

            delete_income(
                conn,
                int(income_id)
            )

            st.success(
                "Income Deleted Successfully!"
            )

            st.rerun()

    
    st.markdown("---")

    st.subheader(
        "📂 Statement History"
    )

    statements = get_statements(conn)

    if statements:

        statement_df = pd.DataFrame(
            statements,
            columns=[
                "ID",
                "File Name",
                "Upload Date",
                "Transactions",
                "Expense",
                "Income"
            ]
        )

        st.dataframe(
            statement_df,
            width="stretch"
        )

        selected_statement = st.selectbox(
            "Select Statement",
            statement_df["ID"]
        )

        if st.button(
            "🗑 Delete Statement"
        ):

            delete_statement(
                conn,
                int(selected_statement)
            )

            st.success(
                "Statement removed successfully."
            )

            st.rerun()

    else:

        st.info(
            "No statements uploaded yet."
        )
    
    
        