def is_similar_color(color1, color2, tolerance=10):
    """
    두 개의 RGB 색상이 비슷한지 확인 (tolerance 값 내에서 허용)
    :param color1: 기준 색상 (예: (34, 177, 76))
    :param color2: 비교할 색상 (예: (36, 180, 78))
    :param tolerance: 허용할 오차 범위 (기본값 10)
    :return: 비슷하면 True, 아니면 False
    """
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))
