import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import sys

def create_images_folder():
    if not os.path.exists('images'):
        os.makedirs('images')

def crop_panorama(image_path, num_crops=50, aspect_ratio=(3,4)):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            target_ratio = aspect_ratio[0] / aspect_ratio[1]

            # 자를 폭 계산
            crop_width = int(target_ratio * height)
            if crop_width > width:
                raise ValueError(f"이미지 높이에 비해 너비가 너무 작습니다: {image_path}")

            # 단계 크기 및 겹침 계산
            step_size = width / num_crops
            overlap = crop_width - step_size

            # 픽셀 단위로 반올림
            step_size = int(round(step_size))
            crop_width = int(round(crop_width))
            overlap = int(round(overlap))

            crops = []
            for i in range(num_crops):
                left = (i * step_size) % width
                right = left + crop_width

                if right <= width:
                    crop = img.crop((left, 0, right, height))
                else:
                    # 이미지의 끝을 넘어갈 경우, 반대편에서 이어붙임
                    right = right - width
                    crop_part1 = img.crop((left, 0, width, height))
                    crop_part2 = img.crop((0, 0, right, height))
                    crop = Image.new('RGB', (crop_width, height))
                    crop.paste(crop_part1, (0,0))
                    crop.paste(crop_part2, (crop_part1.width, 0))
                
                crops.append(crop)

            # 저장
            base_name, ext = os.path.splitext(os.path.basename(image_path))
            for idx, crop_img in enumerate(crops):
                output_filename = f"{base_name}_{idx+1:03d}{ext}"
                output_path = os.path.join('images', output_filename)
                crop_img.save(output_path)
                print(f"저장됨: {output_path}")

    except Exception as e:
        print(f"{image_path} 처리 중 오류 발생: {e}")

def select_image():
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우 숨기기
    file_path = filedialog.askopenfilename(
        title="파노라마로 자를 이미지를 선택하세요",
        filetypes=[("이미지 파일", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif *.jfif")]
    )
    return file_path

def main():
    create_images_folder()
    image_path = select_image()
    
    if not image_path:
        print("이미지 선택이 취소되었습니다.")
        sys.exit()

    print(f"선택된 이미지: {image_path}")
    crop_panorama(image_path)

if __name__ == "__main__":
    main()
