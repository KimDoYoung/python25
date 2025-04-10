# 이미지 명령어

## 명령어와 데이터 타입

1. Image데이터타입이 있다.
2. 명령어도 IMAGE가 있다.
3. from_file, to_file, from_var, to_var 라는 key명을 쓰면 좋을 것 같아.
4. 예를 보이면 아래와 같음

```kvs
MAIN
set base_dir = "C:\\Users\\PC\\Pictures\\";
SET img1 = IMAGE(f"{base_dir}\\efriend1.png")
IMAGE resize factor=20 from_var=img1 to_var="img2"
IMAGE save from_var=img2 to_file=f"{base_dir}\\efriend2.png"
END_MAIN
```

4 아래 명령어들과 3.의 옵션들을 사용해서 명령어를 제안해줘

### save

IMAGE save from_var=img2 to_file=f"{base_dir}\\efriend2.png"

### resize

IMAGE resize factor=0.5 from_var=img1 to_var=img2
IMAGE resize width=300 height=200 from_file="input.png" to_file="output.png"

### clip

IMAGE clip region=region(0,0,400,300) from_file="src.png" to_file="cropped.png"
IMAGE clip rectangle= rectangle(0,0,100,100) from_file="src.png" to_var="img4"

### to_gray

IMAGE to_gray from_var=img3 to_var=gray1
IMAGE to_gray from_file="color.png" to_file="gray.png"

### convert

IMAGE convert_to mode="RGB" from_var=gray1 to_var=rgb1
IMAGE convert_to mode="L" from_file="gray.png" to_file="gray_l.png"

### rotate

IMAGE rotate angle=90 expand=True from_var=img1 to_var=rotated1
IMAGE rotate angle=45 from_file="input.png" to_file="rotated.png"

### blur

IMAGE blur radius=5 from_var=img1 to_var=blurred1
IMAGE blur radius=2.0 from_file="input.png" to_file="blurred.png"

### threshold

IMAGE threshold threshold=128 from_var=gray1 to_var=binary1
IMAGE threshold threshold=100 from_file="gray.png" to_file="binary.png"
