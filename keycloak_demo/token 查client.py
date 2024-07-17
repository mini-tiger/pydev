import sys

import requests

# Keycloak server details
KEYCLOAK_SERVER_URL = 'http://120.133.63.166:8080'
REALM_NAME = 'fastgpt'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'
CLIENT_ID = 'login'
CLIENT_SECRET = 'A8w8cXHLfJJ8kwiSPKck7vmaU211uCG6'
username='tao'
password='1234'
client_role = "pass"

def get_oauth_token():
    oauth_token_url = f'{KEYCLOAK_SERVER_URL}/realms/{REALM_NAME}/protocol/openid-connect/token'
    oauth_token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'password',
        # 'username': new_user['username'],
        # 'password': new_password
        'username': username,
        'password': password
    }

    response = requests.post(oauth_token_url, data=oauth_token_data)
    try:
        response.raise_for_status()
        res = response.json()
        # print(res)
        oauth_token = res['access_token']
        print(oauth_token)
        return oauth_token
    except requests.exceptions.HTTPError as err:
        # print(err)
        print(response.text)
        sys.exit(1)

def get_admin_token():
    token_url = f'{KEYCLOAK_SERVER_URL}/realms/master/protocol/openid-connect/token'
    token_data = {
        'client_id': 'admin-cli',
        'username': ADMIN_USERNAME,
        'password': ADMIN_PASSWORD,
        'grant_type': 'password'
    }
    response = requests.post(token_url, data=token_data)
    response.raise_for_status()
    return response.json()['access_token']

def get_user_info(oauth_token):
    userinfo_url = f'{KEYCLOAK_SERVER_URL}/realms/{REALM_NAME}/protocol/openid-connect/userinfo'
    headers = {'Authorization': f'Bearer {oauth_token}'}

    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_user_id(token, username):
    users_url = f'{KEYCLOAK_SERVER_URL}/admin/realms/{REALM_NAME}/users'
    headers = {'Authorization': f'Bearer {token}'}
    params = {'username': username}

    response = requests.get(users_url, headers=headers, params=params)
    response.raise_for_status()
    users = response.json()
    if not users:
        raise ValueError(f'User {username} not found')
    return users[0]['id']

def get_clients(token):
    clients_url = f'{KEYCLOAK_SERVER_URL}/admin/realms/{REALM_NAME}/clients'
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(clients_url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_client_roles(token, client_id):
    roles_url = f'{KEYCLOAK_SERVER_URL}/admin/realms/{REALM_NAME}/clients/{client_id}/roles'
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(roles_url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_user_client_roles(token, user_id, client_id):
    roles_url = f'{KEYCLOAK_SERVER_URL}/admin/realms/{REALM_NAME}/users/{user_id}/role-mappings/clients/{client_id}'
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(roles_url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_clients_with_role(admin_token, user_id, client_role):
    clients = get_clients(admin_token)
    client_ids_with_role = []

    for client in clients:
        client_id = client['id']
        client_roles = get_client_roles(admin_token, client_id)

        # Check if specified role exists in the client
        specified_role = next((role for role in client_roles if role['name'] == client_role), None)
        if specified_role:
            # Check if user has the specified role in this client
            user_roles = get_user_client_roles(admin_token, user_id, client_id)
            if any(role['id'] == specified_role['id'] for role in user_roles):
                client_ids_with_role.append(client['clientId'])

    return client_ids_with_role
def main():
    # User token
    oauth_token = get_oauth_token()
    # Get user info from the OAuth token
    user_info = get_user_info(oauth_token)
    username = user_info['preferred_username']

    # Get admin token
    admin_token = get_admin_token()
    print(username)
    # Get user ID
    user_id = get_user_id(admin_token, username)

    # Get all clients
    clients = get_clients(admin_token)

    # Get client IDs where the user has the specified role
    client_ids_with_role = get_clients_with_role(admin_token, user_id, client_role)

    print(f"User {username} has the '{client_role}' role in the following clients: {client_ids_with_role}")

if __name__ == "__main__":
    main()
