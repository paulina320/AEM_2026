#!/usr/bin/env bash
set -e

CONFIG_FILE="$(pwd)/arduino-cli.yaml"
export ARDUINO_CONFIG_FILE="$CONFIG_FILE"

if ! command -v arduino-cli >/dev/null 2>&1; then
  echo "arduino-cli not found. Install it first:"
  echo "https://arduino.github.io/arduino-cli/latest/installation/"
  
  # make prompt to install arduino-cli
  read -p "Do you want to install arduino-cli? (y/n) "
  if [[ "$REPLY" == "y" ]]; then
    # install arduino-cli
    curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
  else
    echo "Please install arduino-cli and run this script again."
  
  exit 1
fi

echo "Using config: $ARDUINO_CONFIG_FILE"

arduino-cli config init --overwrite || true

echo "Updating index..."
arduino-cli core update-index

echo "Installing core..."
arduino-cli core install VENDOR:ARCH

echo "Done."