import os
from pathlib import Path
import oracledb
from dotenv import load_dotenv

# Ensure .env is always loaded from the project folder
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

DB_USER = os.getenv("DB_USER", "system")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Oracle_123")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_SERVICE = os.getenv("DB_SERVICE_NAME", "FREEPDB1")
def get_db_connection():
    """Establish connection to Oracle Database in Thin mode."""
    dsn = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"
    connection = oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=dsn
    )
    return connection

def query_all(sql, params=None):
    """Execute a SELECT query and return rows as a list of dictionaries."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params or {})
        # Extract column names in lowercase
        cols = [col[0].lower() for col in cursor.description]
        rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
        return rows
    finally:
        cursor.close()
        conn.close()

def query_one(sql, params=None):
    """Execute a SELECT query and return a single dictionary row."""
    rows = query_all(sql, params)
    return rows[0] if rows else None

def execute_commit(sql, params=None):
    """Execute INSERT/UPDATE/DELETE and commit changes."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params or {})
        conn.commit()
    finally:
        cursor.close()
        conn.close()