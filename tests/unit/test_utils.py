from unittest import TestCase
import unittest
import os
import sys

from anki_dynamic_fields.utils import preprocess_config


class TestUtils(TestCase):
    @unittest.skipIf(
        sys.platform not in ("linux", "darwin"), "Test is only for Linux and macOS"
    )
    def test_preprocess_config_linux_macos(self):
        config = {"extensions_path": "~/extensions", "templates_path": "~/templates"}
        config = preprocess_config(config)
        home_path = os.environ["HOME"]
        self.assertEqual(config["extensions_path"], f"{home_path}/extensions")
        self.assertEqual(config["templates_path"], f"{home_path}/templates")

    @unittest.skipIf(sys.platform != "win32", "Test is only for Windows")
    def test_preprocess_config_windows(self):
        config = {"extensions_path": "~/extensions", "templates_path": "~/templates"}
        config = preprocess_config(config)
        home_path = os.environ["USERPROFILE"]
        self.assertEqual(config["extensions_path"], f"{home_path}/extensions")
        self.assertEqual(config["templates_path"], f"{home_path}/templates")
