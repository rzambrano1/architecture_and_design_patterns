"""
The Flask app should focus on web API endpoint tasks only. The app cannot do orchestration tasks.

Tasks such as fetching, validating, handling errors and committing should be the job of the service layer
(a.k.a orchestration layer). This layer sits between the Flask app and the domain model.
"""

# Boilerplate Modules
# -------------------

# Domain Model Modules
# --------------------

from ..adapters.repository import RepositoryProtocol
from ..domain.model import OrderLine, Batch
from ..domain import (
    model,
)  # Imported model to avoid model.allocate to colide with services.allocate defined in this module.

# Functions and Class Definitions/Declarations
# --------------------------------------------


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    """Check if SKU exists in any batch"""
    return sku in {b.sku for b in batches}


def allocate(line: OrderLine, repo: RepositoryProtocol, session) -> str:
    """

    Parameters:
    -----------

    line :  OrderLine

    repo : RepositoryProtocol
        This makes the service layer dependent on a repository, By
        depending on the protocol will make this function work with
        both FakeRepository (for tests) and SqlAlcemyRepository
        (for when running the Flask app). This approach follows
        the Dependency Inversion Principle concept of depending
        on abstractions.

    session

    Notes:
    ------

    This function does orchestration tasks, such as fetching objects from
    the repository, making checks/assertions about the request against
    current state of the world, and saves or updates any changed state.
    """
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = model.allocate(line, batches)
    session.commit()
    return batchref
