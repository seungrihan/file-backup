import os
import datetime
import shutil
import zipfile
from tqdm import tqdm

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
        # 백업할 파일의 총 개수를 계산한다.
        total_files = sum([len(files) for _, _, files in os.walk(source_dir)])

        # 진행 상황을 표시하는 프로그래스바를 생성한다.
        with tqdm(total=total_files, unit="file") as progress:
            # 디렉토리를 복사한다.
            shutil.copytree(
                source_dir, dest_dir, ignore=exclude_directory, copy_function=shutil.copy2
            )
            # 진행 상황을 업데이트한다.
            progress.update(total_files)

        # 백업 폴더를 압축 파일로 만든다.
        with zipfile.ZipFile(backup_file, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dest_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 파일을 압축 파일에 추가한다.
                    zipf.write(file_path, os.path.relpath(file_path, dest_dir))

    except Exception as e:
        print(f"Directory copy failed. Error: {e}")

    finally:
        # 백업 폴더를 삭제한다.
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
