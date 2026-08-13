import json
from pathlib import Path
from typing import Any, Mapping

CONFIG_DIR = Path(__file__).resolve().parent
CONFIG_PATH = CONFIG_DIR / "config.json"
ENV_PATH = CONFIG_DIR / ".env"

DEFAULT_CONFIG = {
    "jira_url": "",
    "jira_email": "",
    "jira_api_token": "",
    "llm_provider": "ollama",
    "ollama_url": "http://localhost:11434",
    "ollama_model": "gemma3:1b",
    "groq_api_key": "",
}

ENV_KEY_MAP = {
    "JIRA_URL": "jira_url",
    "JIRA_EMAIL": "jira_email",
    "JIRA_API_TOKEN": "jira_api_token",
    "OLLAMA_URL": "ollama_url",
    "OLLAMA_MODEL": "ollama_model",
    "GROQ_API_KEY": "groq_api_key",
    "LLM_PROVIDER": "llm_provider",
}


def _parse_env() -> dict[str, str]:
    result: dict[str, str] = {}
    if not ENV_PATH.exists():
        return result

    for raw_line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip().upper().replace(" ", "_")
        value = value.strip().strip('"').strip("'")
        mapped = ENV_KEY_MAP.get(key)
        if mapped:
            result[mapped] = value
    return result


def load_config() -> dict[str, Any]:
    config = DEFAULT_CONFIG.copy()
    config.update(_parse_env())
    if CONFIG_PATH.exists():
        try:
            with CONFIG_PATH.open("r", encoding="utf-8") as f:
                data = json.load(f)
                config.update({k: v for k, v in data.items() if v is not None})
        except json.JSONDecodeError:
            pass
    return config


def save_config(config: Mapping[str, Any]) -> None:
    data = {**DEFAULT_CONFIG, **config}
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
