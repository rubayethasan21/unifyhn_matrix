import requests
import json

#domain_name ="localhost" #local
domain_name ="85.215.118.180" #remote

# Synapse server details
server_url = "http://"+domain_name+":8081"

# Admin user credentials (must be an admin to delete rooms)
admin_username = "admin"  # Replace with actual admin username
admin_password = "12345"  # Replace with actual admin password

# Step 1: Admin login to the Matrix server to obtain access token
def admin_login(username, password):
    url = f"{server_url}/_matrix/client/r0/login"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "type": "m.login.password",
        "user": username,
        "password": password
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        access_token = response.json().get("access_token")
        user_id = response.json().get("user_id")
        print(f"Login successful for {user_id}")
        return access_token, user_id
    except requests.RequestException as e:
        print(f"Error logging in: {e}")
        return None, None

# Step 2: Get a list of all rooms on the server (Admin API)
def get_all_rooms(access_token):
    url = f"{server_url}/_synapse/admin/v1/rooms"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        rooms = response.json().get("rooms", [])
        print(f"All rooms on the server: {rooms}")
        return rooms
    except requests.RequestException as e:
        print(f"Error fetching rooms: {e}")
        return []

# Step 3: Delete a room as admin
def delete_room_as_admin(access_token, room_id):
    url = f"{server_url}/_synapse/admin/v1/rooms/{room_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "purge": True  # Purge the room data entirely
    }
    try:
        response = requests.delete(url, headers=headers, json=payload)
        response.raise_for_status()
        print(f"Room {room_id} successfully deleted.")
    except requests.RequestException as e:
        print(f"Error deleting room {room_id}: {e}")

# Step 4: Admin logout
def logout(access_token):
    url = f"{server_url}/_matrix/client/r0/logout"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        print("Logout successful!")
    except requests.RequestException as e:
        print(f"Error logging out: {e}")

if __name__ == "__main__":
    # Step 1: Admin login
    access_token, user_id = admin_login(admin_username, admin_password)
    if not access_token:
        print("Failed to login as admin. Exiting...")
        exit()

    # Step 2: Get all rooms on the server
    rooms = get_all_rooms(access_token)
    if not rooms:
        print("No rooms found. Exiting...")
    else:
        # Step 3: Delete each room as admin
        for room in rooms:
            room_id = room['room_id']
            delete_room_as_admin(access_token, room_id)

    # Step 4: Admin logout
    logout(access_token)
