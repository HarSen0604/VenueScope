#!/bin/bash

# Make the script executable by running `chmod +x install_dependencies.sh` in the terminal.
# Execute the script by running `./install_dependencies.sh`.

# Check if pip is installed
if ! command -v pip &> /dev/null
then
    echo "pip could not be found, please install it first."
    exit
fi

# Install dependencies from requirements.txt
pip install -r requirements.txt
echo "Dependencies have been installed."
