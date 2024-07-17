from keycloak import KeycloakAdmin


# xxx pip install python-keycloak===2.16.6 对应 keycloak v18.0.2
# Keycloak服务器URL和管理员账号信息
KEYCLOAK_SERVER_URL = "http://localhost:8080"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"
REALM_NAME = "demo1"
NEW_USER_USERNAME = "newuser"
NEW_USER_PASSWORD = "password123"
NEW_USER_EMAIL = "newuser@example.com"

# 初始化Keycloak Admin客户端
from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection


keycloak_connection = KeycloakOpenIDConnection(
                        server_url="http://120.133.63.166:8080/",
                        username='admin',
                        password='password',
                        realm_name="demo1",
                        # user_realm_name="only_if_other_realm_than_master",
                        client_id="admin-cli",
                        client_secret_key="TXYfcd8qGCFCTdc4ZNpM3s7m5GuAKOOU",
                        verify=True)

keycloak_admin = KeycloakAdmin(connection=keycloak_connection)

# 创建新的realm
# keycloak_admin.create_realm({"realm": REALM_NAME, "enabled": True})

# 在新的realm中创建用户
user_id = keycloak_admin.create_user({
    "username": NEW_USER_USERNAME,
    "email": NEW_USER_EMAIL,
    "firstName": "New",
    "lastName": "User",
    "enabled": True,
    "credentials": [{
        "type": "password",
        "value": NEW_USER_PASSWORD,
        "temporary": False
    }]
})

# 获取realm-management客户端ID
clients = keycloak_admin.get_clients()
realm_management_client = next(client for client in clients if client["clientId"] == "realm-management")
realm_management_client_id = realm_management_client["id"]

# 获取realm-admin角色ID
roles = keycloak_admin.get_client_roles(client_id=realm_management_client_id, realm_name=REALM_NAME)
realm_admin_role = next(role for role in roles if role["name"] == "realm-admin")

# 为用户分配realm-admin角色
keycloak_admin.assign_client_role(client_id=realm_management_client_id, user_id=user_id, roles=[{
    "id": realm_admin_role["id"],
    "name": realm_admin_role["name"]
}], realm_name=REALM_NAME)

print(f"User {NEW_USER_USERNAME} with admin role created in realm {REALM_NAME}")
