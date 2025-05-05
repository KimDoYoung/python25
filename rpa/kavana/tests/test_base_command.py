import pytest
from unittest.mock import MagicMock

from lib.core.commands.base_command import BaseCommand
from lib.core.token import StringToken, Token
from lib.core.token_type import TokenType
from lib.core.datatypes.kavana_datatype import String, Integer
from lib.core.exceptions.kavana_exception import KavanaSyntaxError, KavanaValueError


class DummyCommand(BaseCommand):
    OPTION_DEFINITIONS = {
        "name": {"required": True, "allowed_types": [TokenType.STRING]},
        "count": {"default": 3, "allowed_types": [TokenType.INTEGER], "min": 1, "max": 10}
    }

    COMMAND_SPECS = {
        "dummy": {
            "keys": ["name", "count"],
            "overrides": {},
            "rules": {}
        }
    }

    def execute(self, args, executor):
        pass


def create_token(token_type, value):
    """KavanaDataType 기반 Token 생성 헬퍼"""
    if token_type == TokenType.STRING:
        return StringToken(data=String(value), type=TokenType.STRING)
    if token_type == TokenType.INTEGER:
        return Token(data=Integer(value), type=TokenType.INTEGER)
    raise ValueError("지원하지 않는 타입")


def mock_executor_for(tokens):
    """ExprEvaluator.evaluate()를 mocking하는 executor"""
    mock_eval = MagicMock()
    mock_eval.evaluate.side_effect = lambda expr: expr[0]
    return mock_eval


@pytest.fixture
def dummy():
    return DummyCommand()


def test_parse_valid_options(dummy):
    options = {
        "name": {"express": [create_token(TokenType.STRING, "John")]},
        "count": {"express": [create_token(TokenType.INTEGER, 5)]}
    }

    executor = mock_executor_for([v["express"] for v in options.values()])
    option_map, _ = dummy.get_option_spec("dummy")
    result = dummy.parse_and_validate_options(options, option_map, executor)

    assert result["name"] == "John"
    assert result["count"] == 5


def test_parse_with_default(dummy):
    options = {
        "name": {"express": [create_token(TokenType.STRING, "Alice")]}
    }

    executor = mock_executor_for([options["name"]["express"]])
    option_map, _ = dummy.get_option_spec("dummy")
    result = dummy.parse_and_validate_options(options, option_map, executor)

    assert result["name"] == "Alice"
    assert result["count"] == 3  # default 적용


def test_missing_required_option(dummy):
    options = {
        "count": {"express": [create_token(TokenType.INTEGER, 4)]}
    }

    executor = mock_executor_for([options["count"]["express"]])
    option_map, _ = dummy.get_option_spec("dummy")

    with pytest.raises(KavanaSyntaxError) as exc:
        dummy.parse_and_validate_options(options, option_map, executor)

    assert "필수 옵션 'name'가 누락되었습니다" in str(exc.value)


def test_option_out_of_range(dummy):
    options = {
        "name": {"express": [create_token(TokenType.STRING, "TooBig")]},
        "count": {"express": [create_token(TokenType.INTEGER, 99)]}
    }

    executor = mock_executor_for([options["name"]["express"], options["count"]["express"]])
    option_map, _ = dummy.get_option_spec("dummy")

    with pytest.raises(KavanaSyntaxError) as exc:
        dummy.parse_and_validate_options(options, option_map, executor)

    assert "최대" in str(exc.value)


def test_unknown_option(dummy):
    options = {
        "name": {"express": [create_token(TokenType.STRING, "Unknown")]},
        "extra": {"express": [create_token(TokenType.STRING, "bad")]}
    }

    executor = mock_executor_for([options["name"]["express"]])
    option_map, _ = dummy.get_option_spec("dummy")

    with pytest.raises(KavanaSyntaxError) as exc:
        dummy.parse_and_validate_options(options, option_map, executor)

    assert "알 수 없는 옵션" in str(exc.value)
