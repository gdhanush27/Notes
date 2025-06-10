#!/bin/bash
# setup-mtrash.sh: Setup script for mtrash and safe-rm CLI trash system

# Default values
DEFAULT_TRASH_DIR="$HOME/.trash"
DEFAULT_MAX_SIZE_MB=1024
BIN_DIR="$HOME/.local/bin"

# Check for source files
SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
SAFE_RM_SOURCE="$SCRIPT_DIR/safe-rm"
MTRASH_SOURCE="$SCRIPT_DIR/mtrash"

if [ ! -f "$SAFE_RM_SOURCE" ]; then
    echo "❌ Error: safe-rm source file not found at $SAFE_RM_SOURCE"
    exit 1
fi

if [ ! -f "$MTRASH_SOURCE" ]; then
    echo "❌ Error: mtrash source file not found at $MTRASH_SOURCE"
    exit 1
fi

echo "✅ Found source files:"
echo "   - safe-rm: $SAFE_RM_SOURCE"
echo "   - mtrash: $MTRASH_SOURCE"
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
sed "s|^TRASH_DIR=.*|TRASH_DIR=\"$TRASH_DIR\"|; s|^MAX_SIZE_MB=.*|MAX_SIZE_MB=$MAX_SIZE_MB|" "$SAFE_RM_SOURCE" > "$BIN_DIR/safe-rm"
chmod +x "$BIN_DIR/safe-rm"
echo "✅ Installed safe-rm to $BIN_DIR/safe-rm"

# Update and install mtrash
echo "📦 Installing mtrash..."
sed "s|^TRASH_DIR=.*|TRASH_DIR=\"$TRASH_DIR\"|" "$MTRASH_SOURCE" > "$BIN_DIR/mtrash"
chmod +x "$BIN_DIR/mtrash"
echo "✅ Installed mtrash to $BIN_DIR/mtrash"

# Create trash directory structure
mkdir -p "$TRASH_DIR/files" "$TRASH_DIR/info"

# Add bin dir to PATH if not present
if ! echo "$PATH" | grep -q "$BIN_DIR"; then
    echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$HOME/.bashrc"
    echo "Added $BIN_DIR to PATH in ~/.bashrc. Please restart your shell."
fi

echo "✅ mtrash and safe-rm installed to $BIN_DIR."
echo "Trash directory: $TRASH_DIR (max $MAX_SIZE_MB MB)"
echo "You can now use 'safe-rm' and 'mtrash' from the CLI."
