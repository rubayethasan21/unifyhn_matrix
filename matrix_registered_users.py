import requests
import json



#domain_name ="localhost" #local
domain_name ="unifyhn.de" #remote
#domain_name ="85.215.118.180" #remote

# Synapse server details
server_url = "http://"+domain_name+":8081"

if domain_name == "localhost":
    admin_token = "syt_YWRtaW4_BoYmJTstrEpKiJlsyiCz_0KmfUR"  # local
else:
    #admin_token = "syt_YWRtaW4_IUidRwSYKEDruVSBYNXn_4HVIYN"  # remote 1
    admin_token = "syt_YWRtaW4_pDqKemFJfJAZRxQbDrKu_28RF6a"  # remote 2



# Step 1: Fetch the list of registered users with pagination support
def get_registered_users():
    # Define the URL for the admin API to list users
    url = f"{server_url}/_synapse/admin/v2/users"

    # Add the Authorization header with Bearer token
    headers = {
        "Authorization": f"Bearer {admin_token}"
    }

    users = []  # To hold all users
    next_token = None  # Pagination token

    try:
        while True:
            # Append pagination token if available
            paginated_url = url
            if next_token:
                paginated_url += f"?from={next_token}"

            # Send the GET request to the server
            response = requests.get(paginated_url, headers=headers)
            response.raise_for_status()  # Check if the request was successful

            # Debug: Print the raw response
            print(f"Raw response: {response.content.decode()}")

            # Parse the response as JSON
            data = response.json()

            # Debug: Print the parsed JSON data
            print(f"Parsed response: {data}")

            # Add users to the list
            users.extend(data['users'])

            # Check if there is a next token (pagination)
            next_token = data.get('next_token')
            if not next_token:
                break  # Exit the loop if there are no more pages

        # Print the list of users for debugging
        print(f"Total Users Found: {len(users)}")
        for user in users:
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
