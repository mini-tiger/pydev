import boto3
from botocore.client import Config

# 输入访问密钥和密钥
access_key = 'GSOTWLJWMVNRYWYMS84L'
secret_key = 'f1sGVbH79EGrvjAaG3BbLxMONA4I2A7hpxqDjxf8'
endpoint_url = 'https://oss.bj.neolink.com'

# 创建 S3 客户端对象
s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key,
                  endpoint_url=endpoint_url, config=Config(signature_version='s3'))

# 生成预签名 URL
# bucket_name = 'test'
bucket_name = 'opendata'
# object_key = 'image.png'
object_key = 'CityScapes/gtFine_trainvaltest.zip'

expiration = 315532800  # URL 的有效期限（以秒为单位）
url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_key}, ExpiresIn=expiration)

print("预签名 URL：", url)
