import unicodedata

def apply_combining_marks_sequentially(input_string):
    # 확장된 결합 가능 기호의 유니코드 범위
    ranges = [
        (0xFE2E, 0xFE2F),
        (0x2DE0, 0x2DFF),
        (0xA8E0, 0xA8FF),
        (0x0E30, 0x0E3A),
        (0x0E47, 0x0E4E),
    ]
    
    combined_strings = []

    # 각 범위에 대하여
    for start, end in ranges:
        # 각 결합 기호를 적용
        for code in range(start, end + 1):
            # 문자열의 각 문자에 대해 결합 기호 적용
            combined_string = ''.join([unicodedata.normalize('NFC', char + chr(code)) for char in input_string])
            # 결합 문자열만 저장
            combined_strings.append(combined_string)

    return combined_strings

# 사용자 입력 받기
input_string = input("적용할 글자를 입력하세요: ")

# 함수 호출 및 결과 출력
combined_results = apply_combining_marks_sequentially(input_string)
for result in combined_results:
    print(result)
