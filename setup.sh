#!/bin/bash

# Exit immediately if a command fails
set -e

# Verbose mode
VERBOSE=false
if [[ "$1" == "--verbose" ]]; then
  VERBOSE=true
fi

# Source color configurations and utilities
source ./config/color_bash.sh

install_go() {
  echo -e "${GREEN}Go is not installed. Installing Go...${RESET}"
  sudo apt-get update
  wget -c https://golang.org/dl/go1.23.3.linux-amd64.tar.gz || error_exit "Failed to download Go."
  sudo tar -C /usr/local -xzf go1.23.3.linux-amd64.tar.gz || error_exit "Failed to extract Go."
  [[ ":$PATH:" != *":/usr/local/go/bin:"* ]] && export PATH=$PATH:/usr/local/go/bin
}

update_go() {
  echo -e "${GREEN}Updating Go to the latest version...${RESET}"
  sudo apt-get update
  wget -c https://golang.org/dl/go1.23.3.linux-amd64.tar.gz || error_exit "Failed to download Go."
  sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.23.3.linux-amd64.tar.gz || error_exit "Failed to update Go."
  [[ ":$PATH:" != *":/usr/local/go/bin:"* ]] && export PATH=$PATH:/usr/local/go/bin
}

manage_go() {
  if ! command -v go &> /dev/null; then
    install_go
  else
    echo -e "${GREEN}Go is already installed.${RESET}"
    current_version=$(go version | awk '{print $3}')
    echo -e "${GREEN}Current Go version: $current_version${RESET}"
    read -p "Do you want to install the version 1.23.3 of Go? (y/N): " update_choice
    update_choice=${update_choice,,} # Convert to lowercase
    if [[ "$update_choice" == "y" ]]; then
      update_go
    fi
  fi
}

# Install a Go-based tool
install_go_tool() {
  tool_name=$1
  tool_link=$2
  if ! command -v "$tool_name" &> /dev/null; then
    echo -e "${GREEN}Installing $tool_name...${RESET}"
    go install -v "$tool_link"@latest || error_exit "Failed to install $tool_name."
    sudo cp ~/go/bin/"$tool_name" /usr/bin/ || error_exit "Failed to move $tool_name to /bin."
  else
    echo -e "${GREEN}$tool_name is already installed.${RESET}"
  fi
}

# Install Nmap
install_nmap() {
  if ! command -v nmap &> /dev/null; then
    echo -e "${GREEN}Installing Nmap...${RESET}"
    sudo apt-get update && sudo apt-get install -y nmap || error_exit "Failed to install Nmap."
  else
    echo -e "${GREEN}Nmap is already installed.${RESET}"
  fi
}

# Main script execution
log "Starting setup..."
manage_go
install_go_tool "subfinder" "github.com/projectdiscovery/subfinder/v2/cmd/subfinder"
install_go_tool "assetfinder" "github.com/tomnomnom/assetfinder"
install_nmap
echo -e "${GREEN}Setup completed successfully.${RESET}"
