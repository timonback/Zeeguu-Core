import random
from datetime import datetime

import zeeguu
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from tests_core_zeeguu.rules.exercise_rule import ExerciseRule
from tests_core_zeeguu.rules.outcome_rule import OutcomeRule
from tests_core_zeeguu.rules.user_rule import UserRule
from zeeguu.algos.ab_testing import ABTesting
from zeeguu.algos.algorithm_service import AlgorithmService


class WordsToStudyTest(ModelTestMixIn):
    def setUp(self):
        super().setUp()

        self.BOOKMARK_COUNT = 20

        self.user_rule = UserRule()
        self.user_rule.add_bookmarks(self.BOOKMARK_COUNT, exercises_count=1)
        self.user = self.user_rule.user

    def test_just_finished_bookmark_has_not_the_highest_priority(self):
        # GIVEN
        ABTesting._algorithms = [ABTesting._algorithms[random.randint(0, len(ABTesting._algorithms) - 1)]]
        AlgorithmService.update_bookmark_priority(zeeguu.db, self.user)
        first_bookmark_to_study = self.__get_bookmark_with_highest_priority()

        # WHEN
        # Add an exercise
        exercise_rule = ExerciseRule()
        exercise_rule.exercise.time = datetime.now()
        exercise_rule.exercise.solving_speed = 100
        exercise_rule.exercise.outcome = OutcomeRule().correct
        first_bookmark_to_study.add_new_exercise(exercise_rule.exercise)

        AlgorithmService.update_bookmark_priority(zeeguu.db, self.user)

        # THEN
        bookmark = self.__get_bookmark_with_highest_priority()
        assert first_bookmark_to_study != bookmark

    def __get_bookmark_with_highest_priority(self):
        bookmarks_to_study = self.user.bookmarks_to_study()
        if len(bookmarks_to_study) == 0:
            return None

        return bookmarks_to_study[0]

    def __get_bookmark_with_lowest_priority(self):
        bookmarks_to_study = self.user.bookmarks_to_study()
        if len(bookmarks_to_study) == 0:
            return None

        return bookmarks_to_study[-1]
