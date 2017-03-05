import random
import unittest
from datetime import datetime
from unittest import TestCase
from zeeguu.tests.model_test_mixin import ModelTestMixIn

import zeeguu
from zeeguu.model import Bookmark, UserWord


class BookmarkTest(ModelTestMixIn, TestCase):

    def test_user_bookmark_count(self):
        assert len(self.mir.all_bookmarks()) > 0

    def test_user_daily_bookmarks(self):

        date = datetime(2011,01,01,01,01,01)

        assert len(self.mir.all_bookmarks()) > 0

        count_bookmarks = 0
        for bookmark in self.mir.all_bookmarks():
            if bookmark.time == date:
                count_bookmarks += 1

        assert (count_bookmarks > 0)

    def test_importance_level(self):
        word = "beschloss"
        if zeeguu.model.ranked_word.RankedWord.exists(word.lower(), self.de):
            rank = UserWord.find_rank(word.lower(), self.de)
            new_word = UserWord.find(word,self.de)
        else:
            new_word = UserWord.find(word,self.de)

        zeeguu.db.session.add(new_word)
        zeeguu.db.session.commit()

        word = "unexistingword"
        beschloss = UserWord.find(word, self.de)
        assert beschloss
        assert beschloss.importance_level() == 0

    def test_get_random_bookmark(self):

        bookmarks = (
            Bookmark.query.filter_by(user=self.mir)
                                    .join(UserWord, Bookmark.origin)
        ).all()

        assert random.choice(bookmarks).origin.word


if __name__ == '__main__':
    unittest.main()