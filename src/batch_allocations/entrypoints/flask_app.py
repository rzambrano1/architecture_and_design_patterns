"""
This module is the API
"""

# Boilerplate Modules
# -------------------

from flask import Flask, request, jsonify, send_from_directory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
from datetime import datetime

# Domain Model Modules
# --------------------

from ..config import get_postgres_uri
from ..domain.model import OrderLine
from ..domain.events import OutOfStock
from ..adapters.orm import start_mappers, metadata
from ..adapters.repository import SqlAlchemyRepository
from ..service_layer.services import allocate, add_batch, InvalidSku
from ..service_layer.unit_of_work import DEFAULT_SESSION_FACTORY, SqlAlchemyUnitOfWork
from ..domain.model import Batch

# Functions and Class Definitions/Declarations
# --------------------------------------------

# Initialize database
engine = create_engine(get_postgres_uri())
metadata.create_all(engine)
start_mappers()
get_session = sessionmaker(bind=engine)

app = Flask(__name__)


@app.route("/")
def home():
    """Root endpoint"""
    return {
        "service": "Batch Allocation API",
        "version": "1.0.0",
        "status": "running",
    }, 200


@app.route("/ui")
def ui():
    """Serve HTML interface"""
    return send_from_directory("static", "index.html")


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    """
    Allocate an order line to a batch.

    Request body:
        {
            "orderid": "order-123",
            "sku": "BLUE-CHAIR",
            "qty": 10
        }
    """

    orderid = request.json["orderid"]
    sku = request.json["sku"]
    qty = request.json["qty"]

    uow = SqlAlchemyUnitOfWork(session_factory=get_session)

    try:
        batchref = allocate(orderid, sku, qty, uow)
    except InvalidSku as e:
        return {"message": str(e)}, 400
    return {"message": "Order Allocated", "batchref": batchref}, 201


@app.route("/add_batch", methods=["POST"])
def add_batch_endpoint():

    eta = request.json.get("eta")
    if eta:
        eta = datetime.fromisoformat(eta).date()

    uow = SqlAlchemyUnitOfWork(session_factory=get_session)

    add_batch(
        request.json["ref"],
        request.json["sku"],
        request.json["qty"],
        eta,
        uow,
    )

    return {"message": "Batch commited"}, 201


if __name__ == "__main__":
    is_test = os.environ.get("ENV") == "test"
    app.run(debug=not is_test, host="0.0.0.0", port=5005)
