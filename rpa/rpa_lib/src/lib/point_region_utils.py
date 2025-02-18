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

def get_point(region , point_name: PointName):
    ''' region 에서 point_name 에 해당하는 좌표를 반환한다.'''
    x, y, w, h = region
    if point_name == PointName.LEFT_TOP:
        return x, y
    elif point_name == PointName.RIGHT_TOP:
        return x+w, y
    elif point_name == PointName.RIGHT_BOTTOM:
        return x+w, y+h
    elif point_name == PointName.LEFT_BOTTOM:
        return x, y+h
    elif point_name == PointName.TOP_MIDDLE:
        return x+w//2, y
    elif point_name == PointName.BOTTOM_MIDDLE:
        return x+w//2, y+h
    elif point_name == PointName.LEFT_MIDDLE:
        return x, y+h//2
    elif point_name == PointName.RIGHT_MIDDLE:
        return x+w, y+h//2
    elif point_name == PointName.CENTER:
        return x+w//2, y+h//2
    else:
        raise ValueError('Invalid point_name: %s' % point_name)
