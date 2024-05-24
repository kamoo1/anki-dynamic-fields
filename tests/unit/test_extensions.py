from unittest import TestCase
import tempfile
import os
import contextlib

from anki_dynamic_fields.extensions import ExtensionManager


@contextlib.contextmanager
def tempdir():
    temp_dir = tempfile.TemporaryDirectory()
    try:
        yield temp_dir
    finally:
        temp_dir.cleanup()


class TestExtensionManager(TestCase):
    def set_up_extension(self, temp_dir, module_name):
        os.makedirs(f"{temp_dir}/extensions/{module_name}", exist_ok=True)
        with open(f"{temp_dir}/extensions/{module_name}/__init__.py", "w") as f:
            f.write("""
exports = {
    "0": lambda: "0",
    "1": lambda: "1"
}
""")

    def set_up_extension_wrong(self, temp_dir, module_name):
        os.makedirs(f"{temp_dir}/extensions/{module_name}", exist_ok=True)
        with open(f"{temp_dir}/extensions/{module_name}/__init__.py", "w") as f:
            f.write("""
foo = "bar"
""")

    def test_get_exports(self):
        with tempdir() as temp_dir:
            self.set_up_extension(temp_dir.name, "ext0")
            self.set_up_extension(temp_dir.name, "ext1")
            ext_manager = ExtensionManager(f"{temp_dir.name}/extensions")
            ext_exports = ext_manager.get_exports()
            names = {
                "ext0_0",
                "ext0_1",
                "ext1_0",
                "ext1_1",
            }
            self.assertEqual(set(ext_exports.keys()), names)
            for name in names:
                self.assertEqual(ext_exports[name](), name[-1])

    def test_get_exports_wrong(self):
        with tempdir() as temp_dir:
            self.set_up_extension_wrong(temp_dir.name, "ext0")
            with self.assertRaises(AttributeError):
                ExtensionManager(f"{temp_dir.name}/extensions")
