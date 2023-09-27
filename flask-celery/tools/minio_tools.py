import os.path

from minio import Minio
from minio.error import S3Error


class minio_process():
    def __init__(self, access_key, secret_key,minio_server :str="172.22.50.25:31088", **kwargs):
        # 配置MinIO服务器连接参数

        # minio_server = "172.22.50.25:31088"  # MinIO服务器的URL
        # access_key = "hlEPG0SuaiBys2Hd"  # 您的访问密钥
        # secret_key = "OiQdBT8XI1O68F6Z3QQbUJl4LzkYR3dw"  # 您的秘密密钥

        self.minio_client = Minio(minio_server, access_key=access_key, secret_key=secret_key, secure=False)

    def list_dir(self, prefix: str="middle_data/test/test_result/", bucket_name: str = "neodata"):
        # 列出存储桶中指定目录下的文件列表
        try:
            # prefix = "middle_data/"  # 指定目录的路径前缀

            objects = self.minio_client.list_objects(bucket_name, prefix=prefix)

            # print(f"Files in directory {prefix}:")
            # for obj in objects:
            #     print(f"- {obj.object_name}")
            return objects
        except S3Error as e:
            print(f"Error: {e}")
        return None
    def upload_file(self,file_path, prefix: str="middle_data/test/test_result/", bucket_name: str = "neodata"):
        try:
            #file_path = "path_to_your_local_file"  # 本地文件的路径
            object_name = os.path.basename(file_path)  # 存储在MinIO上的对象名称

            self.minio_client.fput_object(bucket_name, os.path.join(prefix,object_name), file_path)

            print(f"File {file_path} [Minio]uploaded successfully as {object_name} to bucket {bucket_name}")
        except S3Error as e:
            print(f"Error: {e}")