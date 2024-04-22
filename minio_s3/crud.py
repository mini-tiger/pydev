import os.path
from datetime import date
from minio import Minio
from minio.error import S3Error
import hashlib


def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class RunError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)  # 初始化父类
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


class minio_process():
    def __init__(self, access_key, secret_key, bucket_name, minio_server: str = "172.22.50.25:31088", **kwargs):
        # 配置MinIO服务器连接参数

        self.minio_client = Minio(minio_server, access_key=access_key, secret_key=secret_key, secure=False)
        self.bucket_name = bucket_name

    def generate_object_name(self, user="test", object_name=None):
        # 获取今天的日期
        today_date = date.today()
        # 格式化日期
        formatted_today = today_date.strftime('%Y-%m-%d')
        return f'{user}/{formatted_today}/{object_name}'

    def list_files_in_directory(self, prefix):
        """列出存储桶中指定目录下的所有文件和子目录"""
        try:
            # 确保前缀以斜杠结束，代表目录
            if not prefix.endswith('/'):
                prefix += '/'
            object_list = self.minio_client.list_objects(self.bucket_name, prefix=prefix, recursive=True)
            return list(object_list)
            # for obj in object_list:
            #     print(f"Object: {obj.object_name}, Size: {obj.size}")
        except S3Error as e:
            print(f"Error: {e}")
            return []

    def upload_file(self, file_path, user="test", object_name=None, valid=True):
        err = False
        err_str = None
        object_name = os.path.basename(file_path)  # 存储在MinIO上的对象名称
        minio_put_path = self.generate_object_name(object_name=object_name, user="test")
        try:
            # file_path = "path_to_your_local_file"  # 本地文件的路径
            wresult = self.minio_client.fput_object(self.bucket_name,
                                                    minio_put_path,
                                                    file_path)
            if valid:
                etag = wresult.etag
                cmd5 = calculate_md5(file_path)
                if etag != cmd5:
                    err_str = f"ETag: {etag}, neq {file_path} hash {cmd5}"
                    err = True
            print(f"File {file_path} [Minio]uploaded successfully as {object_name} to bucket {self.bucket_name}")

        except S3Error as e:
            print(f"Error: {e}")
            err_str = str(e)
            err = True
        return {"error": err, "error_str": err_str, "minio_put_path": minio_put_path, "local_file_path": file_path}
    def download_file(self, local_dir,prefix: str):
        err_str = None
        err = False
        local_file_path=''
        try:
            file_stat = self.minio_client.stat_object(self.bucket_name, prefix)
            local_file_path=os.path.join(local_dir,os.path.basename(file_stat.object_name))
            self.minio_client.fget_object(self.bucket_name, prefix, local_file_path)
            print(f"File {prefix} [Minio]downloaded successfully as {local_file_path} to bucket {self.bucket_name}")
        except S3Error as e:
            print(f"Error: {e}")
            err_str = str(e)
            err = True
        return {"error": err, "error_str": err_str, "minio_path": prefix, "local_file_path": local_file_path}

    def delete_file(self, prefix):
        err_str = None
        err = False
        """从指定存储桶中删除一个文件"""
        try:
            self.minio_client.remove_object(self.bucket_name, prefix)
            print(f"File '{prefix}' has been deleted from bucket '{self.bucket_name}'.")
        except S3Error as e:
            print(f"Error during file deletion: {e}")
            err_str = f"Error during file deletion: {e}"
            err = True
        return {"error": err, "error_str": err_str, "minio_path": prefix}

if __name__ == "__main__":
    # 1. create minio conn
    m = minio_process(access_key="6slMTVw1pbhMnwwK", secret_key="RRTDj8UfVcIG1NyIEdFgP9Bg4Y0JgD2e",
                      minio_server="172.22.220.90:31088", bucket_name="neodata")
    # 2. upload file
    upload_result = m.upload_file(file_path="/data/work/pydev/README.md")
    print(f"upload result: {upload_result}")
    # 3. get list dir
    list_files= m.list_files_in_directory(os.path.dirname(upload_result['minio_put_path']))
    print(f"File list len: {len(list_files)}")

    # 4. download file
    if not upload_result['error']:
        m.download_file(prefix=upload_result['minio_put_path'],local_dir='/data/work/pydev/面试/')

    # 4. delete file
    m.delete_file(prefix=upload_result['minio_put_path'])

    # 5. get list dir
    list_files= m.list_files_in_directory(os.path.dirname(upload_result['minio_put_path']))
    print(f"File list len: {len(list_files)}")


