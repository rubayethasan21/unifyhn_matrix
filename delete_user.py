import requests

# Synapse server details
server_url = "http://localhost:8080"  # Update if using a different server URL
#shared_secret = "SP;j&7cAKeqqjtQS2fk1W#ejuiT:G&uaggV&E,;g8Mx:1Xl#^X"  # local
shared_secret = "V3EIxdN5=J5cWv+RJ74RG#14QWpFj:O,_60Yed:+PoztoSC20X"  # remote

# Admin credentials
admin_username = "admin"  # Admin username
admin_password = "Hosting+12345"  # Admin password

# Step 1: Login as admin and get access token
def login_as_admin(username, password):
    try:
        response = requests.post(f"{server_url}/_matrix/client/r0/login", json={
            "type": "m.login.password",
            "user": username,
            "password": password
        })
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Error logging in as admin: {e}")

# Step 2: Get a list of all registered users
def get_all_users(access_token):
    url = f"{server_url}/_synapse/admin/v2/users"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get("users", [])
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Error fetching user list: {e}")

# Step 3: Delete a user by user_id
def delete_user(access_token, user_id):
    url = f"{server_url}/_synapse/admin/v1/deactivate/{user_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        print(f"User {user_id} deleted successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error deleting user {user_id}: {e}")

# Step 4: Main function to delete all users except the admin
def delete_all_users_except_admin(admin_username, admin_password):
    access_token = login_as_admin(admin_username, admin_password)

    users = get_all_users(access_token)
    if not users:
        print("No users found to delete.")
        return

    for user in users:
        user_id = user["name"]
        if user_id != f"@{admin_username}:localhost":  # Avoid deleting the admin user
            print(f"Deleting user: {user_id}")
            delete_user(access_token, user_id)
        else:
            print(f"Skipping admin user: {user_id}")

if __name__ == "__main__":
    delete_all_users_except_admin(admin_username, admin_password)
