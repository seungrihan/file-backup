import os
import datetime
import shutil
import zipfile

# "node_modules" 디렉토리를 제외하기 위한 함수
def exclude_directory(dir, contents):
    # "node_modules" 디렉토리를 제외한다.
    return ["node_modules"]


# 디렉토리를 백업하는 함수
def backup_directory(source_dir, current_directory):
    # 현재 시간을 가져와서 "YYYYMMDD" 형식으로 변환한다.
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    # 백업 폴더 경로를 생성한다.
    dest_dir = os.path.join(current_directory, f"backup_{timestamp}")
    # 백업 파일 경로를 생성한다.
    backup_file = os.path.join(current_directory, f"backup_{timestamp}.zip")

    try:
        # "exclude_node_modules" 함수를 이용하여 "source_dir" 디렉토리와 그 내용물을 "dest_dir"로 복사한다.
        shutil.copytree(source_dir, dest_dir, ignore=exclude_directory)
        print("Directory copied successfully!")

        # 백업 폴더를 압축 파일로 만든다.
        with zipfile.ZipFile(backup_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dest_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 압축 파일에 파일을 추가한다.
                    zipf.write(file_path, os.path.relpath(file_path, dest_dir))

    except Exception as e:
        print(f"Directory copy failed. Error: {e}")

    finally:
        # 임시 백업 폴더를 삭제한다.
        shutil.rmtree(dest_dir)
