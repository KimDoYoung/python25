import pytest
from unittest.mock import Mock, patch
from lib.core.datatypes.application import Application
from lib.core.datatypes.point import Point
from lib.core.datatypes.rectangle import Rectangle
from lib.core.datatypes.region import Region
from lib.core.datatypes.window import Window
from lib.core.token import Token
from lib.core.token_type import TokenType
from lib.core.datatypes.kavana_datatype import Integer, String
from lib.core.token_custom import (
    PointToken, RectangleToken, RegionToken,
    ImageToken, ApplicationToken, WindowToken
)
from lib.core.token import StringToken
from lib.core.token import Token, TokenStatus
from lib.core.token_type import TokenType
from lib.core.token_custom import (
    CUSTOM_TYPES,
    ApplicationToken,
    CustomToken,
    ImageToken,
    PointToken,
    RectangleToken,
    RegionToken,
    WindowToken,
)


class DummyEvaluator:
    def evaluate(self, tokens):
        if isinstance(tokens, list):
            return tokens[0]
        return tokens


@pytest.fixture
def evaluator():
    return DummyEvaluator()


def test_point_token(evaluator):
    point = PointToken(data=None)
    point.expressions = [
        [Token(data=Integer(1), type=TokenType.INTEGER)],
        [Token(data=Integer(2), type=TokenType.INTEGER)]
    ]
    result = point.evaluate(evaluator)
    assert result.data.x == 1
    assert result.data.y == 2


def test_rectangle_token(evaluator):
    rect = RectangleToken(data=None)
    rect.expressions = [
        [Token(data=Integer(10), type=TokenType.INTEGER)],
        [Token(data=Integer(20), type=TokenType.INTEGER)],
        [Token(data=Integer(110), type=TokenType.INTEGER)],
        [Token(data=Integer(120), type=TokenType.INTEGER)],
    ]
    result = rect.evaluate(evaluator)
    assert result.data.p1.x == 10
    assert result.data.p1.y == 20
    assert result.data.p2.x == 110
    assert result.data.p2.y == 120


def test_region_token(evaluator):
    region = RegionToken(data=None)
    region.expressions = [
        [Token(data=Integer(5), type=TokenType.INTEGER)],
        [Token(data=Integer(10), type=TokenType.INTEGER)],
        [Token(data=Integer(150), type=TokenType.INTEGER)],
        [Token(data=Integer(80), type=TokenType.INTEGER)],
    ]
    result = region.evaluate(evaluator)
    assert result.data.x == 5
    assert result.data.y == 10
    assert result.data.width == 150
    assert result.data.height == 80


def test_application_token(evaluator):
    app = ApplicationToken(data=None)
    app.expressions = [
        [ Token(data=String("notepad.exe"), type=TokenType.STRING)],
        [ Token(data=String("process_name"), type=TokenType.STRING)]
    ]
    result = app.evaluate(evaluator)
    assert result.data.path == "notepad.exe"


def test_window_token(evaluator):
    win = WindowToken(data=None)
    win.expressions = [
        [StringToken(data=String("MyApp Window"), type=TokenType.STRING)],
        [Token(data=Integer(0), type=TokenType.INTEGER)],
        [StringToken(data=String("MyApp Window"), type=TokenType.STRING)]
    ]
    result = win.evaluate(evaluator)
    assert result.data.title == "MyApp Window"


def test_image_token(tmp_path, evaluator):
    import cv2
    import numpy as np
    from lib.core.datatypes.kavana_datatype import String

    # 테스트용 이미지 생성
    test_image_path = tmp_path / "test_image.png"
    cv2.imwrite(str(test_image_path), np.ones((1, 1, 3), dtype=np.uint8) * 255)

    img = ImageToken(data=None)
    img.expressions = [
        [Token(data=String(str(test_image_path)), type=TokenType.STRING)]
    ]
    result = img.evaluate(evaluator)
    assert result.data.path == str(test_image_path)
    assert result.data.data is not None

class TestCustomTypes:
    def test_custom_types_set(self):
        """사용자 정의 타입 집합 테스트"""
        expected_types = {
            TokenType.POINT,
            TokenType.REGION,
            TokenType.RECTANGLE,
            TokenType.IMAGE,
            TokenType.WINDOW,
            TokenType.APPLICATION,
        }
        assert CUSTOM_TYPES == expected_types


