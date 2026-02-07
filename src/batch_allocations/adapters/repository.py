"""
Repository: The ORM should depend on the model
"""

# Boilerplate Modules
# -------------------

from typing import Protocol

# Domain Model Modules
# --------------------
from batch_allocations.domain.model import Batch

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


class SqlAlchemyRepository(RepositoryProtocol):
    """
    Notes:
    ------

    This is an 'Adapter': it implements the interface/abstraction (or Port).

    When using production code Flask instantiates the SqlAlchemyRepository with a 'real' database.
    """

    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return (
            self.session.query(Batch).filter_by(reference=reference).one()
        )  # one() is the "strict" execution method. It tells SQLAlchemy to execute the query and expects exactly one result

    def list(self):
        return self.session.query(Batch).all()


class FakeRepository(RepositoryProtocol):
    """
    Notes:
    ------

    When unit testing the service layer, the test files instantiate the FakeRepository class in memory.
    """

    def __init__(self, batches):
        self._batches = set(batches)

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)
