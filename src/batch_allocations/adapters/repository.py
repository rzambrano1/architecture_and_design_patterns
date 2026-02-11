"""
Repository: The ORM should depend on the model
"""

# Boilerplate Modules
# -------------------

from typing import Protocol, List

# Domain Model Modules
# --------------------
from ..domain.model import Batch, Product

# Functions and Class Definitions/Declarations
# --------------------------------------------


class RepositoryProtocol(Protocol):
    """
    Notes:
    ------

    This is a 'Port': the interface between the application and what it is trying to abstract away.
    """

    def add(self, batch: Batch) -> None: ...

    def get(self, reference) -> Batch: ...

    def list(self) -> List[Batch]: ...


# When implementing the Aggregate pattern we go from a Repository to a ProductRepository


class ProductRepositoryProtocol(Protocol):

    def add(self, product: Product): ...

    def get(self, sku) -> Product: ...


class SqlAlchemyRepository(ProductRepositoryProtocol):
    """
    Notes:
    ------

    This is an 'Adapter': it implements the interface/abstraction (or Port).

    When using production code Flask instantiates the SqlAlchemyRepository with a 'real' database.
    """

    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def get(self, sku):
        return self.session.query(Product).filter_by(sku=sku).first()

    def get_by_batchref(self, batchref):
        return self.session.query(Batch).filter_by(reference=batchref).first()
