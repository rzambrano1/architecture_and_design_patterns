"""
The goal is that the model raises events -- which are facts about things that have happened.

The message bus will respond to the events.
"""

# Boilerplate Modules
# -------------------

from dataclasses import dataclass

# Functions and Class Definitions/Declarations
# --------------------------------------------


class Event:
    pass


@dataclass
class OutOfStock(Event):
    sku: str
