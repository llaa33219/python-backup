import os
import openai
import threading
import sys
import asyncio
import queue

# OpenAI API 키 설정 (환경변수로 설정 권장)
openai.api_key = os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE")

# 사용자 입력을 비동기적으로 처리하기 위한 큐
user_input_queue = queue.Queue()

# 사용자 입력을 별도의 스레드에서 받는 함수
def input_thread():
    while True:
        user_input = input()
        user_input_queue.put(user_input)

# 메시지 히스토리 관리
# role: system, user, assistant
messages = [
    {"role": "system", "content": "You are a helpful assistant."}
]

async def stream_chat_response(messages):
    """OpenAI API에 메시지를 보내고 스트림 형태로 응답을 받는 비동기 함수"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True,
        temperature=0.7
    )

    # 스트림 형식의 응답 출력
    full_response = ""
    for chunk in response:
        if 'choices' in chunk:
            delta = chunk['choices'][0]['delta']
            if 'content' in delta:
                text = delta['content']
                # 여기서 바로 출력 (개행 없이)
                sys.stdout.write(text)
                sys.stdout.flush()
                full_response += text
    print()  # 응답 종료 후 개행
    return full_response

async def main():
    # 입력용 스레드 시작
    threading.Thread(target=input_thread, daemon=True).start()

    while True:
        # 사용자 입력 대기
        print("당신: ", end="", flush=True)
        
        # 입력이 들어올 때까지 대기 (비동기 상황 흉내를 위해 asyncio.sleep 사용)
        user_msg = None
        while user_msg is None:
            await asyncio.sleep(0.1)
            if not user_input_queue.empty():
                user_msg = user_input_queue.get()
        
        # 사용자 입력 메시지를 히스토리에 추가
        messages.append({"role": "user", "content": user_msg})

        # ChatGPT 응답 받기
        assistant_response = await stream_chat_response(messages)
        # 응답을 히스토리에 추가
        messages.append({"role": "assistant", "content": assistant_response})

        # 이제 다음 루프로 넘어가서 다시 사용자 입력을 기다리고 응답을 생성함

if __name__ == "__main__":
    # asyncio 이벤트 루프 실행
    asyncio.run(main())
