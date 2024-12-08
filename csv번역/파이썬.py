import pandas as pd
from googletrans import Translator
from tqdm import tqdm
import time
import sys

# 번역할 CSV 파일 경로
input_csv = 'input.csv'  # 원본 CSV 파일 경로를 지정하세요
# 번역된 내용을 저장할 CSV 파일 경로
output_csv = 'translated_output.csv'  # 결과를 저장할 CSV 파일 경로를 지정하세요
# 번역할 대상 언어 (한국어는 'ko')
target_language = 'ko'
# 번역할 열 목록 (예: ['Question', 'Answer'])
columns_to_translate = ['Question', 'Answer']  # 번역할 열 이름을 리스트로 지정하세요

def translate_text(text, translator, target_lang):
    """
    단일 텍스트를 Googletrans를 사용하여 번역합니다.
    """
    try:
        if not text.strip():
            return ''
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        print(f"번역 중 오류 발생: {e}")
        return text  # 오류 발생 시 원본 텍스트 반환

def translate_csv_columns_individual(input_file, output_file, columns, target_lang):
    # Translator 객체 초기화
    translator = Translator()
    
    # CSV 파일 읽기
    try:
        df = pd.read_csv(input_file, encoding='utf-8-sig')
    except UnicodeDecodeError:
        # utf-8-sig로 실패하면 기본 utf-8로 시도
        try:
            df = pd.read_csv(input_file, encoding='utf-8')
        except Exception as e:
            print(f"CSV 파일을 읽는 중 오류 발생: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"CSV 파일을 읽는 중 오류 발생: {e}")
        sys.exit(1)

    for column in columns:
        if column not in df.columns:
            print(f"'{column}' 열이 CSV 파일에 존재하지 않습니다.")
            continue

        print(f"'{column}' 열을 '{target_lang}' 언어로 번역 중...")
        # NaN 값을 빈 문자열로 대체
        texts = df[column].fillna('').astype(str).tolist()

        translated_texts = []
        for text in tqdm(texts, desc=f"Translating '{column}'"):
            translated = translate_text(text, translator, target_lang)
            translated_texts.append(translated)
            time.sleep(0.1)  # API 제한 방지를 위해 잠시 대기

        # 샘플 번역 확인
        if texts:
            sample_original = texts[0]
            sample_translated = translated_texts[0]
            print(f"Sample translation - Original: '{sample_original}' | Translated: '{sample_translated}'")

        # 원본 텍스트를 번역된 텍스트로 교체
        df[column] = translated_texts

    # 번역된 CSV 저장
    try:
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"번역 완료! '{output_file}' 파일이 생성되었습니다.")
    except Exception as e:
        print(f"CSV 파일을 저장하는 중 오류 발생: {e}")

if __name__ == "__main__":
    translate_csv_columns_individual(input_csv, output_csv, columns_to_translate, target_language)
