from tests_core_zeeguu.rules.user_rule import UserRule
from tests_core_zeeguu.rules.user_word_rule import UserWordRule

print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(
    __file__, __name__, str(__package__)))

from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from datetime import datetime

from zeeguu.model import UserWord


class BookmarkTest(ModelTestMixIn):
    def setUp(self):
        super().setUp()

        self.user_rule = UserRule()
        self.user_rule.add_bookmarks(5)
        self.user = self.user_rule.user

    def test_user_bookmark_count(self):
        assert len(self.user.all_bookmarks()) > 0

    def test_bookmark_is_serializable(self):
        assert self.user.all_bookmarks()[0].json_serializable_dict()

    def test_user_daily_bookmarks(self):

        date = datetime(2011, 1, 1, 1, 1, 1)

        assert len(self.user.all_bookmarks()) > 0

        count_bookmarks = 0
        for bookmark in self.user.all_bookmarks():
            if bookmark.time == date:
                count_bookmarks += 1

        assert (count_bookmarks > 0)

    def test_importance_level(self):
        mutter = UserWord.find("mutter", self.de)
        reg = UserWord.find("regierung", self.de)
        assert mutter.importance_level() == 10
        assert reg.importance_level() == 8

    def test_default_bookmarks(self):
        from zeeguu.temporary.default_words import default_bookmarks
        b = default_bookmarks(self.user, "es")

        import zeeguu
        db = zeeguu.db
        db.session.add_all(b)
        db.session.commit()
