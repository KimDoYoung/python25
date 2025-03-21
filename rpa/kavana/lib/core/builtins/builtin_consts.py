from enum import Enum


class PointName(Enum):
    CENTER = "center"
    LEFT_TOP = "left_top"
    LEFT_MIDDLE = "left_middle"
    LEFT_BOTTOM = "left_bottom"
    MIDDLE_TOP = "middle_top"
    MIDDLE_BOTTOM = "middle_bottom"
    RIGHT_TOP = "right_top"
    RIGHT_MIDDLE = "right_middle"
    RIGHT_BOTTOM = "right_bottom"


class RegionName(Enum):
    LEFT_ONE_THIRD = "left_one_third"
    RIGHT_ONE_THIRD = "right_one"
    TOP_ONE_THIRD = "top_one_third"
    BOTTOM_ONE_THIRD = "bottom_one_third"
    LEFT_TOP = "left_top"
    RIGHT_TOP = "right_top"
    RIGHT_BOTTOM = "right_bottom"
    LEFT_BOTTOM = "left_bottom"
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
