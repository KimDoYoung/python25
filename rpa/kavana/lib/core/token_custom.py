from dataclasses import dataclass, field
from typing import List

from lib.core.datatypes.application import Application
from lib.core.datatypes.kavana_datatype import Integer, KavanaDataType
from lib.core.datatypes.point import Point
from lib.core.datatypes.rectangle import Rectangle
from lib.core.datatypes.region import Region
from lib.core.datatypes.window import Window
from lib.core.token import Token, TokenStatus
from lib.core.token_type import TokenType
from lib.core.datatypes.image import Image

CUSTOM_TYPES = {
    TokenType.POINT,
    TokenType.REGION,
    TokenType.RECTANGLE,
    TokenType.IMAGE,
    TokenType.WINDOW,
    TokenType.APPLICATION,
}

@dataclass
class CustomToken(Token):
    expressions: List[List[Token]] = field(default_factory=list)
    status: TokenStatus = TokenStatus.PARSED

    def __post_init__(self):
        self.type = TokenType.CUSTOM_TYPE  # 서브클래스에서 덮어씀

    def evaluate(self, evaluator) -> Token:
        raise NotImplementedError("evaluate()는 서브클래스에서 구현되어야 합니다")

    def __repr__(self):
        return f"<{self.__class__.__name__}(args={self.expressions})>"


@dataclass
class PointToken(CustomToken):
    type: TokenType = field(default=TokenType.POINT, init=False)

    def __post_init__(self):
        super().__post_init__()
        self.type = TokenType.POINT

    def evaluate(self, evaluator) -> Token:
        if self.status == TokenStatus.EVALUATED:
            return self

        if self.expressions:
            x = evaluator.evaluate(self.expressions[0]).data.value
            y = evaluator.evaluate(self.expressions[1]).data.value

        self.data = Point(x, y)
        self.status = TokenStatus.EVALUATED
        return self

    def __repr__(self):
        if self.status == TokenStatus.EVALUATED and self.data:
            return f"<PointToken x={self.data.x}, y={self.data.y}>"
        return f"<PointToken (not evaluated)>"


@dataclass
class RectangleToken(CustomToken):
    type: TokenType = field(default=TokenType.RECTANGLE, init=False)

    def __post_init__(self):
        super().__post_init__()
        self.type = TokenType.RECTANGLE

    def evaluate(self, evaluator) -> Token:
        if self.status == TokenStatus.EVALUATED:
            return self

        x1_token = evaluator.evaluate(self.expressions[0])
        y1_token = evaluator.evaluate(self.expressions[1])
        x2_token = evaluator.evaluate(self.expressions[2])
        y2_token = evaluator.evaluate(self.expressions[3])

        self.data = Rectangle(
            x1_token.data.value,
            y1_token.data.value,
            x2_token.data.value,
            y2_token.data.value
        )
        self.status = TokenStatus.EVALUATED
        return self

    def __repr__(self):
        if self.status == TokenStatus.EVALUATED and self.data:
            return (f"<RectangleToken x1={self.data.p1.x}, y1={self.data.p1.y}, "
                    f"x2={self.data.p2.x}, y2={self.data.p2.y}>")
        return "<RectangleToken (not evaluated)>"


@dataclass
class RegionToken(CustomToken):
    type: TokenType = field(default=TokenType.REGION, init=False)

    def __post_init__(self):
        super().__post_init__()
        self.type = TokenType.REGION

    def evaluate(self, evaluator) -> Token:
        if self.status == TokenStatus.EVALUATED:
            return self

        x_token = evaluator.evaluate(self.expressions[0])
        y_token = evaluator.evaluate(self.expressions[1])
        width_token = evaluator.evaluate(self.expressions[2])
        height_token = evaluator.evaluate(self.expressions[3])

        self.data = Region(
            x_token.data.value,
            y_token.data.value,
            width_token.data.value,
            height_token.data.value
        )
        self.status = TokenStatus.EVALUATED
        return self

    def __repr__(self):
        if self.status == TokenStatus.EVALUATED and self.data:
            return (f"<RegionToken x={self.data.x}, y={self.data.y}, "
                    f"w={self.data.width}, h={self.data.height}>")
        return "<RegionToken (not evaluated)>"

@dataclass
class ImageToken(CustomToken):

    type: TokenType = field(default=TokenType.IMAGE, init=False)

    def __post_init__(self):
        self.object_type = TokenType.IMAGE

    def evaluate(self, evaluator) -> Token:
        if self.status == TokenStatus.EVALUATED:
            return self

        # ✅ 문자열 토큰 평가 → 이미지 경로 추출
        path_token = evaluator.evaluate(self.expressions[0])
        path = path_token.data.value

        # ✅ 즉시 로딩!
        image = Image(path)
        image.load()

        self.data = image
        self.status = TokenStatus.EVALUATED
        return self

    def __repr__(self):
        if self.status == TokenStatus.EVALUATED and self.data:
            return f"<ImageToken path='{self.data.path}'>"
        return "<ImageToken (not evaluated)>"

@dataclass
class ApplicationToken(CustomToken):
    type: TokenType = field(default=TokenType.APPLICATION, init=False)

    def __post_init__(self):
        self.type = TokenType.APPLICATION

    def evaluate(self, evaluator) -> Token:
        if self.status == TokenStatus.EVALUATED:
            return self

        path_token = evaluator.evaluate(self.expressions[0])
        path = path_token.data.value
        process_name_token = evaluator.evaluate(self.expressions[1])
        process_name = process_name_token.data.value if process_name_token else None

        self.data = Application(path, process_name=process_name)
        self.status = TokenStatus.EVALUATED
        return self

    def __repr__(self):
        if self.status == TokenStatus.EVALUATED and self.data:
            return f"<ApplicationToken path='{self.data.path}'>"
        return "<ApplicationToken (not evaluated)>"

@dataclass
class WindowToken(CustomToken):
    type: TokenType = field(default=TokenType.WINDOW, init=False)

    def __post_init__(self):
        self.type = TokenType.WINDOW

    def evaluate(self, evaluator) -> Token:
        if self.status == TokenStatus.EVALUATED:
            return self

        title_token = evaluator.evaluate(self.expressions[0])
        hwnd_token = evaluator.evaluate(self.expressions[1])
        class_name_token = evaluator.evaluate(self.expressions[2])
        title = title_token.data.value
        hwnd = hwnd_token.data.value
        class_name = class_name_token.data.value if class_name_token else None

        self.data = Window(title, hwnd, class_name)
        self.status = TokenStatus.EVALUATED
        return self

    def __repr__(self):
        if self.status == TokenStatus.EVALUATED and self.data:
            return f"<WindowToken title='{self.data.title}'>"
        return "<WindowToken (not evaluated)>"
