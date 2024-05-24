__all__ = (
    "preprocess_config",
    "ensure_path",
)

from typing import Dict, Any
import os


def preprocess_config(config: Dict[str, Any]) -> Dict[str, Any]:
    expand_path_keys = ("extensions_path", "templates_path")
    for key in expand_path_keys:
        if key in config and isinstance(config[key], str):
            config[key] = os.path.expanduser(config[key])

    return config


def ensure_path(path: str) -> None:
    os.makedirs(path, exist_ok=True)
