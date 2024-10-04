import requests
import json

#domain_name ="localhost" #local
domain_name ="85.215.118.180" #remote

# Synapse server details
server_url = "http://"+domain_name+":8081"


if domain_name == "localhost":
    admin_token = "syt_YWRtaW4_gDLlUrSzulYzGubIsdFK_16BvZV"  # local
else:
    admin_token = "syt_YWRtaW4_IUidRwSYKEDruVSBYNXn_4HVIYN"  # remote

# User credentials
user_id = "@rubayet.hasan:"+domain_name  # Replace with the user you want to reactivate
new_password = "12345"  # Set a new password for the user

# Step 1: Reactivate the user by setting 'deactivated' to 'false'
def reactivate_user(user_id, new_password):
    url = f"{server_url}/_synapse/admin/v2/users/{user_id}"
    headers = {
        "Authorization": f"Bearer {admin_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "deactivated": False,
        "password": new_password  # Provide a new password for the reactivated user
    }

    try:
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for unsuccessful requests
        print(f"User {user_id} reactivated successfully.")
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error reactivating user {user_id}: {e}")

if __name__ == "__main__":
    reactivate_user(user_id, new_password)
