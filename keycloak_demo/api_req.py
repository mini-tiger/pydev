
import requests

keycloak_url = "http://120.133.63.166:8080"
# keycloak_url = "http://172.22.220.21:8080"
realm_name = "master"
client_id = "admin-cli"
admin_username = "admin"
admin_password = "password"

# 获取访问令牌
token_url = f"{keycloak_url}/realms/{realm_name}/protocol/openid-connect/token"
data = {
    "grant_type": "password",
    "client_id": client_id,
    "username": admin_username,
    "password": admin_password
}

response = requests.post(token_url, data=data)
try:
    response.raise_for_status()
    token = response.json()["access_token"]
except requests.exceptions.HTTPError:
    print(response.text)
print("Access Token:", token)

# 创建用户
create_user_url = f"{keycloak_url}/admin/realms/{realm_name}/users"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

user_data = {
    "username": "new_user",
    "enabled": True,
    "firstName": "First",
    "lastName": "Last",
    "email": "new_user@example.com",
    "credentials": [
        {
            "type": "password",
            "value": "new_user_password",
            "temporary": False
        }
    ]
}
response = requests.post(create_user_url, headers=headers, json=user_data)
try:

    response.raise_for_status()
    print("User created successfully.")
except requests.exceptions.HTTPError as err:
    print(err)
    print(response.content)

# 获取用户信息
get_users_url = f"{keycloak_url}/admin/realms/{realm_name}/users"
response = requests.get(get_users_url, headers=headers)
response.raise_for_status()
users = response.json()

for user in users:
    print(f"User ID: {user['id']}, Username: {user['username']}")