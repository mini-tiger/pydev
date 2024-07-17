import sys

import requests

# Keycloak server details
import requests
import os
import sys

KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", "http://120.133.63.166:8080")
REALM_NAME = os.getenv("REALM_NAME", "fastgpt")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password")
CLIENT_ID = os.getenv("CLIENT_ID", "login")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "A8w8cXHLfJJ8kwiSPKck7vmaU211uCG6")

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

def client_exists(token, realm_name, client_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}/admin/realms/{realm_name}/clients", headers=headers)
    response.raise_for_status()
    clients = response.json()
    return next((client for client in clients if client["clientId"] == client_id), None)

def create_client(token, realm_name, client_id):
    client = client_exists(token, realm_name, client_id)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    if not client:
        data = {
            "clientId": client_id,
            "enabled": True,
            "protocol": "openid-connect",
            "publicClient": False,
            "redirectUris": ["http://localhost:3000/*"],
            "webOrigins": ["*"],
            "secret": CLIENT_SECRET
        }
        response = requests.post(f"{KEYCLOAK_SERVER_URL}/admin/realms/{realm_name}/clients", json=data, headers=headers)
        response.raise_for_status()
        print(f"Client '{client_id}' created in realm '{realm_name}'.")
        return response.json()
    else:
        print(f"Client '{client_id}' already exists in realm '{realm_name}'. Updating existing client.")
        client_id = client['id']
        response = requests.put(f"{KEYCLOAK_SERVER_URL}/admin/realms/{realm_name}/clients/{client_id}", json=client, headers=headers)
        response.raise_for_status()
        return client

def role_exists(token, realm_name, client_id, role_name):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}/admin/realms/{realm_name}/clients/{client_id}/roles", headers=headers)
    response.raise_for_status()
    roles = response.json()
    return next((role for role in roles if role["name"] == role_name), None)

def create_role(token, realm_name, client_id, role_name):
    role = role_exists(token, realm_name, client_id, role_name)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    if not role:
        data = {
            "name": role_name,
            "clientRole": True
        }
        response = requests.post(f"{KEYCLOAK_SERVER_URL}/admin/realms/{realm_name}/clients/{client_id}/roles", json=data, headers=headers)
        response.raise_for_status()
        print(f"Role '{role_name}' created in client '{client_id}'.")
        return response.text
    else:
        print(f"Role '{role_name}' already exists in client '{client_id}'.")
        return role

def user_exists(token, realm_name, username):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{KEYCLOAK_SERVER_URL}/admin/realms/{realm_name}/users", headers=headers, params={"username": username})
    response.raise_for_status()
    users = response.json()
    return next((user for user in users if user["username"] == username), None)

def create_user(token, realm_name, username, password):
    user = user_exists(token, realm_name, username)
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    if not user:
        data = {
            "username": username,
            "enabled": True,
            "credentials": [{"type": "password", "value": password, "temporary": False}]
        }
        response = requests.post(f"{KEYCLOAK_SERVER_URL}/admin/realms/{realm_name}/users", json=data, headers=headers)
        response.raise_for_status()
        print(f"User '{username}' created in realm '{realm_name}'.")
        return response
    else:
        print(f"User '{username}' already exists in realm '{realm_name}'. Updating existing user.")
        user_id = user['id']
        response = requests.put(f"{KEYCLOAK_SERVER_URL}/admin/realms/{realm_name}/users/{user_id}", json=user, headers=headers)
        response.raise_for_status()
        return user

def assign_role_to_user(token, realm_name, user_id, client_id, role_name):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    roles_url = f"{KEYCLOAK_SERVER_URL}/admin/realms/{realm_name}/users/{user_id}/role-mappings/clients/{client_id}"
    role = role_exists(token, realm_name, client_id, role_name)
    if role:
        data = [role]
        response = requests.post(roles_url, json=data, headers=headers)
        response.raise_for_status()
        print(f"Role '{role_name}' assigned to user '{user_id}'.")




if __name__ == "__main__":
    token = get_admin_token()
    client = create_client(token, REALM_NAME, CLIENT_ID)
    client_id = client['id']
    role = create_role(token, REALM_NAME, client_id, "pass")
    user = create_user(token, REALM_NAME, "tao", "1234")
    user_id = user['id']
    assign_role_to_user(token, REALM_NAME, user_id, client_id, "pass")


    # Step 5: Get OAuth token
    oauth_token_url = f'{KEYCLOAK_SERVER_URL}/realms/{REALM_NAME}/protocol/openid-connect/token'
    oauth_token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'password',
        # 'username': new_user['username'],
        # 'password': new_password
        'username': 'root',
        'password': '1234'
    }

    response = requests.post(oauth_token_url, data=oauth_token_data)
    try:
        response.raise_for_status()
        res = response.json()
        print(res)
        oauth_token = res['access_token']

        print(oauth_token)
    except requests.exceptions.HTTPError as err:
        print(err)
        print(response.text)
        sys.exit(1)

    # Step 6: Get userinfo with token
    # Function to get user access token
    def get_user_info(token):
        userinfo_url = f'{KEYCLOAK_SERVER_URL}/realms/{REALM_NAME}/protocol/openid-connect/userinfo'
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        return response.json()

    print(get_user_info(oauth_token))