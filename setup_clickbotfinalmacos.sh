#!/bin/bash

# --- Full macOS Clickbot Installer ---
set -e

echo "🔍 Checking macOS setup requirements..."

# Ensure we're on macOS
if [[ "$(uname)" != "Darwin" ]]; then
  echo "❌ This installer is designed for macOS only."
  exit 1
fi

# Check for Xcode Command Line Tools
if ! xcode-select -p &>/dev/null; then
  echo "❌ Xcode Command Line Tools not installed."
  echo "➡️  Installing Xcode CLI tools..."
  xcode-select --install
  echo "✅ Please rerun this script after installation completes."
  exit 1
fi

# Check for Homebrew
if ! command -v brew &>/dev/null; then
  echo "🍺 Homebrew not found. Installing Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Check for Python 3
if ! command -v python3 &>/dev/null; then
  echo "🐍 Python 3 not found. Installing via Homebrew..."
  brew install python
fi

# Check for pip
if ! command -v pip3 &>/dev/null; then
  echo "❌ pip3 is missing. Please ensure Python 3 is correctly installed."
  exit 1
fi

echo "✅ All system dependencies satisfied."

# Clone the bot repo if not already present
if [ ! -d "Clickbotwithkeysandorigins" ]; then
  echo "📦 Cloning Clickbotwithkeysandorigins repository..."
  git clone https://github.com/princeshergill/Clickbotwithkeysandorigins.git
fi

cd Clickbotwithkeysandorigins

# Set up virtual environment
echo "🧪 Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install required Python packages
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt
pip install playwright

# Install Playwright browsers
echo "🌐 Installing Playwright browser binaries..."
playwright install

echo ""
echo "🎉 Setup complete!"

# Offer to launch the bot
read -p "▶️ Do you want to run the bot now? [y/n]: " launch
if [[ "$launch" == "y" ]]; then
  python search_click_bot.py
else
  echo "💡 You can run the bot later by executing:"
  echo "   cd Clickbotwithkeysandorigins"
  echo "   source .venv/bin/activate"
  echo "   python search_click_bot.py"
fi
