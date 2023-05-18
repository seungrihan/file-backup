import os
import subprocess


def move_zip_files(current_directory, destination_directory):
    # 현재 디렉토리의 모든 파일과 폴더를 가져온다.
    contents = os.listdir(current_directory)

    # "backup_YYYYMMDD.zip" 형식과 일치하는 폴더만 필터링한다.
    backup_files = [
        files for files in contents if files.startswith("backup_") and files.endswith(".zip")
    ]

    # Google Drive에 backup_YYYYMMDD.zip 파일을 업로드한다.
    for file in backup_files:
        source_path = f"{current_directory}/{file}"
        destination_path = f"{destination_directory}/{file}"
        rsync_command = [
            "rsync",
            "-av",
            "--remove-source-files",
            "--progress",
            "--stats",
            "--human-readable",
            "--log-file=rsync.log",
            source_path,
            destination_path,
        ]
        subprocess.run(rsync_command)
        print(f"Moved the file: {file}")
