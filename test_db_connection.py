"""
Test database connection. This file is not part of the application. It's meant to test setup.
"""

from sqlalchemy import create_engine, text
from src.batch_allocations.config import get_postgres_uri

def test_connection():
    # Create engine
    engine = create_engine(get_postgres_uri())
    
    # Test connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"   Connected to Postgres!")
        print(f"   Version: {version[:50]}...")

if __name__ == "__main__":
    test_connection()