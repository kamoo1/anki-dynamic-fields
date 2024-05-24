import os
import sys
from logging import getLogger
from typing import Any, Dict, Callable
import importlib.util

# class ExtensionConfig:
#     NAME_REGEX = r"^[a-z0-9_]+$"

#     def __init__(
#         self,
#         path: str,
#         name: str,
#         description: str,
#     ) -> None:
#         self.path = path
#         self.name = name
#         self.description = description

#         if not isinstance(self.path, str):
#             raise TypeError("path must be a string")

#         if not os.path.exists(self.path):
#             raise FileNotFoundError(f"Path not found: {self.path}")

#         if not isinstance(self.name, str):
#             raise TypeError("name must be a string")
#         if not self.name:
#             raise ValueError("name cannot be empty")
#         if not re.match(self.NAME_REGEX, self.name):
#             raise ValueError("name must match regex: {self.NAME_REGEX}")

#         if not isinstance(self.description, str):
#             raise TypeError("description must be a string")
#         if not self.description:
#             raise ValueError("description cannot be empty")

#     @classmethod
#     def from_dict(cls, data: dict) -> "ExtensionConfig":
#         return cls(
#             path=data["path"],
#             name=data["name"],
#             description=data["description"],
#         )

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class Extension:
    def __init__(self, base_path, module_name) -> None:
        self.name = module_name
        self.module = load_module(module_name, f"{base_path}/{module_name}/__init__.py")
        if "exports" not in self.module.__dict__:
            raise AttributeError("Module must have 'exports' defined")
        if module_name in sys.modules:
            raise ValueError(f"Module {module_name} pollutes the global namespace")

    def get_exports(self) -> Dict[str, Any]:
        mapping = {}
        for key in self.module.exports:
            mapping[f"{self.name}_{key}"] = self.module.exports[key]

        return mapping

class ExtensionManager:
    logger = getLogger("ExtensionManager")
    def __init__(self, base_path: str) -> None:
        sys.path += [os.path.abspath(base_path)]
        self.base_path = base_path
        self.extensions = self._load_all()

    def _load(self, module_name: str) -> "Extension":
        module_path = os.path.join(self.base_path, module_name)
        if not os.path.exists(module_path):
            raise FileNotFoundError(f"Module not found: {module_path}")

        return Extension(self.base_path, module_name)

    def _load_all(self) -> Dict[str, Extension]:
        extensions = {}
        for module_name in os.listdir(self.base_path):
            ext = self._load(module_name)
            extensions[module_name] = ext

        return extensions

    def get_exports(self) -> Dict[str, Callable]:
        exports = {}
        for ext in self.extensions.values():
            for name, func in ext.get_exports().items():
                exports[name] = func
        
        return exports
