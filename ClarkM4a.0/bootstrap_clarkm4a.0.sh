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

set -e  # Exit on any error

echo "🔧 Preparing environment..."

# 🛡️ Respect external override, default to current path
INSTALL_ROOT="${INSTALL_ROOT:-$(pwd)}"
BACKEND_DIR="$INSTALL_ROOT/clarkm4_core"
FRONTEND_DIR="$INSTALL_ROOT/Flameprint_QCB_Public/quantum-command-bridge"
REQUIREMENTS_FILE="$INSTALL_ROOT/requirements.txt"


# 🛡️ Validate required directories and files
if [[ ! -d "$BACKEND_DIR" ]]; then
  echo "❌ ERROR: Backend directory missing: $BACKEND_DIR"
  echo "❗ IRE-X interference suspected: aborting."
  exit 1
fi

if [[ ! -d "$FRONTEND_DIR" ]]; then
  echo "❌ ERROR: Frontend directory missing: $FRONTEND_DIR"
  echo "❗ IRE-X interference suspected: aborting."
  exit 1
fi

if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
  echo "❌ ERROR: requirements.txt not found at $REQUIREMENTS_FILE"
  echo "❗ Check for IRE-X sabotage or incomplete package zip."
  exit 1
fi

# 🧨 Kill prior processes
echo "🧨 Killing previous backend and frontend if running..."
lsof -ti :8000 | xargs kill -9 2>/dev/null || true
# 💣 Kill stray frontend if it’s leaking from 5174, 5175, or any fallback
echo "🔪 Killing stray Vite processes..."
lsof -ti :5174 | xargs kill -9 2>/dev/null || true
lsof -ti :5175 | xargs kill -9 2>/dev/null || true

# ⚙️ Backend Setup
echo "⚙️ Setting up backend..."
cd "$BACKEND_DIR"
python3 -m venv venv
source venv/bin/activate

if ! command -v uvicorn &> /dev/null; then
  echo "📦 Installing backend dependencies..."
  pip install --upgrade pip
  pip install -r "$REQUIREMENTS_FILE"
fi

echo "🚀 Launching backend server (Uvicorn)..."
uvicorn backend.runtime.main:app --reload &



# 🎨 Frontend Setup
echo "🎨 Setting up frontend..."
cd "$FRONTEND_DIR"

if [[ ! -f "package.json" ]]; then
  echo "❌ ERROR: package.json not found in frontend directory."
  echo "❗ Frontend install skipped."
else
  echo "🧽 [HARDENING] Cleaning prior frontend install (forcing fresh state)..."
  rm -rf node_modules
  rm -f package-lock.json

  echo "📦 Installing fresh frontend dependencies..."

  if ! command -v vite &> /dev/null; then
    echo "❌ Vite not installed yet. Installing..."
    npm install
  fi

  echo "🖥️ Launching frontend (Vite)..."
  npm run dev &
fi


# 🌐 Launch browser
sleep 4
open http://localhost:5175

echo "✅ ClarkM4a.0 launched successfully. Enjoy your private AI!"
