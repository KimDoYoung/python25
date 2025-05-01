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

    def POINT_MOVE_NORTH(p: Tuple[int,int], distance: int) -> PointToken:
        """Point p를 북쪽으로 distance 만큼 이동시킨 PointToken 반환"""
        x, y = p
        return TokenUtil.xy_to_point_token(x, y - distance)

    def POINT_MOVE_SOUTH(p: Tuple[int,int], distance: int) -> PointToken:
        """Point p를 남쪽으로 distance 만큼 이동시킨 PointToken 반환"""
        x, y = p
        return TokenUtil.xy_to_point_token(x, y + distance)
    def POINT_MOVE_EAST(p: Tuple[int,int], distance: int) -> PointToken:
        """Point p를 동쪽으로 distance 만큼 이동시킨 PointToken 반환"""
        x, y = p
        return TokenUtil.xy_to_point_token(x + distance, y)
    def POINT_MOVE_WEST(p: Tuple[int,int], distance: int) -> PointToken:
        """Point p를 서쪽으로 distance 만큼 이동시킨 PointToken 반환"""
        x, y = p
        return TokenUtil.xy_to_point_token(x - distance, y)
    
