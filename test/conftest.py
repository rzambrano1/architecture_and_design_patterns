"""
Shared test fixtures
"""

# Boilerplate Modules
# -------------------


import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

import os
import sys
import subprocess
import time
import requests

# Domain Model Modules
# --------------------
from batch_allocations.adapters import orm
from batch_allocations.config import get_api_url

# Fixture Definitions
# -------------------


@pytest.fixture(autouse=True, scope="session")
def set_test_env():
    os.environ["ENV"] = "test"


@pytest.fixture(scope="function")
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    orm.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def session(in_memory_db):
    orm.start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture
def restart_api():
    """
    Restarts the Flask API before each test.
    """
    proc = subprocess.Popen(
        [sys.executable, "-m", "batch_allocations.entrypoints.flask_app"],
        env=os.environ.copy(),
    )

    time.sleep(2.0)  # allow Flask time to start

    yield

    proc.kill()  # .kill() enforces a more agressive teardown than proc.terminate()
    proc.wait()


@pytest.fixture
def add_stock():
    """
    Helper fixture to add stock via API.
    """

    def _add_stock(batches):
        url = get_api_url()
        for ref, sku, qty, eta in batches:
            r = requests.post(
                f"{url}/add_batch",
                json={
                    "ref": ref,
                    "sku": sku,
                    "qty": qty,
                    "eta": eta,
                },
            )
            assert r.status_code == 201

    return _add_stock
