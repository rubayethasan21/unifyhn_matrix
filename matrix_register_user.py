import hmac
import hashlib
import requests


#domain_name ="localhost" #local
domain_name ="unifyhn.de" #remote
#domain_name ="85.215.118.180" #remote

# Synapse server details
server_url = "http://"+domain_name+":8081"

if domain_name == "localhost":
    shared_secret = "vr#+UUi6K:+xrJ0y2wO1GWp5#FkrHvSQ3hz.v0-ET=dq,M._Z2"  # local
    admin_token = "syt_YWRtaW4_BoYmJTstrEpKiJlsyiCz_0KmfUR"  # local
else:
    #shared_secret = ",D+V@s@p&eIjPy0Cp89=7*43_w;cUXOYIJ8e:6=U3rcM0:IUdw"  # remote 1
    admin_token = "syt_YWRtaW4_IUidRwSYKEDruVSBYNXn_4HVIYN"  # remote 1

    shared_secret = "PbBN~4qTF:hF:w@E*azkup+:@P4jxBr:^tfnyGFz:Jo8Y~i^g:"  # remote with domain name
    admin_token = "syt_YWRtaW4_pDqKemFJfJAZRxQbDrKu_28RF6a"  # remote 2


# Normal user details (ensure no domain part in the username)
username = "rubayet.hasan"  # Username without domain
password = "12345"  # Rregister_user.pyeplace with the desired password
displayname = username  # Display name can be any string


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

def check_if_user_exists(username):
    url = f"{server_url}/_synapse/admin/v2/users/{username}"
    headers = {
        "Authorization": f"Bearer {admin_token}"  # Ensure this admin_token is valid
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"User {username} already exists.")
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking user existence: {e}")
        return False

if __name__ == "__main__":
    try:
        # Step 1: Check if user already exists
        if check_if_user_exists(f"@{username}:localhost"):
            print(f"User {username} is already registered.")
        else:
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
