#!/bin/bash

# Fail the script if any command fails
set -e

# Define variables
VENV_DIR="matrix-env"
CONFIG_FILE="homeserver.yaml"

# Step 1: Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found! Please run './setup.sh' to create it."
    exit 1
fi

# Step 2: Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Step 3: Stop the Matrix Synapse server (if running)
echo "Stopping Matrix Synapse server..."
synctl stop || echo "Matrix Synapse server was not running."

# Step 4: Prompt for custom port if not provided as an argument
if [ -z "$1" ]; then
  read -p "Enter the custom port to run the Matrix server on (default 8008): " CUSTOM_PORT
  CUSTOM_PORT=${CUSTOM_PORT:-8008}  # Set default to 8008 if no input
else
  CUSTOM_PORT=$1
fi

# Step 5: Check if the custom port is already in the homeserver.yaml, if not, add it
if grep -q "port: $CUSTOM_PORT" $CONFIG_FILE; then
  echo "Port $CUSTOM_PORT is already configured in $CONFIG_FILE."
else
  echo "Configuring $CONFIG_FILE with custom port $CUSTOM_PORT..."

  # Add the port configuration under the listeners section
  sed -i "/^listeners:/a\ \ \ \ - port: $CUSTOM_PORT\n      tls: false\n      bind_addresses: ['0.0.0.0']\n      type: http\n      x_forwarded: true\n      resources:\n        - names: [client, federation]" $CONFIG_FILE
fi

# Step 6: Start the Matrix Synapse server again
echo "Restarting Matrix Synapse server on port $CUSTOM_PORT..."
synctl start

# Deactivate virtual environment
deactivate

echo "Matrix Synapse server has been restarted on port $CUSTOM_PORT."
