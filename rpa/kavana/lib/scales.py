import ctypes


def get_scale_factor() -> float:
    """ 현재 사용자의 화면 DPI 스케일 팩터를 반환합니다. """
    return ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100