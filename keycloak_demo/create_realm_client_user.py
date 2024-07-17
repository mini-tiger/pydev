import requests
from urllib import parse
# Keycloak 服务器 URL 和管理员账户信息
KEYCLOAK_SERVER_URL = "http://120.133.63.166:8080/"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

REALM_NAME = "fastgpt"
CLIENT_ID = "login"
USER_USERNAME = "root"
USER_PASSWORD = "1234"
USER_EMAIL = "root@keycloak.com"

# 获取管理员令牌
def get_admin_token():
    data = {
        "client_id": "admin-cli",
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD,
        "grant_type": "password"
    }
    response = requests.post(parse.urljoin(KEYCLOAK_SERVER_URL,"realms/master/protocol/openid-connect/token"), data=data)
    response.raise_for_status()
    return response.json()["access_token"]

admin_token = get_admin_token()
print(admin_token)

# 创建新的 realm
# 检查 realm 是否存在
def realm_exists(token, realm_name):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}admin/realms", headers=headers)
    response.raise_for_status()
    realms = response.json()
    return any(realm["realm"] == realm_name for realm in realms)
def update_realm_ssl(token, realm_name):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        'sslRequired': 'none',
        'enabled': True,
        'ssoSessionIdleTimeout': 86400,  # SSO Session Idle Timeout in seconds (e.g., 1 day)
        'ssoSessionMaxLifespan': 86400,
        'accessTokenLifespan': 3600      # Access Token Lifespan in seconds (e.g., 60 minutes)
    }
    realm_url = f'{KEYCLOAK_SERVER_URL}/admin/realms/{realm_name}'
    response = requests.put(realm_url, json=data, headers=headers)
    print(response.text)
    response.raise_for_status()
    return response
# 创建新的 realm（如果不存在）
def create_realm(token, realm_name):
    if not realm_exists(token, realm_name):
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"realm": realm_name, "enabled": True}
        response = requests.post(f"{KEYCLOAK_SERVER_URL}admin/realms", json=data, headers=headers)
        response.raise_for_status()
        print(f"Realm '{realm_name}' created.")
    else:
        update_realm_ssl(token,realm_name)
        print(f"Realm '{realm_name}' already exists.")


create_realm(admin_token, REALM_NAME)

# 创建新的 client
# 检查 client 是否存在
def client_exists(token, realm_name, client_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/clients", headers=headers)
    response.raise_for_status()
    clients = response.json()
    return any(client["clientId"] == client_id for client in clients)

# 创建新的 client（如果不存在）
def create_client(token, realm_name, client_id):
    if not client_exists(token, realm_name, client_id):
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {
            "clientId": client_id,
            "enabled": True,
            "protocol": "openid-connect",
            "publicClient": True,
            "redirectUris": ["http://localhost:3000/*"],
            "webOrigins": ["*"]
        }
        response = requests.post(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/clients", json=data, headers=headers)
        response.raise_for_status()
        print(f"Client '{client_id}' created in realm '{realm_name}'.")
    else:
        print(f"Client '{client_id}' already exists in realm '{realm_name}'.")

create_client(admin_token, REALM_NAME, CLIENT_ID)

# 创建新的用户
def user_exists(token, realm_name, username):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/users", headers=headers)
    response.raise_for_status()
    users = response.json()
    return any(user["username"] == username for user in users)

# 创建新的 user（如果不存在）
def create_user(token, realm_name, username, email, password):
    if not user_exists(token, realm_name, username):
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {
            "username": username,
            "email": email,
            "firstName": "New",
            "lastName": "User",
            "enabled": True,
            "credentials": [{"type": "password", "value": password, "temporary": False}]
        }
        response = requests.post(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/users", json=data, headers=headers)
        response.raise_for_status()
        user_id = response.headers["Location"].split("/")[-1]
        print(f"User '{username}' created in realm '{realm_name}'.")
        return user_id
    else:
        print(f"User '{username}' already exists in realm '{realm_name}'.")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/users", headers=headers, params={"username": username})
        response.raise_for_status()
        users = response.json()
        return users[0]["id"]

user_id = create_user(admin_token, REALM_NAME, USER_USERNAME, USER_EMAIL, USER_PASSWORD)

# 获取 realm-management 客户端 ID
def get_realm_management_client_id(token, realm_name):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/clients", headers=headers)
    response.raise_for_status()
    clients = response.json()
    for client in clients:
        if client["clientId"] == "realm-management":
            return client["id"]
    raise Exception("realm-management client not found")

realm_management_client_id = get_realm_management_client_id(admin_token, REALM_NAME)



# 设置客户端令牌过期时间

# 获取 client-admin 角色 ID
def get_client_admin_role_id(token, realm_name, client_id):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/clients/{client_id}/roles", headers=headers)
    response.raise_for_status()
    roles = response.json()
    for role in roles:
        if role["name"] == "manage-clients":
            return role["id"]
    raise Exception("client-admin role not found")

client_admin_role_id = get_client_admin_role_id(admin_token, REALM_NAME, realm_management_client_id)

# 为用户分配 client-admin 角色
def assign_client_admin_role(token, realm_name, user_id, client_id, role_id):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = [{"id": role_id, "name": "manage-clients"}]
    response = requests.post(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/users/{user_id}/role-mappings/clients/{client_id}", json=data, headers=headers)
    response.raise_for_status()
    print(f"User '{USER_USERNAME}' assigned manage-clients role in realm '{REALM_NAME}'.")

assign_client_admin_role(admin_token, REALM_NAME, user_id, realm_management_client_id, client_admin_role_id)
