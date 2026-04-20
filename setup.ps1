$ErrorActionPreference = "Stop"

$env:ARDUINO_CONFIG_FILE = Join-Path (Get-Location) "arduino-cli.yaml"


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

Write-Host "Using config: $env:ARDUINO_CONFIG_FILE"

& $arduinoCli config init --overwrite | Out-Null

Write-Host "Updating index..."
& $arduinoCli core update-index

Write-Host "Installing core..."
& $arduinoCli core install arduino:avr

Write-Host "Done."