import zipfile
import subprocess
import os

# 압축 해제할 zip 파일 경로와 압축 해제할 디렉토리 설정
zip_file_path = r"D:\다운로드\miui_HOUJIEEAGlobal_OS1.0.21.0.UNCEUXM_4be0482345_14.0.zip"
extracted_folder = r"D:\다운로드\extracted_files"
iso_output_path = r"D:\다운로드\output.iso"

# 압축 해제
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extracted_folder)

# mkisofs 명령어 실행
def create_iso(source_folder, output_iso):
    result = subprocess.run(
        ["mkisofs", "-o", output_iso, "-b", "boot.img", "-c", "boot.catalog", 
         "-no-emul-boot", "-boot-load-size", "4", "-boot-info-table", source_folder],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout, result.stderr

# ISO 이미지 생성
stdout, stderr = create_iso(extracted_folder, iso_output_path)

# 출력 및 오류 메시지 출력
print(stdout)
print(stderr)
