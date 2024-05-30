import datetime
import hashlib
import hmac
import requests

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing

def upload_file_s3(url, filepath, bucket, object_name, access_key, secret_key):
    service = 's3'
    region = 'us-east-1'
    method = 'PUT'
    t = datetime.datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope

    canonical_uri = f'/{bucket}/{object_name}'
    canonical_querystring = ''
    canonical_headers = f'host:{url}\nx-amz-content-sha256:UNSIGNED-PAYLOAD\nx-amz-date:{amz_date}\n'
    signed_headers = 'host;x-amz-content-sha256;x-amz-date'
    payload_hash = 'UNSIGNED-PAYLOAD'
    canonical_request = f'{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}'

    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = f'{date_stamp}/{region}/{service}/aws4_request'
    string_to_sign = f'{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()}'

    signing_key = get_signature_key(secret_key, date_stamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

    authorization_header = (
        f'{algorithm} Credential={access_key}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}'
    )

    headers = {
        'x-amz-date': amz_date,
        'x-amz-content-sha256': payload_hash,
        'Authorization': authorization_header
    }

    with open(filepath, 'rb') as f:
        files = {'file': (object_name, f)}
        r = requests.put(f'http://{url}/{bucket}/{object_name}', data=f, headers=headers)
        print(r.text)

# 用法示例
upload_file_s3(
    url='120.133.63.166:9110',
    filepath='/data/work/pydev/minio_s3/crud.py',
    bucket='files',
    object_name='crud.py',
    access_key='dcSUnb8eHqlatvmN',
    secret_key='FnG7BAwoyGqqni0LDcWczIgRqLPx5BL3'
)
