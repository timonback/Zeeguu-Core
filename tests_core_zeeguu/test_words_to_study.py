import configparser
import random
from datetime import datetime

from zeeguu.algos.algorithm_wrapper import AlgorithmWrapper

import zeeguu
from tests_core_zeeguu.model_test_mixin import ModelTestMixIn
from tests_core_zeeguu.rules.bookmark_rule import BookmarkRule
from tests_core_zeeguu.rules.exercise_rule import ExerciseRule
from tests_core_zeeguu.rules.outcome_rule import OutcomeRule
from tests_core_zeeguu.rules.user_rule import UserRule
from zeeguu.algos.ab_testing import ABTesting
from zeeguu.algos.algo_service import AlgoService
from zeeguu.algos.arts.arts_rt import ArtsRT


class WordsToStudyTest(ModelTestMixIn):
    def setUp(self):
        super().setUp()

        BOOKMARK_COUNT = 10

        self.user_rule = UserRule()
        self.user_rule.add_bookmarks(BOOKMARK_COUNT, exercises_count=1)
        self.user = self.user_rule.user

    def test_new_bookmark_has_the_highest_priority(self):
        # GIVEN
        new_bookmark = self.user_rule.add_bookmarks(1)[0].bookmark

        # WHEN
        AlgoService.update_bookmark_priority(zeeguu.db, self.user)

        # THEN
        bookmark = self.__get_bookmark_with_highest_priority()

        assert new_bookmark == bookmark, "The newly added bookmark does not have the highest priority. Based on non-existing exercise"

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

    def test_load_algorithms(self):
        config, algorithms = self.__get_config_with_random_algorithm_parameters()
        algorithm_should_be = algorithms[0]

        algorithms_loaded = ABTesting.load_algorithms(config)
        algorithm_to_check = algorithms_loaded[0]

        assert algorithm_to_check == algorithm_should_be

    def test_get_algorithm_for_id(self):
        config, algorithms = self.__get_config_with_random_algorithm_parameters(algorithm_count=random.randint(2, 5))
        ABTesting._algorithms = ABTesting.load_algorithms(config)
        new_bookmark = BookmarkRule(self.user).bookmark

        idx_should_be = divmod(new_bookmark.id, len(algorithms))[1]
        algorithm_should_be = algorithms[idx_should_be]

        algorithm_to_check = ABTesting.get_algorithm_for_id(new_bookmark.id)

        assert algorithm_should_be == algorithm_to_check

    def test_get_algorithm_wrapper_by_id(self):
        config, algorithms = self.__get_config_with_random_algorithm_parameters(algorithm_count=random.randint(2, 5))
        ABTesting._algorithms = ABTesting.load_algorithms(config)
        new_bookmark = BookmarkRule(self.user).bookmark

        idx_should_be = divmod(new_bookmark.id, len(algorithms))[1]
        algorithm_should_be = algorithms[idx_should_be]
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
                    a=random.randint(1, 1000),
                    D=random.randint(1, 1000),
                    b=random.randint(1, 1000),
                    r=random.randint(1, 1000),
                    w=random.randint(1, 1000)
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
