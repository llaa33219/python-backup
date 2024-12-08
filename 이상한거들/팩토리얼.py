import math
number = int(input("팩토리얼 계산 값 입력"))

if number < 0:
    print("음수는 안됨")
else:
    print(math.factorial(number))