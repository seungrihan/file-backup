import os

def delete_oldest_backup_file(current_directory):
    # 현재 디렉토리의 모든 파일과 폴더를 가져온다.
    contents = os.listdir(current_directory)
    file_count = 2

    # "backup_YYYYMMDD.zip" 형식과 일치하는 폴더만 필터링한다.
    backup_files = [
        files for files in contents if files.startswith("backup_") and files.endswith(".zip")
    ]

    # 폴더 이름을 기준으로 오름차순으로 정렬한다.
    sorted_files = sorted(backup_files)

    # 파일이 2개 이상이면 가장 오래된 파일을 삭제한다.
    if len(sorted_files) > file_count:
        oldest_file = sorted_files[0]
        oldest_file_path = os.path.join(current_directory, oldest_file)
        print(f"Deleted the oldest folder: {oldest_file}")
        print(f"Deleted the oldest folder: {oldest_file_path}")
        os.remove(oldest_file_path)
    else:
        print("No folders to delete.")
