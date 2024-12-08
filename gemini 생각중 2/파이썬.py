import requests
import os
import time
import json

def user_input_command():
    """
    사용자로부터 자연어 명령을 입력받는다.
    """
    print("실행할 명령을 자연어로 입력하세요. (done 또는 빈 줄 입력 시 종료)")
    line = input("> ").strip()
    if line.lower() == "done" or line == "":
        return None
    return line

def call_gemini_api(command):
    """
    Gemini API(또는 유사 LLM API)에 사용자 명령을 보내고,
    적절한 명령어 리스트를 포함한 JSON 응답을 받는다고 가정.
    
    실제 구현 시:
    - Gemini API 엔드포인트 및 인증 정보 필요
    - command를 prompt로 보내서 actions 리스트를 추출하도록 지시
    """
    # 가상의 응답 예시 (사용자 명령: "html파일 하나 만드는데 멋진 세계지도가 담겨있게 해줘")
    # 실제로는 command를 전송하고 LLM 응답을 받아 파싱하는 로직 필요
    # 여기서는 단순히 특정 키워드가 있는지 확인 후 하드코딩된 응답 예시를 반환
    # 실제 상황에서는 command를 post하여 LLM 응답을 받는 HTTP 요청 로직을 구현해야 한다.
    
    command_lower = command.lower()
    # 매우 단순한 예: "html파일" "만드" "멋진 세계지도" 키워드 존재 시 다음과 같은 결과 가정
    if "html" in command_lower and ("만드" in command_lower or "create" in command_lower) and ("세계지도" in command_lower):
        # 예: worldmap.html 파일을 만들고 그 안에 멋진 세계지도를 담은 HTML을 덮어쓰는 작업
        fake_response = {
            "actions": [
                {"action": "create_file", "filepath": "worldmap.html"},
                {"action": "overwrite_file", "filepath": "worldmap.html", "content": "<html><body><h1>멋진 세계 지도</h1></body></html>"}
            ]
        }
        return fake_response
    else:
        # 명령어를 판단하지 못했을 경우 빈 액션
        return {"actions": []}


def make_plan(command):
    """
    (1) 계획 수립
    Gemini API에 사용자 명령을 보내 actions를 받아온다.
    actions가 비어있다면 None 반환(유효한 계획 수립 실패).
    """
    response = call_gemini_api(command)
    actions = response.get("actions", [])
    if not actions:
        return None
    plan = {
        "actions": actions
    }
    return plan

def define_tasks(plan):
    """
    (2) 할 일 정의
    plan["actions"]에 따라 tasks를 생성.
    """
    tasks = []
    for action_item in plan["actions"]:
        action = action_item.get("action")
        if action == "call_api":
            endpoint = action_item.get("endpoint", "")
            tasks.append({
                "action": "call_api",
                "endpoint": endpoint,
                "method": "GET",
                "check_type": list
            })
        elif action == "list_directory":
            dirname = action_item.get("directory", "")
            tasks.append({
                "action": "list_directory",
                "directory": dirname
            })
        elif action == "create_file":
            filepath = action_item.get("filepath", "")
            tasks.append({
                "action": "create_file",
                "filepath": filepath
            })
        elif action == "open_file":
            filepath = action_item.get("filepath", "")
            tasks.append({
                "action": "open_file",
                "filepath": filepath
            })
        elif action == "overwrite_file":
            filepath = action_item.get("filepath", "")
            content = action_item.get("content", "")
            tasks.append({
                "action": "overwrite_file",
                "filepath": filepath,
                "content": content
            })
        else:
            return None

    return tasks if tasks else None

def perform_tasks(tasks):
    """
    (3) 할 일 수행
    """
    results = []
    for task in tasks:
        action = task["action"]
        if action == "call_api":
            endpoint = task.get("endpoint", "")
            response = requests.get(endpoint)
            if response.status_code == 200:
                try:
                    data = response.json()
                except:
                    data = None
                results.append({
                    "task": task,
                    "success": True,
                    "data": data
                })
            else:
                results.append({
                    "task": task,
                    "success": False,
                    "error": f"HTTP {response.status_code}"
                })
        elif action == "list_directory":
            directory = task.get("directory", "")
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except Exception as e:
                    results.append({
                        "task": task,
                        "success": False,
                        "error": f"Directory creation failed: {e}"
                    })
                    continue
            try:
                files = os.listdir(directory)
                results.append({
                    "task": task,
                    "success": True,
                    "files": files
                })
            except Exception as e:
                results.append({
                    "task": task,
                    "success": False,
                    "error": f"Directory list failed: {e}"
                })
        elif action == "create_file":
            filepath = task.get("filepath", "")
            try:
                dirpath = os.path.dirname(filepath)
                if dirpath and not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("")
                results.append({
                    "task": task,
                    "success": True
                })
            except Exception as e:
                results.append({
                    "task": task,
                    "success": False,
                    "error": f"File creation failed: {e}"
                })
        elif action == "open_file":
            filepath = task.get("filepath", "")
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                results.append({
                    "task": task,
                    "success": True,
                    "content": content
                })
            except Exception as e:
                results.append({
                    "task": task,
                    "success": False,
                    "error": f"File open failed: {e}"
                })
        elif action == "overwrite_file":
            filepath = task.get("filepath", "")
            content = task.get("content", "")
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                results.append({
                    "task": task,
                    "success": True
                })
            except Exception as e:
                results.append({
                    "task": task,
                    "success": False,
                    "error": f"File overwrite failed: {e}"
                })
        else:
            results.append({
                "task": task,
                "success": False,
                "error": f"Unknown action: {action}"
            })
    return results

def verify_results(tasks, results):
    """
    (4) 검증 단계
    모든 task가 success여야 하며,
    call_api의 경우 기대하는 타입(list) 확인
    """
    for result in results:
        if not result["success"]:
            return False
        if result["task"]["action"] == "call_api":
            expected_type = result["task"].get("check_type", None)
            if expected_type and result.get("data") is not None:
                if not isinstance(result["data"], expected_type):
                    return False
    return True

def main_loop():
    while True:
        command = user_input_command()
        if command is None:
            print("종료합니다.")
            break

        # 계획 수립
        while True:
            plan = make_plan(command)
            if plan is not None:
                break
            else:
                print("명령으로부터 유효한 계획을 수립하지 못했습니다. 다시 명령을 입력하세요.")
                command = user_input_command()
                if command is None:
                    print("종료합니다.")
                    return

        # 할 일 정의
        while True:
            tasks = define_tasks(plan)
            if tasks is not None:
                break
            else:
                print("할 일 정의 실패. 명령을 다시 입력하세요.")
                command = user_input_command()
                if command is None:
                    print("종료합니다.")
                    return
                # 다시 계획
                while True:
                    plan = make_plan(command)
                    if plan is not None:
                        break
                    else:
                        print("명령으로부터 유효한 계획을 수립하지 못했습니다. 다시 명령을 입력하세요.")
                        command = user_input_command()
                        if command is None:
                            print("종료합니다.")
                            return

        results = perform_tasks(tasks)

        if verify_results(tasks, results):
            print("모든 작업이 성공적으로 완료되었습니다!")
            for r in results:
                print(r)
            # 작업 완료 후 다시 새로운 명령을 받을 수 있음
        else:
            print("결과 검증 실패. 처음부터 다시 진행합니다.")

if __name__ == "__main__":
    main_loop()
