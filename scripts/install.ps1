# Check if the script is running as Administrator
$admin = [Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
if (-not $admin.IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Restarting the script with administrator privileges..."
    Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Define variables
$URL = "https://github.com/BastienBYRA/DocCLI/releases/download/v0.1.0/main-windows.exe"
$INSTALL_DIR = "C:\Program Files\DocCLI"
$BINARY_NAME = "doccli.exe"
$DEST_PATH = "$INSTALL_DIR\$BINARY_NAME"

# Check if the project already exists and remove it
if (Test-Path $DEST_PATH) {
    Write-Host "$BINARY_NAME already exists. Removing the old version..."
    Remove-Item $DEST_PATH -Force
} else {
    Write-Host "$BINARY_NAME does not exist. Proceeding with installation..."
}

# Create installation directory if it does not exist
if (!(Test-Path $INSTALL_DIR)) {
    Write-Host "Creating installation directory: $INSTALL_DIR..."
    New-Item -ItemType Directory -Path $INSTALL_DIR -Force | Out-Null
}

# Download the binary
Write-Host "Downloading $BINARY_NAME..."
Invoke-WebRequest -Uri $URL -OutFile $DEST_PATH

# Grant execution permissions to the current user
Write-Host "Setting execution permissions..."
$acl = Get-Acl $DEST_PATH
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule($currentUser, "FullControl", "Allow")
$acl.SetAccessRule($rule)
Set-Acl -Path $DEST_PATH -AclObject $acl


# Add the installation directory to the system PATH
Write-Host "Adding $INSTALL_DIR to the system PATH..."
$envPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::Machine)
if ($envPath -notlike "*$INSTALL_DIR*") {
    $newPath = "$envPath;$INSTALL_DIR"
    [System.Environment]::SetEnvironmentVariable("Path", $newPath, [System.EnvironmentVariableTarget]::Machine)
}

Write-Host "Installation completed! Type 'doccli --help' to run the application."

# Keep the window open
Read-Host "Press Enter to close the window"