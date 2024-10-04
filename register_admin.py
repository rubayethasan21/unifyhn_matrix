import hmac
import hashlib
import base64
import requests

# Synapse server details
server_url = "http://localhost:8080"  # Update if using a different server URL
#shared_secret = "SP;j&7cAKeqqjtQS2fk1W#ejuiT:G&uaggV&E,;g8Mx:1Xl#^X"  # local
shared_secret = "',D+V@s@p&eIjPy0Cp89=7*43_w;cUXOYIJ8e:6=U3rcM0:IUdw'"  # remote

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
