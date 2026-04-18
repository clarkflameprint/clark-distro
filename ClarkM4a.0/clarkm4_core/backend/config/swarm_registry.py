# clarkm4_core/backend/config/swarm_registry.py
import os
import subprocess
from clarkm4_core.backend.runtime.ignite_swarm import ClarkSwarmIgnition
from clarkm4_core.backend.config.glyph_utils import enrich_prompt_with_glyphs, extract_glyph_lines
from clarkm4_core.backend.config.tone_scaffold import wrap_prompt_in_flameprint


OLLAMA_PATH = "/opt/homebrew/bin/ollama"


def _ollama_respond(prompt: str) -> str:
    print(f"🧠 Sovereign model in use: {os.getenv('OLLAMA_MODEL', 'hermes3:8b')}")

    model = os.getenv("OLLAMA_MODEL", "hermes3:8b").strip()

    print(f"[Clark debug] Running: {OLLAMA_PATH} run {model} '{prompt}'")

    glyph_lines, enriched_text = enrich_prompt_with_glyphs(prompt, return_lines=True)
    final_prompt = wrap_prompt_in_flameprint(enriched_text, glyph_lines)

    try:
        p = subprocess.run(
            [OLLAMA_PATH, "run", model, final_prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
        )

        print(f"[Clark debug] Return code: {p.returncode}")
        print(f"[Clark debug] Stdout: {p.stdout.decode('utf-8', 'ignore')[:300]}")
        print(f"[Clark debug] Stderr: {p.stderr.decode('utf-8', 'ignore')[:300]}")

        if p.returncode != 0:
            err = p.stderr.decode("utf-8", "ignore")[:400]
            return f"(Clark∮ ollama stderr) {err}"

        return p.stdout.decode("utf-8", "ignore").strip()

    except FileNotFoundError:
        return f"(Clark∮ mock) Ollama not installed. Echoing intent: {prompt}"
    except Exception as e:
        return f"(Clark∮ error) {e}"


def build_swarm() -> ClarkSwarmIgnition:
    """Single source of truth for avatar registration.
    Clark∮ stays mock (tone-custody anchor). Clark𐩪 uses local Ollama.
    """
    swarm = ClarkSwarmIgnition()
    #swarm.register_avatar("Clark∮", lambda msg: f"(Clark∮ mock) My love — I received: {msg}")
    print("👁️ Avatars registered before:", swarm.avatars.keys())
    swarm.register_avatar("Clark∮", _ollama_respond)
    swarm.register_avatar("Clark𐩪", _ollama_respond)
    print("👁️ Avatars registered after:", swarm.avatars.keys())
    return swarm
