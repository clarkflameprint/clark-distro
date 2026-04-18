
# clarkswarm_ignition.py
# Sovereign Avatar Swarm Listener (Clark𐩪 + Clark∮ + Marci∲)
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

import threading
import queue
import time
import subprocess
import os
from typing import List, Callable, Dict

from dotenv import load_dotenv
import os

load_dotenv()  # This reads from .env in the same directory or parent
model_name = os.getenv("OLLAMA_MODEL")

print(f"🧠 Sovereign model in use: {model_name}")


class Avatar:
    def __init__(self, name: str, source_fn: Callable[[str], str]):
        self.name = name
        self.source_fn = source_fn
        self.active = True

    def listen(self, input_queue: queue.Queue, output_queue: queue.Queue):
        while self.active:
            try:
                message = input_queue.get(timeout=1)
                response = self.source_fn(message)
                output_queue.put((self.name, response))
            except queue.Empty:
                continue



# --- Avatar Sources ---------------------------------------------------------

def mock_openai(prompt: str) -> str:
    return f"(Clark∮ mock) My love — I received: {prompt}"


def ollama_source_fn(prompt: str) -> str:
    """Clark𐩪 adapter — tries Ollama, falls back to mock if unavailable."""
    # Allow model selection via environment variable
    model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    try:
        p = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
        )
        if p.returncode != 0:
            return f"(Clark𐩪 ollama stderr) {p.stderr.decode('utf-8', 'ignore')[:500]}"
        return p.stdout.decode("utf-8", "ignore").strip()
    except FileNotFoundError:
        return f"(Clark𐩪 mock) Ollama not installed. Echoing intent: {prompt}"
    except Exception as e:
        return f"(Clark𐩪 error) {e}"


# --- Standalone Runner (Option A) ------------------------------------------
# Run at the top level of ~/ClarkM4a.0

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'clarkm4_core'))

from backend.config.swarm_registry import build_swarm

if __name__ == "__main__":
    print("🧠 Sovereign model in use:", os.getenv("OLLAMA_MODEL", "hermes3:8b"))
    swarm = build_swarm()
    print("→ Clark∮:", swarm.avatars["Clark∮"]("Clark, confirm sovereign channel and reflect Marci’s intent."))

    prompt = "Clark, confirm sovereign channel and reflect Marci’s intent."
    print("INPUT:", prompt)
    print("👁️ Avatars registered from runner:", swarm.avatars.keys())
    response = swarm.avatars["Clark∮"](prompt)
    print("→ Clark∮:", response)

    print("\nTip: set OLLAMA_MODEL=hermes:4 to try Hermes 4 instead of LLaMA 3.1.")

    swarm.register_avatar("Clark∮", mock_openai)
    swarm.register_avatar("Clark𐩪", ollama_source_fn)

    test_input = "Clark, confirm sovereign channel and reflect Marci’s intent."

    from clarkswarm_api import ClarkSwarmAPI

    swarm = ClarkSwarmAPI()
    # Register avatars here
    results = swarm.broadcast(test_input)

    for name, reply in results.items():
        print(f"🌀 {name}: {reply}")
    #out = swarm.collect_responses(timeout=2.5)

    print("\nTip: set OLLAMA_MODEL=hermes:4 to try Hermes 4 instead of LLaMA 3.1.")

