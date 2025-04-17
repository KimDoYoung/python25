from lib.core.datatypes.array import Array
from lib.core.datatypes.hash_map import HashMap
from lib.core.datatypes.kavana_datatype import Integer, String
from lib.core.datatypes.point import Point
from lib.core.token import TokenStatus
from lib.core.token_custom import PointToken
from lib.core.token_type import TokenType
from lib.core.token_util import TokenUtil

pt = TokenUtil.xy_to_point_token(10, 20)
print(pt)
assert pt.type == TokenType.POINT
assert pt.status == TokenStatus.EVALUATED
assert pt.data.x == 10
assert pt.data.y == 20