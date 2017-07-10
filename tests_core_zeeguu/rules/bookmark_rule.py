import random
import re
from datetime import timedelta

from tests_core_zeeguu.rules.base_rule import BaseRule
from tests_core_zeeguu.rules.language_rule import LanguageRule
from tests_core_zeeguu.rules.text_rule import TextRule
from tests_core_zeeguu.rules.url_rule import UrlRule
from tests_core_zeeguu.rules.user_word_rule import UserWordRule
from zeeguu.model.bookmark import Bookmark
from zeeguu.model.user_word import UserWord


class BookmarkRule(BaseRule):
    """A Rule testing class for the zeeguu.model.Bookmark model class.

    Creates a Bookmark object with random data and saves it to the database.
    """

    props = ['origin', 'translation', 'text', 'date']

    def __init__(self, user, **kwargs):
        super().__init__()
        self.bookmark = self._create_model_object(user, **kwargs)

        self.save(self.bookmark)

    def _create_model_object(self, user, **kwargs):
        """
        Creates a Bookmark object with random data.

        Behind the random words, a random number is added since the Faker library does not have too many RANDOM words
        and random words get repeated whenever many random bookmarks are created. To forcome the problem of bookmarks
        with duplicate words in the database, a random number is added.

        :param user: User Object, to which the bookmark is assigned.
        :param kwargs: Holds any of the 'props' as key if a field should not be random
        :return:
        """
        # This line is needed so that the URL is created in the database
        random_url = UrlRule().url

        random_text = TextRule().text

        random_origin_word = self.faker.word() + str(random.random())
        random_origin_language = LanguageRule().random

        random_translation_word = self.faker.word() + str(random.random())
        random_translation_language = LanguageRule().random

        if UserWord.exists(random_origin_word, random_origin_language) \
                or UserWord.exists(random_translation_word, random_translation_language):
            return self._create_model_object(user)

        random_origin = UserWordRule(random_origin_word,
                                     random_origin_language).user_word
        random_translation = UserWordRule(random_translation_word,
                                          random_translation_language).user_word
        random_date = self.faker.date_time_this_month() - timedelta(days=1)

        bookmark = Bookmark(random_origin, random_translation, user,
                            random_text, random_date)

        for k in kwargs:
            if k in self.props:
                setattr(bookmark, k, kwargs.get(k))

        if self._exists_in_db(bookmark):
            return self._create_model_object(user)

        return bookmark

    @staticmethod
    def _exists_in_db(obj):
        return Bookmark.exists(obj)

    @staticmethod
    def __get_random_word_from_sentence(sentence):
        word_list = re.sub("[^\w]", " ", sentence).split()
        random_index = random.randint(0, len(word_list) - 1)
        return word_list[random_index]
