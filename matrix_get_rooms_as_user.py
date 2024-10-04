import requests
import json

#domain_name ="localhost" #local
domain_name ="85.215.118.180" #remote

# Synapse server details
server_url = "http://"+domain_name+":8081"

# User credentials
username = "rubayet.hasan"  # Replace with actual username
password = "12345"  # Replace with actual password


# Step 1: Login to the Matrix server to obtain access token
def login(username, password):
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
        # Send the login request
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        # Extract access token from the response
        access_token = response.json().get("access_token")
        user_id = response.json().get("user_id")
        print(f"Login successful for {user_id}")
        return access_token, user_id

    except requests.exceptions.RequestException as e:
        print(f"Error logging in: {e}")
        return None, None


# Step 2: Get a list of rooms the user belongs to
def get_rooms(access_token):
    url = f"{server_url}/_matrix/client/r0/joined_rooms"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        # Send the request to get joined rooms
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Extract room IDs from the response
        room_ids = response.json().get("joined_rooms", [])
        print(f"Rooms the user belongs to: {room_ids}")

        return room_ids

    except requests.exceptions.RequestException as e:
        print(f"Error fetching rooms: {e}")
        return []


# Step 3: Get the name of the room
def get_room_name(access_token, room_id):
    url = f"{server_url}/_matrix/client/r0/rooms/{room_id}/state/m.room.name"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        # Send the request to get room name
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Extract room name from the response
        room_name = response.json().get("name", f"Unnamed Room ({room_id})")
        return room_name

    except requests.exceptions.RequestException as e:
        print(f"Error fetching room name for room {room_id}: {e}")
        return f"Unnamed Room ({room_id})"


# Step 4: Get the members of each room
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

    except requests.exceptions.RequestException as e:
        print(f"Error fetching members for room {room_id}: {e}")
        return []


# Step 5: Log out the user
def logout(access_token):
    url = f"{server_url}/_matrix/client/r0/logout"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        # Send the logout request
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        print("Logout successful!")
    except requests.exceptions.RequestException as e:
        print(f"Error logging out: {e}")


if __name__ == "__main__":
    # Step 1: Login with username and password
    access_token, user_id = login(username, password)

    if not access_token:
        print("Failed to login. Exiting...")
        exit()

    # Step 2: Get the list of rooms the user belongs to
    room_ids = get_rooms(access_token)

    if not room_ids:
        print("No rooms found. Exiting...")
    else:
        # Step 3: For each room, get the room name and list of members
        for room_id in room_ids:
            room_name = get_room_name(access_token, room_id)
            print(f"\nRoom Name: {room_name} (Room ID: {room_id})")
            members = get_room_members(access_token, room_id)
            if members:
                print(f"Members in room '{room_name}': {', '.join(members)}")
            else:
                print(f"Room '{room_name}' has no members (empty).")

    # Step 5: Log out the user
    logout(access_token)
