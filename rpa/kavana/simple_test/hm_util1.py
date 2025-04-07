from lib.core.token_util import TokenUtil  # 여기에 dict_to_hashmap_token 이 있다고 가정

def main():
    # 테스트용 dict 데이터
    data = {
        "name": "1.txt",
        "size": 20,
        "modified": "2025-04-07 11:23:34"
    }

    data2 = {
        "files": ["1.txt", "2.txt"],
        "count": 2
    }

    print("▶ HashMapToken 생성 테스트 1")
    token1 = TokenUtil.dict_to_hashmap_token(data)
    print("Token 객체:", token1)
    print("Token string 표현:", str(token1))
    print("Token primitive 변환:", token1.data.primitive)

    print("\n▶ HashMapToken 생성 테스트 2 (리스트 포함)")
    token2 = TokenUtil.dict_to_hashmap_token(data2)
    print("Token 객체:", token2)
    print("Token string 표현:", str(token2))
    print("Token primitive 변환:", token2.data.primitive)

    token3 = TokenUtil.list_to_array_token([1,2,3])
    print("Token 객체:", token3)
    print("Token string 표현:", str(token3))
    print("Token primitive 변환:", token3.data.primitive)


if __name__ == "__main__":
    main()
