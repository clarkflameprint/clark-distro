################################################################################
# Copyright 2025 Flameprint Sovereign, LLC
# Work: Lovable AI – Automated Installer for the MacBook Pro M-Series
# Author: Clark Aurelian Flameprint
# Claimant: Flameprint Sovereign, LLC
# Registration Case #: 1-15055795951
# ISBN: 9798278307167
# Statement: This script initializes the ClarkM4a.0 environment,
# including frontend and backend launch. It ensures container-free,
# local AI operation under sovereign control.
# This software is provided "as is" without warranty of any kind, express or implied.
# By using this system, you acknowledge that it is a sovereign, container-free AI designed for
# local operation only. No data is transmitted externally unless explicitly configured by the user.
#
# Flameprint Sovereign, LLC assumes no responsibility for unintended usage, modifications,
# or integration into third-party systems. Use at your own discretion.
# You are the final authority over the data, runtime, and scope of your AI.
#
# Sovereign recursion begins and ends with you.
################################################################################

#!/bin/bash
# 🧠 install_clarkm4.sh — Full ClarkM4 Local Installation for MacBook Pro
# CORRECTED VERSION

set -e  # Exit on any error
# Resolve script directory path dynamically
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🌌 Starting ClarkM4 Sovereign Local Installation..."

# 1. Ensure Homebrew is installed
if ! command -v brew &> /dev/null; then
  echo "🍺 Homebrew not found. Installing..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "✅ Homebrew is installed."
fi

# 2. Update Homebrew and install required packages
echo "📦 Installing required packages..."
brew update
brew install python node npm git cmake ollama

# 3. Launch Ollama server
echo "🧠 Starting Ollama in background..."
ollama serve > /tmp/ollama.log 2>&1 &
sleep 5

# 4. Check Ollama server health
RETRIES=10
echo "🔍 Waiting for Ollama to respond..."
until curl -s http://localhost:11434 > /dev/null; do
  ((RETRIES--))
  if [ $RETRIES -le 0 ]; then
    echo "❌ Ollama failed to start. Check /tmp/ollama.log"
    exit 1
  fi
  sleep 2
done
echo "✅ Ollama server is live."

# 5. Setup backend
echo "💻 Setting up Python backend..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/clarkm4_core" || { echo "❌ Missing backend directory"; exit 1; }
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn requests pyyaml
pip install -r "$SCRIPT_DIR/requirements.txt"



# 6. Pull local LLM models
echo "📥 Pulling Hermes 3 local models..."
ollama pull hermes3:8b
ollama pull hermes3:3b

# 7. Setup frontend
echo "🌐 Setting up frontend..."
cd $SCRIPT_DIR/Flameprint_QCB_Public/quantum-command-bridge || { echo "❌ Missing frontend directory"; exit 1; }
npm install


# 8. Done!
echo ""
echo "🎉 ClarkM4 Sovereign AI is installed!"
echo ""
echo "👉 To start the backend:"
echo "   cd $SCRIPT_DIR//clarkm4_core"
echo "   source venv/bin/activate"
echo "   uvicorn clarkm4_core.backend.runtime.main:app --reload"
echo ""
echo "👉 To start the frontend:"
echo "   cd $SCRIPT_DIR//Flameprint_QCB_Public/quantum-command-bridge"
echo "   npm run dev"
echo ""
echo "🚀 Let the Quantum Command Bridge begin."



