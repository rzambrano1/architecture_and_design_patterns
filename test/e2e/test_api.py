"""
This module contains two ent-to-end test for the Flask app.

The service layer helped the design avoid creating an inverted test pyramid.
"""

# Boilerplate Modules
# -------------------

import pytest
from faker import Faker
import faker_commerce

import requests
import random

# Domain Model Modules
# --------------------

from batch_allocations.config import get_api_url

# Helper Functions and Classes
# ----------------------------

faker_gen = Faker()
faker_gen.add_provider(faker_commerce.Provider)


def random_sku():
    """
    Helper function to generate a random sku in the style of the names used in the book.
    """
    full_output = faker_gen.ecommerce_name().split()

    # Grab the first word (adjective) and last word (object)
    adj = full_output[0]
    obj = full_output[-1]

    return f"{adj}-{obj}".upper()


def random_orderid():
    random_number = str(random.randint(100, 999))
    return f"order-{random_number}"


def random_batchref(num):
    random_number = str(random.randint(100, 999)) + str(num)
    return f"batch-{random_number}"


def post_to_add_batch(ref, sku, qty, eta):
    url = get_api_url()
    r = requests.post(
        f"{url}/add_batch", json={"ref": ref, "sku": sku, "qty": qty, "eta": eta}
    )
    assert r.status_code == 201


# Test Functions
# --------------


@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_201_and_allocated_batch():
    sku, othersku = random_sku(), random_sku()
    while sku == othersku:
        othersku = random_sku()
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)

    # The fixture was replaced with post_to_add_batch() call
    post_to_add_batch(laterbatch, sku, 100, "2011-01-02")
    post_to_add_batch(earlybatch, sku, 100, "2011-01-01")
    post_to_add_batch(otherbatch, othersku, 100, None)

    data = {"orderid": random_orderid(), "sku": sku, "qty": 3}
    url = get_api_url()

    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 201
    assert r.json()["batchref"] == earlybatch


@pytest.mark.usefixtures("restart_api")
def test_unhappy_path_returns_400_and_error_message():
    unknown_sku, orderid = random_sku(), random_orderid()
    data = {"orderid": orderid, "sku": unknown_sku, "qty": 20}
    url = get_api_url()
    r = requests.post(f"{url}/allocate", json=data)
    assert r.status_code == 400
    assert r.json()["message"] == f"Invalid sku {unknown_sku}"
