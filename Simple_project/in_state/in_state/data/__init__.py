from .state import STATES
from .district import DISTRICTS
from .tehsil import TEHSILS
from .state_village import get_villages_by_state_tehsil

__all__ = [
    "STATES",
    "DISTRICTS",
    "TEHSILS",
    "get_villages_by_state_tehsil",
]
