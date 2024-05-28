__all__ = ("IS_DEBUG",)

import os
import sys


__version__ = "0.0.0"
IS_DEBUG = "unittest" in sys.modules

sys.path.append(os.path.join(os.path.dirname(__file__), "vendors"))

from .adf import AnkiDynamicFields
from .utils import preprocess_config

if not IS_DEBUG:
    from aqt import mw, gui_hooks

    config = mw.addonManager.getConfig(__name__)
    config = preprocess_config(config)
    adf = AnkiDynamicFields(config=config)
    gui_hooks.card_will_show.append(adf.on_card_will_show)
    gui_hooks.editor_did_init_buttons.append(adf.on_setup_editor_buttons)
