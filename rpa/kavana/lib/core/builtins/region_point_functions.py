from typing import Tuple

from lib.core.builtins.builtin_consts import PointName, RegionName
from lib.core.datatypes.point import Point
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.token import Token, TokenStatus
from lib.core.token_custom import PointToken, RegionToken
from lib.core.token_util import TokenUtil



class RegionPointFunctions:
    """Region과 Point 관련 내장 함수들"""
    
    executor = None  # ✅ 클래스 변수로 executor 저장

    @staticmethod
    def set_executor(executor_instance):
        RegionPointFunctions.executor = executor_instance

    @staticmethod
    def REGION_DEVIDE_BY_POINT(region: Tuple[int, int, int, int], point: Tuple[int, int], name:str) -> Token:
        """Region을 Point로 나누기"""
        x,y,w,h = region
        point_x, point_y = point
        if name.lower() == "left":
            result_region = (x, y, point_x - x, h)
        elif name.lower() == "right":
            result_region = (point_x, y, w - (point_x - x), h)
        elif name.lower() == "top":
            result_region = (x, y, w, point_y - y)
        elif name.lower() == "bottom":
            result_region = (x, point_y, w, h - (point_y - y))
        else:
            raise KavanaValueError(f"DEVIDE_REGION_BY_POINT: 잘못된 영역이름입니다.: {name}")
        
        result_token = TokenUtil.region_to_token(result_region)
        return result_token

    @staticmethod
    def IS_POINT_IN_REGION(p: Tuple[int,int], region: Tuple[int, int, int, int]) -> Token:
        """Point p가 Region에 포함되는지 여부를 반환"""
        x, y, width, height = region
        px, py = p
        if x <= px <= x + width and y <= py <= y + height:
            return TokenUtil.boolean_to_boolean_token(True)
        else:
            return TokenUtil.boolean_to_boolean_token(False)

    @staticmethod
    def POINT_OF_REGION(region: Tuple[int, int, int, int], point_name: str) -> PointToken:
        """Region 객체 (x, y, width, height) 에서 point_name에 해당하는 PointToken 반환"""
        x, y, width, height = region
        point_name = point_name.lower()  # 🔥 대소문자 구분 없이 처리
        pt = None
        if point_name == PointName.CENTER.value:
            pt=Point(x + width // 2, y + height // 2)
        elif point_name == PointName.TOP_LEFT.value:
            pt=Point(x, y)
        elif point_name == PointName.TOP_CENTER.value:
            pt=Point(x + width // 2, y)
        elif point_name == PointName.TOP_RIGHT.value:
            pt=Point(x + width, y)
        elif point_name == PointName.MIDDLE_LEFT.value:
            pt=Point(x, y + height // 2)
        elif point_name == PointName.MIDDLE_RIGHT.value:
            pt=Point(x + width, y + height // 2)
        elif point_name == PointName.BOTTOM_LEFT.value:
            pt=Point(x, y + height)
        elif point_name == PointName.BOTTOM_CENTER.value:
            pt=Point(x + width // 2, y + height)
        elif point_name == PointName.BOTTOM_RIGHT.value:
            pt=Point(x + width, y + height)
        else:
            raise KavanaValueError(f"Unknown point name: {point_name}")
        point_token=  PointToken(data=pt)
        point_token.status = TokenStatus.EVALUATED
        return point_token
    
    def REGION_OF_REGION(region: Tuple[int, int, int, int], region_name: str) -> RegionToken:
        """Region 객체 (x, y, width, height) 에서 region_name에 해당하는 RegionToken 반환"""
        x, y, width, height = region
        region_name = region_name.lower().replace("_", "-")  # 🔥 대소문자 구분 없이 처리
        if region_name == RegionName.LEFT_ONE_THIRD.value:
            return TokenUtil.region_to_token((x, y, width // 3, height))
        elif region_name == RegionName.RIGHT_ONE_THIRD.value:
            return TokenUtil.region_to_token((x + 2 * (width // 3), y, width // 3, height))
        elif region_name == RegionName.TOP_ONE_THIRD.value:
            return TokenUtil.region_to_token((x, y, width, height // 3))
        elif region_name == RegionName.BOTTOM_ONE_THIRD.value:
            return TokenUtil.region_to_token((x, y + 2 * (height // 3), width, height // 3))
        elif region_name == RegionName.TOP_LEFT.value:
            return TokenUtil.region_to_token((x, y, width // 2, height // 2))
        elif region_name == RegionName.TOP_RIGHT.value:
            return TokenUtil.region_to_token((x + width // 2, y, width // 2, height // 2))
        elif region_name == RegionName.BOTTOM_RIGHT.value:
            return TokenUtil.region_to_token((x + width // 2, y + height // 2, width // 2, height // 2))
        elif region_name == RegionName.BOTTOM_LEFT.value:
            return TokenUtil.region_to_token((x, y + height // 2, width // 2, height // 2))
        elif region_name == RegionName.CENTER.value:
            return TokenUtil.region_to_token((x + width // 3, y + height // 3, width // 3, height // 3))
        elif region_name == RegionName.LEFT.value:
            return TokenUtil.region_to_token((x, y, width // 2, height))
        elif region_name == RegionName.RIGHT.value:
            return TokenUtil.region_to_token((x + width // 2, y, width // 2, height))
        elif region_name == RegionName.TOP.value:
            return TokenUtil.region_to_token((x, y, width, height // 2))
        elif region_name == RegionName.BOTTOM.value:
            return TokenUtil.region_to_token((x, y + height // 2, width, height // 2))
        else:
            raise KavanaValueError(f"Unknown region name: {region_name}")
    
    @staticmethod    
    def POINT_MOVE(p: Tuple[int,int], move_str:str) -> RegionToken:
        """ 
            p를 move_str 만큼 이동시킨 PointToken 반환
            move_str는 "N:30, S:20, E:10, W:5" 형식으로 주어짐
            N: 북쪽, S: 남쪽, E: 동쪽, W: 서쪽
            U: 위쪽, D: 아래쪽, L: 왼쪽, R: 오른쪽
        """
        x, y = p
        # move_dict = {}
        for move in move_str.split(","):
            direction, distance = move.split(":")
            if direction.strip() not in ["N", "S", "E", "W", "U", "D", "L", "R"]:
                raise KavanaValueError(f"POINT_MOVE:Invalid direction: {direction.strip()}")
            if not distance.strip().isdigit():
                raise KavanaValueError(f"POINT_MOVE:Invalid distance: {distance.strip()}")
            if direction.strip() == "N" or direction.strip() == "U":
                y -= int(distance.strip())
            elif direction.strip() == "S" or direction.strip() == "D":
                y += int(distance.strip())
            elif direction.strip() == "E" or direction.strip() == "R":
                x += int(distance.strip())
            elif direction.strip() == "W" or direction.strip() == "L":
                x -= int(distance.strip())
        return TokenUtil.xy_to_point_token(x, y)
    
    @staticmethod
    def POINT_TO_REGION(p: Tuple[int,int], width: int, height:int)->RegionToken:
        """Point p를 중심으로 width, height 크기의 RegionToken 반환"""
        x, y = p
        return TokenUtil.region_to_token((x - width // 2, y - height // 2, width, height))
    
    @staticmethod
    def POINTS_TO_REGION(p1: Tuple[int,int], p2: Tuple[int,int]) -> RegionToken:
        """두 점 p1, p2를 연결하는 직사각형의 RegionToken 반환"""
        x1, y1 = p1
        x2, y2 = p2
        x = min(x1, x2)
        y = min(y1, y2)
        width = abs(x1 - x2)
        height = abs(y1 - y2)
        return TokenUtil.region_to_token((x, y, width, height))