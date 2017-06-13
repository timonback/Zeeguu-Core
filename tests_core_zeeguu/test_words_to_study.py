from datetime import datetime

import zeeguu
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from tests_core_zeeguu.rules.exercise_rule import ExerciseRule
from tests_core_zeeguu.rules.outcome_rule import OutcomeRule
from tests_core_zeeguu.rules.user_rule import UserRule
from zeeguu.algos.algo_service import AlgoService


class WordsToStudyTest(ModelTestMixIn):
    def setUp(self):
        super().setUp()

        self.BOOKMARK_COUNT = 10

        self.user_rule = UserRule()
        self.user_rule.add_bookmarks(self.BOOKMARK_COUNT, exercises_count=1)
        self.user = self.user_rule.user

    def test_new_bookmark_has_the_highest_priority(self):
        # GIVEN
        new_bookmark = self.user_rule.add_bookmarks(1)[0].bookmark
        AlgoService.algorithm_wrapper.algorithm.D = self.BOOKMARK_COUNT

        # WHEN
        AlgoService.update_bookmark_priority(zeeguu.db, self.user)

        # THEN
        bookmark = self.__get_bookmark_with_highest_priority()

        assert new_bookmark == bookmark, "The newly added bookmark does not have the highest priority. Based on non existing exercise"

    def test_just_finished_bookmark_has_not_the_highest_priority(self):
        # GIVEN
        AlgoService.update_bookmark_priority(zeeguu.db, self.user)
        first_bookmark_to_study = self.__get_bookmark_with_highest_priority()

        # WHEN
        # Add an exercise
        exercise_rule = ExerciseRule()
        exercise_rule.exercise.time = datetime.now()
        exercise_rule.exercise.solving_speed = 100
        exercise_rule.exercise.outcome = OutcomeRule().correct
        first_bookmark_to_study.add_new_exercise(exercise_rule.exercise)

        AlgoService.update_bookmark_priority(zeeguu.db, self.user)

        # THEN
        bookmark = self.__get_bookmark_with_highest_priority()
        assert first_bookmark_to_study != bookmark

    def __get_bookmark_with_highest_priority(self):
        bookmarks_to_study = self.user.bookmarks_to_study()
        return bookmarks_to_study[0]

    def __get_bookmark_with_lowest_priority(self):
        bookmarks_to_study = self.user.bookmarks_to_study()
        return bookmarks_to_study[-1]
