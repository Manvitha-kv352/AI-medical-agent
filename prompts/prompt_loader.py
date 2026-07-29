from pathlib import Path
from typing import Any, Dict

PROMPTS_DIR = Path(__file__).resolve().parent


def load_prompt(prompt_name: str, version: str = "v1") -> str:
    filename = f"{prompt_name}_{version}.txt"
    prompt_path = PROMPTS_DIR / filename
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8").strip()


def render_prompt(prompt_name: str, version: str = "v1", **values: Any) -> str:
    template = load_prompt(prompt_name, version)
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{" + key + "}", str(value))
    return rendered


def get_prompt_versions() -> Dict[str, str]:
    return {
        "answer": "v1",
        "citation": "v1",
        "evaluation": "v1",
        "query": "v1",
    }
