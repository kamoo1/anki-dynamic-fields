from unittest import TestCase

from anki_dynamic_fields.adf import AnkiDynamicFields

class TestAnkiDynamicFields(TestCase):
    def test_render(self):
        config = {
            "extensions_path": "tests/extensions",
            "templates_path": "tests/templates"
        }
        adf = AnkiDynamicFields(config=config)
        text = "aaa {{ stropt_concat('hello ', 'world') }}"
        self.assertEqual(adf.render(text), "aaa hello world")

        text = "aaa {{ stropt_reverse('hello') }}"
        self.assertEqual(adf.render(text), "aaa olleh")