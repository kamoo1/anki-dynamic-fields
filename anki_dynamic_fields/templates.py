import re
import os
from typing import Dict, Any, List

import jinja2
# https://realpython.com/primer-on-jinja-templating/

from .utils import ensure_path


class TemplateManager:
    REGEX_FILE_NAME = r"^([A-Za-z0-9_\-]+)(?:\.([A-Za-z0-9]+))?$"  # file_name.extension

    def __init__(self, path: str) -> None:
        ensure_path(path)
        self.path = path
        self.templates = {}
        self.environment = jinja2.Environment(loader=jinja2.FileSystemLoader(self.path))

    def _load(self, file_name: str) -> None:
        path = os.path.join(self.path, file_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        self.templates = {}
        match = re.match(self.REGEX_FILE_NAME, file_name)
        if not match:
            raise ValueError(f"Invalid file name: {file_name}")

        template_name = match.group(1)
        self.templates[template_name] = self.environment.get_template(file_name)
