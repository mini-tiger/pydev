import sys
import time
import requests
import os

# Keycloak server details
KEYCLOAK_SERVER_URL="http://120.133.63.166:8080"
REALM_NAME="fastgpt"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="password"
CLIENT_ID="login"
CLIENT_SECRET="A8w8cXHLfJJ8kwiSPKck7vmaU211uCG6"

username_to_check = 'root'  # 要检查的用户名
password_to_check = '1234'  # 要检查的密码
# 获取管理员访问令牌
def get_admin_token():
    token_url = f'{KEYCLOAK_SERVER_URL}/realms/master/protocol/openid-connect/token'
    token_data = {
        'username': ADMIN_USERNAME,
        'password': ADMIN_PASSWORD,
        'grant_type': 'password',
        'client_id': 'admin-cli'
    }

    response = requests.post(token_url, data=token_data)
    response.raise_for_status()
    return response.json()['access_token']

# 检查用户名是否存在
def check_user_exists(token, username):
    users_url = f'{KEYCLOAK_SERVER_URL}/admin/realms/{REALM_NAME}/users'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'username': username}

    response = requests.get(users_url, headers=headers, params=params)
    response.raise_for_status()
    users = response.json()
    return len(users) > 0

# 验证用户名和密码
def validate_user_credentials(username, password):
    oauth_token_url = f'{KEYCLOAK_SERVER_URL}/realms/{REALM_NAME}/protocol/openid-connect/token'
    oauth_token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'password',
        'username': username,
        'password': password
    }

    response = requests.post(oauth_token_url, data=oauth_token_data)
    if response.status_code == 200:
        res = response.json()
        return True, res['access_token'], res['refresh_token'], res['expires_in']
    else:
        return False, None, None, None

if __name__ == "__main__":


    # 获取管理员访问令牌
    admin_token = get_admin_token()

    # 检查用户名是否存在
    if check_user_exists(admin_token, username_to_check):
        print(f'Username "{username_to_check}" exists.')

        # 验证用户名和密码
        valid, access_token, refresh_token, expires_in = validate_user_credentials(username_to_check, password_to_check)
        if valid:
            print('Username and password are correct.')
            print('Access token:', access_token)
            print('Refresh token:', refresh_token)
            print('Access token expires in:', expires_in, 'seconds')

            # Decode the token to get the expiration time
            access_token_expiry = time.time() + expires_in
            print('Access token will expire at:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(access_token_expiry)))

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
        else:
            print('Username and password are incorrect.')
    else:
        print(f'Username "{username_to_check}" does not exist.')
