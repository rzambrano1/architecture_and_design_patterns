"""
The application will access configurantions in this script. In this case, the database configuration.
"""

import os

from dotenv import load_dotenv

# Load .env file
load_dotenv()


def get_postgres_uri():
    """Get Postgres connection string"""
    if os.environ.get("ENV") == "test":
        return get_sqlite_uri()

    host = os.environ.get("DB_HOST", "localhost")
    port = 54321 if host == "localhost" else 5432
    user = os.environ.get("DB_USER", "batch_allocations")
    password = os.environ.get("DB_PASSWORD")
    db_name = "batch_allocations"

    if not password:
        raise ValueError("DB_PASSWORD environment variable must be set")

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    """Get API URL"""
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"


def get_sqlite_uri():
    """Get SQLite connection string for tests"""
    return "sqlite:///test.db"  # Originally I used "sqlite:///:memory:" but using memory would not
    # allow both processes in the test to talk to the same database
    # because of restart_api fixture.
