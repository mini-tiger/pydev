import requests
from urllib import parse
# Keycloak 服务器 URL 和管理员账户信息
KEYCLOAK_SERVER_URL = "http://120.133.63.166:8080/"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"
REALM_NAME = "demo2"
USER_USERNAME = "newuser"
CLIENT_ID = "my-client"

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

def get_user_id(token, realm_name, username):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/users", headers=headers, params={"username": username})
    response.raise_for_status()
    users = response.json()
    if users:
        return users[0]["id"]
    raise Exception(f"User '{username}' not found")

user_id = get_user_id(admin_token, REALM_NAME, USER_USERNAME)

def get_client_id(token, realm_name, client_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/clients", headers=headers, params={"clientId": client_id})
    response.raise_for_status()
    clients = response.json()
    if clients:
        return clients[0]["id"]
    raise Exception(f"Client '{client_id}' not found")

client_id = get_client_id(admin_token, REALM_NAME, CLIENT_ID)

def get_user_client_roles(token, realm_name, user_id, client_id):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/users/{user_id}/role-mappings/clients/{client_id}", headers=headers)
    response.raise_for_status()
    return response.json()

def print_user_client_roles(token, realm_name, user_id, client_id):
    client_roles = get_user_client_roles(token, realm_name, user_id, client_id)
    if not client_roles:
        print(f"User '{USER_USERNAME}' has no client roles on client '{CLIENT_ID}'.")
    else:
        role_names = [role['name'] for role in client_roles]
        print(f"User '{USER_USERNAME}' has roles {role_names} on client '{CLIENT_ID}'")

print_user_client_roles(admin_token, REALM_NAME, user_id, client_id)
