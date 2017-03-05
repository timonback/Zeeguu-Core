from unittest import TestCase
from zeeguu.tests.model_test_mixin import ModelTestMixIn
import zeeguu
from zeeguu.model.user_word import UserWord


class UserPreferenceTest(ModelTestMixIn, TestCase):

    def test_preferred_word(self):
        starred_words_count_before = len(self.mir.starred_words)

        hauen = UserWord.find("hauen", self.de)
        self.mir.starred_words.append(hauen)
        self.session.commit()

        starred_words_count_after = len(self.mir.starred_words)
        assert starred_words_count_after == starred_words_count_before + 1

    def test_add_new_word_to_DB(self):
        word = "baum"
        rank = UserWord.find_rank(word, self.de)
        new_word = UserWord(word, self.de, rank)

        self.session.add(new_word)
        self.mir.star(new_word)
        self.session.commit()

    def test_find_word(self):
        word = "baum"
        assert UserWord.find(word, self.de)

    def test_user_word(self):
        assert self.mir.user_words() == map((lambda x: x.origin.word), self.mir.all_bookmarks())

    def test_preferred_words(self):
        word = "hauen"
        if(zeeguu.model.ranked_word.RankedWord.exists(word.lower(), self.de)):
            rank = UserWord.find_rank(word.lower(), self.de)
            someword = UserWord.find(word,self.de)
        else:
            someword = UserWord.find(word,self.de)
        assert someword
        # add someword to starred words
        self.mir.starred_words.append(someword)
        zeeguu.db.session.commit()

        assert someword in self.mir.starred_words

        self.mir.starred_words.remove(someword)
        zeeguu.db.session.commit()
        assert not self.mir.starred_words