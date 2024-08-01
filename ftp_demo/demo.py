import ftplib
import os
import shutil
import mysql.connector
import csv

current_directory = os.path.dirname(__file__)

def clear_download_directory_and_csv(local_base_dir):
    # 清空下载目录
    if os.path.exists(local_base_dir):
        shutil.rmtree(local_base_dir)
    os.makedirs(local_base_dir, exist_ok=True)
    
    # 删除 CSV 文件
    success_csv_path = os.path.join(current_directory, 'download_success_records.csv')
    failure_csv_path = os.path.join(current_directory, 'download_failure_records.csv')
    
    if os.path.exists(success_csv_path):
        os.remove(success_csv_path)
    if os.path.exists(failure_csv_path):
        os.remove(failure_csv_path)

def fetch_filepaths_from_db():
    # Database connection
    conn = mysql.connector.connect(
        host='172.21.10.119',
        user='root',
        password='vchat@QAZ',
        database='testdb',
        port=13306
    )
    cursor = conn.cursor()

    # Execute the query
    # query = "SELECT REPLACE(filepath, 'upload', 'OA') AS replaced_filepath, filename FROM v_business_report WHERE SUBSTRING_INDEX(SUBSTRING_INDEX(filepath, '/', -2), '/', 1) BETWEEN '2022-11' AND '2025-10';"
    query = "SELECT REPLACE(filepath, 'upload', 'OA') AS replaced_filepath, filename FROM v_business_report;"
    cursor.execute(query)

    # Fetch all results and store in a dictionary
    file_info = {}
    for replaced_filepath, filename in cursor.fetchall():
        file_info[replaced_filepath] = filename

    cursor.close()
    conn.close()

    return file_info

def truncate_filename(filename, max_bytes=255, encoding='utf-8'):
    """
    Truncate the filename if it exceeds max_bytes, preserving the extension.
    """
    if len(filename.encode(encoding)) <= max_bytes:
        return filename

    name, ext = os.path.splitext(filename)
    ext_length = len(ext.encode(encoding))
    max_name_bytes = max_bytes - ext_length

    truncated_name = ''
    current_bytes = 0

    for char in name:
        char_bytes = len(char.encode(encoding))
        if current_bytes + char_bytes > max_name_bytes:
            break
        truncated_name += char
        current_bytes += char_bytes

    return truncated_name + ext

def download_file_exec(ftp, root_dir, local_file_name, remote_file_path, local_base_dir, success_records, failure_records):
    current_directory = os.getcwd()
    try:
        os.chdir(local_base_dir)
        # Truncate local file name if too long
        local_file_name = truncate_filename(local_file_name)
        # Determine local file path
        local_file_path = os.path.join(local_base_dir, local_file_name)
        # Create local directory if it doesn't exist
        # os.makedirs(local_base_dir, exist_ok=True)

        # Change to the directory containing the file on FTP server
        remote_dir = os.path.dirname(remote_file_path)
        remote_file = os.path.basename(remote_file_path)
        ftp.cwd(root_dir)
        if remote_dir:
            ftp.cwd(remote_dir)

        # Download the file
        with open(local_file_name, 'wb') as local_file:
            ftp.retrbinary(f"RETR {remote_file}", local_file.write)
        
        # Check file size
        if os.path.getsize(local_file_name) < 1024:  # 1K = 1024 bytes
            raise ValueError("File size is less than 1K")
        
        print(f"File downloaded successfully: {remote_file_path}")
        success_records.append((remote_file_path, local_file_path))
    except Exception as e:
        print(f"File download error ({str(e)}): {remote_file_path}")
        failure_records.append((remote_file_path, local_file_path, str(e)))
         # 删除下载的文件
        if os.path.exists(local_file_name):
            os.remove(local_file_name)
    finally:
        os.chdir(current_directory)

def download_files(ftp_server, username, password, file_info, local_base_dir):
    success_records = []
    failure_records = []
    
    try:
        # Connect to the FTP server
        ftp = ftplib.FTP(ftp_server)
        ftp.login(user=username, passwd=password)
        print(f"Connected to FTP server: {ftp_server}")
        # Save the root directory
        root_dir = ftp.pwd()
        for remote_file_path, local_file_name in file_info.items():
            download_file_exec(ftp, root_dir, local_file_name, remote_file_path, local_base_dir, success_records, failure_records)
        # Close the FTP connection
        ftp.quit()
    except ftplib.all_errors as e:
        print(f"FTP error: {e}")

    # Print or save the download records
    # print("\nDownload Success Records:")
    # for remote_path, local_path in success_records:
    #     print(f"Remote: {remote_path} -> Local: {local_path}")

    # print("\nDownload Failure Records:")
    # for remote_path, local_path, error in failure_records:
    #     print(f"Remote: {remote_path} -> Local: {local_path}: {error}")

    # Save the records to CSV files
    success_csv_path = os.path.join(current_directory, 'download_success_records.csv')
    failure_csv_path = os.path.join(current_directory, 'download_failure_records.csv')

    with open(success_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Remote Path', 'Local Path'])
        writer.writerows(success_records)

    with open(failure_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Remote Path', 'Local Path', 'Error'])
        writer.writerows(failure_records)


# Main script
ftp_server = '172.21.10.227'
username = 'ciecc_ai'
password = 'ciecc2024'
local_base_dir = 'download'

# 清空下载目录并删除 CSV 文件
clear_download_directory_and_csv(local_base_dir)

# Fetch file paths from the database
file_info = fetch_filepaths_from_db()
print(file_info)
print(len(file_info.keys()))

# Download files from FTP
download_files(ftp_server, username, password, file_info, local_base_dir)
