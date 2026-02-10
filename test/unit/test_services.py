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


def test_allocate_returns_allocation():
    uow = FakeUnitOfWork()
    add_batch("batch1", "COMPLICATED-LAMP", 100, None, uow)
    result = allocate("o1", "COMPLICATED-LAMP", 10, uow)
    assert result == "batch1"


def test_allocate_errors_for_invalid_sku(session_factory):
    uow = FakeUnitOfWork()
    add_batch("b1", "AREALSKU", 100, None, uow)

    with pytest.raises(InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        allocate("o1", "NONEXISTENTSKU", 10, uow)


def test_commits(session_factory):
    uow = FakeUnitOfWork()
    add_batch("b1", "OMINOUS-MIRROR", 100, None, uow)
    allocate("o1", "OMINOUS-MIRROR", 10, uow)
    assert uow.committed is True


def test_add_batch():
    uow = FakeUnitOfWork()
    add_batch("b1", "CRUNCHY-ARMCHAIR", 100, None, uow)
    assert uow.batches.get("b1") is not None
    assert uow.committed
