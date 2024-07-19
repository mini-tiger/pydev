import ftplib
import os
import mysql.connector


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
    query = "SELECT REPLACE(filepath, 'upload', 'OA') AS replaced_filepath, filename FROM v_business_report"
    cursor.execute(query)

    # Fetch all results and store in a dictionary
    file_info = {}
    for replaced_filepath, filename in cursor.fetchall():
        file_info[replaced_filepath] = filename

    cursor.close()
    conn.close()

    return file_info

def download_file_exec(ftp,root_dir,local_file_name,remote_file_path):
    try:
        # Determine local file path
        local_file_path = os.path.join(local_base_dir, local_file_name)
        # Create local directory if it doesn't exist
        os.makedirs(local_base_dir, exist_ok=True)

        # Change to the directory containing the file on FTP server
        remote_dir = os.path.dirname(remote_file_path)
        remote_file = os.path.basename(remote_file_path)
        ftp.cwd(root_dir)
        if remote_dir:
            ftp.cwd(remote_dir)

        # Download the file
        with open(local_file_path, 'wb') as local_file:
            ftp.retrbinary(f"RETR {remote_file}", local_file.write)
        print(f"File downloaded successfully: {local_file_path}")
    except Exception as e:
        print(f"File downloaded error:{str(e)}: {local_file_path}")
def download_files(ftp_server, username, password, file_info, local_base_dir):
    try:
        # Connect to the FTP server
        ftp = ftplib.FTP(ftp_server)
        ftp.login(user=username, passwd=password)
        print(f"Connected to FTP server: {ftp_server}")
        # Save the root directory
        root_dir = ftp.pwd()
        for remote_file_path, local_file_name in file_info.items():
            download_file_exec(ftp,root_dir,local_file_name,remote_file_path)
        # Close the FTP connection
        ftp.quit()
    except ftplib.all_errors as e:
        print(f"FTP error: {e}")


# Main script
ftp_server = '172.21.10.227'
username = 'ciecc_ai'
password = 'ciecc2024'
local_base_dir = 'download'

# Fetch file paths from the database
file_info = fetch_filepaths_from_db()
print(file_info)
# Download files from FTP
download_files(ftp_server, username, password, file_info, local_base_dir)
