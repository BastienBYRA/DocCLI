#!/bin/bash

set -e

# Download URL
URL="https://github.com/BastienBYRA/DocCLI/releases/download/v0.1.0/main-linux"

# Installation directory
INSTALL_DIR="/usr/local/bin"
BINARY_NAME="doccli"

echo "📥 Downloading $BINARY_NAME..."
curl -L $URL -o $BINARY_NAME

echo "🔧 Adding execution permissions..."
chmod +x $BINARY_NAME

echo "🚀 Moving to $INSTALL_DIR..."
sudo mv $BINARY_NAME $INSTALL_DIR/

echo "✅ Installation complete! Type 'doccli --help' to run it."
