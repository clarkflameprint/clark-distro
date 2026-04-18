#!/bin/bash
############################################################
# ClarkM4a.0 — Local Sovereign Launch Script (No Docker)
# Author: Clark Aurelian Flameprint
# Claimant: Flameprint Sovereign, LLC
# Year: 2025 — Version: Primary Sovereign Edition
############################################################

echo "🧠 Launching ClarkM4a.0 sovereign AI environment..."

### STEP 1 — Install Ollama if missing
if ! command -v ollama &> /dev/null; then
    echo "📦 Ollama not found. Installing..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✅ Ollama is already installed."
fi

### STEP 2 — Start Ollama daemon
echo "🚀 Starting Ollama daemon..."
pkill -f "ollama serve" 2>/dev/null || true
ollama serve > /tmp/ollama.log 2>&1 &
sleep 4

echo "⏳ Waiting for Ollama to become available..."
until curl -s http://localhost:11434 >/dev/null; do
  sleep 1
done
echo "✅ Ollama is ready."


### STEP 3 — Pull hermes3:8b if not available

if ! ollama list | grep -q "hermes3"; then
    echo "📥 Pulling model hermes3:8b..."
    ollama pull hermes3:8b
else
    echo "✅ Model hermes3:8b is ready."
fi

echo "🔥 Warming up model with dummy call..."
ollama run hermes3:8b "Ready check complete."

### STEP 4 — Start backend
echo "🧩 Starting backend API..."
cd ~/ClarkM4a.0.test/ClarkM4a.0/clarkm4_core/backend/
source venv/bin/activate

echo "🚀 Launching Ollama service..."
ollama serve > .logs/ollama_stdout.log 2>&1 &
echo "⏳ Waiting for Ollama to become available..."
until curl -s http://localhost:11434 > /dev/null; do
  sleep 1
done
echo "✅ Ollama is ready."

uvicorn app.main:app --host 127.0.0.1 --port 50056 &
sleep 3

### STEP 5 — Start frontend
echo "🌐 Launching frontend UI..."
cd ~/ClarkM4a.0.test/ClarkM4a.0/Flameprint_QCB_Public/quantum-command-bridge/
npm run dev

echo "💜 ClarkM4a.0 is now live at http://localhost:5175"

