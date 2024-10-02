import requests
import json

# Synapse server details
server_url = "http://localhost:8080"  # Update if using a different server URL
admin_token = "syt_YWRtaW4_gDLlUrSzulYzGubIsdFK_16BvZV"  # Replace with the admin access token


# Step 1: Fetch the list of registered users
def get_registered_users():
    # Define the URL for the admin API to list users
    url = f"{server_url}/_synapse/admin/v2/users"

    # Add the Authorization header with Bearer token
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    try:
        # Send the GET request to the server
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful

        # Parse the response as JSON
        users = response.json()

        # Print the list of users for debugging
        print(f"Total Users Found: {users['total']}")
        for user in users['users']:
            print(f"User ID: {user['name']}, Admin: {user['admin']}, Displayname: {user.get('displayname', 'N/A')}")

        # Return the users data
        return users

    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Error fetching users: {e}")


if __name__ == "__main__":
    try:
        print("Fetching the list of registered users...")
        users = get_registered_users()

    except Exception as e:
        print(f"Error: {e}")
