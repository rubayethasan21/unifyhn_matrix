import requests

#domain_name ="localhost" #local
domain_name ="unifyhn.de" #remote
#domain_name ="85.215.118.180" #remote

# Synapse server details
server_url = "http://"+domain_name+":8081"



if domain_name == "localhost":
    shared_secret = "SP;j&7cAKeqqjtQS2fk1W#ejuiT:G&uaggV&E,;g8Mx:1Xl#^X"  # local
else:
    shared_secret = ",D+V@s@p&eIjPy0Cp89=7*43_w;cUXOYIJ8e:6=U3rcM0:IUdw"  # remote 1

# Admin credentials
admin_username = "admin"  # Admin username
admin_password = "12345"  # Admin password

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

# Step 3: Deactivate a user by user_id
def deactivate_user(access_token, user_id):
    url = f"{server_url}/_synapse/admin/v1/deactivate/{user_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        print(f"User {user_id} deactivated successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error deactivating user {user_id}: {e}")

# Step 4: Erase a user by user_id (using the correct purge URL)
def erase_user(access_token, user_id):
    url = f"{server_url}/_synapse/admin/v1/users/{user_id}/erase"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers)  # Corrected to POST request
        response.raise_for_status()
        print(f"User {user_id} erased successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error erasing user {user_id}: {e}")

# Step 5: Main function to delete all users except the admin
def delete_all_users_except_admin(admin_username, admin_password):
    access_token = login_as_admin(admin_username, admin_password)

    users = get_all_users(access_token)
    if not users:
        print("No users found to delete.")
        return

    for user in users:
        user_id = user["name"]
        if user_id != f"@{admin_username}:"+domain_name:  # Avoid deleting the admin user
            print(f"Deleting user: {user_id}")
            deactivate_user(access_token, user_id)  # Step 3: Deactivate the user first
            #erase_user(access_token, user_id)  # Step 4: Erase the user after deactivation
        else:
            print(f"Skipping admin user: {user_id}")

if __name__ == "__main__":
    delete_all_users_except_admin(admin_username, admin_password)
