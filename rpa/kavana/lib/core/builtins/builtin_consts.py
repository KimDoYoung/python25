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
    LEFT_ONE_THIRD = "left_one_third"
    RIGHT_ONE_THIRD = "right_one"
    TOP_ONE_THIRD = "top_one_third"
    BOTTOM_ONE_THIRD = "bottom_one_third"
    TOP_LEFT = "top_left"
    BOTTOM_LEFT = "bottom_left"
    TOP_RIGHT = "top_right"
    BOTTOM_RIGHT = "bottom_right"         
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
