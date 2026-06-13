# ==================================================
# CREATE TABLES
# ==================================================

def create_tables(conn, cursor):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        expense_date TEXT NOT NULL,
        description TEXT,
        statement_id INTEGER
                   
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        income_date TEXT NOT NULL,
        source TEXT NOT NULL,
        description TEXT,
        statement_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS statements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT NOT NULL,
        upload_date TEXT NOT NULL,
        transaction_count INTEGER NOT NULL,
        total_expense REAL DEFAULT 0,
        total_income REAL DEFAULT 0
    )
    """)

    conn.commit()
# ==================================================
# EXPENSE CRUD
# ==================================================

def insert_expense(
    conn,
    amount,
    category,
    expense_date,
    description,
    statement_id= None
):

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO expenses
        (
            amount,
            category,
            expense_date,
            description,
            statement_id
        )
        VALUES (?, ?, ?, ?,?)
        """,
        (
            amount,
            category,
            expense_date,
            description,
            statement_id
        )
    )

    conn.commit()


def delete_expense(
    conn,
    expense_id
):

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE id = ?
        """,
        (expense_id,)
    )

    conn.commit()


# ==================================================
# INCOME CRUD
# ==================================================

def insert_income(
    conn,
    amount,
    income_date,
    source,
    description,
    statement_id = None
):

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO income
        (
            amount,
            income_date,
            source,
            description,
            statement_id
        )
        VALUES (?, ?, ?, ?,?)
        """,
        (
            amount,
            income_date,
            source,
            description,
            statement_id
        )
    )

    conn.commit()


def delete_income(
    conn,
    income_id
):

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM income
        WHERE id = ?
        """,
        (income_id,)
    )

    conn.commit()

def insert_statement(
    conn,
    file_name,
    upload_date,
    transaction_count,
    total_expense,
    total_income
):

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO statements
        (
            file_name,
            upload_date,
            transaction_count,
            total_expense,
            total_income
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            file_name,
            upload_date,
            transaction_count,
            total_expense,
            total_income
        )
    )

    conn.commit()

    return cursor.lastrowid

def get_statements(conn):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM statements
        ORDER BY id DESC
        """
    )

    return cursor.fetchall()

def delete_statement(
    conn,
    statement_id
):

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM expenses
        WHERE statement_id = ?
        """,
        (statement_id,)
    )

    cursor.execute(
        """
        DELETE FROM income
        WHERE statement_id = ?
        """,
        (statement_id,)
    )

    cursor.execute(
        """
        DELETE FROM statements
        WHERE id = ?
        """,
        (statement_id,)
    )

    conn.commit()

def clear_all_expenses(conn):

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses"
    )

    conn.commit()


def clear_all_income(conn):

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM income"
    )

    conn.commit()

def get_statement_count(conn):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM statements
        """
    )

    return cursor.fetchone()[0]

def statement_exists(conn, file_name):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM statements
        WHERE file_name = ?
        """,
        (file_name,)
    )

    return cursor.fetchone()[0] > 0

