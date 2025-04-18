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
    if [ "$tool_name" == "katana" ]; then
      CGO_ENABLED=1 go install -v "$tool_link"@latest || error_exit "Failed to install $tool_name."
    else
      go install -v "$tool_link"@latest || error_exit "Failed to install $tool_name."
    fi
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
# Function to check and install a Python package
install_python_package() {
  package_name=$1
  package_=$2
  if ! python3 -c "import $package_name" &> /dev/null; then
    echo -e "${GREEN}Installing Python package: $package_name...${RESET}"
    pip install "$package_" || error_exit "Failed to install $package_name."
  else
    echo -e "${BLUE}Python package $package_name is already installed.${RESET}"
  fi
}
# Verify all tools are available
verify_tools() {
  required_tools=("go" "subfinder" "assetfinder" "nmap" "knockpy" "katana" "ffuf" "httpx" "paramspider")
  for tool in "${required_tools[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
      error_exit "${tool} is not installed or not found in PATH. Please check the installation process."
    fi
  done
}
install_paramspider() {
    # Navigate to ./.tool directory
    mkdir -p ./.tool
    cd ./.tool || { echo "Failed to enter ./.tool directory"; return 1; }

    # Check if paramspider is already installed
    if command -v paramspider &> /dev/null; then
        echo "ParamSpider is already installed."
        return 0
    fi

    # Clone the repository if it doesn't exist
    if [ ! -d "paramspider" ]; then
        echo "Cloning ParamSpider repository..."
        git clone https://github.com/devanshbatham/paramspider || { echo "Failed to clone repository"; return 1; }
    fi

    # Install the package
    cd paramspider || { echo "Failed to enter paramspider directory"; return 1; }
    echo "Installing ParamSpider..."
    pip install . || { echo "Installation failed"; return 1; }

    echo "ParamSpider installed successfully."
}

# Main script execution
log "Starting setup..."
manage_go
install_go_tool "subfinder" "github.com/projectdiscovery/subfinder/v2/cmd/subfinder"
install_go_tool "assetfinder" "github.com/tomnomnom/assetfinder"
install_go_tool "katana" "github.com/projectdiscovery/katana/cmd/katana"
install_go_tool "ffuf" "github.com/ffuf/ffuf/v2"
install_go_tool "httpx" "github.com/projectdiscovery/httpx/cmd/httpx"
install_nmap
install_python_package "knock" "knock-subdomains"
install_paramspider
# install_python_package "httpx" "httpx"
verify_tools
echo -e "${GREEN}Setup completed successfully.${RESET}"
