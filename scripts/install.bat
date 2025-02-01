@echo off
REM Set the URL for the download
set URL=https://github.com/BastienBYRA/DocCLI/releases/download/v0.1.0/main-windows.exe

REM Set the installation directory
set INSTALL_DIR="C:\Program Files\DocCLI"
set BINARY_NAME="doccli.exe"
set BINARY_PATH=%INSTALL_DIR%\%BINARY_NAME%

echo Downloading %BINARY_NAME%...

REM Download the binary
powershell -Command "Invoke-WebRequest -Uri %URL% -OutFile %BINARY_NAME%"

REM Check if the installation directory exists, create it if not
if not exist %INSTALL_DIR% (
    echo Creating installation directory: %INSTALL_DIR%
    mkdir %INSTALL_DIR%
)

echo Moving the file to %INSTALL_DIR%...
move /Y %BINARY_NAME% %BINARY_PATH%

echo Adding %INSTALL_DIR% to PATH...
setx PATH "%PATH%;%INSTALL_DIR%" /M

echo Installation complete! You can now run 'doccli' from the command line.
pause
