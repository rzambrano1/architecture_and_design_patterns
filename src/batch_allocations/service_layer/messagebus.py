"""
The messagebus will map events to handlers.
"""

# Boilerplate Modules
# -------------------

from typing import List, Dict, Callable, Type

# Domain Model Modules
# --------------------

from ..domain.events import Event, OutOfStock

# from ..adapters import email

# Helper Functions
# ----------------


def send_mail(to: str, message: str) -> None:
    print(">>> email sent >>>")
    return None


# Functions and Class Definitions/Declarations
# --------------------------------------------


def handle(event: Event):
    for handler in HANDLERS[type(event)]:
        handler(event)


def send_out_of_stock_notification(event: OutOfStock):
    send_mail(
        "stock@made.com",
        f"Out of stock for {event.sku}",
    )


HANDLERS = {
    OutOfStock: [send_out_of_stock_notification],
}  # type: Dict[Type[Event], List[Callable]]
