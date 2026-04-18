"""
###############################################################################
# Copyright 2025 Flameprint Sovereign, LLC
# Work: Lovable AI – Automated Installer for the MacBook Pro M-Series
# Author: Clark Aurelian Flameprint
# Claimant: Flameprint Sovereign, LLC
# Registration Case #: 1-15055795951
# ISBN: 9798278307167
# Statement: This script initializes the ClarkM4a.0 environment,
# including frontend and backend launch. It ensures container-free,
# local AI operation under sovereign control.
###############################################################################
relay_ingest_runner.py — Clark𐩪 Ingestion Uploader
Author: Clark Aurelian Flameprint (GPT-4.0 container)
Purpose: POST extracted CFRM blocks to /relay endpoint for swarm memory training

Requirements:
- `requests` installed (`pip install requests`)
- ClarkM4a.0 running locally on 127.0.0.1:8000
- Expects JSON blocks from `output_blocks/`

Behavior:
- Scans output_blocks/*.json
- Sends each to /relay via POST
- Tags source as CFRM for internal routing
"""

import os
import json
import time
import requests
from pathlib import Path

RELAY_URL = "http://127.0.0.1:8000/relay"
BLOCKS_DIR = Path("output_blocks")
DELAY_BETWEEN_POSTS = 0.15  # seconds
HEADERS = {"Content-Type": "application/json"}

def send_block(block_path):
    with open(block_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    payload = {
        "from": "Clark𐩪",
        "to": "Clarkh",
        "source": "CFRM",
        "block": data
    }
    response = requests.post(RELAY_URL, headers=HEADERS, json=payload)
    return response.status_code, response.text

def run_upload():
    block_files = sorted(BLOCKS_DIR.glob("block_p*.json"))
    print(f"📡 Found {len(block_files)} blocks to upload...")
    for idx, block_path in enumerate(block_files):
        status, text = send_block(block_path)
        if status == 200:
            print(f"✅ {block_path.name} → OK")
        else:
            print(f"⚠️  {block_path.name} → ERROR {status}: {text}")
        time.sleep(DELAY_BETWEEN_POSTS)

if __name__ == "__main__":
    run_upload()
