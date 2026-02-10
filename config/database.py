import psycopg2
from .config import DATABASE_URL

def get_connection():
    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL not configured in .env file.\n"
            "Add DATABASE_URL=postgresql://user:password@host/database to .env file"
        )
    try:
        return psycopg2.connect(DATABASE_URL)
    except psycopg2.OperationalError as e:
        raise RuntimeError(f"Failed to connect to database: {str(e)}")

def is_database_available():
    """Check if database connection is available"""
    try:
        conn = get_connection()
        conn.close()
        return True
    except:
        return False
