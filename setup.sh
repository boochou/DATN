#!/bin/bash

# Exit immediately if a command fails
set -e

install_go() {
  echo -e "\033[0;32mGo is not installed. Installing Go...\033[0m"
  sudo apt-get update
  sudo apt-get install -y golang-go || { echo -e "\033[0;31mFailed to install Go\033[0m"; exit 1; }
}

# Check if Go is installed
if ! command -v go &> /dev/null; then
  install_go
else
  echo -e "\033[0;32mGo is already installed.\033[0m"
fi

# Function to check if Go tool is installed
install_go_tool() {
  tool_name=$1
  tool_link=$2
  if ! command -v $tool_name &> /dev/null; then
    echo -e "\033[0;32mInstalling $tool_name...\033[0m"
    go install -v $tool_link@latest || { echo -e "\033[0;31mFailed to install $tool_name\033[0m"; exit 1; }
  else
    echo -e "\033[0;32m$tool_name is already installed.\033[0m"
  fi
}

# Install Recon tools
install_go_tool subfinder "github.com/projectdiscovery/subfinder/v2/cmd/subfinder"
install_go_tool assetfinder "github.com/tomnomnom/assetfinder"

# Function to install Nmap if not installed
install_nmap() {
  if ! command -v nmap &> /dev/null; then
    echo -e "\033[0;32mInstalling Nmap...\033[0m"
    sudo apt-get update && sudo apt-get install -y nmap || { echo -e "\033[0;31mFailed to install nmap\033[0m"; exit 1; }
  else
    echo -e "\033[0;32mNmap is already installed.\033[0m"
  fi
}

# Install Nmap
install_nmap

echo -e "\033[0;32mSetup completed successfully.\033[0m"
