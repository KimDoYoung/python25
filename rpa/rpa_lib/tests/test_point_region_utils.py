import pytest
from src.lib.point_region_utils import get_point, PointName

@pytest.mark.parametrize("region, point_name, expected", [
    ((10, 20, 100, 200), PointName.LEFT_TOP, (10, 20)),
    ((10, 20, 100, 200), PointName.RIGHT_TOP, (110, 20)),
    ((10, 20, 100, 200), PointName.RIGHT_BOTTOM, (110, 220)),
    ((10, 20, 100, 200), PointName.LEFT_BOTTOM, (10, 220)),
    ((10, 20, 100, 200), PointName.TOP_MIDDLE, (60, 20)),
    ((10, 20, 100, 200), PointName.BOTTOM_MIDDLE, (60, 220)),
    ((10, 20, 100, 200), PointName.LEFT_MIDDLE, (10, 120)),
    ((10, 20, 100, 200), PointName.RIGHT_MIDDLE, (110, 120)),
    ((10, 20, 100, 200), PointName.CENTER, (60, 120)),
])
def test_get_point_name(region, point_name, expected):
    assert get_point(region, point_name) == expected