from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

def translate_image(image_path):
    # ChromeDriver의 경로를 올바르게 지정합니다.
    chrome_driver_path = r'C:\chromedriver\chromedriver.exe'
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        # Google Translate의 이미지 번역 페이지로 이동
        driver.get("https://translate.google.com/?sl=auto&tl=en&op=docs")

        # 이미지 파일 업로드 버튼을 찾고 파일 경로 전송
        upload_button = driver.find_element(By.XPATH, '//input[@type="file"]')
        upload_button.send_keys(image_path)

        # 업로드 후 번역이 완료될 때까지 대기
        time.sleep(10)  # 이미지 크기에 따라 다름

        # 번역된 텍스트 결과 가져오기
        translated_text = driver.find_element(By.XPATH, '//span[@jsname="W297wb"]')
        result = translated_text.text

        return result

    finally:
        # 브라우저 닫기
        driver.quit()

def main():
    image_path = 'path_to_your_image.png'  # 사용자가 번역하고자 하는 이미지 경로
    translated_text = translate_image(image_path)
    print("번역된 텍스트:")
    print(translated_text)

if __name__ == "__main__":
    main()
