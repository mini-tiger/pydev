import boto3

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """生成 S3 预签名 URL"""
    s3_client = boto3.client('s3',
                             endpoint_url='http://120.133.63.166:9110',  # MinIO 服务器地址
                             aws_access_key_id='dcSUnb8eHqlatvmN',      # 替换为你的 access key
                             aws_secret_access_key='FnG7BAwoyGqqni0LDcWczIgRqLPx5BL3',  # 替换为你的 secret key
                             region_name='us-east-1')                  # 使用与你的 MinIO 设置相匹配的区域

    try:
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except Exception as e:
        print(e)
        return None

    return response

# 用法示例
url = create_presigned_url('files', '/data/work/pydev/minio_s3/crud.py')
print("Presigned URL: ", url)
import requests

def upload_file(file_path, url):
    """通过预签名 URL 上传文件"""
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f)}
        response = requests.put(url, data=f)
        print(response.text)  # 打印响应内容，可以根据需要处理响应

# 用法示例
file_path = '/data/work/pydev/minio_s3/crud.py'  # 替换为你的本地文件路径
upload_file(file_path, url)
