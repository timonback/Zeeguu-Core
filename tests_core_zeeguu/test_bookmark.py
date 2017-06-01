print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))


from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from datetime import datetime
from unittest import TestCase

from zeeguu.model.user_word import UserWord
import zeeguu


class BookmarkTest(ModelTestMixIn, TestCase):

    def setUp(self):
        super(BookmarkTest, self).setUp()
        self.first_bookmark = self.mir.all_bookmarks()[0]

    def test_user_bookmark_count(self):
        assert len(self.mir.all_bookmarks()) > 0

    def test_bookmark_is_serializable(self):
        assert self.first_bookmark.json_serializable_dict()

    def test_user_daily_bookmarks(self):

        date = datetime(2011,1,1,1,1,1)

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

    def test_default_bookmarks(self):
        from zeeguu.temporary.default_words import create_default_bookmarks

        b = create_default_bookmarks(zeeguu.db.session, self.mir, "es")
        zeeguu.db.session.add_all(b)
        zeeguu.db.session.commit()


