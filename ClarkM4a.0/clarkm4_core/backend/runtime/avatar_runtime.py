import toml
import subprocess
import sys
from pathlib import Path


def launch_model_if_needed(model_name, port):
    check_command = ["ollama", "list"]
    try:
        result = subprocess.run(check_command, capture_output=True, text=True)
        if model_name not in result.stdout:
            print(f"Model '{model_name}' not found. Pulling from registry...")
            subprocess.run(["ollama", "pull", model_name], check=True)

        # Check if model is already running on the given port
        result = subprocess.run(["lsof", "-i", f":{port}"], capture_output=True, text=True)
        if result.stdout:
            print(f"Model '{model_name}' already running on port {port}.")
        else:
            print(f"Starting model '{model_name}' on port {port}...")
            subprocess.Popen(["ollama", "serve"])

    except Exception as e:
        print(f"Failed to launch model '{model_name}': {e}")
        sys.exit(1)


def main(profile_path):
    profile = toml.load(Path(profile_path).expanduser())

    model_info = profile.get("model", {})
    model_name = model_info.get("name")
    port = model_info.get("port")

    if model_name and port:
        launch_model_if_needed(model_name, port)
    else:
        print("Model name or port missing in profile.")
        sys.exit(1)

    print(f"\n🧠 Avatar is ready: {profile['identity']['name']} on {model_name} @ localhost:{port}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 avatar_runtime.py <profile_path>")
        sys.exit(1)

    profile_path = sys.argv[1]
    main(profile_path)
