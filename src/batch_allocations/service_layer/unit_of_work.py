"""
This script implements the Unit of Work pattern. the purpose is decoupling the service layer from the 
data layer. It reliex on Python's context managers.
"""

# Boilerplate Modules
# -------------------

from typing import Protocol

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Domain Model Modules
# --------------------

from ..adapters.repository import RepositoryProtocol, SqlAlchemyRepository
from ..config import get_postgres_uri

# Constants
# ---------

DEFAULT_SESSION_FACTORY = sessionmaker( 
    bind=create_engine(
        get_postgres_uri(),
    )
)

# Functions and Class Definitions/Declarations
# --------------------------------------------

class UnitOfWorkProtocol(Protocol):
    batches: RepositoryProtocol

    def __exit__(self, *args):  
        self.rollback()  

    def commit(self):  
        raise NotImplementedError

    def rollback(self):  
        raise NotImplementedError



class SqlAlchemyUnitOfWork(UnitOfWorkProtocol):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory  

    def __enter__(self):
        """
        Excecutes when entering the with block.
        """
        self.session = self.session_factory()  # type: Session  
        self.batches = SqlAlchemyRepository(self.session)  
        return self

    def __exit__(self, exn_type, exn_value, traceback):
        """
        Excecutes when exit the with block.
        """
        super().__exit__(exn_type, exn_value, traceback) # Handle protocol
        self.rollback() # Default action. A UOW should commit only when it is explicitly told to.
        self.session.close()


    def commit(self): 
        self.session.commit()

    def rollback(self): 
        self.session.rollback()