from typing import Tuple

from lib.core.builtins.builtin_consts import PointName
from lib.core.datatypes.point import Point
from lib.core.exceptions.kavana_exception import KavanaValueError
from lib.core.token import TokenStatus
from lib.core.token_custom import PointToken


class RegionPointFunctions:
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