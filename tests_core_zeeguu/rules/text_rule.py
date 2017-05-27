from tests_core_zeeguu.rules.language_rule import LanguageRule
from tests_core_zeeguu.rules.url_rule import UrlRule

from tests_core_zeeguu.rules.base_rule import BaseRule
from zeeguu.model.text import Text


class TextRule(BaseRule):

    def __init__(self):
        super().__init__()

        self.text = self._create_model_object()

        self.save(self.text)

    def _create_model_object(self):
        random_content = self.faker.text()
        random_language = LanguageRule().random
        random_url = UrlRule().url

        text = Text(random_content, random_language, random_url)

        if self._exists_in_db(text):
            return self._create_model_object()

        return text

    @staticmethod
    def _exists_in_db(obj):
        """An database existence check is not necessary since no primary key
        constraints can be violated.

        """
        return False
