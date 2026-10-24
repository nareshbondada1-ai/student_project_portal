import os
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Establish connection to PostgreSQL Cloud Database."""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def query_all(sql, params=None):
    """Execute SELECT and return rows as dictionary list."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params or ())
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

def query_one(sql, params=None):
    """Execute SELECT and return a single dictionary row."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params or ())
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def execute_commit(sql, params=None):
    """Execute INSERT/UPDATE/DELETE and commit changes."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params or ())
        conn.commit()
    finally:
        cursor.close()
        conn.close()