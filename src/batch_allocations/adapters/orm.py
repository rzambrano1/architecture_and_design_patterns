"""
Repository: The ORM should depend on the model
"""

# Boilerplate Modules
# -------------------

from sqlalchemy import Column, Date, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.orm import registry, relationship

# Domain Model Modules
# --------------------
from batch_allocations.domain.model import Batch, OrderLine

# Functions and Class Definitions/Declarations
# --------------------------------------------

metadata = (
    MetaData()
)  # A container that holds all your table definitions and schema information

mapper_registry = registry(metadata=metadata)  # Creates the registry instance

order_lines = Table(
    "order_lines",  # Table name in the database
    metadata,  # Links this table to the metadata catalog
    # These statements define the database schema
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

batch_stock = Table(
    "batch_stock",  # Table name
    metadata,
    # Schema
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("reference", String(255)),  # Match Batch.reference attribute
    Column("sku", String(255)),
    Column("_purchased_quantity", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

# Association table to track which order lines are allocated to which batches in our batch stock
allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", Integer, ForeignKey("order_lines.id")),
    Column("batch_id", Integer, ForeignKey("batch_stock.id")),
)

# Schema Diagram
# [diagram generated using LLM]
#
# ┌─────────────┐         ┌──────────────┐         ┌─────────────────────┐
# │ order_lines │         │ allocations  │         │  batch_stock        │
# ├─────────────┤         ├──────────────┤         ├─────────────────────┤
# │ id (PK)     │◄────────│orderline_id  │         │ id (PK)             │
# │ orderid     │         │batch_id      │────────►│ reference           │
# │ sku         │         └──────────────┘         │ sku                 │
# │ qty         │                                  │_purchased_quantity  │
# └─────────────┘                                  │ eta                 │
#                                                  └─────────────────────┘
#


def start_mappers():
    """
    Creates a mapping between the Python class and the database table

    model.OrderLine = the domain class (business logic)
    order_lines = the database table (persistence layer)
    mapper() = connects them so SQLAlchemy knows how to convert between them
    """
    lines_mapper = mapper_registry.map_imperatively(OrderLine, order_lines)

    mapper_registry.map_imperatively(
        Batch,
        batch_stock,
        properties={
            "_allocations": relationship(
                lines_mapper,
                secondary=allocations,  # The join table
                collection_class=set,  # Store as a set (matches domain model)
            )
        },
    )
