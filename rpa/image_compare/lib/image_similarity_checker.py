import numpy as np
from PIL import Image
import cv2
import imagehash
from scipy.spatial.distance import hamming
import matplotlib.pyplot as plt

class ImageSimilarityChecker:
    def __init__(self):
        pass
    
    def dhash(self, image_path, hash_size=8):
        """
        차분 해싱(Difference Hashing) 구현
        이미지의 인접 픽셀 간의 밝기 차이를 기반으로 해시 생성
        """
        # 이미지 열기 및 크기 조정
        image = Image.open(image_path).convert('L')  # 흑백으로 변환
        image = image.resize((hash_size + 1, hash_size))
        
        # 차분 값 계산
        pixels = np.array(image)
        diff = pixels[:, 1:] > pixels[:, :-1]
        
        # 비트 배열을 정수로 변환
        hash_value = 0
        for row in diff:
            for bit in row:
                hash_value = (hash_value << 1) | int(bit)
                
        return hash_value
    
    def phash(self, image_path, hash_size=8):
        """
        인지 해싱(Perceptual Hashing) - imagehash 라이브러리 사용
        DCT(이산 코사인 변환)를 사용하여 이미지 특성을 추출
        """
        image = Image.open(image_path)
        return imagehash.phash(image, hash_size=hash_size)
    
    def ahash(self, image_path, hash_size=8):
        """
        평균 해싱(Average Hashing) - imagehash 라이브러리 사용
        이미지의 평균 밝기를 기준으로 해시 생성
        """
        image = Image.open(image_path)
        return imagehash.average_hash(image, hash_size=hash_size)
    
    def whash(self, image_path, hash_size=8):
        """
        웨이블릿 해싱(Wavelet Hashing) - imagehash 라이브러리 사용
        웨이블릿 변환을 사용하여 이미지 특성을 추출
        """
        image = Image.open(image_path)
        return imagehash.whash(image, hash_size=hash_size)
    
    def colorhash(self, image_path, binbits=3):
        """
        색상 해싱(Color Hashing) - imagehash 라이브러리 사용
        이미지의 색상 분포를 기반으로 해시 생성
        """
        image = Image.open(image_path)
        return imagehash.colorhash(image, binbits=binbits)
    
    def compare_hashes(self, hash1, hash2):
        """
        두 해시 값의 해밍 거리 계산(비트 차이)
        0은 완전 일치, 값이 작을수록 유사도가 높음
        """
        return hash1 - hash2
    
    def hash_similarity(self, distance, hash_size=8):
        """
        해밍 거리를 백분율 유사도로 변환
        """
        max_distance = hash_size * hash_size  # 최대 가능한 거리
        similarity = (1 - (distance / max_distance)) * 100
        return similarity
    
    def histogram_comparison(self, image_path1, image_path2):
        """
        히스토그램 비교 방식
        이미지의 색상 분포를 비교하는 방법
        """
        # 이미지 로드
        img1 = cv2.imread(image_path1)
        img2 = cv2.imread(image_path2)
        
        # 크기 조정 (선택사항)
        img1 = cv2.resize(img1, (256, 256))
        img2 = cv2.resize(img2, (256, 256))
        
        # RGB 채널별로 히스토그램 계산
        hist1_r = cv2.calcHist([img1], [0], None, [256], [0, 256])
        hist1_g = cv2.calcHist([img1], [1], None, [256], [0, 256])
        hist1_b = cv2.calcHist([img1], [2], None, [256], [0, 256])
        
        hist2_r = cv2.calcHist([img2], [0], None, [256], [0, 256])
        hist2_g = cv2.calcHist([img2], [1], None, [256], [0, 256])
        hist2_b = cv2.calcHist([img2], [2], None, [256], [0, 256])
        
        # 히스토그램 정규화
        cv2.normalize(hist1_r, hist1_r, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist1_g, hist1_g, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist1_b, hist1_b, 0, 1, cv2.NORM_MINMAX)
        
        cv2.normalize(hist2_r, hist2_r, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist2_g, hist2_g, 0, 1, cv2.NORM_MINMAX)
        cv2.normalize(hist2_b, hist2_b, 0, 1, cv2.NORM_MINMAX)
        
        # 히스토그램 비교 (상관관계 방식)
        similarity_r = cv2.compareHist(hist1_r, hist2_r, cv2.HISTCMP_CORREL)
        similarity_g = cv2.compareHist(hist1_g, hist2_g, cv2.HISTCMP_CORREL)
        similarity_b = cv2.compareHist(hist1_b, hist2_b, cv2.HISTCMP_CORREL)
        
        # 평균 유사도
        avg_similarity = (similarity_r + similarity_g + similarity_b) / 3.0
        return avg_similarity * 100  # 백분율로 변환
    
    def feature_matching(self, image_path1, image_path2):
        """
        특징점 기반 매칭 방식 (SIFT, ORB 등의 알고리즘 사용)
        이미지의 특징점을 추출하고 매칭하는 방법
        """
        # 이미지 로드
        img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)
        
        # 크기 조정 (선택사항)
        img1 = cv2.resize(img1, (512, 512))
        img2 = cv2.resize(img2, (512, 512))
        
        # ORB(Oriented FAST and Rotated BRIEF) 알고리즘 사용
        orb = cv2.ORB_create()
        
        # 특징점과 설명자 추출
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        
        # 특징점이 너무 적으면 유사도가 낮다고 판단
        if len(kp1) < 10 or len(kp2) < 10:
            return 0.0
        
        # 브루트 포스 매처 생성
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        
        # 특징점 매칭
        matches = bf.match(des1, des2)
        
        # 거리 기준으로 정렬
        matches = sorted(matches, key=lambda x: x.distance)
        
        # 좋은 매칭점의 개수를 기준으로 유사도 계산
        good_matches = [m for m in matches if m.distance < 50]  # 임계값 조정 가능
        
        similarity = len(good_matches) / max(len(kp1), len(kp2)) * 100
        return min(similarity, 100.0)  # 100%를 넘지 않도록 제한
    
    def ssim_comparison(self, image_path1, image_path2):
        """
        SSIM(Structural Similarity Index) 비교
        구조적 유사성을 비교하는 방법
        """
        # 이미지 로드 및 그레이스케일 변환
        img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)
        
        # 크기 조정 (같은 크기여야 함)
        img1 = cv2.resize(img1, (256, 256))
        img2 = cv2.resize(img2, (256, 256))
        
        # SSIM 계산 (scikit-image 필요)
        try:
            from skimage.metrics import structural_similarity as ssim
            similarity = ssim(img1, img2)
            return similarity * 100  # 백분율로 변환
        except ImportError:
            # scikit-image가 없는 경우 대체 방법 사용
            return self.histogram_comparison(image_path1, image_path2)
    
    def are_images_similar(self, image_path1, image_path2, method='phash', threshold=90):
        """
        두 이미지가 지정된 임계값보다 유사한지 확인
        
        Parameters:
        - image_path1, image_path2: 비교할 이미지 경로
        - method: 비교 방법 ('phash', 'dhash', 'ahash', 'whash', 'colorhash', 
                 'histogram', 'feature', 'ssim')
        - threshold: 유사도 임계값 (0-100), 이 값 이상이면 유사하다고 판단
        
        Returns:
        - 유사 여부(Boolean), 유사도 점수(0-100)
        """
        similarity = 0
        
        if method == 'phash':
            hash1 = self.phash(image_path1)
            hash2 = self.phash(image_path2)
            distance = self.compare_hashes(hash1, hash2)
            similarity = self.hash_similarity(distance)
            
        elif method == 'dhash':
            hash1 = self.dhash(image_path1)
            hash2 = self.dhash(image_path2)
            # 해밍 거리 계산 (비트 비교)
            bin_hash1 = bin(hash1)[2:].zfill(64)
            bin_hash2 = bin(hash2)[2:].zfill(64)
            distance = sum(b1 != b2 for b1, b2 in zip(bin_hash1, bin_hash2))
            similarity = (1 - (distance / 64)) * 100
            
        elif method == 'ahash':
            hash1 = self.ahash(image_path1)
            hash2 = self.ahash(image_path2)
            distance = self.compare_hashes(hash1, hash2)
            similarity = self.hash_similarity(distance)
            
        elif method == 'whash':
            hash1 = self.whash(image_path1)
            hash2 = self.whash(image_path2)
            distance = self.compare_hashes(hash1, hash2)
            similarity = self.hash_similarity(distance)
            
        elif method == 'colorhash':
            hash1 = self.colorhash(image_path1)
            hash2 = self.colorhash(image_path2)
            distance = self.compare_hashes(hash1, hash2)
            similarity = self.hash_similarity(distance, hash_size=4)  # ColorHash는 크기가 다를 수 있음
            
        elif method == 'histogram':
            similarity = self.histogram_comparison(image_path1, image_path2)
            
        elif method == 'feature':
            similarity = self.feature_matching(image_path1, image_path2)
            
        elif method == 'ssim':
            similarity = self.ssim_comparison(image_path1, image_path2)
            
        else:
            raise ValueError(f"지원하지 않는 비교 방법입니다: {method}")
        
        # 유사도 임계값 기준으로 판단
        is_similar = similarity >= threshold
        
        return is_similar, similarity

# 예제 사용법
if __name__ == "__main__":
    checker = ImageSimilarityChecker()
    
    # 테스트할 이미지 파일 경로
    image1 = "image1.jpg"
    image2 = "image2.jpg"  # image1과 유사한 이미지
    image3 = "image3.jpg"  # image1과 다른 이미지
    
    # 여러 방법으로 비교
    methods = ['phash', 'dhash', 'ahash', 'whash', 'colorhash', 'histogram', 'feature', 'ssim']
    
    print("이미지 1과 이미지 2 비교 (유사한 이미지):")
    for method in methods:
        try:
            is_similar, similarity = checker.are_images_similar(image1, image2, method=method)
            print(f"  {method}: 유사도 {similarity:.2f}% {'(유사함)' if is_similar else '(다름)'}")
        except Exception as e:
            print(f"  {method}: 오류 - {e}")
    
    print("\n이미지 1과 이미지 3 비교 (다른 이미지):")
    for method in methods:
        try:
            is_similar, similarity = checker.are_images_similar(image1, image3, method=method)
            print(f"  {method}: 유사도 {similarity:.2f}% {'(유사함)' if is_similar else '(다름)'}")
        except Exception as e:
            print(f"  {method}: 오류 - {e}")