"""
Repository: The ORM should depend on the model
"""

# Boilerplate Modules
# -------------------

from typing import Protocol

# Domain Model Modules
# --------------------
from architecture_patterns.model import Batch

# Functions and Class Definitions/Declarations
# --------------------------------------------


class RepositoryProtocol(Protocol):

    def add(self, batch: Batch) -> None: ...

    def get(self, reference) -> Batch: ...


class SqlAlchemyRepository(RepositoryProtocol):
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
