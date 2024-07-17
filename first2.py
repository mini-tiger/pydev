import requests

# Keycloak 服务器 URL 和管理员账户信息
KEYCLOAK_SERVER_URL = "http://120.133.63.166:8080/"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"
REALM_NAME = "demo2"
USER_USERNAME = "newuser"
TARGET_ROLE_NAME = "query"

def get_admin_token():
    data = {
        "client_id": "admin-cli",
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD,
        "grant_type": "password"
    }
    response = requests.post(f"{KEYCLOAK_SERVER_URL}realms/master/protocol/openid-connect/token", data=data)
    response.raise_for_status()
    return response.json()["access_token"]

admin_token = get_admin_token()

def get_user_id(token, realm_name, username):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/users", headers=headers, params={"username": username})
    response.raise_for_status()
    users = response.json()
    if users:
        return users[0]["id"]
    raise Exception(f"User '{username}' not found")

user_id = get_user_id(admin_token, REALM_NAME, USER_USERNAME)

def get_all_clients(token, realm_name):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/clients", headers=headers)
    response.raise_for_status()
    return response.json()

def get_user_client_roles(token, realm_name, user_id, client_id):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}admin/realms/{realm_name}/users/{user_id}/role-mappings/clients/{client_id}", headers=headers)
    response.raise_for_status()
    return response.json()

def find_clients_with_role(token, realm_name, user_id, target_role_name):
    clients_with_role = []
    all_clients = get_all_clients(token, realm_name)
    for client in all_clients:
        client_id = client["id"]
        client_roles = get_user_client_roles(token, realm_name, user_id, client_id)
        for role in client_roles:
            if role["name"] == target_role_name:
                clients_with_role.append(client["clientId"])
                break
    return clients_with_role

clients_with_query_role = find_clients_with_role(admin_token, REALM_NAME, user_id, TARGET_ROLE_NAME)

print(f"User '{USER_USERNAME}' has the role '{TARGET_ROLE_NAME}' on the following clients: {clients_with_query_role}")
