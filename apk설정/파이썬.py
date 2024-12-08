import subprocess
import os
import shutil
import xml.etree.ElementTree as ET

def run_command(command, cwd=None, env=None):
    try:
        result = subprocess.run(
            command,
            check=True,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"명령어 실행 중 오류 발생: {e.stderr}")
        exit(1)

def decompile_apk(apk_path, output_dir, env):
    command = f"apktool d -f \"{apk_path}\" -o \"{output_dir}\""
    print("APK 디컴파일 중...")
    run_command(command, env=env)

def remove_lib_folder(apk_dir):
    lib_path = os.path.join(apk_dir, "lib")
    if os.path.exists(lib_path):
        shutil.rmtree(lib_path)
        print("lib 폴더가 성공적으로 삭제되었습니다.")
    else:
        print("lib 폴더가 존재하지 않습니다.")

def remove_other_abis(apk_dir, target_abi):
    lib_path = os.path.join(apk_dir, "lib")
    if os.path.exists(lib_path):
        for abi in os.listdir(lib_path):
            if abi != target_abi:
                abi_path = os.path.join(lib_path, abi)
                shutil.rmtree(abi_path)
                print(f"{abi} 폴더가 삭제되었습니다.")
        print(f"필요한 ABI 폴더 ({target_abi})만 남겨두었습니다.")
    else:
        print("lib 폴더가 존재하지 않습니다.")

def modify_raws_xml(apk_dir):
    raws_xml_path = os.path.join(apk_dir, "res", "values", "raws.xml")
    if os.path.exists(raws_xml_path):
        try:
            tree = ET.parse(raws_xml_path)
            root = tree.getroot()
            modified = False
            for item in root.findall('item'):
                if item.get('type') == 'raw':
                    # 변경: type을 'bool'로 수정
                    item.set('type', 'bool')
                    modified = True
            if modified:
                tree.write(raws_xml_path, encoding='utf-8', xml_declaration=True)
                print("raws.xml 파일이 성공적으로 수정되었습니다.")
            else:
                print("raws.xml 파일에 수정할 항목이 없습니다.")
        except ET.ParseError as e:
            print(f"raws.xml 파일 파싱 중 오류 발생: {e}")
            exit(1)
    else:
        print("res/values/raws.xml 파일이 존재하지 않습니다.")

def compile_apk(decompiled_dir, compiled_apk_path, env):
    command = f"apktool b \"{decompiled_dir}\" -o \"{compiled_apk_path}\""
    print("APK 재컴파일 중...")
    run_command(command, env=env)

def sign_apk(compiled_apk_path, signed_apk_path, keystore_path, alias, keystore_password, key_password, apksigner_path, env):
    command = f"\"{apksigner_path}\" sign --ks \"{keystore_path}\" --ks-pass pass:{keystore_password} --key-pass pass:{key_password} --out \"{signed_apk_path}\" \"{compiled_apk_path}\""
    print("APK 서명 중...")
    run_command(command, env=env)

def install_apk(adb_path, apk_path, env):
    command = f"\"{adb_path}\" install -r -d \"{apk_path}\""
    print("APK 설치 중...")
    run_command(command, env=env)

def main():
    # 현재 환경 복사 및 JAVA_TOOL_OPTIONS 설정
    env = os.environ.copy()
    env["JAVA_TOOL_OPTIONS"] = "-Dfile.encoding=UTF8"
    
    original_apk = r"C:\apk_tool_link\com-mod-beaker-mix-chemicals-mod-v23-unlocked-23000000.apk"
    decompiled_dir = r"C:\apk_tool_link\modified_apk"
    compiled_apk = r"C:\apk_tool_link\compiled_app.apk"
    signed_apk = r"C:\apk_tool_link\signed_modified_app.apk"
    keystore_path = r"C:\apk_tool_link\my-release-key.jks"
    alias = "my_alias"
    keystore_password = "your_keystore_password"  # 실제 키스토어 비밀번호로 변경
    key_password = "your_key_password"            # 실제 키 비밀번호로 변경
    adb_path = r"C:\Program Files (x86)\Minimal ADB and Fastboot\adb.exe"  # ADB 경로
    apksigner_path = r"C:\platform-tools\apksigner.bat"  # apksigner 경로 (환경 변수에 추가된 경우 "apksigner"로 가능)
    
    target_abi = "arm64-v8a"  # 실제 기기의 ABI로 변경
    
    # 1. APK 디컴파일
    decompile_apk(original_apk, decompiled_dir, env)
    
    # 2. lib 폴더 삭제 및 특정 ABI 유지
    remove_lib_folder(decompiled_dir)
    remove_other_abis(decompiled_dir, target_abi)
    
    # 3. raws.xml 파일 수정
    modify_raws_xml(decompiled_dir)
    
    # 4. APK 재컴파일
    compile_apk(decompiled_dir, compiled_apk, env)
    
    # 5. APK 서명
    sign_apk(compiled_apk, signed_apk, keystore_path, alias, keystore_password, key_password, apksigner_path, env)
    
    # 6. APK 설치
    install_apk(adb_path, signed_apk, env)

if __name__ == "__main__":
    main()
