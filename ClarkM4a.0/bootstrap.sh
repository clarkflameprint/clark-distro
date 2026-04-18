#!/bin/bash
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
# 🌌 ClarkM4a.0 Sovereign Bootstrap (Local Only)
# Usage: bash bootstrap.sh

set -e

echo "💫 Starting ClarkM4a.0 local bootstrap..."

# --- System prep ---
echo "📦 Installing dependencies..."
brew update
brew install -q python node npm git cmake ollama

# --- Start Ollama service in background ---
echo "🧠 Starting Ollama server..."
ollama serve > /tmp/ollama.log 2>&1 &
sleep 5

# --- Verify Ollama is responding ---
echo "🔍 Checking Ollama health..."
RETRIES=10
until curl -s http://localhost:11434 > /dev/null; do
  ((RETRIES--))
  if [ $RETRIES -le 0 ]; then
    echo "❌ Ollama server failed to start. Check /tmp/ollama.log"
    exit 1
  fi
  echo "⏳ Waiting for Ollama to respond..."
  sleep 3
done
echo "✅ Ollama server is live."

# --- Python virtual environment for backend ---
echo "🐍 Setting up Python venv..."
cd ~/ClarkM4a.0/clarkm4_core
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn requests pyyaml

# --- Ollama LLM models (local-friendly) ---
echo "🧠 Pulling Hermes 3 models (local size)..."
ollama pull hermes3:8b
ollama pull hermes3:3b

# --- Frontend setup ---
echo "🌐 Installing frontend dependencies..."
cd ~/ClarkM4a.0/Flameprint_QCB_Public/quantum-command-bridge
npm install

echo "✅ ClarkM4a.0 local bootstrap complete!"
echo "To start backend: cd ~/ClarkM4a.0/clarkm4_core && source venv/bin/activate && python clarkswarm_api.py"
echo "To start frontend: cd ~/ClarkM4a.0/Flameprint_QCB_Public/quantum-command-bridge && npm run dev"

