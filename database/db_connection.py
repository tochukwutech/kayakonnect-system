"""
database/db_connection.py
PostgreSQL connection handler for KayaKonnect
"""

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()


def get_connection():
    """
    Returns a live PostgreSQL connection using .env credentials.
    Uses RealDictCursor so rows come back as dicts (column_name: value).
    """
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "kayakonnect"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        port=os.getenv("DB_PORT", "5433"),
        cursor_factory=RealDictCursor
    )
    return connection
