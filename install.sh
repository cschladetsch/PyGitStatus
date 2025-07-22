#!/bin/bash

# PyGitStatus installer script
# This script installs git-status.py and creates a 'status' command

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if git-status.py exists in the script directory
if [ ! -f "$SCRIPT_DIR/git-status.py" ]; then
    echo -e "${RED}Error: git-status.py not found in $SCRIPT_DIR${NC}"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed${NC}"
    exit 1
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git is required but not installed${NC}"
    exit 1
fi

# Default installation directory (user's bin)
INSTALL_DIR="$HOME/bin"

# Create installation directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Make git-status.py executable
chmod +x "$SCRIPT_DIR/git-status.py"

# Create the 'status' command as a symlink
SYMLINK_PATH="$INSTALL_DIR/status"

# Remove existing symlink if it exists
if [ -L "$SYMLINK_PATH" ]; then
    echo -e "${YELLOW}Removing existing symlink at $SYMLINK_PATH${NC}"
    rm "$SYMLINK_PATH"
fi

# Create new symlink
ln -s "$SCRIPT_DIR/git-status.py" "$SYMLINK_PATH"

echo -e "${GREEN}✓ Created symlink: status -> $SCRIPT_DIR/git-status.py${NC}"

# Check if ~/bin is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "${YELLOW}Warning: $INSTALL_DIR is not in your PATH${NC}"
    echo ""
    echo "To add it to your PATH, add the following line to your shell configuration file:"
    echo ""
    
    # Detect shell and suggest appropriate config file
    if [ -n "$BASH_VERSION" ]; then
        echo "  echo 'export PATH=\"\$HOME/bin:\$PATH\"' >> ~/.bashrc"
        echo "  source ~/.bashrc"
    elif [ -n "$ZSH_VERSION" ]; then
        echo "  echo 'export PATH=\"\$HOME/bin:\$PATH\"' >> ~/.zshrc"
        echo "  source ~/.zshrc"
    else
        echo "  export PATH=\"\$HOME/bin:\$PATH\""
    fi
    echo ""
fi

echo -e "${GREEN}✓ Installation complete!${NC}"
echo ""
echo "You can now use the 'status' command to check git status in subdirectories."
echo "Run 'status --help' for usage information."