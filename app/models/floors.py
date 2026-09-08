"""Floor names"""

from enum import Enum


class FloorNames(str, Enum):
    """Fixed floor names 

    Attributes:
        BASEMENT
        GROUND_FLOOR
    """

    BASEMENT = "basement"
    GROUND_FLOOR = "ground_floor"
