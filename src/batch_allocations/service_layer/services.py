"""
The Flask app should focus on web API endpoint tasks only. The app cannot do orchestration tasks.

Tasks such as fetching, validating, handling errors and committing should be the job of the service layer
(a.k.a orchestration layer). This layer sits between the Flask app and the domain model.

Tip: if the service-tests have the need to do a bunch of domain layer stuff, check if the service layer
is incomplete.
"""

# Boilerplate Modules
# -------------------

from typing import Optional

from datetime import date

# Domain Model Modules
# --------------------

from ..adapters.repository import RepositoryProtocol
from ..domain.model import OrderLine, Batch
from ..domain import (
    model,
)  # Imported model to avoid model.allocate to colide with services.allocate defined in this module.

from ..service_layer.unit_of_work import UnitOfWorkProtocol

# Functions and Class Definitions/Declarations
# --------------------------------------------


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    """Check if SKU exists in any batch"""
    return sku in {b.sku for b in batches}


def allocate(
    orderid: str,
    sku: str,
    qty: int,  # Fully decoupled from the domain layer.
    uow: UnitOfWorkProtocol,  # The one dependency in the service layer is with an abstract unit of work
) -> str:
    line = OrderLine(orderid, sku, qty)
    with uow:
        batches = uow.batches.list()
        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f"Invalid sku {line.sku}")
        batchref = model.allocate(line, batches)
        uow.commit()
    return batchref


def add_batch(
    ref: str,
    sku: str,
    qty: int,
    eta: Optional[date],
    uow: UnitOfWorkProtocol,
):
    with uow:
        uow.batches.add(model.Batch(ref, sku, qty, eta))
        uow.commit()
