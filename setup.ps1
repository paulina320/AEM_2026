$ErrorActionPreference = "Stop"


# Check if arduino-cli is installed
$isInLocalFolder = Get-ChildItem -Path (Get-Location) -Filter "arduino-cli.exe" -ErrorAction SilentlyContinue
$isInstalled = Get-Command arduino-cli -ErrorAction SilentlyContinue

if (-not $isInstalled -and -not $isInLocalFolder) {
    Write-Host "arduino-cli not found. Install it first:"
    Write-Host "https://arduino.github.io/arduino-cli/latest/installation/"
    
    # make prompt to install arduino-cli
    $install = Read-Host "Do you want to install arduino-cli (this will download to this directory)? (y/n)"
    if ($install -eq "y") {
        # install arduino-cli
        # check 32 or 64 bit
        if ([System.Environment]::Is64BitOperatingSystem) {
                $url = "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_64bit.zip"
            } else {
                $url = "https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Windows_32bit.zip"
            }
    
            $output = Join-Path (Get-Location) "arduino-cli.zip"
            Invoke-WebRequest -Uri $url -OutFile $output
    
            # extract the zip file
            Expand-Archive -Path $output -DestinationPath (Get-Location)
    
            # remove the zip file
            Remove-Item -Path $output

            Write-Host "arduino-cli installed to $(Get-Location)"

    } else {
        Write-Host "Please install arduino-cli and run this script again."
        exit 1
    }

}

# Check if arduino-cli is installed
$isInLocalFolder = Get-ChildItem -Path (Get-Location) -Filter "arduino-cli.exe" -ErrorAction SilentlyContinue
$isInstalled = Get-Command arduino-cli -ErrorAction SilentlyContinue


if ($isInLocalFolder) {
    Write-Host "arduino-cli found in local folder: $($isInLocalFolder.FullName)"
    $arduinoCli = $isInLocalFolder.FullName
} else {
    Write-Host "arduino-cli found in system path: $($isInstalled.Source)"
    $arduinoCli = $isInstalled.Source
}

# Add board URL only if missing
$existing = & $arduinoCli config dump | Select-String "https://github.com/stm32duino/BoardManagerFiles/raw/main/package_stmicroelectronics_index.json
"

if (-not $existing) {
    Write-Host "Adding board manager URL..."
    & $arduinoCli config add board_manager.additional_urls https://github.com/stm32duino/BoardManagerFiles/raw/main/package_stmicroelectronics_index.json
}

# Install core if not installed
$coreInstalled = & $arduinoCli core list | Select-String "STMicroelectronics:stm32"

if (-not $coreInstalled) {
    Write-Host "Installing core..."
    & $arduinoCli core update-index
    & $arduinoCli core install STMicroelectronics:stm32
} else {
    Write-Host "Core already installed."
}

# -------------------------
# Check if STM32CubeProgrammer is installed
# -------------------------

$stm32ProgrammerPath = "C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\bin\STM32_Programmer_CLI.exe"
if (Test-Path $stm32ProgrammerPath) {
    Write-Host "STM32CubeProgrammer found at: $stm32ProgrammerPath"
} else {
    Write-Host "STM32CubeProgrammer not found. Please install it first:"
    Write-Host "https://www.st.com/en/development-tools/stm32cubeprog.html"
    Write-Host "After installing, run this script again."
    exit 1
}


Write-Host "Setup complete. You can now use arduino IDE to program your STM32 boards."
