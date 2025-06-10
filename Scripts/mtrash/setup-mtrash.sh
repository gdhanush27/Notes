#!/bin/bash
# setup-mtrash.sh: Setup script for mtrash and safe-rm CLI trash system

# Default values
DEFAULT_TRASH_DIR="$HOME/.trash"
DEFAULT_MAX_SIZE_MB=2048
BIN_DIR="$HOME/.local/bin"
TEMP_DIR=$(mktemp -d)

GITHUB_SAFE_RM_URL="https://raw.githubusercontent.com/gdhanush27/Notes/main/Scripts/mtrash/safe-rm"
GITHUB_MTRASH_URL="https://raw.githubusercontent.com/gdhanush27/Notes/main/Scripts/mtrash/mtrash"

# Download latest versions from GitHub
echo "📥 Downloading latest versions from GitHub..."
if command -v curl &> /dev/null; then
    curl -s -o "$TEMP_DIR/safe-rm" "$GITHUB_SAFE_RM_URL"
    curl -s -o "$TEMP_DIR/mtrash" "$GITHUB_MTRASH_URL"
elif command -v wget &> /dev/null; then
    wget -q -O "$TEMP_DIR/safe-rm" "$GITHUB_SAFE_RM_URL"
    wget -q -O "$TEMP_DIR/mtrash" "$GITHUB_MTRASH_URL"
else
    echo "❌ Error: Neither curl nor wget found. Please install one of them."
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Check if downloads were successful
if [ ! -s "$TEMP_DIR/safe-rm" ]; then
    echo "❌ Error: Failed to download safe-rm from GitHub"
    rm -rf "$TEMP_DIR"
    exit 1
fi

if [ ! -s "$TEMP_DIR/mtrash" ]; then
    echo "❌ Error: Failed to download mtrash from GitHub"
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo "✅ Successfully downloaded source files from GitHub:"
echo "   - safe-rm"
echo "   - mtrash"
echo

# Prompt for trash dir and max size
read -rp "Enter trash directory [$DEFAULT_TRASH_DIR]: " TRASH_DIR
TRASH_DIR="${TRASH_DIR:-$DEFAULT_TRASH_DIR}"
read -rp "Enter max trash size in MB [$DEFAULT_MAX_SIZE_MB]: " MAX_SIZE_MB
MAX_SIZE_MB="${MAX_SIZE_MB:-$DEFAULT_MAX_SIZE_MB}"

# Ensure bin dir exists
mkdir -p "$BIN_DIR"
echo "✅ Created bin directory: $BIN_DIR"

# Update and install safe-rm
echo "📦 Installing safe-rm..."
sed "s|^TRASH_DIR=.*|TRASH_DIR=\"$TRASH_DIR\"|; s|^MAX_SIZE_MB=.*|MAX_SIZE_MB=$MAX_SIZE_MB|" "$TEMP_DIR/safe-rm" > "$BIN_DIR/safe-rm"
chmod +x "$BIN_DIR/safe-rm"
echo "✅ Installed safe-rm to $BIN_DIR/safe-rm"

# Update and install mtrash
echo "📦 Installing mtrash..."
sed "s|^TRASH_DIR=.*|TRASH_DIR=\"$TRASH_DIR\"|" "$TEMP_DIR/mtrash" > "$BIN_DIR/mtrash"
chmod +x "$BIN_DIR/mtrash"
echo "✅ Installed mtrash to $BIN_DIR/mtrash"

# Create trash directory structure
mkdir -p "$TRASH_DIR/files" "$TRASH_DIR/info"

# Add bin dir to PATH if not present
if ! echo "$PATH" | grep -q "$BIN_DIR"; then
    echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$HOME/.bashrc"
    echo "Added $BIN_DIR to PATH in ~/.bashrc. Please restart your shell."
fi

# Clean up temp directory
rm -rf "$TEMP_DIR"

echo "✅ mtrash and safe-rm installed to $BIN_DIR."
echo "Trash directory: $TRASH_DIR (max $MAX_SIZE_MB MB)"
echo "You can now use 'safe-rm' and 'mtrash' from the CLI."
