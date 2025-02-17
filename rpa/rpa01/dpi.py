import ctypes

scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100  # 현재 DPI 배율 가져오기
print(f"현재 DPI 배율: {scale_factor}")
print(f"현재 DPI 배율: {scale_factor*100}%")
if scale_factor == 1.0:
    print("DPI 배율이 100%입니다.")