from datetime import datetime, date
from lib.core.datatypes.ymd_time import YmdTime, Ymd

def test_ymdtime_operations():
    print("=== YmdTime 테스트 ===")
    a = YmdTime(2025, 3, 5, 10, 20, 30)
    print("a.string:", a.string)
    print("a.primitive:", a.primitive)

    b = a + 3
    print("a + 3 days:", b.string)

    diff = b - a
    print("b - a:", diff, "일")

    dt_now = datetime.now()
    ymd_from_dt = YmdTime.from_datetime(dt_now)
    print("from_datetime:", ymd_from_dt.string)


def test_ymd_operations():
    print("\n=== Ymd 테스트 ===")
    a = Ymd(2023, 4, 1)
    print("a.string:", a.string)
    print("a.primitive:", a.primitive)

    b = a + 10
    print("a + 10 days:", b.string)

    diff = b - a
    print("b - a:", diff, "일")

    d_now = date.today()
    ymd_from_date = Ymd.from_date(d_now)
    print("from_date:", ymd_from_date.string)


if __name__ == "__main__":
    test_ymdtime_operations()
    test_ymd_operations()
    print("테스트 완료")