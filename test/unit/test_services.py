"""
Tests the service layer
"""

# Boilerplate Modules
# -------------------

import pytest
from typing import Protocol

# Domain Model Modules
# --------------------

from batch_allocations.adapters.repository import RepositoryProtocol
from batch_allocations.domain.model import OrderLine, Batch
from batch_allocations.service_layer.services import allocate, add_batch, InvalidSku
from batch_allocations.service_layer.unit_of_work import UnitOfWorkProtocol

# Helper Functions and Classes
# ----------------------------


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


class FakeSession:
    """
    Notes:
    -----

    Temporary solution to test commits to a database.
    """

    committed = False

    def commit(self):
        self.committed = True

class FakeUnitOfWork(UnitOfWorkProtocol):
    def __init__(self):
        self.batches = FakeRepository([])  
        self.committed = False  

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return self.rollback()

    def commit(self):
        self.committed = True  

    def rollback(self):
        pass

# Test Functions
# --------------

# <-------------------------------------------- test_allocate_returns_allocation -------------------------------------------->
# <--------------------------------------------         record of changes        -------------------------------------------->

# [[1]] This function was replaced by test_allocate_returns_allocation() as a result of the signature change of services.allocate()
# def test_returns_allocation():
    # line = OrderLine("o1", "COMPLICATED-LAMP", 10)          # Commented out because now allocate is expresseed in primitives
    # batch = Batch("b1", "COMPLICATED-LAMP", 100, eta=None)  # No longer necessary because of services.add_batch() that 
                                                              # expresses a batch on terms of primitives.
    # repo = FakeRepository([batch])

    # result = allocate(line, repo, FakeSession()) # Uses old allocate() signature
    # result = allocate("b1", "COMPLICATED-LAMP", 100, repo, FakeSession())
    # assert result == "b1"

# [[2]] Once the unit of work was introduced the test was upgraded again. 
# def test_allocate_returns_allocation():
#     repo, session = FakeRepository([]), FakeSession()
#     add_batch("batch1", "COMPLICATED-LAMP", 100, None, repo, session)
#     result = allocate("o1", "COMPLICATED-LAMP", 10, repo, session)
#     assert result == "batch1"

def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()  
    add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)  
    result = allocate("o1", "COMPLICATED-LAMP", 10, uow)  
    assert result == "batch1"



# <------------------------------------------ test_allocate_errors_for_invalid_sku ------------------------------------------>
# <--------------------------------------------         record of changes        -------------------------------------------->
# [[1]] This function was replaced by test_allocate_errors_for_invalid_sku() as a result of the signature change of 
# services.allocate()and the addition of the missing service add_batch()
# def test_error_for_invalid_sku():
#     line = OrderLine("o1", "NONEXISTENTSKU", 10)
#     batch = Batch("b1", "AREALSKU", 100, eta=None)
#     repo = FakeRepository([batch])

#     with pytest.raises(InvalidSku, match="Invalid sku NONEXISTENTSKU"):
#         allocate(line, repo, FakeSession())

# [[2]] Replaced again to account for unit of work
# def test_allocate_errors_for_invalid_sku():
#     repo, session = FakeRepository([]), FakeSession()
#     add_batch("b1", "AREALSKU", 100, None, repo, session)

#     with pytest.raises(InvalidSku, match="Invalid sku NONEXISTENTSKU"):
#         allocate("o1", "NONEXISTENTSKU", 10, repo, FakeSession())


def test_allocate_errors_for_invalid_sku(session_factory):
    uow = FakeUnitOfWork()
    add_batch("b1", "AREALSKU", 100, None, uow)

    with pytest.raises(InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        allocate("o1", "NONEXISTENTSKU", 10, uow)

def test_commits(session_factory):

    # No longer needed
    # line = OrderLine("o1", "OMINOUS-MIRROR", 10)
    # batch = Batch("b1", "OMINOUS-MIRROR", 100, eta=None)
    # repo = FakeRepository([batch])
    # session = FakeSession()

    # allocate(line, repo, session) # Not compatible with updated allocate()

    uow = FakeUnitOfWork()
    add_batch("b1", "OMINOUS-MIRROR", 100, None, uow)
    allocate("o1", "OMINOUS-MIRROR", 10, uow)
    assert uow.committed is True

# <----------------------------------------------------- test_add_batch ----------------------------------------------------->
# <--------------------------------------------         record of changes        -------------------------------------------->

# [[1]] This function was also upgraded with the introduction of the unit of work
# def test_add_batch():
#     repo, session = FakeRepository([]), FakeSession()
#     add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, repo, session)
#     assert repo.get("b1") is not None
#     assert session.committed

def test_add_batch():
    uow = FakeUnitOfWork()  
    add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)  
    assert uow.batches.get("b1") is not None
    assert uow.committed


