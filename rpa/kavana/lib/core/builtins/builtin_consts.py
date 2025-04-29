from enum import Enum


class PointName(Enum):
    CENTER = "center"
    TOP_LEFT = "top-left"
    MIDDLE_LEFT = "middle-left"
    BOTTOM_LEFT = "bottom-left"
    TOP_CENTER = "top-center"
    BOTTOM_CENTER = "bottom-center"
    TOP_RIGHT = "top-right"
    MIDDLE_RIGHT = "middle-right"
    BOTTOM_RIGHT = "bottom-right"

class RegionName(Enum):
    LEFT_ONE_THIRD = "left-one-third"
    RIGHT_ONE_THIRD = "right-one-third"
    TOP_ONE_THIRD = "top-one-third"
    BOTTOM_ONE_THIRD = "bottom-one-third"
    TOP_LEFT = "top-left"
    BOTTOM_LEFT = "bottom-left"
    TOP_RIGHT = "top-right"
    BOTTOM_RIGHT = "bottom-right"
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"
    TOP = "top"
    BOTTOM = "bottom"

class DirectionName(Enum):
    RIGHT = "right"
    LEFT = "left"
    UP = "up"
    DOWN = "down"
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
