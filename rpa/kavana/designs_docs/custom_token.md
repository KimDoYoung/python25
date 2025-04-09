# custom_token

## 리팩토링

1. token 하위에 custom_token
2. custom_token 에는 express_list, status ['parsed', 'evaluated']
3. custom_token하위에 pointtoken... 이런식으로

## 종류
1. point
2. region
3. rectangle
4. image
5. window
6. application

## 리팩토링코드

### POINT
```kvs
set x = 10
set y = 20
set p1 = Point(10,20)
set p2 = Point(x+2, y+(1+1))
print p1, p2
set x1 = Point_x(p1)
set y1 = Point_y(p2)
set xy = POINT_xy(p1)
print xy[0], xy[1]

```