class TestCustomToken:
    def test_custom_token_init(self):
        """CustomToken 초기화 테스트"""
        custom_token = CustomToken(data=String("test"), type=TokenType.CUSTOM_TYPE)
        
        assert custom_token.data.value == "test"
        assert custom_token.type == TokenType.CUSTOM_TYPE
        assert custom_token.expressions == []
        assert custom_token.status == TokenStatus.PARSED
    
    def test_custom_token_repr(self):
        """CustomToken __repr__ 테스트"""
        custom_token = CustomToken(data=String("test"), type=TokenType.CUSTOM_TYPE)
        assert repr(custom_token) == "<CustomToken(args=[])>"
    
    def test_evaluate_not_implemented(self):
        """CustomToken evaluate 메서드 NotImplementedError 테스트"""
        custom_token = CustomToken(data=String("test"), type=TokenType.CUSTOM_TYPE)
        evaluator = Mock()
        
        with pytest.raises(NotImplementedError, match=r"evaluate\(\)는 서브클래스에서 구현되어야 합니다"):
            custom_token.evaluate(evaluator)



class TestPointToken:
    def test_point_token_init(self):
        """PointToken 초기화 테스트"""
        point_token = PointToken(data=None)
        
        assert point_token.type == TokenType.POINT
        assert point_token.expressions == []
        assert point_token.status == TokenStatus.PARSED
        assert point_token.data is None
    
    def test_point_token_repr_not_evaluated(self):
        """평가되지 않은 PointToken __repr__ 테스트"""
        point_token = PointToken(data=None)
        assert repr(point_token) == "<PointToken (not evaluated)>"
    
    def test_point_token_repr_evaluated(self):
        """평가된 PointToken __repr__ 테스트"""
        point = Point(10, 20)
        point_token = PointToken(data=point)
        point_token.status = TokenStatus.EVALUATED
        
        assert repr(point_token) == "<PointToken x=10, y=20>"
    
    def test_point_token_evaluate(self):
        """PointToken evaluate 메서드 테스트"""
        # 모의 평가기 생성
        evaluator = Mock()
        evaluator.evaluate.side_effect = [
            Token(data=Integer(100), type=TokenType.INTEGER),
            Token(data=Integer(200), type=TokenType.INTEGER)
        ]
        
        # x, y 표현식 생성 (실제 내용은 중요하지 않음, 모의 객체가 처리)
        x_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        y_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        
        point_token = PointToken(data=None)
        point_token.expressions = [x_expr, y_expr]
        
        # 평가 실행
        result = point_token.evaluate(evaluator)
        
        # 평가기가 두 번 호출되었는지 확인
        assert evaluator.evaluate.call_count == 2
        evaluator.evaluate.assert_any_call(x_expr)
        evaluator.evaluate.assert_any_call(y_expr)
        
        # 결과 확인
        assert result is point_token
        assert point_token.status == TokenStatus.EVALUATED
        assert isinstance(point_token.data, Point)
        assert point_token.data.x == 100
        assert point_token.data.y == 200
    
    def test_point_token_evaluate_already_evaluated(self):
        """이미 평가된 PointToken evaluate 메서드 테스트"""
        point = Point(10, 20)
        point_token = PointToken(data=point)
        point_token.status = TokenStatus.EVALUATED
        
        evaluator = Mock()
        result = point_token.evaluate(evaluator)
        
        # 평가기가 호출되지 않아야 함
        evaluator.evaluate.assert_not_called()
        
        # 같은 토큰이 반환되어야 함
        assert result is point_token
        assert point_token.data is point


