__all__ = ("AnkiDynamicFields",)

from logging import getLogger

from jinja2 import Environment, FileSystemLoader

from .extensions import ExtensionManager
from . import IS_DEBUG

if not IS_DEBUG:
    from anki.cards import Card
    from aqt.qt import QIcon


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
        # TODO: add context to render, e.g. fields
        try:
            return self.env.from_string(text).render()
        except Exception as e:
            self.logger.debug(f"Error rendering template: {text}")
            if IS_DEBUG:
                self.logger.exception(e)
            return text

    def on_render_editor(self, editor):
        notes = editor.note
        for field in notes.keys():
            self.logger.debug(notes[field])
        
        editor.saveNow()

    def on_card_will_show(self, text: str, card: "Card", kind: str) -> str:
        return self.render(text)

    def on_setup_editor_buttons(self, buttons, editor):
        button = editor.addButton(
            # QIcon(":/icons/anki-dynamic-fields.svg"),
            "",
            "anki_dynamic_fields",
            self.on_render_editor,
            tip="render dynamic fields",
        )
        buttons.append(button)
