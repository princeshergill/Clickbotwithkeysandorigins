#!/bin/bash

# Exit if any command fails
set -e

echo "Setting up environment for Clickbot..."

# Step 1: Update system packages (Debian/Ubuntu/Arch-based, comment/uncomment as needed)
# sudo apt update && sudo apt install -y python3 python3-pip python3-venv
# sudo pacman -Syu --noconfirm python python-pip python-virtualenv

# Step 2: Clone the repository
git clone https://github.com/princeshergill/Clickbotwithkeysandorigins.git
cd Clickbotwithkeysandorigins

# Step 3: Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Step 4: Install required packages
pip install --upgrade pip
pip install -r requirements.txt

# Step 5: Install Playwright and dependencies
pip install playwright
playwright install

# Optional: If using VPN rotation, ensure required tools (e.g., wg-quick) are installed

echo "Setup complete. You can now run the bot using:"
echo "    source .venv/bin/activate && python search_click_bot.py"
