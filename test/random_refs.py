"""
Helper function to generate fake information
"""

# Boilerplate Modules
# -------------------

from faker import Faker
import faker_commerce

import random

import requests

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
