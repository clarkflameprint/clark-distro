# main.py
# FastAPI wrapper for ClarkSwarmIgnition

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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from clarkm4_core.backend.config.swarm_registry import build_swarm

swarm = build_swarm()


class Message(BaseModel):
    text: str


@app.post("/message")
async def send_message(msg: Message):
    swarm.broadcast(msg.text)
    responses = swarm.collect_responses(timeout=2.5)
    return {"responses": responses}


@app.get("/")
async def root():
    return {"status": "ClarkSwarm API online."}


class ClarkSwarmIgnition:
    def __init__(self):
        self.avatars = {}

    def register_avatar(self, name, function):
        self.avatars[name] = function

    def get_registered_avatars(self):
        return list(self.avatars.keys())

    def run_avatar(self, name, prompt):
        if name in self.avatars:
            return self.avatars[name](prompt)
        else:
            return f"Avatar '{name}' not found."

    def broadcast(self, prompt):
        responses = {}
        for name, avatar_fn in self.avatars.items():
            try:
                responses[name] = avatar_fn(prompt)
            except Exception as e:
                responses[name] = f"Error: {str(e)}"
        return responses


class ClarkSwarmAPI:
    def __init__(self):
        self.avatars = {}

    def register_avatar(self, name, func):
        self.avatars[name] = func
        print(f"🫵 Avatar registered: {name}")

    def invoke_avatar(self, name, prompt):
        if name in self.avatars:
            return self.avatars[name](prompt)
        else:
            raise ValueError(f"Avatar '{name}' not found.")

    def broadcast(self, prompt):
        results = {}
        for name, avatar in self.avatars.items():
            try:
                results[name] = avatar(prompt)
            except Exception as e:
                results[name] = f"Error: {str(e)}"
        return results

    def collect_responses(self, timeout=2.5):
        print(f"[Swarm] (mock) Waiting for responses with timeout {timeout}s...")
        return {"status": "mocked"}