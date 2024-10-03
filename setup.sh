#!/bin/bash

# Fail the script if any command fails
set -e

# Define variables
VENV_DIR="matrix-env"
CONFIG_FILE="homeserver.yaml"
DOMAIN="localhost"
CUSTOM_PORT=8081  # Set custom port to 8081

# Step 1: Install Python3 and virtualenv if not installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install Python3 to proceed."
    exit 1
fi

if ! python3 -m venv --help &> /dev/null
then
    echo "virtualenv is not installed. Installing now..."
    sudo apt-get install python3-venv -y
fi

# Step 2: Create a virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Step 3: Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Step 4: Install dependencies from requirements.txt
if [ ! -f "requirements.txt" ]; then
  echo "requirements.txt not found!"
  exit 1
fi

echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Step 5: Generate Synapse configuration if it doesn't exist
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Generating Matrix Synapse configuration..."
    synapse_homeserver --server-name $DOMAIN --config-path $CONFIG_FILE --generate-config --report-stats=no
else
    echo "Matrix Synapse configuration already exists."
fi

# Step 6: Modify homeserver.yaml using Python script
echo "Modifying $CONFIG_FILE to enable registration and set port $CUSTOM_PORT..."

python3 <<EOF
import yaml

config_file = "$CONFIG_FILE"
port = $CUSTOM_PORT

# Load YAML configuration
with open(config_file, "r") as file:
    config = yaml.safe_load(file)

# Enable registration
config["enable_registration"] = True
config["enable_registration_without_verification"] = True

# Update listeners to use port 8081
for listener in config["listeners"]:
    if listener["type"] == "http":
        listener["port"] = port

# Save changes back to the YAML file
with open(config_file, "w") as file:
    yaml.dump(config, file)

print(f"Updated {config_file}: enable_registration and port set to {port}")
EOF

# Step 7: Restart the Matrix Synapse server
echo "Restarting Matrix Synapse server on port $CUSTOM_PORT..."
synctl restart

# Step 8: Deactivate the virtual environment
deactivate

echo "Setup completed. Matrix Synapse server is running on port $CUSTOM_PORT, and registration is enabled."
