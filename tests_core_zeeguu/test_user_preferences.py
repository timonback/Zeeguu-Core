from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from tests_core_zeeguu.rules.language_rule import LanguageRule
from tests_core_zeeguu.rules.user_rule import UserRule
from tests_core_zeeguu.rules.user_word_rule import UserWordRule
from zeeguu.model.user_word import UserWord


class UserPreferenceTest(ModelTestMixIn):
    def setUp(self):
        super().setUp()

        self.user_rule = UserRule()
        self.user = self.user_rule.user

        self.random_origin_word = self.faker.word()
        self.random_origin_language = LanguageRule().random
        self.user_word_rule = UserWordRule(self.random_origin_word, self.random_origin_language)

    def test_find_word(self):
        assert UserWord.find(self.random_origin_word, self.random_origin_language)
