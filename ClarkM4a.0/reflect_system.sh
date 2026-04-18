#!/bin/bash

echo "📦 Reflecting System Configuration for ClarkM4a.0..."
echo "--------------------------------------------"

echo -e "\n🖥️ macOS and Hardware Info:"
sw_vers
uname -a
system_profiler SPHardwareDataType

echo -e "\n🧱 Node, NPM, Python Versions:"
node -v
npm -v
python3 --version
pip3 --version

echo -e "\n⚙️ Vite and React Versions:"
npm list vite
npm list react

echo -e "\n📦 package.json Snapshot:"
cat ClarkM4a.0/Flameprint_QCB_Public/package.json

echo -e "\n🧪 Installed Python Packages (Backend):"
pip freeze

echo -e "\n🧬 Folder Tree Structure:"
tree ClarkM4a.0 -L 2

echo -e "\n🛠️ Current Port Mappings:"
lsof -i :5173
lsof -i :5175

echo -e "\n✅ Reflection complete."
