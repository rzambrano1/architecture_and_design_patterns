"""
Testing Repository
"""

# Boilerplate Modules
# -------------------


from sqlalchemy import text

# Domain Model Modules
# --------------------
from architecture_patterns.model import Batch, OrderLine
from architecture_patterns.repository import SqlAlchemyRepository

# Fixtures
# --------

# Stored in conftest.py for clearer organization

# Helper Functions
# ----------------


def insert_order_line(session):
    session.execute(
        text(
            "INSERT INTO order_lines (orderid, sku, qty)"
            ' VALUES ("order1", "GENERIC-SOFA", 12)'
        )
    )
    [[orderline_id]] = session.execute(
        text("SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku"),
        dict(orderid="order1", sku="GENERIC-SOFA"),
    )
    return orderline_id


def insert_batch(
    session, batch_ref
):  # I did not understand why the batch_id was passed as a
    # string parameter instead of the Batch instance
    session.execute(
        text(
            "INSERT INTO batch_stock (reference, sku, _purchased_quantity, eta)"
            ' VALUES (:ref, "GENERIC-SOFA", 100, NULL)'
        ),
        dict(ref=batch_ref),
    )
    [[batch_id_result]] = session.execute(
        text("SELECT id FROM batch_stock WHERE reference=:ref AND sku=:sku"),
        dict(ref=batch_ref, sku="GENERIC-SOFA"),
    )
    return batch_id_result


def insert_allocation(session, orderline_id, batch_id):
    session.execute(
        text(
            "INSERT INTO allocations (orderline_id, batch_id)"
            " VALUES (:orderline_id, :batch_id)"
        ),
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )


# Test Functions
# --------------


def test_repository_can_save_a_batch(session):
    batch = Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

    repo = SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.execute(
        text('SELECT reference, sku, _purchased_quantity, eta FROM "batch_stock"')
    )
    assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]


def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)

    repo = SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = Batch("batch1", "GENERIC-SOFA", 100, eta=None)
    assert retrieved == expected  # Batch.__eq__ only compares reference
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        OrderLine("order1", "GENERIC-SOFA", 12),
    }
