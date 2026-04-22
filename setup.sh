#!/usr/bin/env bash
set -e

BOARD_URL="https://github.com/stm32duino/BoardManagerFiles/raw/main/package_stmicroelectronics_index.json"

# -------------------------
# Find arduino-cli
# -------------------------

ARDUINO_CLI=""

if [ -f "./arduino-cli" ]; then
    echo "arduino-cli found in local folder"
    ARDUINO_CLI="./arduino-cli"
elif command -v arduino-cli >/dev/null 2>&1; then
    echo "arduino-cli found in system PATH"
    ARDUINO_CLI="arduino-cli"
else
    echo "arduino-cli not found."
    echo "https://arduino.github.io/arduino-cli/latest/installation/"

    read -p "Do you want to install arduino-cli? (y/n) " REPLY
    if [[ "$REPLY" == "y" ]]; then
        curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

        # assume installed in current directory or PATH
        if [ -f "./arduino-cli" ]; then
            ARDUINO_CLI="./arduino-cli"
        else
            ARDUINO_CLI="arduino-cli"
        fi
    else
        echo "Please install arduino-cli and rerun."
        exit 1
    fi
fi

echo "Using: $ARDUINO_CLI"

# -------------------------
# Add STM32 board package if missing
# -------------------------

EXISTING=$($ARDUINO_CLI config dump | grep "$BOARD_URL" || true)

if [ -z "$EXISTING" ]; then
    echo "Adding STM32 board URL..."
    $ARDUINO_CLI config add board_manager.additional_urls "$BOARD_URL"
else
    echo "Board URL already present"
fi

# -------------------------
# Install STM32 core if needed
# -------------------------

CORE_INSTALLED=$($ARDUINO_CLI core list | grep "STMicroelectronics:stm32" || true)

if [ -z "$CORE_INSTALLED" ]; then
    echo "Installing STM32 core..."
    $ARDUINO_CLI core update-index
    $ARDUINO_CLI core install STMicroelectronics:stm32
else
    echo "Core already installed"
fi



echo "Done."