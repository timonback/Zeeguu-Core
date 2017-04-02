from model_test_mixin import ModelTestMixIn
from datetime import datetime
from unittest import TestCase

from zeeguu.model import UserWord


class BookmarkTest(ModelTestMixIn, TestCase):

    def setUp(self):
        super(BookmarkTest, self).setUp()
        self.first_bookmark = self.mir.all_bookmarks()[0]

    def test_user_bookmark_count(self):
        assert len(self.mir.all_bookmarks()) > 0

    def test_bookmark_is_serializable(self):
        assert not self.first_bookmark.json_serializable_dict()

    def test_user_daily_bookmarks(self):

        date = datetime(2011,01,01,01,01,01)

        assert len(self.mir.all_bookmarks()) > 0

        count_bookmarks = 0
        for bookmark in self.mir.all_bookmarks():
            if bookmark.time == date:
                count_bookmarks += 1

        assert (count_bookmarks > 0)

    def test_importance_level(self):

        mutter = UserWord.find("mutter", self.de)
        reg = UserWord.find("regierung", self.de)
        assert mutter.importance_level() == 10
        assert reg.importance_level() == 8

