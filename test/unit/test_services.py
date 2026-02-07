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
from batch_allocations.service_layer.services import allocate, InvalidSku

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


# Test Functions
# --------------


def test_returns_allocation():
    line = OrderLine("o1", "COMPLICATED-LAMP", 10)
    batch = Batch("b1", "COMPLICATED-LAMP", 100, eta=None)
    repo = FakeRepository([batch])

    result = allocate(line, repo, FakeSession())
    assert result == "b1"


def test_error_for_invalid_sku():
    line = OrderLine("o1", "NONEXISTENTSKU", 10)
    batch = Batch("b1", "AREALSKU", 100, eta=None)
    repo = FakeRepository([batch])

    with pytest.raises(InvalidSku, match="Invalid sku NONEXISTENTSKU"):
        allocate(line, repo, FakeSession())


def test_commits():
    line = OrderLine("o1", "OMINOUS-MIRROR", 10)
    batch = Batch("b1", "OMINOUS-MIRROR", 100, eta=None)
    repo = FakeRepository([batch])
    session = FakeSession()

    allocate(line, repo, session)
    assert session.committed is True
