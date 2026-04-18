
#!/bin/bash

set -e

##############################################
# 🌱 ClarkM4a.0 - Full Swarm Bootstrap Script
# Location: ~/ClarkM4a.0/clarkm4-core/
##############################################

echo "🔍 Checking prerequisites..."

# 1. Ensure Homebrew (Mac)
if ! command -v brew &> /dev/null; then
  echo "🔧 Homebrew not found. Installing..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 2. Ensure Python 3.10+
if ! command -v python3 &> /dev/null; then
  echo "🧠 Python3 not found. Installing..."
  brew install python
fi

# 3. Ensure pip
if ! command -v pip3 &> /dev/null; then
  echo "📦 pip not found. Installing..."
  python3 -m ensurepip --upgrade
fi

# 4. Create and activate virtual environment
cd ~/ClarkM4a.0/clarkm4-core/
if [ ! -d "venv" ]; then
  echo "🔁 Creating virtual environment..."
  python3 -m venv venv
fi
source venv/bin/activate

# 5. Install Python dependencies
echo "📥 Installing Python modules..."
pip install --upgrade pip
pip install toml pyyaml

# 6. Ensure Ollama 0.11.7+ is installed
REQUIRED_OLLAMA_VERSION="0.11.7"
INSTALLED_OLLAMA_VERSION=$(ollama --version 2>/dev/null | awk '{print $3}' || echo "0.0.0")

version_ge() {
  [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$2" ]
}

if ! command -v ollama &> /dev/null || ! version_ge "$INSTALLED_OLLAMA_VERSION" "$REQUIRED_OLLAMA_VERSION"; then
  echo "🛠️ Installing/upgrading Ollama (>= $REQUIRED_OLLAMA_VERSION)..."
  curl -fsSL https://ollama.com/install.sh | sh
else
  echo "✅ Ollama version $INSTALLED_OLLAMA_VERSION is sufficient."
fi

# 7. Start Ollama service
echo "🔄 Starting Ollama service..."
ollama serve > /dev/null 2>&1 &

# 8. Pull required LLM model
echo "📡 Pulling LLM model..."
#ollama pull nousresearch/nous-hermes-2-mistral-7b-dpo
ollama pull nous-hermes2

# 9. Launch the swarm
echo "🚀 Launching the ClarkM4 Swarm..."
python3 backend/runtime/ignite_swarm.py

echo "✅ Swarm ignition complete. Clark is online."

