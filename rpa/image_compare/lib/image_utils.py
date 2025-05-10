from image_similarity_checker import ImageSimilarityChecker
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2

def show_comparison_results(image1_path, image2_path):
    """여러 방법으로 이미지 유사도를 비교하고 결과 시각화"""
    checker = ImageSimilarityChecker()
    
    # 이미지 로드 및 표시
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)
    
    # BGR에서 RGB로 변환 (matplotlib 표시용)
    img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    
    # 여러 방법으로 비교
    methods = ['phash', 'dhash', 'ahash', 'whash', 'colorhash', 'histogram', 'feature', 'ssim']
    similarity_scores = []
    
    for method in methods:
        try:
            _, similarity = checker.are_images_similar(image1_path, image2_path, method=method)
            similarity_scores.append(similarity)
        except Exception as e:
            similarity_scores.append(0)
            print(f"  {method} 오류: {e}")
    
    # 결과 시각화
    plt.figure(figsize=(12, 8))
    
    # 이미지 표시
    plt.subplot(2, 1, 1)
    plt.subplot(2, 2, 1)
    plt.imshow(img1_rgb)
    plt.title('이미지 1')
    plt.axis('off')
    
    plt.subplot(2, 2, 2)
    plt.imshow(img2_rgb)
    plt.title('이미지 2')
    plt.axis('off')
    
    # 유사도 결과 그래프 표시
    plt.subplot(2, 1, 2)
    bars = plt.bar(methods, similarity_scores, color='skyblue')
    plt.axhline(y=90, color='red', linestyle='-', alpha=0.7, label='90% 임계값')
    
    # 바 위에 값 표시
    for bar, score in zip(bars, similarity_scores):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{score:.1f}%', ha='center', va='bottom')
    
    plt.ylim(0, 105)  # y축 범위 설정
    plt.xlabel('비교 방법')
    plt.ylabel('유사도 (%)')
    plt.title('이미지 유사도 비교 결과')
    plt.legend()
    plt.tight_layout()
    
    plt.savefig('similarity_comparison.png')  # 결과 저장
    plt.show()

def find_similar_images(target_image_path, image_paths_list, method='phash', threshold=90):
    """
    주어진 대상 이미지와 유사한 이미지들을 찾아 반환
    
    Parameters:
    - target_image_path: 대상 이미지 경로
    - image_paths_list: 비교할 이미지 경로 리스트
    - method: 비교 방법
    - threshold: 유사도 임계값
    
    Returns:
    - 유사한 이미지 경로와 유사도 점수가 담긴 리스트
    """
    checker = ImageSimilarityChecker()
    similar_images = []
    
    for img_path in image_paths_list:
        try:
            is_similar, similarity = checker.are_images_similar(
                target_image_path, img_path, method=method, threshold=threshold
            )
            if is_similar:
                similar_images.append((img_path, similarity))
        except Exception as e:
            print(f"이미지 {img_path} 처리 중 오류 발생: {e}")
    
    # 유사도 기준 내림차순 정렬
    similar_images.sort(key=lambda x: x[1], reverse=True)
    return similar_images

def precompute_hash_database(image_paths_list, method='phash'):
    """
    이미지 해시를 미리 계산하여 데이터베이스 생성
    실제 사용 시 이 값을 파일이나 데이터베이스에 저장하면 됨
    
    Parameters:
    - image_paths_list: 이미지 경로 리스트
    - method: 해시 방법
    
    Returns:
    - 이미지 경로와 해시값을 매핑한 딕셔너리
    """
    checker = ImageSimilarityChecker()
    hash_database = {}
    
    for img_path in image_paths_list:
        try:
            if method == 'phash':
                hash_value = checker.phash(img_path)
            elif method == 'dhash':
                hash_value = checker.dhash(img_path)
            elif method == 'ahash':
                hash_value = checker.ahash(img_path)
            elif method == 'whash':
                hash_value = checker.whash(img_path)
            elif method == 'colorhash':
                hash_value = checker.colorhash(img_path)
            else:
                raise ValueError(f"지원하지 않는 해시 방법: {method}")
                
            hash_database[img_path] = hash_value
            
        except Exception as e:
            print(f"이미지 {img_path} 해시 계산 중 오류 발생: {e}")
    
    return hash_database

def find_similar_from_database(target_image_path, hash_database, method='phash', threshold=90):
    """
    미리 계산된 해시 데이터베이스에서 유사한 이미지 찾기
    
    Parameters:
    - target_image_path: 대상 이미지 경로
    - hash_database: 이미지 경로와 해시를 매핑한 딕셔너리
    - method: 해시 방법
    - threshold: 유사도 임계값
    
    Returns:
    - 유사한 이미지 경로와 유사도 점수가 담긴 리스트
    """
    checker = ImageSimilarityChecker()
    similar_images = []
    
    # 대상 이미지 해시 계산
    if method == 'phash':
        target_hash = checker.phash(target_image_path)
    elif method == 'dhash':
        target_hash = checker.dhash(target_image_path)
    elif method == 'ahash':
        target_hash = checker.ahash(target_image_path)
    elif method == 'whash':
        target_hash = checker.whash(target_image_path)
    elif method == 'colorhash':
        target_hash = checker.colorhash(target_image_path)
    else:
        raise ValueError(f"지원하지 않는 해시 방법: {method}")
    
    # 유사도 계산 및 임계값 기준 필터링
    for img_path, img_hash in hash_database.items():
        distance = checker.compare_hashes(target_hash, img_hash)
        if method == 'colorhash':
            similarity = checker.hash_similarity(distance, hash_size=4)
        else:
            similarity = checker.hash_similarity(distance)
        
        if similarity >= threshold:
            similar_images.append((img_path, similarity))
    
    # 유사도 기준 내림차순 정렬
    similar_images.sort(key=lambda x: x[1], reverse=True)
    return similar_images

# 예제 사용법
if __name__ == "__main__":
    # 1. 두 이미지의 유사도 측정 및 시각화
    print("이미지 유사도 비교 시각화")
    show_comparison_results("image1.jpg", "image2.jpg")
    
    # 2. 폴더 내 유사 이미지 검색
    print("\n유사 이미지 검색")
    image_list = ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg", "image5.jpg"]
    similar_images = find_similar_images("target.jpg", image_list, method='phash', threshold=90)
    
    print(f"대상 이미지와 유사한 이미지 {len(similar_images)}개 발견:")
    for img_path, similarity in similar_images:
        print(f"  {img_path}: 유사도 {similarity:.2f}%")
    
    # 3. 해시 데이터베이스 생성 및 검색
    print("\n해시 데이터베이스 활용")
    hash_db = precompute_hash_database(image_list, method='phash')
    
    similar_from_db = find_similar_from_database("query.jpg", hash_db, method='phash', threshold=90)
    print(f"데이터베이스에서 유사한 이미지 {len(similar_from_db)}개 발견:")
    for img_path, similarity in similar_from_db:
        print(f"  {img_path}: 유사도 {similarity:.2f}%")