class TestRectangleToken:
    def test_rectangle_token_init(self):
        """RectangleToken 초기화 테스트"""
        rect_token = RectangleToken(data=None)
        
        assert rect_token.type == TokenType.RECTANGLE
        assert rect_token.expressions == []
        assert rect_token.status == TokenStatus.PARSED
        assert rect_token.data is None
    
    def test_rectangle_token_repr_not_evaluated(self):
        """평가되지 않은 RectangleToken __repr__ 테스트"""
        rect_token = RectangleToken(data=None)
        assert repr(rect_token) == "<RectangleToken (not evaluated)>"
    
    def test_rectangle_token_repr_evaluated(self):
        """평가된 RectangleToken __repr__ 테스트"""
        rect = Rectangle(10, 20, 30, 40)
        rect_token = RectangleToken(data=rect)
        rect_token.status = TokenStatus.EVALUATED
        
        assert repr(rect_token) == "<RectangleToken x1=10, y1=20, x2=30, y2=40>"
    
    def test_rectangle_token_evaluate(self):
        """RectangleToken evaluate 메서드 테스트"""
        # 모의 평가기 생성
        evaluator = Mock()
        evaluator.evaluate.side_effect = [
            Token(data=Integer(10), type=TokenType.INTEGER),
            Token(data=Integer(20), type=TokenType.INTEGER),
            Token(data=Integer(30), type=TokenType.INTEGER),
            Token(data=Integer(40), type=TokenType.INTEGER)
        ]
        
        # 좌표 표현식 생성
        x1_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        y1_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        x2_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        y2_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        
        rect_token = RectangleToken(data=None)
        rect_token.expressions = [x1_expr, y1_expr, x2_expr, y2_expr]
        
        # 평가 실행
        result = rect_token.evaluate(evaluator)
        
        # 평가기가 네 번 호출되었는지 확인
        assert evaluator.evaluate.call_count == 4
        
        # 결과 확인
        assert result is rect_token
        assert rect_token.status == TokenStatus.EVALUATED
        assert isinstance(rect_token.data, Rectangle)
        assert rect_token.data.p1.x == 10
        assert rect_token.data.p1.y == 20
        assert rect_token.data.p2.x == 30
        assert rect_token.data.p2.y == 40


class TestRegionToken:
    def test_region_token_init(self):
        """RegionToken 초기화 테스트"""
        region_token = RegionToken(data=None)
        
        assert region_token.type == TokenType.REGION
        assert region_token.expressions == []
        assert region_token.status == TokenStatus.PARSED
        assert region_token.data is None
    
    def test_region_token_repr_not_evaluated(self):
        """평가되지 않은 RegionToken __repr__ 테스트"""
        region_token = RegionToken(data=None)
        assert repr(region_token) == "<RegionToken (not evaluated)>"
    
    def test_region_token_repr_evaluated(self):
        """평가된 RegionToken __repr__ 테스트"""
        region = Region(10, 20, 100, 50)
        region_token = RegionToken(data=region)
        region_token.status = TokenStatus.EVALUATED
        
        assert repr(region_token) == "<RegionToken x=10, y=20, w=100, h=50>"
    
    def test_region_token_evaluate(self):
        """RegionToken evaluate 메서드 테스트"""
        # 모의 평가기 생성
        evaluator = Mock()
        evaluator.evaluate.side_effect = [
            Token(data=Integer(10), type=TokenType.INTEGER),
            Token(data=Integer(20), type=TokenType.INTEGER),
            Token(data=Integer(100), type=TokenType.INTEGER),
            Token(data=Integer(50), type=TokenType.INTEGER)
        ]
        
        # 리전 파라미터 표현식 생성
        x_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        y_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        width_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        height_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        
        region_token = RegionToken(data=None)
        region_token.expressions = [x_expr, y_expr, width_expr, height_expr]
        
        # 평가 실행
        result = region_token.evaluate(evaluator)
        
        # 평가기가 네 번 호출되었는지 확인
        assert evaluator.evaluate.call_count == 4
        
        # 결과 확인
        assert result is region_token
        assert region_token.status == TokenStatus.EVALUATED
        assert isinstance(region_token.data, Region)
        assert region_token.data.x == 10
        assert region_token.data.y == 20
        assert region_token.data.width == 100
        assert region_token.data.height == 50


