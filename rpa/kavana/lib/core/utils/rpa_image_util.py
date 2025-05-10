from datetime import datetime
import imagehash
import pyautogui


class RpaImageUtil:
    def __init__(self):
        """이미지 유사도 체크 초기화"""
        pass

    @staticmethod
    def compare_hashes(hash1, hash2):
        return hash1 - hash2  # 해밍 거리

    @staticmethod
    def hash_similarity(distance, hash_size=8):
        max_distance = hash_size * hash_size
        return (1 - (distance / max_distance)) * 100
    
    @staticmethod
    def screen_image_split_and_hash(region: tuple, grid_shape: str) -> list[dict]:
        """Region 영역을 grid 단위로 나누고 각 조각의 해시값 계산"""
        x, y, w, h = region
        cols, rows = map(int, grid_shape.lower().split("x"))  # 예: "10x5"
        tile_w, tile_h = w // cols, h // rows

        full_image = pyautogui.screenshot(region=(x, y, w, h))
        # 파일에 저장
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"c:\\tmp\\screenshot_{x}_{y}_{w}_{h}_{current_time}.png"
        full_image.save(file_name)
        blocks = []

        for row in range(rows):
            for col in range(cols):
                cx = col * tile_w
                cy = row * tile_h
                tile = full_image.crop((cx, cy, cx + tile_w, cy + tile_h))
                tile_hash = str(imagehash.phash(tile))
                blocks.append({
                    "hash": tile_hash,
                    "x": x + cx,
                    "y": y + cy,
                    "w": tile_w,
                    "h": tile_h
                })
        
        return blocks
    
    @staticmethod
    def changed_region_by_hash( before: list[dict], after: list[dict]) -> dict:
        """변경된 영역을 찾아서 Region 객체로 반환"""
        changed_blocks = []
        for b, a in zip(before, after):
            dist = RpaImageUtil.compare_hashes(
                    imagehash.hex_to_hash(b["hash"]),
                    imagehash.hex_to_hash(a["hash"])
                )
            similarity = RpaImageUtil.hash_similarity(dist)
            if similarity < 90:
                changed_blocks.append(a)
        if not changed_blocks:
            return {
                "x": 0,
                "y": 0,
                "w": 0,
                "h": 0
            }

        min_x = min(block["x"] for block in changed_blocks)
        min_y = min(block["y"] for block in changed_blocks)
        max_x = max(block["x"] + block["w"] for block in changed_blocks)
        max_y = max(block["y"] + block["h"] for block in changed_blocks)

        return {
            "x": min_x,
            "y": min_y,
            "w": max_x - min_x,
            "h": max_y - min_y
        }
