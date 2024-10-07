import hmac
import hashlib
import base64
import requests


#domain_name ="localhost" #local
domain_name ="unifyhn.de" #remote
#domain_name ="85.215.118.180" #remote

# Synapse server details
server_url = "https://"+domain_name+":8081"

if domain_name == "localhost":
    shared_secret = "vr#+UUi6K:+xrJ0y2wO1GWp5#FkrHvSQ3hz.v0-ET=dq,M._Z2"  # local
else:
    #shared_secret = ",D+V@s@p&eIjPy0Cp89=7*43_w;cUXOYIJ8e:6=U3rcM0:IUdw"  # remote with ip
    shared_secret = "PbBN~4qTF:hF:w@E*azkup+:@P4jxBr:^tfnyGFz:Jo8Y~i^g:"  # remote with domain name

# Admin user details
username = "admin"  # Replace with the desired username
password = "12345"  # Replace with the desired password
displayname = username  # Replace with the desired display name


# Step 1: Get the nonce from the Matrix server
def get_nonce():
    try:
        response = requests.get(f"{server_url}/_synapse/admin/v1/register")
        response.raise_for_status()
        return response.json()['nonce']
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Error getting nonce: {e}")


# Step 2: Generate HMAC-SHA1 for registration
def generate_hmac_sha1(nonce, username, password, shared_secret, is_admin=True):
    admin_string = "admin" if is_admin else "notadmin"

    # Prepare the registration string with null byte separation
    registration_string = f"{nonce}\0{username}\0{password}\0{admin_string}"

    # Generate the HMAC-SHA1
    mac = hmac.new(shared_secret.encode(), registration_string.encode(), hashlib.sha1)

    # Return the hex digest of the HMAC
    return mac.hexdigest()


# Step 3: Register the admin user
def register_admin(nonce, username, password, hmac_value, displayname):
    data = {
        "nonce": nonce,
        "username": username,
        "password": password,
        "displayname": displayname,  # Add the displayname here
        "admin": True,
        "mac": hmac_value
    }

    try:
        response = requests.post(f"{server_url}/_synapse/admin/v1/register", json=data)
        response.raise_for_status()
        print(f"Success! Admin user '{username}' registered.")
        print("Response:", response.json())
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Error registering admin: {e}")


if __name__ == "__main__":
    try:
        print("Step 1: Getting nonce from the server...")
        nonce = get_nonce()
        print(f"Nonce received: {nonce}")

        print("Step 2: Generating HMAC for registration...")
        hmac_value = generate_hmac_sha1(nonce, username, password, shared_secret)
        print(f"HMAC: {hmac_value}")

        print("Step 3: Registering admin user...")
        register_admin(nonce, username, password, hmac_value, displayname)

    except Exception as e:
        print(f"Error: {e}")
