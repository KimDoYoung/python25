
from enum import Enum


class PointName(Enum):
    LEFT_TOP = 1
    RIGHT_TOP = 2
    RIGHT_BOTTOM = 3
    LEFT_BOTTOM = 4
    TOP_MIDDLE = 5
    BOTTOM_MIDDLE = 6
    LEFT_MIDDLE = 7
    RIGHT_MIDDLE = 8
    CENTER = 9    
    
class RegionName(Enum):
    LEFT_ONE_THIRD = 1
    RIGHT_ONE_THIRD = 2
    TOP_ONE_THIRD = 3
    BOTTOM_ONE_THIRD = 4
    LEFT_TOP = 5
    RIGHT_TOP = 6
    RIGHT_BOTTOM = 7
    LEFT_BOTTOM = 8
    CENTER = 9
    LEFT = 10
    RIGHT = 11
    TOP = 12
    BOTTOM = 13

class Direction(Enum):
    RIGHT = "Right"
    LEFT = "Left"
    UP = "Up"
    DOWN = "Down"
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"        