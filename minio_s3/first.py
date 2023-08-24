import boto3

# 设置 MinIO 客户端
s3_client = boto3.client(
    "s3",
    endpoint_url="http://172.22.50.25:31088",
    aws_access_key_id="b2zej0nMVpF7wp7D",
    aws_secret_access_key="yugGrDYOvMbwOtfT8udo8oGRLdZdjQtW",
)

bucket_name = "tttt"

# 获取存储桶中的文件列表
try:
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    for obj in response.get("Contents", []):
        print(obj["Key"])  # 打印文件名
except Exception as e:
    print(e)
