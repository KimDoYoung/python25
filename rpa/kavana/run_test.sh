#!/bin/bash
export PYTHON_PATH=/c/Users/PC/Work/python25/rpa/kavana

if pytest -v -s --disable-warnings --cache-clear ./tests; then
    rm -rf ./htmlcov
    pytest --cov=lib/core --cov-report=term --cov-report=html --cov-report=lcov --disable-warnings tests/
else
    echo "❌ 테스트 실패 → 커버리지 측정 생략"
fi
