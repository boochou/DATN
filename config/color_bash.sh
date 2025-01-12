#!/bin/bash

# Define color codes
GREEN="\033[0;32m"
RED="\033[0;31m"
RESET="\033[0m"

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
