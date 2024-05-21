import os
def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            os.removedirs(file_path)
        else:
            os.remove(file_path)
def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)