class TestImageToken:
    @patch('lib.core.token_custom.Image')
    def test_image_token_init(self, mock_image):
        """ImageToken 초기화 테스트"""
        image_token = ImageToken(data=None)
        
        assert image_token.type == TokenType.IMAGE
        assert image_token.expressions == []
        assert image_token.status == TokenStatus.PARSED
        assert image_token.data is None
        assert image_token.object_type == TokenType.IMAGE
    
    def test_image_token_repr_not_evaluated(self):
        """평가되지 않은 ImageToken __repr__ 테스트"""
        image_token = ImageToken(data=None)
        assert repr(image_token) == "<ImageToken (not evaluated)>"
    
    @patch('lib.core.token_custom.Image')
    def test_image_token_repr_evaluated(self, mock_image):
        """평가된 ImageToken __repr__ 테스트"""
        mock_instance = Mock()
        mock_instance.path = "/path/to/image.png"
        mock_image.return_value = mock_instance
        
        image_token = ImageToken(data=mock_instance)
        image_token.status = TokenStatus.EVALUATED
        
        assert repr(image_token) == "<ImageToken path='/path/to/image.png'>"
    
    @patch('lib.core.token_custom.Image')
    def test_image_token_evaluate(self, mock_image):
        """ImageToken evaluate 메서드 테스트"""
        # 모의 Image 객체 설정
        mock_instance = Mock()
        mock_image.return_value = mock_instance
        
        # 모의 평가기 생성
        evaluator = Mock()
        evaluator.evaluate.return_value = Token(data=String("/path/to/image.png"), type=TokenType.STRING)
        
        # 경로 표현식 생성
        path_expr = [Token(data=String(""), type=TokenType.STRING)]
        
        image_token = ImageToken(data=None)
        image_token.expressions = [path_expr]
        
        # 평가 실행
        result = image_token.evaluate(evaluator)
        
        # 평가기가 한 번 호출되었는지 확인
        evaluator.evaluate.assert_called_once_with(path_expr)
        
        # Image 객체가 생성되고 load가 호출되었는지 확인
        mock_image.assert_called_once_with("/path/to/image.png")
        mock_instance.load.assert_called_once()
        
        # 결과 확인
        assert result is image_token
        assert image_token.status == TokenStatus.EVALUATED
        assert image_token.data is mock_instance


class TestApplicationToken:
    def test_application_token_init(self):
        """ApplicationToken 초기화 테스트"""
        app_token = ApplicationToken(data=None)
        
        assert app_token.type == TokenType.APPLICATION
        assert app_token.expressions == []
        assert app_token.status == TokenStatus.PARSED
        assert app_token.data is None
    
    def test_application_token_repr_not_evaluated(self):
        """평가되지 않은 ApplicationToken __repr__ 테스트"""
        app_token = ApplicationToken(data=None)
        assert repr(app_token) == "<ApplicationToken (not evaluated)>"
    
    def test_application_token_repr_evaluated(self):
        """평가된 ApplicationToken __repr__ 테스트"""
        app = Application("/path/to/app.exe", "app_process")
        app_token = ApplicationToken(data=app)
        app_token.status = TokenStatus.EVALUATED
        
        assert repr(app_token) == "<ApplicationToken path='/path/to/app.exe'>"
    
    @patch('lib.core.token_custom.Application')
    def test_application_token_evaluate_with_process_name(self, mock_application):
        """ApplicationToken evaluate 메서드 테스트 (프로세스 이름 포함)"""
        # 모의 Application 객체 설정
        mock_instance = Mock()
        mock_instance.path = "/path/to/app.exe"
        mock_application.return_value = mock_instance
        
        # 모의 평가기 생성
        evaluator = Mock()
        evaluator.evaluate.side_effect = [
            Token(data=String("/path/to/app.exe"), type=TokenType.STRING),
            Token(data=String("app_process"), type=TokenType.STRING)
        ]
        
        # 경로와 프로세스 이름 표현식 생성
        path_expr = [Token(data=String(""), type=TokenType.STRING)]
        process_expr = [Token(data=String(""), type=TokenType.STRING)]
        
        app_token = ApplicationToken(data=None)
        app_token.expressions = [path_expr, process_expr]
        
        # 평가 실행
        result = app_token.evaluate(evaluator)
        
        # 평가기가 두 번 호출되었는지 확인
        assert evaluator.evaluate.call_count == 2
        
        # Application 객체가 올바르게 생성되었는지 확인
        mock_application.assert_called_once_with("/path/to/app.exe", process_name="app_process")
        
        # 결과 확인
        assert result is app_token
        assert app_token.status == TokenStatus.EVALUATED
        assert app_token.data is mock_instance
    
    @patch('lib.core.token_custom.Application')
    def test_application_token_evaluate_without_process_name(self, mock_application):
        """ApplicationToken evaluate 메서드 테스트 (프로세스 이름 없음)"""
        # 모의 Application 객체 설정
        mock_instance = Mock()
        mock_instance.path = "/path/to/app.exe"
        mock_application.return_value = mock_instance
        
        # 모의 평가기 생성
        evaluator = Mock()
        evaluator.evaluate.side_effect = [
            Token(data=String("/path/to/app.exe"), type=TokenType.STRING),
            None  # 프로세스 이름 없음
        ]
        
        # 경로 표현식만 생성
        path_expr = [Token(data=String(""), type=TokenType.STRING)]
        process_expr = [Token(data=String(""), type=TokenType.STRING)]
        
        app_token = ApplicationToken(data=None)
        app_token.expressions = [path_expr, process_expr]
        
        # 평가 실행
        result = app_token.evaluate(evaluator)
        
        # Application 객체가 올바르게 생성되었는지 확인
        mock_application.assert_called_once_with("/path/to/app.exe", process_name=None)
        
        # 결과 확인
        assert result is app_token
        assert app_token.status == TokenStatus.EVALUATED
        assert app_token.data is mock_instance


