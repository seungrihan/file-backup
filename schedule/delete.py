import os
from .move import get_current_directory_data

def delete_oldest_backup_file(current_directory):
    # 현재 디렉토리에서 백업 ZIP 파일들을 가져온다.
    file_count = 2
    
    backup_files = get_current_directory_data(current_directory)

    # 폴더 이름을 기준으로 오름차순으로 정렬한다.
    sorted_files = sorted(backup_files)

    # 파일이 2개 이상이면 가장 오래된 파일을 삭제한다.
    if len(sorted_files) > file_count:
        oldest_file = sorted_files[0]
        oldest_file_path = os.path.join(current_directory, oldest_file)
        print(f"Deleted the oldest file: {oldest_file}")
        print(f"Deleted the oldest file: {oldest_file_path}")
        os.remove(oldest_file_path)
    else:
        print("No folders to delete.")
