from unittest import TestCase
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from zeeguu.model.user_word import UserWord


class UserPreferenceTest(ModelTestMixIn, TestCase):

    def test_preferred_word(self):
        starred_words_count_before = len(self.mir.starred_words)

        hauen = UserWord.find("hauen", self.de)
        self.mir.starred_words.append(hauen)
        self.session.commit()

        starred_words_count_after = len(self.mir.starred_words)
        assert starred_words_count_after == starred_words_count_before + 1

    def test_find_word(self):
        word = "baum"
        assert UserWord.find(word, self.de)

    def test_user_word(self):
        assert self.mir.user_words() == list(map((lambda x: x.origin.word), self.mir.all_bookmarks()))