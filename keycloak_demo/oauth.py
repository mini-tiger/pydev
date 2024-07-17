import sys
import time
import requests

# Keycloak server details
keycloak_server = 'http://120.133.63.166:8080'
realm_name = 'fastgpt'
admin_username = 'admin'
admin_password = 'password'
CLIENT_ID = "login"
CLIENT_SECRET = "A8w8cXHLfJJ8kwiSPKck7vmaU211uCG6"

# 获取 OAuth token
oauth_token_url = f'{keycloak_server}/realms/{realm_name}/protocol/openid-connect/token'
oauth_token_data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'password',
    'username': 'root',
    'password': '1234'
}

response = requests.post(oauth_token_url, data=oauth_token_data)
try:
    response.raise_for_status()
    res = response.json()
    access_token = res['access_token']
    refresh_token = res['refresh_token']
    expires_in = res['expires_in']

    print('Access token:', access_token)
    print('Refresh token:', refresh_token)
    print('Access token expires in:', expires_in, 'seconds')

    # Decode the token to get the expiration time
    access_token_expiry = time.time() + expires_in
    print('Access token will expire at:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(access_token_expiry)))

except requests.exceptions.HTTPError as err:
    print(err)
    print(response.text)
    sys.exit(1)

# 等待几秒
wait_time = 5
print(f'Waiting for {wait_time} seconds...')
time.sleep(wait_time)

# 刷新 OAuth token
refresh_token_data = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'grant_type': 'refresh_token',
    'refresh_token': refresh_token
}

response = requests.post(oauth_token_url, data=refresh_token_data)
try:
    response.raise_for_status()
    res = response.json()
    new_access_token = res['access_token']
    new_refresh_token = res['refresh_token']
    new_expires_in = res['expires_in']

    print('New access token:', new_access_token)
    print('New refresh token:', new_refresh_token)
    print('New access token expires in:', new_expires_in, 'seconds')

    # Decode the new token to get the new expiration time
    new_access_token_expiry = time.time() + new_expires_in
    print('New access token will expire at:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(new_access_token_expiry)))

    # 比较两个过期时间
    if new_access_token_expiry > access_token_expiry:
        print('Token expiration time has been extended.')
    else:
        print('Token expiration time has not changed.')

except requests.exceptions.HTTPError as err:
    print(err)
    print(response.text)
    sys.exit(1)
