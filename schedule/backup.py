import os
import datetime
import shutil
import zipfile
from tqdm import tqdm

def backup_directory(source_dir, current_directory, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = []

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_dir = os.path.join(current_directory, f"backup_{timestamp}")
    backup_file = os.path.join(current_directory, f"backup_{timestamp}.zip")

    try:
        # 복사 대상 파일 목록 수집 및 크기 계산
        file_list = []
        total_size = 0
        for root, dirs, files in os.walk(source_dir):
            # 제외할 디렉토리를 현재 디렉토리에서 제거
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                file_list.append((file_path, file_size))
                total_size += file_size

        # 복사
        with tqdm(total=total_size, unit="B", unit_scale=True, desc="Copying files") as copy_progress:
            for file_path, file_size in file_list:
                rel_path = os.path.relpath(file_path, source_dir)
                dest_path = os.path.join(dest_dir, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(file_path, dest_path)
                copy_progress.update(file_size)

        # 압축 대상 목록
        zip_file_list = []
        zip_total_size = 0
        for root, _, files in os.walk(dest_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                zip_file_list.append((file_path, file_size))
                zip_total_size += file_size

        # 압축
        with zipfile.ZipFile(backup_file, "w", zipfile.ZIP_DEFLATED) as zipf, \
             tqdm(total=zip_total_size, unit="B", unit_scale=True, desc="Compressing files") as zip_progress:
            for file_path, file_size in zip_file_list:
                arcname = os.path.relpath(file_path, dest_dir)
                zipf.write(file_path, arcname)
                zip_progress.update(file_size)

    except Exception as e:
        print(f"Directory backup failed. Error: {e}")

    finally:
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
