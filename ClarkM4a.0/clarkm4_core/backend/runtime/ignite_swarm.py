
import os
import toml
import yaml
from clarkm4_core.backend.runtime.avatar_engine import load_registry

import subprocess
from pathlib import Path

class ClarkSwarmIgnition:
    def __init__(self):
        self.avatars = {}

    def register_avatar(self, name: str, respond_fn):
        self.avatars[name] = respond_fn

    def respond(self, name: str, prompt: str) -> str:
        if name not in self.avatars:
            raise ValueError(f"No avatar registered with name '{name}'")
        return self.avatars[name](prompt)



PYTHON_EXEC = str(Path("~/ClarkM4a.0/venv/bin/python").expanduser())
AVATAR_RUNNER = str(Path("~/ClarkM4a.0/clarkm4_core/backend/runtime/avatar_runtime.py").expanduser())


def launch_avatar(avatar):
    profile_path = Path(avatar.profile_path).expanduser()
    log_path = Path(avatar.config['logging']['log_path']).expanduser()
    print(f"🚀 Launching {avatar.name} ({avatar.persona_class})...")
    subprocess.Popen([
        PYTHON_EXEC,
        AVATAR_RUNNER,
        str(profile_path),
    ])


def ignite_all():
    registry_path = "~/ClarkM4a.0/clarkm4_core/profiles/clarkm4_registry.yaml"
    avatars = load_registry(Path(registry_path).expanduser())
    for avatar in avatars:
        if avatar.name == "Clark𐩪" and avatar.status == "active":
            launch_avatar(avatar)


if __name__ == "__main__":
    ignite_all()
