import pyzipper
import itertools
import string
from multiprocessing import Pool, Manager, cpu_count
from tqdm import tqdm
import sys
import time
from threading import Thread, Event

# ZIP 파일 경로와 비밀번호 길이 설정
ZIP_FILE_PATH = r'entryExtension.zip'  # 여기에 ZIP 파일의 전체 경로를 입력하세요.
START_LENGTH = 5  # 시작 비밀번호 길이
MAX_LENGTH = 30  # 최대 비밀번호 길이 (원하는 대로 설정)

# 비밀번호에 포함할 문자 집합 설정 (영어 대소문자, 숫자, 일반적인 특수 문자)
CHARACTER_SET = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:',.<>/?`~"

def try_password(args):
    zip_path, password, counter, lock = args
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.extractall(pwd=password.encode('utf-8'))
        with lock:
            counter.value += 1
        return password  # 비밀번호가 맞으면 반환
    except:
        with lock:
            counter.value += 1
        return None  # 비밀번호가 틀리면 None 반환

def password_generator(length, characters):
    for pwd in itertools.product(characters, repeat=length):
        yield ''.join(pwd)

def display_counter(counter, total_combinations, stop_event, lock):
    with tqdm(total=total_combinations, desc="총 시도된 비밀번호", unit="pwd") as pbar:
        last_count = 0
        while not stop_event.is_set():
            with lock:
                current = counter.value
            increment = current - last_count
            if increment > 0:
                pbar.update(increment)
                last_count = current
            time.sleep(0.5)
        # 최종 업데이트
        with lock:
            current = counter.value
        increment = current - last_count
        if increment > 0:
            pbar.update(increment)

def main():
    manager = Manager()
    found = manager.Value('found', False)
    password_found = manager.list()
    counter = manager.Value('i', 0)  # 시도된 비밀번호 수를 저장할 공유 변수
    lock = manager.Lock()  # 별도의 Lock 생성

    pool = Pool(processes=cpu_count())

    try:
        current_length = START_LENGTH
        while current_length <= MAX_LENGTH:
            print(f"\n현재 비밀번호 길이: {current_length}")
            generator = password_generator(current_length, CHARACTER_SET)
            args_generator = ((ZIP_FILE_PATH, pwd, counter, lock) for pwd in generator)

            total_combinations = len(CHARACTER_SET) ** current_length

            # 카운터 표시를 위한 스레드와 이벤트 생성
            stop_event = Event()
            counter_thread = Thread(target=display_counter, args=(counter, total_combinations, stop_event, lock))
            counter_thread.start()

            for result in pool.imap_unordered(try_password, args_generator):
                if result:
                    print(f"\n비밀번호를 찾았습니다: {result}")
                    found.value = True
                    password_found.append(result)
                    pool.terminate()
                    stop_event.set()
                    break

            stop_event.set()
            counter_thread.join()

            if found.value:
                break

            current_length += 1  # 다음 길이로 증가

    except KeyboardInterrupt:
        print("\n사용자에 의해 중단되었습니다.")
    finally:
        pool.close()
        pool.join()

    if not password_found:
        print("비밀번호를 찾지 못했습니다.")

if __name__ == "__main__":
    if not ZIP_FILE_PATH:
        print("ZIP 파일 경로를 설정하세요.")
        sys.exit(1)
    main()
