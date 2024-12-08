import csv

# 파일 경로 설정
txt_file1 = '아름다운 질문 라이트.txt'
txt_file2 = '간지나는 대답 라이트.txt'
csv_file = 'questions_answers_merged1.csv'

# 파일 읽기
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

# 각 txt 파일에서 문장 읽어오기
lines1 = read_txt_file(txt_file1)
lines2 = read_txt_file(txt_file2)

# 두 리스트의 길이를 맞추기 (짧은 쪽에 빈 문자열 추가)
max_len = max(len(lines1), len(lines2))
lines1.extend([''] * (max_len - len(lines1)))
lines2.extend([''] * (max_len - len(lines2)))

# CSV 파일로 저장
with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Question', 'Answer'])  # 헤더 작성
    for line1, line2 in zip(lines1, lines2):
        csvwriter.writerow([line1, line2])

print(f"CSV 파일로 저장되었습니다: {csv_file}")