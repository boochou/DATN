#!/bin/bash
set -e

echo "Installing Reconn Tool..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest || { echo "Failed to install subfinder"; exit 1; }
go install -v github.com/tomnomnom/assetfinder@latest || { echo "Failed to install assetfinder"; exit 1; }

# Install Nmap
echo "Installing Nmap..."
sudo apt-get update && sudo apt-get install -y nmap || { echo "Failed to install nmap"; exit 1; }

echo "Setup completed successfully."
