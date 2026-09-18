import sqlite3
from werkzeug.security import generate_password_hash

DB_PATH = "spendly.db"

def get_db():
    """
    Opens a connection to the SQLite database and configures it.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """
    Initializes the database schema.
    """
    conn = get_db()
    try:
        # Create users table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)

        # Create expenses table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        conn.commit()
    finally:
        conn.close()

def seed_db():
    """
    Seeds the database with initial demo data.
    """
    conn = get_db()
    try:
        # Check if data already exists to prevent duplication
        user_exists = conn.execute("SELECT 1 FROM users LIMIT 1").fetchone()
        if user_exists:
            return

        # Insert demo user
        password_hash = generate_password_hash("demo123")
        cursor = conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Demo User", "demo@spendly.com", password_hash)
        )
        user_id = cursor.lastrowid

        # Insert 8 sample expenses
        expenses = [
            (user_id, 12.50, 'Food', '2026-09-01', 'Lunch at Deli'),
            (user_id, 5.00, 'Transport', '2026-09-02', 'Bus fare'),
            (user_id, 120.00, 'Bills', '2026-09-05', 'Internet bill'),
            (user_id, 25.00, 'Health', '2026-09-08', 'Pharmacy'),
            (user_id, 15.00, 'Entertainment', '2026-09-10', 'Movie ticket'),
            (user_id, 45.00, 'Shopping', '2026-09-12', 'Clothing'),
            (user_id, 10.00, 'Other', '2026-09-15', 'Misc'),
            (user_id, 30.00, 'Food', '2026-09-16', 'Dinner with friends'),
        ]

        conn.executemany(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
            expenses
        )

        conn.commit()
    finally:
        conn.close()
