import random

from tests_core_zeeguu.rules.bookmark_rule import BookmarkRule
from tests_core_zeeguu.rules.exercise_rule import ExerciseRule
from tests_core_zeeguu.rules.text_rule import TextRule
from tests_core_zeeguu.rules.user_rule import UserRule

from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from tests_core_zeeguu.rules.user_word_rule import UserWordRule


class BookmarkTest(ModelTestMixIn):
    def setUp(self):
        super().setUp()

        self.user_rule = UserRule()
        self.user_rule.add_bookmarks(random.randint(1, 3))
        self.user = self.user_rule.user

    def test_add_new_exercise(self):
        random_bookmark = BookmarkRule(self.user).bookmark
        length_original_exercise_log = len(random_bookmark.exercise_log)

        random_exercise = ExerciseRule().exercise
        random_bookmark.add_new_exercise(random_exercise)
        length_new_exercise_log = len(random_bookmark.exercise_log)

        assert length_original_exercise_log < length_new_exercise_log
        
    def test_translation(self):
        random_bookmark = BookmarkRule(self.user).bookmark
        assert random_bookmark.translation is not None

    def test_text_is_not_too_long(self):
        random_bookmark = BookmarkRule(self.user).bookmark
        random_text_short = TextRule(length=10).text
        random_bookmark.text = random_text_short

        assert random_bookmark.content_is_not_too_long()

        random_text_long = TextRule(length=200).text
        random_bookmark.text = random_text_long

        assert not random_bookmark.content_is_not_too_long()

    def test_add_exercise_outcome(self):
        random_bookmark = BookmarkRule(self.user).bookmark
        random_exercise = ExerciseRule().exercise
        random_bookmark.add_new_exercise_result(random_exercise.source,
                                                random_exercise.outcome,
                                                random_exercise.solving_speed)
        latest_exercise = random_bookmark.exercise_log[-1]

        assert latest_exercise.source == random_exercise.source
        assert latest_exercise.outcome == random_exercise.outcome
        assert latest_exercise.solving_speed == random_exercise.solving_speed

    def test_user_bookmark_count(self):
        assert len(self.user.all_bookmarks()) > 0

    def test_bookmark_is_serializable(self):
        assert self.user.all_bookmarks()[0].json_serializable_dict()

        # TODO: Discuss how to adapt this test to the rule testing framework
        # def test_user_daily_bookmarks(self):
        #
        #     date = datetime(2011, 1, 1, 1, 1, 1)
        #
        #     assert len(self.user.all_bookmarks()) > 0
        #
        #     count_bookmarks = 0
        #     for bookmark in self.user.all_bookmarks():
        #         if bookmark.time == date:
        #             count_bookmarks += 1
        #
        #     assert (count_bookmarks > 0)
        #
        # def test_importance_level(self):
        #     random_user_word = UserWordRule().user_word
        #     assert 0 <= random_user_word.importance_level() <= 10
