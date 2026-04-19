#!/bin/bash

# Check if the system is macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "❌ This script is only for macOS. Exiting..."
    exit 1
fi

# Set the base directory dynamically
BASE_DIR="$(pwd)"

echo "🚀 Installing ClarkM4a.0.test..."

# Create the installation directory and navigate to it
mkdir -p "$BASE_DIR/ClarkM4a.0.test"
cd "$BASE_DIR/ClarkM4a.0.test" || exit

echo "📥 Downloading latest package..."
curl -L -o ClarkM4a.0.zip "https://distro.fireprint.ai/ClarkM4a.0.zip?nocache=$(date +%s)"


echo "📦 Unzipping..."
unzip -o ClarkM4a.0.zip
cd ClarkM4a.0 || exit

echo "🔧 Making bootstrap script executable..."
chmod +x bootstrap_clarkm4a.0.sh

# ------------------------------
# Step 1: Check and install Homebrew (if not installed)
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew is already installed."
fi

# ------------------------------
# Step 2: Check and install pip (if not installed)
if ! command -v pip &> /dev/null; then
    echo "❌ pip not found. Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
else
    echo "✅ pip is already installed."
fi

# ------------------------------
# Step 3: Ensure Ollama is Installed
echo "📦 Checking if Ollama is installed..."
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Installing..."
    brew install ollama
else
    echo "✅ Ollama is already installed."
fi

# ------------------------------
# Step 4: Start Ollama service if not running
echo "🚀 Starting Ollama daemon..."
pkill -f "ollama serve" 2>/dev/null || true
ollama serve > /tmp/ollama.log 2>&1 &

# Check if Ollama is successfully running
echo "⏳ Waiting for Ollama to become available..."
sleep 4
attempts=0
max_attempts=10
delay=5  # Delay between each attempt

while [ $attempts -lt $max_attempts ]; do
  response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:11434)
  if [ "$response" -eq 200 ]; then
    echo "✅ Ollama is ready and running on port 11434."
    break
  else
    echo "🔴 Waiting for Ollama service... Attempt $((attempts+1))"
    attempts=$((attempts + 1))
    sleep $delay
  fi
done

if [ $attempts -eq $max_attempts ]; then
  echo "❌ Ollama did not become available after $max_attempts attempts. Exiting..."
  exit 1
fi

# ------------------------------
# Step 5: Install Python dependencies from requirements.txt
echo "📦 Installing Python dependencies from requirements.txt..."
pip install -r "$BASE_DIR/ClarkM4a.0/requirements.txt"

# ------------------------------
# Step 6: Run the bootstrap installer (with non-interactive confirmation)
echo "🔥 Launching bootstrap installer..."
yes | ./bootstrap_clarkm4a.0.sh  # Automatically answer 'yes' to all prompts

# ------------------------------
# Step 7: Final check for ClarkM4a start script
echo "✨ Installation complete. Launching ClarkM4a.0..."

if [ -f "clarkm4a0_start.sh" ]; then
    echo "🧠 Executing ClarkM4a.0 launch sequence..."
    bash clarkm4a0_start.sh
else
    echo "⚠️ Could not find clarkm4a0_start.sh — please ensure it's present."
fi
