import pandas as pd

# ==================================================
# COLUMN DETECTION
# ==================================================

DATE_COLUMNS = [
    "date",
    "txn date",
    "transaction date",
    "value date",
    "posting date",
    "tran date"
]

DESCRIPTION_COLUMNS = [
    "description",
    "narration",
    "particulars",
    "remarks",
    "details",
    "name"
]

DEBIT_COLUMNS = [
    "debit",
    "deb",
    "withdrawal",
    "withdrawal amt",
    "withdrawal amount",
    "debit amount",
    "dr amount"
]

CREDIT_COLUMNS = [
    "credit",
    "cred",
    "deposit",
    "deposit amt",
    "deposit amount",
    "credit amount",
    "cr amount"
]

TYPE_COLUMNS = [
    "drcr",
    "transaction type",
    "type"
]

AMOUNT_COLUMNS = [
    "amount",
    "transaction amount"
]


# ==================================================
# FIND COLUMN
# ==================================================

def find_column(df, candidates):

    for col in df.columns:

        col_lower = str(col).lower().strip()

        for candidate in candidates:

            candidate = candidate.lower().strip()

            if col_lower == candidate:

                return col

    return None


# ==================================================
# PARSE STATEMENT
# ==================================================

def parse_statement(df):

    # ------------------------------------------
    # CLEAN COLUMN NAMES
    # ------------------------------------------

    df.columns = [

        str(col).strip()

        for col in df.columns

    ]

    # ------------------------------------------
    # DETECT COLUMNS
    # ------------------------------------------

    date_col = find_column(
        df,
        DATE_COLUMNS
    )

    description_col = find_column(
        df,
        DESCRIPTION_COLUMNS
    )

    debit_col = find_column(
        df,
        DEBIT_COLUMNS
    )

    credit_col = find_column(
        df,
        CREDIT_COLUMNS
    )

    type_col = find_column(
        df,
        TYPE_COLUMNS
    )

    amount_col = find_column(
        df,
        AMOUNT_COLUMNS
    )

    # ------------------------------------------
    # VALIDATION
    # ------------------------------------------

    if not date_col:

        raise ValueError(
            f"Date column not detected. Columns found: {list(df.columns)}"
        )

    if not description_col:

        raise ValueError(
            f"Description column not detected. Columns found: {list(df.columns)}"
        )

    # ------------------------------------------
    # DATE CLEANING
    # ------------------------------------------

    date_series = df[date_col].astype(str).str.strip()

    # DD-MM-YYYY
    parsed_dates = pd.to_datetime(
        date_series,
        format="%d-%m-%Y",
        errors="coerce"
    )

    # DD/MM/YYYY
    mask = parsed_dates.isna()

    parsed_dates.loc[mask] = pd.to_datetime(
        date_series.loc[mask],
        format="%d/%m/%Y",
        errors="coerce"
    )

    # DD-Mon-YYYY
    mask = parsed_dates.isna()

    parsed_dates.loc[mask] = pd.to_datetime(
        date_series.loc[mask],
        format="%d-%b-%Y",
        errors="coerce"
    )

    # YYYY-MM-DD
    mask = parsed_dates.isna()

    parsed_dates.loc[mask] = pd.to_datetime(
        date_series.loc[mask],
        format="%Y-%m-%d",
        errors="coerce"
    )

    df[date_col] = parsed_dates

    df = df.dropna(subset=[date_col])

    parsed_rows = []

    # ==================================================
    # FORMAT 1
    # DATE | DESCRIPTION | DEBIT | CREDIT
    # ==================================================

    if debit_col or credit_col:

        for _, row in df.iterrows():

            # -------------------------
            # DEBIT
            # -------------------------

            if debit_col:

                try:

                    debit_value = pd.to_numeric(
                        row[debit_col],
                        errors="coerce"
                    )

                    if (
                        pd.notna(debit_value)
                        and debit_value > 0
                    ):

                        parsed_rows.append({

                            "Date":
                            row[date_col],

                            "Description":
                            str(
                                row[description_col]
                            ),

                            "Amount":
                            float(
                                debit_value
                            ),

                            "Type":
                            "Debit"

                        })

                except:
                    pass

            # -------------------------
            # CREDIT
            # -------------------------

            if credit_col:

                try:

                    credit_value = pd.to_numeric(
                        row[credit_col],
                        errors="coerce"
                    )

                    if (
                        pd.notna(credit_value)
                        and credit_value > 0
                    ):

                        parsed_rows.append({

                            "Date":
                            row[date_col],

                            "Description":
                            str(
                                row[description_col]
                            ),

                            "Amount":
                            float(
                                credit_value
                            ),

                            "Type":
                            "Credit"

                        })

                except:
                    pass

    # ==================================================
    # FORMAT 2
    # DATE | DESCRIPTION | AMOUNT | DRCR
    # ==================================================

    elif amount_col and type_col:

        for _, row in df.iterrows():

            txn_type = str(
                row[type_col]
            ).strip().upper()

            if txn_type in [
                "DEBIT",
                "DB",
                "DR",
                "WITHDRAWAL"
            ]:

                parsed_type = "Debit"

            elif txn_type in [
                "CREDIT",
                "CR",
                "DEPOSIT"
            ]:

                parsed_type = "Credit"

            else:

                parsed_type = "Unknown"

            try:

                amount = pd.to_numeric(
                    row[amount_col],
                    errors="coerce"
                )

                if pd.isna(amount):

                    amount = 0

            except:

                amount = 0

            parsed_rows.append({

                "Date":
                row[date_col],

                "Description":
                str(
                    row[description_col]
                ),

                "Amount":
                float(amount),

                "Type":
                parsed_type

            })

    else:

        raise ValueError(
            "Unsupported statement format."
        )

    # ==================================================
    # CREATE DATAFRAME
    # ==================================================

    parsed_df = pd.DataFrame(
        parsed_rows
    )

    if not parsed_df.empty:

        parsed_df = parsed_df.sort_values(
            "Date"
        )

        parsed_df.reset_index(
            drop=True,
            inplace=True
        )
    
    return parsed_df