class TestWindowToken:
    def test_window_token_init(self):
        """WindowToken 초기화 테스트"""
        window_token = WindowToken(data=None)  # Removed type=TokenType.CUSTOM_TYPE
        
        assert window_token.type == TokenType.WINDOW
        assert window_token.expressions == []
        assert window_token.status == TokenStatus.PARSED
        assert window_token.data is None
    
    def test_window_token_repr_not_evaluated(self):
        """평가되지 않은 WindowToken __repr__ 테스트"""
        window_token = WindowToken(data=None)  # Removed type=TokenType.CUSTOM_TYPE
        assert repr(window_token) == "<WindowToken (not evaluated)>"
    
    def test_window_token_repr_evaluated(self):
        """평가된 WindowToken __repr__ 테스트"""
        window = Window("Test Window", 12345, "TestClass")
        window_token = WindowToken(data=window)
        window_token.status = TokenStatus.EVALUATED
        
        assert repr(window_token) == "<WindowToken title='Test Window'>"
    
    @patch('lib.core.token_custom.Window')
    def test_window_token_evaluate_with_class_name(self, mock_window):
        """WindowToken evaluate 메서드 테스트 (클래스 이름 포함)"""
        # 모의 Window 객체 설정
        mock_instance = Mock()
        mock_instance.title = "Test Window"
        mock_window.return_value = mock_instance
        
        # 모의 평가기 생성
        evaluator = Mock()
        evaluator.evaluate.side_effect = [
            Token(data=String("Test Window"), type=TokenType.STRING),
            Token(data=Integer(12345), type=TokenType.INTEGER),
            Token(data=String("TestClass"), type=TokenType.STRING)
        ]
        
        # 표현식 생성
        title_expr = [Token(data=String(""), type=TokenType.STRING)]
        hwnd_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        class_expr = [Token(data=String(""), type=TokenType.STRING)]
        
        window_token = WindowToken(data=None)
        window_token.expressions = [title_expr, hwnd_expr, class_expr]
        
        # 평가 실행
        result = window_token.evaluate(evaluator)
        
        # 평가기가 세 번 호출되었는지 확인
        assert evaluator.evaluate.call_count == 3
        
        # Window 객체가 올바르게 생성되었는지 확인
        mock_window.assert_called_once_with("Test Window", 12345, "TestClass")
        
        # 결과 확인
        assert result is window_token
        assert window_token.status == TokenStatus.EVALUATED
        assert window_token.data is mock_instance
    
    @patch('lib.core.token_custom.Window')
    def test_window_token_evaluate_without_class_name(self, mock_window):
        """WindowToken evaluate 메서드 테스트 (클래스 이름 없음)"""
        # 모의 Window 객체 설정
        mock_instance = Mock()
        mock_instance.title = "Test Window"
        mock_window.return_value = mock_instance
        
        # 모의 평가기 생성
        evaluator = Mock()
        evaluator.evaluate.side_effect = [
            Token(data=String("Test Window"), type=TokenType.STRING),
            Token(data=Integer(12345), type=TokenType.INTEGER),
            None  # 클래스 이름 없음
        ]
        
        # 표현식 생성
        title_expr = [Token(data=String(""), type=TokenType.STRING)]
        hwnd_expr = [Token(data=Integer(0), type=TokenType.INTEGER)]
        class_expr = [Token(data=String(""), type=TokenType.STRING)]
        
        window_token = WindowToken(data=None)
        window_token.expressions = [title_expr, hwnd_expr, class_expr]
        
        # 평가 실행
        result = window_token.evaluate(evaluator)
        
        # Window 객체가 올바르게 생성되었는지 확인
        mock_window.assert_called_once_with("Test Window", 12345, None)
        
        # 결과 확인
        assert result is window_token
        assert window_token.status == TokenStatus.EVALUATED
        assert window_token.data is mock_instance