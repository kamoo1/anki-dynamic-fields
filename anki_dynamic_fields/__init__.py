__all__ = ("IS_DEBUG",)

import os
import sys
from logging import basicConfig


__version__ = "0.0.0"
IS_DEBUG = "unittest" in sys.modules

sys.path.append(os.path.join(os.path.dirname(__file__), "vendors"))

from .adf import AnkiDynamicFields
from .utils import preprocess_config

if IS_DEBUG:
    basicConfig(level="DEBUG")

else:
    from aqt import mw, gui_hooks

    config = mw.addonManager.getConfig(__name__)
    config = preprocess_config(config)
    basicConfig(level=config.get("log_level", "INFO"))
    AnkiDynamicFields(config=config)
    gui_hooks.card_will_show.append(AnkiDynamicFields.on_card_will_show)
