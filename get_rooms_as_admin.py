import requests
import json

#domain_name ="localhost" #local
domain_name ="85.215.118.180" #remote

# Synapse server details
server_url = "http://"+domain_name+":8081"

# Admin user credentials (must be an admin)
#admin_username = "admin"  # Replace with actual admin username
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
        print(f"Admin login successful for {user_id}")
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


# Step 3: Get the members of each room
def get_room_members(access_token, room_id):
    url = f"{server_url}/_matrix/client/r0/rooms/{room_id}/members"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    try:
        # Send the request to get room members
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Extract members from the response
        members = response.json().get("chunk", [])
        member_ids = [member['state_key'] for member in members]
        return member_ids

    except requests.RequestException as e:
        print(f"Error fetching members for room {room_id}: {e}")
        return []


# Step 4: Log out the admin user
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
    # Step 1: Admin login with username and password
    access_token, user_id = admin_login(admin_username, admin_password)

    if not access_token:
        print("Failed to login as admin. Exiting...")
        exit()

    # Step 2: Get all rooms on the server
    rooms = get_all_rooms(access_token)

    if not rooms:
        print("No rooms found. Exiting...")
    else:
        # Step 3: For each room, get the room name and list of members
        for room in rooms:
            room_id = room.get('room_id')
            room_name = room.get('name', f"Unnamed Room ({room_id})")
            print(f"\nRoom Name: {room_name} (Room ID: {room_id})")

            members = get_room_members(access_token, room_id)
            if members:
                print(f"Members in room '{room_name}': {', '.join(members)}")
            else:
                print(f"Room '{room_name}' has no members (empty).")

    # Step 4: Admin logout
    logout(access_token)
