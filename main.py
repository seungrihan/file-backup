from schedule import *

def main():
    source_directory = "../study"
    destination_directory = "/Users/seungrihan/Google Drive/내 드라이브/Backup"
    current_directory = os.getcwd()
    backup_directory(source_directory, current_directory, exclude_dirs=["node_modules"])
    move_zip_files(current_directory, destination_directory)
    delete_oldest_backup_file(destination_directory)
    

if __name__ == "__main__":
    main()
