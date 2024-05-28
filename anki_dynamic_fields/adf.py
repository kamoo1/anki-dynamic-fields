__all__ = ("AnkiDynamicFields",)

import re
from functools import partial

from jinja2 import Environment, FileSystemLoader

from .extensions import ExtensionManager
from . import IS_DEBUG
from .utils import log

if not IS_DEBUG:
    from anki.cards import Card
    # from aqt.qt import QIcon


class AnkiDynamicFields:
    def __init__(self, config=None):
        config = config or {}
        ext_path = config.get("extensions_path", "extensions")
        tpl_path = config.get("templates_path", "templates")
        self.field_matcher = re.compile(config.get("match_render_field", r".*"))
        env = Environment(loader=FileSystemLoader(tpl_path))
        ext_manager = ExtensionManager(ext_path)
        exports = ext_manager.get_exports()
        env.globals.update(exports)
        self.env = env

        s_exports = "\n".join(exports.keys())
        log(f"loaded exports: {s_exports}")

    def render(self, text: str):
        # TODO: add context to render, e.g. fields
        log(f"rendering template: {text}")
        try:
            return self.env.from_string(text).render()
        except Exception as e:
            log(f"error rendering template: {text}", is_error=True)
            if IS_DEBUG:
                self.logger.exception(e)
            return text

    def is_field_match(self, field):
        return self.field_matcher.fullmatch(field) is not None

    def on_render_btn_press(self, editor):
        editor.saveNow(partial(self._on_render_btn_press, editor))

    def _on_render_btn_press(self, editor):
        notes = editor.note
        for field in notes.keys():
            if self.is_field_match(field):
                notes[field] = self.render(notes[field])

    def on_card_will_show(self, text: str, card: "Card", kind: str) -> str:
        return self.render(text)

    def on_setup_editor_buttons(self, buttons, editor):
        button = editor.addButton(
            "",
            "ADF",
            self.on_render_btn_press,
            tip="render dynamic fields",
        )
        buttons.append(button)
