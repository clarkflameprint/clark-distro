import os
import toml
import yaml
import time

class Avatar:
    def __init__(self, name, profile_path, signature, persona_class, status, sovereign_channel):
        self.name = name
        self.profile_path = os.path.expanduser(profile_path)
        self.signature = signature
        self.persona_class = persona_class
        self.status = status
        self.sovereign_channel = sovereign_channel
        self.config = {}

    def load_profile(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r') as f:
                self.config = toml.load(f)
            return True
        return False

    def __init__(self, name, profile_path, signature="", persona_class="Unknown", status="inactive", sovereign_channel=False):
        self.name = name
        self.profile_path = profile_path
        self.signature = signature
        self.persona_class = persona_class
        self.status = status
        self.sovereign_channel = sovereign_channel

    def listen(self):
        import time
        print(f"👂 {self.name} is listening... (stub method)")
        while True:
            time.sleep(5)

    def __repr__(self):
        return f"<Avatar {self.name} | {self.persona_class} | {self.status}>"


def load_registry(registry_path):
    registry_path = os.path.expanduser(registry_path)
    avatars = []

    if not os.path.exists(registry_path):
        raise FileNotFoundError(f"Registry not found: {registry_path}")

    with open(registry_path, 'r') as f:
        registry_data = yaml.safe_load(f)

    for avatar in registry_data.get('avatars', []):
        new_avatar = Avatar(
            name=avatar['name'],
            profile_path=avatar['profile_path'],
            signature=avatar.get('signature', ''),
            persona_class=avatar.get('class', 'Unknown'),
            status=avatar.get('status', 'inactive'),
            sovereign_channel=avatar.get('sovereign_channel', False)
        )
        if new_avatar.load_profile():
            print(f"Loaded: {new_avatar}")
        else:
            print(f"Failed to load profile for: {new_avatar.name}")
        avatars.append(new_avatar)

    return avatars

if __name__ == "__main__":
    registry_path = "~/ClarkM4a.0/clarkm4_core/profiles/clarkm4_registry.yaml"
    avatar_swarm = load_registry(registry_path)
