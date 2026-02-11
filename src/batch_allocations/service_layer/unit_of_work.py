"""
This script implements the Unit of Work pattern. the purpose is decoupling the service layer from the
data layer. It reliex on Python's context managers.
"""

# Boilerplate Modules
# -------------------

from __future__ import annotations

from typing import Protocol, Optional, Type, Any
from types import TracebackType

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Domain Model Modules
# --------------------

from ..adapters.repository import (
    RepositoryProtocol,
    ProductRepositoryProtocol,
    SqlAlchemyRepository,
)
from ..config import get_postgres_uri

# Constants
# ---------


def get_session_factory(uri=None, isolation_level=None):
    """Create session factory with appropriate isolation level"""
    if uri is None:
        uri = get_postgres_uri()

    # Only set isolation_level for PostgreSQL
    if uri.startswith("postgresql") and isolation_level:
        engine = create_engine(uri, isolation_level=isolation_level)
    else:
        # For SQLite, use default or SERIALIZABLE
        if uri.startswith("sqlite"):
            engine = create_engine(uri, isolation_level="SERIALIZABLE")
        else:
            engine = create_engine(uri)

    return sessionmaker(bind=engine)


# DEFAULT_SESSION_FACTORY = sessionmaker(
#     bind=create_engine(
#         get_postgres_uri(),
#         isolation_level="REPEATABLE READ",
#     )
# )

DEFAULT_SESSION_FACTORY = get_session_factory(
    isolation_level="REPEATABLE READ"  # Only applied to PostgreSQL
)

# Functions and Class Definitions/Declarations
# --------------------------------------------


class UnitOfWorkProtocol(Protocol):
    # batches: RepositoryProtocol
    products: ProductRepositoryProtocol  # With the Product Aggregate the RepositoryProtocol was updated to ProductRepositoryProtocol

    def __enter__(self) -> "UnitOfWorkProtocol": ...

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.rollback()

    def commit(self): ...

    def rollback(self): ...


class SqlAlchemyUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        """
        Excecutes when entering the with block.
        """
        self.session = self.session_factory()  # type: Session
        self.products = SqlAlchemyRepository(self.session)
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        """
        Excecutes when exit the with block.
        """
        super().__exit__(exn_type, exn_value, traceback)  # Handle protocol
        self.rollback()  # Default action. A UOW should commit only when it is explicitly told to.
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
