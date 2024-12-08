import json
import re
import os
import logging
import google.generativeai as genai

# 로깅 설정
logging.basicConfig(filename='execution.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# API 키를 직접 설정 (보안상 권장되지 않음)
api_key = "AIzaSyAgLwJmesiDug0FOab3TRN8Dyv8AeTd8cA"  # 여기에 실제 API 키를 입력하세요.
genai.configure(api_key=api_key)

def get_user_input():
    return input("원하시는 내용을 입력하세요: ")

def get_reference_path():
    path = input("참조할 파일 또는 폴더의 경로를 입력하세요 (없으면 Enter 키를 누르세요): ").strip()
    if path:
        if os.path.isfile(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"'{path}' 파일을 성공적으로 읽었습니다.")
                return 'file', path, content
            except Exception as e:
                print(f"파일을 읽는 중 오류가 발생했습니다: {e}")
                return None, None, None
        elif os.path.isdir(path):
            try:
                files = [os.path.join(path, fname) for fname in os.listdir(path) if os.path.isfile(os.path.join(path, fname))]
                if not files:
                    print(f"'{path}' 폴더에 파일이 없습니다.")
                    return None, None, None
                contents = {}
                for file in files:
                    with open(file, 'r', encoding='utf-8') as f:
                        contents[file] = f.read()
                print(f"'{path}' 폴더의 파일들을 성공적으로 읽었습니다.")
                return 'folder', path, contents
            except Exception as e:
                print(f"폴더를 읽는 중 오류가 발생했습니다: {e}")
                return None, None, None
        else:
            print(f"'{path}'는 유효한 파일 또는 폴더 경로가 아닙니다.")
            return None, None, None
    else:
        return None, None, None

def generate_plan(user_input, reference_type=None, reference_content=None):
    if reference_type == 'file':
        prompt = (
            f"사용자의 요청: {user_input}\n\n"
            f"참조 파일 내용:\n{reference_content}\n\n"
            "이 요청을 완벽하게 수행하기 위한 계획을 단계별로 작성해줘."
        )
    elif reference_type == 'folder':
        folder_contents = "\n".join([f"--- {fname} ---\n{content}" for fname, content in reference_content.items()])
        prompt = (
            f"사용자의 요청: {user_input}\n\n"
            f"참조 폴더 내용:\n{folder_contents}\n\n"
            "이 요청을 완벽하게 수행하기 위한 계획을 단계별로 작성해줘."
        )
    else:
        prompt = f"사용자의 요청: {user_input}\n\n이 요청을 완벽하게 수행하기 위한 계획을 단계별로 작성해줘."
    
    response = model.generate_content(prompt)
    return response.text.strip()

def generate_tasks(plan, reference_type=None, reference_content=None):
    if reference_type == 'file':
        prompt = (
            f"계획: {plan}\n\n"
            f"참조 파일 내용:\n{reference_content}\n\n"
            "각 단계에 따른 구체적인 해야할 일들을 스크립트에서 실행할 수 있는 'action' 필드와 함께 JSON 형식으로 작성해줘. "
            "지원되는 'action'은 다음과 같아: "
            "'create_folder' (폴더 생성), "
            "'create_file' (파일 생성), "
            "'write_to_file' (파일에 내용 작성), "
            "'test_and_debug' (테스트 및 디버깅). "
            "각 'action'에 필요한 추가 필드는 다음과 같아: "
            "- create_folder: 'folder_name'"
            "- create_file: 'filename'"
            "- write_to_file: 'filename', 'content'"
            "- test_and_debug: 'description'"
            "코드 블록이나 기타 텍스트 없이 순수한 JSON만 제공해줘. "
            "예시 형식: "
            "[{\"action\": \"create_file\", \"filename\": \"example.html\"}, "
            "{\"action\": \"write_to_file\", \"filename\": \"example.html\", \"content\": \"<html></html>\"}]"
        )
    elif reference_type == 'folder':
        folder_contents = "\n".join([f"--- {fname} ---\n{content}" for fname, content in reference_content.items()])
        prompt = (
            f"계획: {plan}\n\n"
            f"참조 폴더 내용:\n{folder_contents}\n\n"
            "각 단계에 따른 구체적인 해야할 일들을 스크립트에서 실행할 수 있는 'action' 필드와 함께 JSON 형식으로 작성해줘. "
            "지원되는 'action'은 다음과 같아: "
            "'create_folder' (폴더 생성), "
            "'create_file' (파일 생성), "
            "'write_to_file' (파일에 내용 작성), "
            "'test_and_debug' (테스트 및 디버깅). "
            "각 'action'에 필요한 추가 필드는 다음과 같아: "
            "- create_folder: 'folder_name'"
            "- create_file: 'filename'"
            "- write_to_file: 'filename', 'content'"
            "- test_and_debug: 'description'"
            "코드 블록이나 기타 텍스트 없이 순수한 JSON만 제공해줘. "
            "예시 형식: "
            "[{\"action\": \"create_file\", \"filename\": \"example.html\"}, "
            "{\"action\": \"write_to_file\", \"filename\": \"example.html\", \"content\": \"<html></html>\"}]"
        )
    else:
        prompt = (
            f"계획: {plan}\n\n"
            "각 단계에 따른 구체적인 해야할 일들을 스크립트에서 실행할 수 있는 'action' 필드와 함께 JSON 형식으로 작성해줘. "
            "지원되는 'action'은 다음과 같아: "
            "'create_folder' (폴더 생성), "
            "'create_file' (파일 생성), "
            "'write_to_file' (파일에 내용 작성), "
            "'test_and_debug' (테스트 및 디버깅). "
            "각 'action'에 필요한 추가 필드는 다음과 같아: "
            "- create_folder: 'folder_name'"
            "- create_file: 'filename'"
            "- write_to_file: 'filename', 'content'"
            "- test_and_debug: 'description'"
            "코드 블록이나 기타 텍스트 없이 순수한 JSON만 제공해줘. "
            "예시 형식: "
            "[{\"action\": \"create_file\", \"filename\": \"example.html\"}, "
            "{\"action\": \"write_to_file\", \"filename\": \"example.html\", \"content\": \"<html></html>\"}]"
        )
    response = model.generate_content(prompt)
    return response.text.strip()

def parse_tasks(tasks_text):
    # 코드 블록 제거 (```json ... ```), 만약 포함되어 있다면
    tasks_text = re.sub(r'```json\s*', '', tasks_text)
    tasks_text = re.sub(r'```', '', tasks_text)
    
    # JSON 파싱 시도
    try:
        tasks = json.loads(tasks_text)
        
        # 각 작업이 'action' 필드를 가지고 있는지 검증
        valid_tasks = []
        for task in tasks:
            if isinstance(task, dict) and 'action' in task:
                valid_tasks.append(task)
            else:
                print(f"유효하지 않은 작업 항목 발견: {task}")
        
        return valid_tasks
    except json.JSONDecodeError as e:
        print(f"작업 JSON 파싱 오류: {e}")
        print("AI의 응답이 올바른 JSON 형식인지 확인하세요.")
        print("생성된 해야할 일들 (JSON 형식):")
        print(tasks_text)
        return []

def execute_tasks(tasks):
    for task in tasks:
        action = task.get('action')
        
        # 'action' 필드가 없는 작업은 건너뜀
        if not action:
            logging.warning(f"'action' 필드가 없는 작업 건너뜀: {task}")
            print(f"알 수 없는 작업 유형: {action}")
            continue
        
        print(f"작업 실행 중: {action}")
        logging.info(f"작업 실행 중: {action}")
        
        if action == 'create_folder':
            folder_name = task.get('folder_name') or task.get('foldername')  # 'folder_name' 또는 'foldername' 사용
            if not folder_name:
                logging.error(f"'folder_name' 또는 'foldername' 키가 없습니다: {task}")
                print(f"'folder_name' 또는 'foldername' 키가 없습니다: {task}")
                continue
            try:
                os.makedirs(folder_name, exist_ok=True)
                logging.info(f"{folder_name} 폴더가 생성되었습니다.")
                print(f"{folder_name} 폴더가 생성되었습니다.")
            except Exception as e:
                logging.error(f"폴더 생성 중 에러 발생: {e}")
                print(f"폴더 생성 중 에러 발생: {e}")
                return False
        elif action == 'create_file':
            filename = task.get('filename')
            if not filename:
                logging.error(f"'filename' 키가 없습니다: {task}")
                print(f"'filename' 키가 없습니다: {task}")
                continue
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("")  # 빈 파일 생성
                logging.info(f"{filename} 파일이 생성되었습니다.")
                print(f"{filename} 파일이 생성되었습니다.")
            except Exception as e:
                logging.error(f"파일 생성 중 에러 발생: {e}")
                print(f"파일 생성 중 에러 발생: {e}")
                return False
        elif action == 'write_to_file':
            filename = task.get('filename')
            content = task.get('content', '')
            if not filename:
                logging.error(f"'filename' 키가 없습니다: {task}")
                print(f"'filename' 키가 없습니다: {task}")
                continue
            try:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(content + "\n")
                logging.info(f"{filename} 파일에 내용이 추가되었습니다.")
                print(f"{filename} 파일에 내용이 추가되었습니다.")
            except Exception as e:
                logging.error(f"파일 쓰기 중 에러 발생: {e}")
                print(f"파일 쓰기 중 에러 발생: {e}")
                return False
        elif action == 'test_and_debug':
            description = task.get('description', '')
            logging.info(f"작업 설명: {description}")
            print(f"작업 설명: {description}")
            # 실제 자동화된 테스트가 아닌 사용자에게 안내 메시지 제공
            print("테스트 및 디버깅을 수행하세요.")
        else:
            logging.warning(f"알 수 없는 작업 유형: {action}")
            print(f"알 수 없는 작업 유형: {action}")
            continue  # 알 수 없는 작업 유형은 건너뜀
    return True

def verify_execution():
    verification = input("작업이 완벽하게 수행되었습니까? (yes/no): ")
    return verification.lower() == 'yes'

def main():
    while True:
        user_input = get_user_input()
        reference_type, reference_path, reference_content = get_reference_path()
        
        # 1. 계획 세우기
        plan = generate_plan(user_input, reference_type, reference_content)
        print("\n생성된 계획:")
        print(plan)
        
        # 2. 해야할 것들 작성
        tasks_text = generate_tasks(plan, reference_type, reference_content)
        print("\n생성된 해야할 일들 (JSON 형식):")
        print(tasks_text)
        
        # 작업 파싱
        tasks = parse_tasks(tasks_text)
        if not tasks:
            print("작업 목록을 파싱하는데 실패했습니다. 다시 시도합니다.")
            continue
        
        print("\n파싱된 작업 리스트:")
        for task in tasks:
            print(f"- {task}")
        
        # 3. 해야할 것들 실행
        execution_success = execute_tasks(tasks)
        
        if not execution_success:
            print("작업 실행 중 문제가 발생했습니다. 다시 시도합니다.")
            continue
        
        # 4. 실행 결과 검증
        if verify_execution():
            print("작업이 성공적으로 완료되었습니다.")
            break
        else:
            print("작업이 완벽하게 완료되지 않았습니다. 다시 계획을 세웁니다.\n")

if __name__ == "__main__":
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        print(f"모델 로드 중 오류 발생: {e}")
        exit(1)
    
    main()
