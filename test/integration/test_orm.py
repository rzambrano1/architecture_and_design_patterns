"""
Testing ORM
"""

# Boilerplate Modules
# -------------------

from sqlalchemy import text

# Domain Model Modules
# --------------------
from batch_allocations.domain.model import OrderLine

# Fixtures
# --------

# Stored in conftest.py for clearer organization

# Test Functions
# --------------


def test_orderline_mapper_can_load_lines(session):
    session.execute(
        text(
            "INSERT INTO order_lines (orderid, sku, qty) VALUES "
            '("order1", "RED-CHAIR", 12),'
            '("order1", "RED-TABLE", 13),'
            '("order2", "BLUE-LIPSTICK", 14)'
        )
    )
    expected = [
        OrderLine("order1", "RED-CHAIR", 12),
        OrderLine("order1", "RED-TABLE", 13),
        OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]
    assert session.query(OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    new_line = OrderLine("order1", "DECORATIVE-WIDGET", 12)
    session.add(
        new_line
    )  # After mapping, SQLAlchemy can now save the OrderLine to the database
    session.commit()  # Becomes a row in order_lines table

    rows = list(session.execute(text('SELECT orderid, sku, qty FROM "order_lines"')))
    assert rows == [("order1", "DECORATIVE-WIDGET", 12)]
