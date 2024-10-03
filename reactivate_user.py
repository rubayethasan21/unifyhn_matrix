import requests
import json

# Synapse server details
server_url = "http://localhost:8080"  # Update if using a different server URL
#admin_token = "syt_YWRtaW4_gDLlUrSzulYzGubIsdFK_16BvZV"  # local
admin_token = "syt_YWRtaW4_wBrVxgtcuwfqixPGwQWS_3qUMJc"  # remote

# User credentials
user_id = "@alexander.jesser:localhost"  # Replace with the user you want to reactivate
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
