from tests_core_zeeguu.rules.language_rule import LanguageRule
from zeeguu.model import UserWord

from tests_core_zeeguu.rules.base_rule import BaseRule


class UserWordRule(BaseRule):

    def __init__(self, word=None, language=None):
        super().__init__()

        if word is None or language is None:
            self.user_word = self._create_model_object()
        else:
            self.user_word = UserWord(word, language)

        self.save(self.user_word)

    def _create_model_object(self):
        random_word = self.faker.word()
        random_language = LanguageRule.random

        user_word = UserWord(random_word, random_language)

        if self._exists_in_db(user_word):
            return self._create_model_object()

        return user_word

    @staticmethod
    def _exists_in_db(obj):
        return UserWord.exists(obj.word, obj.language)


