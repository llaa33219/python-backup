import tkinter as tk
from tkinter import ttk
from googletrans import Translator
import pyperclip
import keyboard
import win32api
import win32gui

# 번역기 초기화
translator = Translator()

# 현재 커서 위치를 가져오는 함수
def get_cursor_position():
    x, y = win32api.GetCursorPos()
    return x, y

# 팝업을 현재 커서 위치에 표시하는 기능
def show_translate_popup():
    x, y = get_cursor_position()  # 현재 커서 위치 가져오기
    popup = tk.Toplevel()
    popup.overrideredirect(True)  # 창 테두리와 타이틀바 없애기
    popup.geometry(f"400x300+{x}+{y}")  # 현재 커서 위치에 표시
    popup.wm_attributes("-topmost", True)  # 항상 위에 표시
    popup.configure(bg="white")

    def close_popup(event=None):
        popup.destroy()

    # 포커스를 잃으면 창 닫기
    popup.bind("<FocusOut>", close_popup)

    # 팝업 내용 구성
    languages = {'영어': 'en', '한국어': 'ko', '일본어': 'ja', '중국어(간체)': 'zh-cn', '독일어': 'de', '프랑스어': 'fr'}
    language_options = list(languages.keys())
    selected_language = tk.StringVar(value=language_options[0])

    input_text = tk.Text(popup, height=5, width=50, bg="white", bd=2)
    input_text.pack(pady=10)

    language_frame = tk.Frame(popup, bg="white")
    language_frame.pack()

    language_label = tk.Label(language_frame, text="언어 자동인식 ->", bg="white")
    language_label.pack(side=tk.LEFT)

    language_combo = ttk.Combobox(language_frame, values=language_options, textvariable=selected_language)
    language_combo.pack(side=tk.LEFT)

    output_text = tk.Text(popup, height=5, width=50, bg="white", bd=2)
    output_text.pack(pady=10)

    def copy_translated_text():
        pyperclip.copy(output_text.get("1.0", tk.END).strip())

    def translate_text():
        text = input_text.get("1.0", tk.END).strip()
        if text:
            dest_lang = languages[selected_language.get()]
            translated = translator.translate(text, src='auto', dest=dest_lang).text
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, translated)

    def replace_text():
        try:
            selected_text = input_text.selection_get()
            dest_lang = languages[selected_language.get()]
            translated = translator.translate(selected_text, src='auto', dest=dest_lang).text
            input_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
            input_text.insert(tk.INSERT, translated)
        except tk.TclError:
            pass

    button_frame = tk.Frame(popup, bg="white")
    button_frame.pack(pady=10)

    copy_button = tk.Button(button_frame, text="복사", command=copy_translated_text)
    copy_button.pack(side=tk.LEFT, padx=10)

    replace_button = tk.Button(button_frame, text="교체", command=replace_text)
    replace_button.pack(side=tk.LEFT, padx=10)

    translate_button = tk.Button(popup, text="번역", command=translate_text)
    translate_button.pack()

    popup.focus_set()

# Alt + T 키 조합으로 팝업 표시
keyboard.add_hotkey('alt+t', show_translate_popup)

# 프로그램이 종료되지 않도록 대기
keyboard.wait('esc')  # 프로그램을 강제로 종료하려면 ESC 키를 누르세요
