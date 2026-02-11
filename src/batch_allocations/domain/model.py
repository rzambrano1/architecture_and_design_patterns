"""
Domain Model Layer
"""

# Boilerplate Modules
# -------------------

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Set

# Domain Model Modules
# --------------------

from ..domain.events import OutOfStock, Event

# Functions and Class Definitions/Declarations
# --------------------------------------------


@dataclass(unsafe_hash=True)  # This allows hashing even though it's mutable
class OrderLine:
    """Value Object Pattern"""

    orderid: str
    sku: str
    qty: int


class Batch:
    """Entity Object"""

    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set()  # type: Set[OrderLine]

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


# class OutOfStock(Exception):
#     pass


# To be able to mantain invariants while escaling to concurrent operations
# the Aggregate pattern is implemented.
class Product:
    def __init__(self, sku: str, batches: List[Batch], version_number: int = 0):
        self.sku = sku
        self.batches = batches  # This is a reference to a colection of batches
        self.version_number = version_number
        self.events: list[Event] = []

    # The function allocate now is a method of the new Aggregate class `Product`
    def allocate(self, line: OrderLine) -> Optional[str]:
        try:
            batch = next(b for b in sorted(self.batches) if b.can_allocate(line))
            batch.allocate(line)
            self.version_number += 1
            return batch.reference
        except StopIteration:
            self.events.append(OutOfStock(line.sku))
            # raise OutOfStock(f"Out of stock for sku {line.sku}")
            return None


# def allocate(line: OrderLine, batches: List[Batch]) -> str:
#     try:
#         batch = next(b for b in sorted(batches) if b.can_allocate(line))
#         batch.allocate(line)
#         return batch.reference
#     except StopIteration:
#         raise OutOfStock(f"Out of stock for sku {line.sku}")
