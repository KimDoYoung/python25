from typing import Tuple

from lib.core.builtins.builtin_consts import PointName, RegionName
from lib.core.datatypes.point import Point
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.token import TokenStatus
from lib.core.token_custom import PointToken, RegionToken
from lib.core.token_util import TokenUtil


class RegionPointFunctions:
    """Region과 Point 관련 내장 함수들"""
    
    executor = None  # ✅ 클래스 변수로 executor 저장

    @staticmethod
    def set_executor(executor_instance):
        RegionPointFunctions.executor = executor_instance

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
        region_name = region_name.lower()
        if region_name == RegionName.LEFT_ONE_THIRD.value:
            return TokenUtil.region_to_token(x, y, width // 3, height)
        elif region_name == RegionName.RIGHT_ONE_THIRD.value:
            return TokenUtil.region_to_token(x + 2 * (width // 3), y, width // 3, height)
        elif region_name == RegionName.TOP_ONE_THIRD.value:
            return TokenUtil.region_to_token(x, y, width, height // 3)
        elif region_name == RegionName.BOTTOM_ONE_THIRD.value:
            return TokenUtil.region_to_token(x, y + 2 * (height // 3), width, height // 3)
        elif region_name == RegionName.LEFT_TOP.value:
            return TokenUtil.region_to_token(x, y, width // 2, height // 2)
        elif region_name == RegionName.RIGHT_TOP.value:
            return TokenUtil.region_to_token(x + width // 2, y, width // 2, height // 2)
        elif region_name == RegionName.RIGHT_BOTTOM.value:
            return TokenUtil.region_to_token(x + width // 2, y + height // 2, width // 2, height // 2)
        elif region_name == RegionName.LEFT_BOTTOM.value:
            return TokenUtil.region_to_token(x, y + height // 2, width // 2, height // 2)
        elif region_name == RegionName.CENTER.value:
            return TokenUtil.region_to_token(x + width // 3, y + height // 3, width // 3, height // 3)
        elif region_name == RegionName.LEFT.value:
            return TokenUtil.region_to_token(x, y, width // 2, height)
        elif region_name == RegionName.RIGHT.value:
            return TokenUtil.region_to_token(x + width // 2, y, width // 2, height)
        elif region_name == RegionName.TOP.value:
            return TokenUtil.region_to_token(x, y, width, height // 2)
        elif region_name == RegionName.BOTTOM.value:
            return TokenUtil.region_to_token(x, y + height // 2, width, height // 2)
        else:
            raise KavanaValueError(f"Unknown region name: {region_name}")
        
