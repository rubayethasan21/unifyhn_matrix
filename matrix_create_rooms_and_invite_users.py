import requests
import json

#domain_name ="localhost" #local
domain_name ="unifyhn.de" #remote
#domain_name ="85.215.118.180" #remote

# Synapse server details
server_url = "http://"+domain_name+":8081"

# User credentials
username = "rubayet.hasan"  # Replace with actual username
password = "12345"  # Replace with actual password

# Room details
room_name = "unifyhn-room-1"  # The desired room name
room_topic = "This is a test room created via API"  # Room topic

# Predefined list of users to be invited (Matrix user IDs)
user_list = [
    "@markus.speidel:" + domain_name,
    "@arpita.sarker:" + domain_name,
    "@alexander.jesser:" + domain_name,
    #"@test.test:" + domain_name,
]


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


# Step 2: Get the list of joined rooms
def get_joined_rooms(access_token):
    url = f"{server_url}/_matrix/client/r0/joined_rooms"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        # Send the request to get the joined rooms
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Return the list of room IDs the user has joined
        return response.json().get("joined_rooms", [])
    except requests.exceptions.RequestException as e:
        print(f"Error getting joined rooms: {e}")
        return []


# Step 3: Check if a room with the desired name exists
def find_room_by_name(access_token, room_name):
    joined_rooms = get_joined_rooms(access_token)

    for room_id in joined_rooms:
        url = f"{server_url}/_matrix/client/r0/rooms/{room_id}/state/m.room.name"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                room_state = response.json()
                if room_state.get("name") == room_name:
                    print(f"Room '{room_name}' already exists with ID: {room_id}")
                    return room_id
        except requests.exceptions.RequestException:
            pass

    return None


# Step 4: Create a new room
def create_room(access_token, room_name, room_topic):
    url = f"{server_url}/_matrix/client/r0/createRoom"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": room_name,
        "topic": room_topic,
        "preset": "private_chat"  # Other options: 'public_chat' or 'trusted_private_chat'
    }

    try:
        # Send the request to create a new room
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        # Extract room_id from the response
        room_id = response.json().get("room_id")
        print(f"Room '{room_name}' created with ID: {room_id}")

        return room_id
    except requests.exceptions.RequestException as e:
        print(f"Error creating room: {e}")
        return None


# Step 5: Invite users to the room
def invite_users_to_room(access_token, room_id, user_list):
    url = f"{server_url}/_matrix/client/r0/rooms/{room_id}/invite"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    for user in user_list:
        payload = {
            "user_id": user
        }

        try:
            # Send the invite request for each user
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            print(f"Successfully invited {user} to room {room_id}")
        except requests.exceptions.RequestException as e:
            print(f"Error inviting {user}: {e}")


# Step 6: Log out the user
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

    # Step 2: Check if the room exists
    room_id = find_room_by_name(access_token, room_name)

    # Step 3: If the room doesn't exist, create a new room
    if not room_id:
        print(f"Room '{room_name}' does not exist. Creating a new one...")
        room_id = create_room(access_token, room_name, room_topic)

    if not room_id:
        print("Failed to create room. Exiting...")
        exit()

    # Step 4: Invite the predefined list of users to the room
    invite_users_to_room(access_token, room_id, user_list)

    # Step 5: Log out the user
    logout(access_token)
