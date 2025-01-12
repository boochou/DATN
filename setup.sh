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

# Logging function for verbose mode
log() {
  if $VERBOSE; then
    echo -e "$1"
  fi
}

# Error handler
error_exit() {
  echo -e "${RED}$1${RESET}"
  exit 1
}

# Install Go
install_go() {
  echo -e "${GREEN}Installing Go version 1.23.3...${RESET}"
  sudo apt-get update
  wget -c https://golang.org/dl/go1.23.3.linux-amd64.tar.gz || error_exit "Failed to download Go."
  sudo tar -C /usr/local -xzf go1.23.3.linux-amd64.tar.gz || error_exit "Failed to extract Go."
  export PATH=$PATH:/usr/local/go/bin
}

# Update Go
update_go() {
  echo -e "${GREEN}Updating Go to version 1.23.3...${RESET}"
  sudo apt-get update
  wget -c https://golang.org/dl/go1.23.3.linux-amd64.tar.gz || error_exit "Failed to download Go."
  sudo apt remove -y golang-go
  sudo apt remove --auto-remove -y golang-go
  sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.23.3.linux-amd64.tar.gz || error_exit "Failed to update Go."
  export PATH=$PATH:/usr/local/go/bin
}

# Manage Go installation
manage_go() {
  if ! command -v go &> /dev/null; then
    install_go
  else
    current_version=$(go version | awk '{print $3}' | sed 's/^go//') 
    minor_version=$(echo "$current_version" | cut -d'.' -f2)       
    echo -e "${BLUE}Current Go version: $current_version${RESET}"

    if (( minor_version > 21 )); then
      echo -e "${BLUE}Go version is greater than 1.21. No update required.${RESET}"
    else
      echo -e "${YELLOW}Go version is less than or equal to 1.21. Updating Go...${RESET}"
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
    echo -e "${BLUE}$tool_name is already installed.${RESET}"
  fi
}

# Install Nmap
install_nmap() {
  if ! command -v nmap &> /dev/null; then
    echo -e "${GREEN}Installing Nmap...${RESET}"
    sudo apt-get update && sudo apt-get install -y nmap || error_exit "Failed to install Nmap."
  else
    echo -e "${BLUE}Nmap is already installed.${RESET}"
  fi
}

# Main script execution
log "Starting setup..."
manage_go
install_go_tool "subfinder" "github.com/projectdiscovery/subfinder/v2/cmd/subfinder"
install_go_tool "assetfinder" "github.com/tomnomnom/assetfinder"
install_nmap
echo -e "${GREEN}Setup completed successfully.${RESET}"
