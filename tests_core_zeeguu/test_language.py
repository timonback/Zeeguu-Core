from unittest import TestCase
from model_test_mixin import ModelTestMixIn
from zeeguu.model import Language


class LanguageTest(ModelTestMixIn, TestCase):

    def test_languages_exists(self):
        assert self.de.name == "German"

    def test_get_all_languages(self):
        assert self.de.id in [lan.id for lan in Language.all()]
        assert u'German' in [lan.name for lan in Language.all()]

    def test_user_set_language(self):
        self.mir.set_learned_language("en")
        assert self.mir.learned_language.id == "en"

    def test_native_language(self):
        assert self.mir.native_language.id == "en"
