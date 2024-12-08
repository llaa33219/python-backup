from datasets import load_dataset

# SQuAD 데이터셋 로드
dataset = load_dataset('squad', split='train')

questions = []
answers = []

for entry in dataset:
    question = entry['question']
    answer = entry['answers']['text'][0]  # 첫 번째 답변만 사용
    questions.append(f"{question}\n")
    answers.append(f"{answer}\n")

# 10만 개의 질문과 대답 추출
questions = questions[:100000]
answers = answers[:100000]

# 질문과 대답의 수가 같은지 확인
if len(questions) == len(answers):
    print(f"Number of questions: {len(questions)}, Number of answers: {len(answers)}")

    # 결과 저장
    questions_file_path = 'questions.txt'
    answers_file_path = 'answers.txt'

    with open(questions_file_path, 'w', encoding='utf-8') as q_file:
        q_file.writelines(questions)

    with open(answers_file_path, 'w', encoding='utf-8') as a_file:
        a_file.writelines(answers)

    print("작업이 완료되었습니다. 'questions.txt'와 'answers.txt' 파일을 확인하세요.")
else:
    print("The number of questions and answers do not match.")
