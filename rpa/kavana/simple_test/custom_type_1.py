from lib.core.datatypes.kavana_datatype import Integer, String
from lib.core.expr_evaluator import ExprEvaluator
from lib.core.token import StringToken, Token
from lib.core.token_custom import ApplicationToken, ImageToken, PointToken, RectangleToken, RegionToken, WindowToken
from lib.core.token_type import TokenType
from lib.core.variable_manager import VariableManager




# ✅ 디버깅 함수
def debug_token(token):
    print(f"Before evaluation: {token}")
    variable_manager = VariableManager()
    evaluated = token.evaluate(ExprEvaluator(variable_manager=variable_manager))
    print(f"After evaluation:  {evaluated}")
    print("-" * 50)


def main():
    print("▶️ 토큰 디버깅 시작")

    # ✅ PointToken 테스트
    point = PointToken(data=None)
    point.expressions = [
        [Token(data=Integer(1), type=TokenType.INTEGER)],
        [Token(data=Integer(2), type=TokenType.INTEGER)]
    ]
    debug_token(point)

    # ✅ RectangleToken 테스트
    rectangle = RectangleToken(data=None)
    rectangle.expressions = [
        [Token(data=Integer(1), type=TokenType.INTEGER)],
        [Token(data=Integer(2), type=TokenType.INTEGER)],
        [Token(data=Integer(100), type=TokenType.INTEGER)],
        [Token(data=Integer(200), type=TokenType.INTEGER)]
    ]
    debug_token(rectangle)

    # ✅ RegionToken 테스트
    from lib.core.datatypes.region import Region  # 이건 내부에서 사용되므로 필요
    region = RegionToken(data = None)
    region.expressions = [
        [Token(data=Integer(5), type=TokenType.INTEGER)],
        [Token(data=Integer(10), type=TokenType.INTEGER)],
        [Token(data=Integer(150), type=TokenType.INTEGER)],
        [Token(data=Integer(80), type=TokenType.INTEGER)]
    ]
    debug_token(region)

    # ✅ ImageToken 테스트
    image = ImageToken(data=None)
    image.expressions = [
        [ StringToken(data=String("C:/Users/PC/Pictures/1.png"), type=TokenType.STRING)],   
    ]
    debug_token(image)
    print("✅ 디버깅 종료")

    # ApplicationToken 테스트
    application = ApplicationToken(data=None)
    application.expressions = [
        [StringToken(data=String("notepad.exe"), type=TokenType.STRING)]
    ]
    debug_token(application)

    print("✅ ApplicationToken 디버깅 종료")
    # Window 테스트
    windown = WindowToken(data=None)
    windown.expressions = [
        [StringToken(data=String("Untitled - Notepad"), type=TokenType.STRING)]
    ]
    debug_token(windown)
    print("✅ WindowToken 디버깅 종료")



if __name__ == "__main__":
    main()
