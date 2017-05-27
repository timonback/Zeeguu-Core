from tests_core_zeeguu.rules.bookmark_rule import BookmarkRule
from tests_core_zeeguu.rules.exercise_rule import ExerciseRule
from tests_core_zeeguu.rules.user_rule import UserRule
from tests_core_zeeguu.rules.user_word_rule import UserWordRule

print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))


from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from datetime import datetime


class BookmarkTest(ModelTestMixIn):

    def setUp(self):
        super().setUp()

        self.user_rule = UserRule()
        self.user_rule.add_bookmarks(5)
        self.user = self.user_rule.user

    def test_add_new_exercise(self):
        random_bookmark = BookmarkRule(self.user).bookmark
        length_original_exercise_log = len(random_bookmark.exercise_log)

        random_exercise = ExerciseRule().exercise
        random_bookmark.add_new_exercise(random_exercise)
        length_new_exercise_log = len(random_bookmark.exercise_log)

        assert length_original_exercise_log < length_new_exercise_log

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
        random_user_word = UserWordRule().user_word
        assert 0 <= random_user_word.importance_level() <= 10

