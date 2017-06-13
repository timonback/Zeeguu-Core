import configparser
import random
from datetime import datetime

import zeeguu
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from tests_core_zeeguu.rules.bookmark_rule import BookmarkRule
from tests_core_zeeguu.rules.exercise_rule import ExerciseRule
from tests_core_zeeguu.rules.outcome_rule import OutcomeRule
from tests_core_zeeguu.rules.user_rule import UserRule
from zeeguu.algos.ab_testing import ABTesting
from zeeguu.algos.algo_service import AlgoService
from zeeguu.algos.algorithm_wrapper import AlgorithmWrapper
from zeeguu.algos.arts.arts_rt import ArtsRT


class WordsToStudyTest(ModelTestMixIn):
    def setUp(self):
        super().setUp()

        self.BOOKMARK_COUNT = 20

        self.user_rule = UserRule()
        self.user_rule.add_bookmarks(self.BOOKMARK_COUNT, exercises_count=1)
        self.user = self.user_rule.user

        self.config, self.algorithms = self.__get_config_with_random_algorithm_parameters(
            algorithm_count=random.randint(2, 5))
        ABTesting._algorithms = ABTesting.load_algorithms(self.config)

    def test_just_finished_bookmark_has_not_the_highest_priority(self):
        # GIVEN
        ABTesting._algorithms = [self.algorithms[random.randint(0, len(self.algorithms) - 1)]]
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

    def test_load_algorithms(self):
        algorithm_should_be = self.algorithms[0]

        algorithms_loaded = ABTesting.load_algorithms(self.config)
        algorithm_to_check = algorithms_loaded[0]

        assert algorithm_to_check == algorithm_should_be

    def test_get_algorithm_for_id(self):
        new_bookmark = BookmarkRule(self.user).bookmark

        idx_should_be = new_bookmark.id % len(self.algorithms)
        algorithm_should_be = self.algorithms[idx_should_be]

        algorithm_to_check = ABTesting.get_algorithm_for_id(new_bookmark.id)

        assert algorithm_should_be == algorithm_to_check

    def test_get_algorithm_wrapper_by_id(self):
        new_bookmark = BookmarkRule(self.user).bookmark

        idx_should_be = divmod(new_bookmark.id, len(self.algorithms))[1]
        algorithm_should_be = self.algorithms[idx_should_be]
        wrapper_should_be = AlgorithmWrapper(algorithm_should_be)

        algorithm_to_check = ABTesting.get_algorithm_for_id(new_bookmark.id)
        wrapper_to_check = AlgorithmWrapper(algorithm_to_check)

        assert wrapper_should_be == wrapper_to_check

    def __get_bookmark_with_highest_priority(self):
        bookmarks_to_study = self.user.bookmarks_to_study()
        return bookmarks_to_study[0]

    def __get_bookmark_with_lowest_priority(self):
        bookmarks_to_study = self.user.bookmarks_to_study()
        return bookmarks_to_study[-1]

    def __get_config_with_random_algorithm_parameters(self, algorithm_count=1):
        algorithms = []
        config = configparser.ConfigParser()

        for i in range(0, algorithm_count):
            new_algorithm = ArtsRT(
                    a=random.randint(1, 100),
                    D=random.randint(1, 5),
                    b=random.randint(1, 100),
                    r=random.randint(1, 100),
                    w=random.randint(1, 100)
            )

            algorithms.append(new_algorithm)

            config[self.faker.word() + str(i)] = {
                'a': str(new_algorithm.a),
                'D': str(new_algorithm.D),
                'b': str(new_algorithm.b),
                'r': str(new_algorithm.r),
                'w': str(new_algorithm.w)
            }

        return config, algorithms
