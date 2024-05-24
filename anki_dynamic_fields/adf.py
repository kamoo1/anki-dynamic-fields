__all__ = ("AnkiDynamicFields",)

from logging import getLogger

from jinja2 import Environment, FileSystemLoader

from .extensions import ExtensionManager
from . import IS_DEBUG

if not IS_DEBUG:
    from anki.cards import Card


class AnkiDynamicFields:
    logger = getLogger("AnkiDynamicFields")

    def __init__(self, config=None):
        config = config or {}
        ext_path = config.get("extensions_path", "extensions")
        tpl_path = config.get("templates_path", "templates")
        env = Environment(loader=FileSystemLoader(tpl_path))
        ext_manager = ExtensionManager(ext_path)
        exports = ext_manager.get_exports()
        env.globals.update(exports)
        self.env = env

        s_exports = "\n".join(exports.keys())
        self.logger.debug(f"Exports:\n{s_exports}")

    def render(self, text: str):
        try:
            return self.env.from_string(text).render()
        except Exception as e:
            self.logger.debug(f"Error rendering template: {text}")
            if IS_DEBUG:
                self.logger.exception(e)
            return text

    def on_card_will_show(self, text: str, card: "Card", kind: str) -> str:
        return self.render(text)
