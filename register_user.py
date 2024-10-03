import hmac
import hashlib
import requests

# Synapse server details
server_url = "http://localhost:8080"  # Update if using a different server URL
#shared_secret = "SP;j&7cAKeqqjtQS2fk1W#ejuiT:G&uaggV&E,;g8Mx:1Xl#^X"  # local
shared_secret = "V3EIxdN5=J5cWv+RJ74RG#14QWpFj:O,_60Yed:+PoztoSC20X"  # remote


# Normal user details (ensure no domain part in the username)
username = "alexander.jesser"  # Username without domain
password = "Hosting+12345"  # Replace with the desired password
displayname = "alexander.jesser"  # Display name can be any string


# Step 1: Get the nonce from the Matrix server
def get_nonce():
    try:
        response = requests.get(f"{server_url}/_synapse/admin/v1/register")
        response.raise_for_status()
        return response.json()['nonce']
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Error getting nonce: {e}")


# Step 2: Generate HMAC-SHA1 for registration
def generate_hmac_sha1(nonce, username, password, shared_secret, is_admin=False):
    admin_string = "admin" if is_admin else "notadmin"  # Change to "notadmin" for non-admin user

    # Prepare the registration string with null byte separation
    registration_string = f"{nonce}\0{username}\0{password}\0{admin_string}"

    # Generate the HMAC-SHA1
    mac = hmac.new(shared_secret.encode(), registration_string.encode(), hashlib.sha1)

    # Return the hex digest of the HMAC
    return mac.hexdigest()


# Step 3: Register the normal user (non-admin)
def register_user(nonce, username, password, hmac_value, displayname):
    data = {
        "nonce": nonce,
        "username": username,
        "password": password,
        "displayname": displayname,
        "admin": False,  # Ensure that this is set to False
        "mac": hmac_value
    }

    # Print the payload being sent for debugging
    print(f"Payload being sent to server: {data}")

    try:
        # Send the registration request to Synapse
        response = requests.post(f"{server_url}/_synapse/admin/v1/register", json=data)
        response.raise_for_status()
        print(f"Success! Normal user '{username}' registered.")
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        # Print the response content to better understand the error
        if response is not None:
            print(f"Response content: {response.content.decode()}")
        raise SystemExit(f"Error registering user: {e}")


if __name__ == "__main__":
    try:
        # Step 1: Get the nonce from the server
        print("Step 1: Getting nonce from the server...")
        nonce = get_nonce()
        print(f"Nonce received: {nonce}")

        # Step 2: Generate the HMAC for registration
        print("Step 2: Generating HMAC for registration...")
        hmac_value = generate_hmac_sha1(nonce, username, password, shared_secret, is_admin=False)
        print(f"HMAC: {hmac_value}")

        # Step 3: Register the user
        print("Step 3: Registering normal user...")
        register_user(nonce, username, password, hmac_value, displayname)

    except Exception as e:
        print(f"Error: {e}")
